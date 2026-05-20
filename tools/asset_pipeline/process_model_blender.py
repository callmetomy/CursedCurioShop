import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from tools.asset_pipeline.config import ProjectPaths
from tools.asset_pipeline.generate_tripo_model import append_manifest_attempt


def build_blender_process_job(*, root: Path, item_id: str) -> dict[str, Any]:
    root = Path(root).resolve()
    item_path = root / "data" / "items" / f"{item_id}.json"
    item = json.loads(item_path.read_text(encoding="utf-8"))
    raw_path = item["model"]["raw_path"].replace("\\", "/")
    processed_path = item["model"]["processed_path"].replace("\\", "/")

    return {
        "item_id": item["id"],
        "display_name": item["display_name"],
        "input_path": str(root / raw_path),
        "output_path": str(root / processed_path),
        "relative_output_path": processed_path,
        "target_longest_axis": float(item["model"].get("scale_meters", 1.0)),
        "manifest_path": f"data/manifests/{item_id}_manifest.json",
    }


def resolve_blender_executable(*, explicit: Path | None = None) -> Path:
    candidates: list[Path] = []
    if explicit is not None:
        candidates.append(Path(explicit))

    env_path = os.environ.get("BLENDER_PATH")
    if env_path:
        candidates.append(Path(env_path))

    found = shutil.which("blender")
    if found:
        candidates.append(Path(found))

    candidates.extend(
        sorted(
            Path("C:/Program Files/Blender Foundation").glob("Blender */blender.exe"),
            reverse=True,
        )
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    raise FileNotFoundError(
        "Could not find Blender. Pass --blender or set BLENDER_PATH to blender.exe."
    )


def build_blender_command(
    *,
    blender_executable: Path,
    script_path: Path,
    input_path: Path,
    output_path: Path,
    item_id: str,
    target_longest_axis: float,
) -> list[str]:
    return [
        str(Path(blender_executable)),
        "--background",
        "--factory-startup",
        "--python",
        str(Path(script_path)),
        "--",
        "--input",
        str(Path(input_path)),
        "--output",
        str(Path(output_path)),
        "--item-id",
        item_id,
        "--target-longest-axis",
        str(target_longest_axis),
    ]


def run_blender_process(
    *,
    root: Path,
    item_id: str,
    blender: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    root = Path(root).resolve()
    paths = ProjectPaths(root)
    paths.ensure_generated_dirs()
    job = build_blender_process_job(root=root, item_id=item_id)
    blender_executable = resolve_blender_executable(explicit=blender)
    script_path = Path(__file__).with_name("blender_process_model.py")
    command = build_blender_command(
        blender_executable=blender_executable,
        script_path=script_path,
        input_path=Path(job["input_path"]),
        output_path=Path(job["output_path"]),
        item_id=job["item_id"],
        target_longest_axis=job["target_longest_axis"],
    )

    preview = {
        "item_id": job["item_id"],
        "display_name": job["display_name"],
        "input_path": job["input_path"],
        "output_path": job["output_path"],
        "target_longest_axis": job["target_longest_axis"],
        "blender": str(blender_executable),
        "command": command,
        "dry_run": dry_run,
    }
    if dry_run:
        return preview

    completed = subprocess.run(
        command,
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Blender processing failed.\n"
            f"STDOUT:\n{completed.stdout}\n"
            f"STDERR:\n{completed.stderr}"
        )

    append_manifest_attempt(
        root=root,
        item_id=item_id,
        stage="model_processing",
        status="blender_normalized",
        output_path=job["relative_output_path"],
    )
    return {
        **preview,
        "dry_run": False,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize a tracked oddity GLB through Blender background mode."
    )
    parser.add_argument("--root", default=".", help="Project root directory.")
    parser.add_argument("--item-id", required=True, help="Oddity item id.")
    parser.add_argument("--blender", help="Path to blender.exe. Defaults to PATH, BLENDER_PATH, or common install paths.")
    parser.add_argument("--dry-run", action="store_true", help="Print the Blender command without running it.")
    args = parser.parse_args()

    result = run_blender_process(
        root=Path(args.root),
        item_id=args.item_id,
        blender=Path(args.blender) if args.blender else None,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
