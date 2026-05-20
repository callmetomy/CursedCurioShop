import argparse
import json
from pathlib import Path
from typing import Any

from tools.asset_pipeline.config import ProjectPaths
from tools.asset_pipeline.env import load_env_file
from tools.asset_pipeline.manifest import AssetManifest
from tools.asset_pipeline.providers.tripo import (
    TripoClient,
    build_text_to_model_payload,
    extract_model_url,
    extract_status,
    extract_task_id,
)


def build_tripo_model_job(
    *,
    root: Path,
    item_id: str,
    model_version: str | None = None,
) -> dict[str, Any]:
    root = Path(root).resolve()
    item_path = root / "data" / "items" / f"{item_id}.json"
    item = json.loads(item_path.read_text(encoding="utf-8"))
    output_path = item["model"]["raw_path"].replace("\\", "/")

    return {
        "item_id": item["id"],
        "display_name": item["display_name"],
        "payload": build_text_to_model_payload(
            prompt=item["generation"]["model_prompt"],
            model_version=model_version,
        ),
        "output_path": output_path,
        "manifest_path": f"data/manifests/{item_id}_manifest.json",
    }


def append_manifest_attempt(
    *,
    root: Path,
    item_id: str,
    stage: str,
    status: str,
    output_path: str,
) -> Path:
    root = Path(root).resolve()
    manifest_path = root / "data" / "manifests" / f"{item_id}_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = AssetManifest()
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest.version = data.get("version", 1)
        manifest.attempts = data.get("attempts", [])

    manifest.add_attempt(
        item_id=item_id,
        stage=stage,
        status=status,
        output_path=output_path,
    )
    manifest_path.write_text(
        json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def build_dry_run_preview(job: dict[str, Any]) -> dict[str, Any]:
    payload = dict(job["payload"])
    payload["prompt"] = payload["prompt"][:240]
    return {
        "dry_run": True,
        "item_id": job["item_id"],
        "display_name": job["display_name"],
        "payload": payload,
        "output_path": job["output_path"],
        "manifest_path": job["manifest_path"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Tripo text-to-3D model for a tracked oddity item."
    )
    parser.add_argument("--root", default=".", help="Project root directory.")
    parser.add_argument("--item-id", required=True, help="Oddity item id.")
    parser.add_argument(
        "--model-version",
        default=None,
        help="Optional Tripo model version. Leave unset to use the account/API default.",
    )
    parser.add_argument("--submit", action="store_true", help="Actually submit a Tripo task.")
    parser.add_argument("--wait", action="store_true", help="Poll until the task finishes.")
    parser.add_argument("--download", action="store_true", help="Download the finished GLB if available.")
    parser.add_argument("--task-id", help="Poll or download an existing Tripo task id.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    paths = ProjectPaths(root)
    paths.ensure_generated_dirs()
    job = build_tripo_model_job(
        root=root,
        item_id=args.item_id,
        model_version=args.model_version,
    )

    if not args.submit and not args.task_id:
        print(json.dumps(build_dry_run_preview(job), ensure_ascii=False, indent=2))
        return 0

    env = load_env_file(root / ".env")
    api_key = env.get("TRIPO_API_KEY")
    if not api_key:
        raise SystemExit("TRIPO_API_KEY is missing in .env")

    client = TripoClient(api_key=api_key)
    task_id = args.task_id

    if args.submit:
        try:
            response = client.submit_text_to_model(
                job["payload"]["prompt"],
                args.model_version,
            )
        except RuntimeError as error:
            print(json.dumps({"submitted": False, "error": str(error)}, ensure_ascii=False, indent=2))
            return 1
        task_id = extract_task_id(response)
        if not task_id:
            print(json.dumps(response, ensure_ascii=False, indent=2))
            raise SystemExit("Tripo response did not include a task id.")

        append_manifest_attempt(
            root=root,
            item_id=args.item_id,
            stage="tripo_text_to_model",
            status="submitted",
            output_path=f"tripo:{task_id}",
        )
        print(
            json.dumps(
                {
                    "submitted": True,
                    "item_id": args.item_id,
                    "task_id": task_id,
                    "output_path": job["output_path"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )

    if args.wait or args.download:
        response = client.wait_for_task(task_id)
    else:
        response = client.get_task(task_id)

    status = extract_status(response)
    model_url = extract_model_url(response)
    print(
        json.dumps(
            {"task_id": task_id, "status": status, "has_model_url": bool(model_url)},
            ensure_ascii=False,
            indent=2,
        )
    )

    if args.download:
        if not model_url:
            print(json.dumps({"downloaded": False, "reason": "model_url_missing"}, indent=2))
            return 1

        output_path = root / job["output_path"]
        client.download_model(model_url, output_path)
        append_manifest_attempt(
            root=root,
            item_id=args.item_id,
            stage="tripo_download",
            status="downloaded",
            output_path=job["output_path"],
        )
        print(json.dumps({"downloaded": str(output_path)}, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
