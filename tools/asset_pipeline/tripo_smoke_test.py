import argparse
import json
from pathlib import Path

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


DEFAULT_PROMPT = (
    "A small cursed porcelain teacup game prop for a first-person indie horror shop game, "
    "cracked white ceramic, dark tea stain, readable silhouette, low poly, PBR texture, "
    "no text, no logo, no human body parts"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Test Tripo API integration.")
    parser.add_argument("--root", default=".", help="Project root directory.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
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
    env = load_env_file(root / ".env")
    api_key = env.get("TRIPO_API_KEY")
    if not api_key:
        raise SystemExit("TRIPO_API_KEY is missing in .env")

    manifest = AssetManifest()
    client = TripoClient(api_key=api_key)

    if not args.submit and not args.task_id:
        payload = build_text_to_model_payload(prompt=args.prompt, model_version=args.model_version)
        safe_preview = dict(payload)
        safe_preview["prompt"] = safe_preview["prompt"][:160]
        print(json.dumps({"dry_run": True, "payload": safe_preview}, ensure_ascii=False, indent=2))
        return 0

    task_id = args.task_id
    if args.submit:
        try:
            response = client.submit_text_to_model(args.prompt, args.model_version)
        except RuntimeError as error:
            print(json.dumps({"submitted": False, "error": str(error)}, ensure_ascii=False, indent=2))
            return 1
        task_id = extract_task_id(response)
        if not task_id:
            print(json.dumps(response, ensure_ascii=False, indent=2))
            raise SystemExit("Tripo response did not include a task id.")
        manifest.add_attempt(
            item_id="tripo_smoke_test",
            stage="tripo_text_to_model",
            status="submitted",
            output_path=f"tripo:{task_id}",
        )
        print(json.dumps({"submitted": True, "task_id": task_id}, ensure_ascii=False, indent=2))

    if args.wait or args.download:
        try:
            response = client.wait_for_task(task_id)
        except RuntimeError as error:
            print(json.dumps({"task_id": task_id, "error": str(error)}, ensure_ascii=False, indent=2))
            return 1
    else:
        try:
            response = client.get_task(task_id)
        except RuntimeError as error:
            print(json.dumps({"task_id": task_id, "error": str(error)}, ensure_ascii=False, indent=2))
            return 1

    status = extract_status(response)
    model_url = extract_model_url(response)
    print(json.dumps({"task_id": task_id, "status": status, "has_model_url": bool(model_url)}, indent=2))

    if args.download and model_url:
        output_path = paths.models_raw / f"tripo_{task_id}.glb"
        client.download_model(model_url, output_path)
        manifest.add_attempt(
            item_id="tripo_smoke_test",
            stage="tripo_download",
            status="downloaded",
            output_path=str(output_path.relative_to(paths.root)).replace("\\", "/"),
        )
        print(json.dumps({"downloaded": str(output_path)}, ensure_ascii=False, indent=2))

    if manifest.attempts:
        manifest_path = paths.manifests / "tripo_smoke_test_manifest.json"
        manifest_path.write_text(
            json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
