import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from tools.asset_pipeline.config import ProjectPaths
from tools.asset_pipeline.generate_tripo_model import append_manifest_attempt
from tools.asset_pipeline.process_model_blender import resolve_blender_executable

REVIEW_ANGLES = ("front", "right", "back", "left")


def build_review_render_job(*, root: Path, item_id: str) -> dict[str, Any]:
    root = Path(root).resolve()
    item_path = root / "data" / "items" / f"{item_id}.json"
    item = json.loads(item_path.read_text(encoding="utf-8"))
    processed_path = item["model"]["processed_path"].replace("\\", "/")
    relative_output_paths = [
        f"assets/review/{item_id}_{angle}.png" for angle in REVIEW_ANGLES
    ]

    return {
        "item_id": item["id"],
        "display_name": item["display_name"],
        "input_path": str(root / processed_path),
        "output_dir": str(root / "assets" / "review"),
        "output_paths": {
            angle: str(root / "assets" / "review" / f"{item_id}_{angle}.png")
            for angle in REVIEW_ANGLES
        },
        "relative_output_paths": relative_output_paths,
        "manifest_path": f"data/manifests/{item_id}_manifest.json",
    }


def build_blender_review_command(
    *,
    blender_executable: Path,
    script_path: Path,
    input_path: Path,
    output_dir: Path,
    item_id: str,
    resolution: int,
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
        "--output-dir",
        str(Path(output_dir)),
        "--item-id",
        item_id,
        "--resolution",
        str(resolution),
    ]


def run_blender_review_render(
    *,
    root: Path,
    item_id: str,
    blender: Path | None = None,
    resolution: int = 768,
    dry_run: bool = False,
) -> dict[str, Any]:
    root = Path(root).resolve()
    paths = ProjectPaths(root)
    paths.ensure_generated_dirs()
    job = build_review_render_job(root=root, item_id=item_id)
    blender_executable = resolve_blender_executable(explicit=blender)
    script_path = Path(__file__).with_name("blender_render_review.py")
    command = build_blender_review_command(
        blender_executable=blender_executable,
        script_path=script_path,
        input_path=Path(job["input_path"]),
        output_dir=Path(job["output_dir"]),
        item_id=job["item_id"],
        resolution=resolution,
    )

    preview = {
        "item_id": job["item_id"],
        "display_name": job["display_name"],
        "input_path": job["input_path"],
        "output_paths": job["output_paths"],
        "resolution": resolution,
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
            "Blender review render failed.\n"
            f"STDOUT:\n{completed.stdout}\n"
            f"STDERR:\n{completed.stderr}"
        )

    append_manifest_attempt(
        root=root,
        item_id=item_id,
        stage="review_render",
        status="rendered_blender_turntable",
        output_path=";".join(job["relative_output_paths"]),
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
        description="Render standard review screenshots for a processed oddity GLB."
    )
    parser.add_argument("--root", default=".", help="Project root directory.")
    parser.add_argument("--item-id", required=True, help="Oddity item id.")
    parser.add_argument("--blender", help="Path to blender.exe. Defaults to PATH, BLENDER_PATH, or common install paths.")
    parser.add_argument("--resolution", type=int, default=768, help="Square PNG resolution.")
    parser.add_argument("--dry-run", action="store_true", help="Print the Blender command without running it.")
    args = parser.parse_args()

    result = run_blender_review_render(
        root=Path(args.root),
        item_id=args.item_id,
        blender=Path(args.blender) if args.blender else None,
        resolution=args.resolution,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
