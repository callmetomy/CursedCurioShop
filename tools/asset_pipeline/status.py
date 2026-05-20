import argparse
import json
from pathlib import Path
from typing import Any


def build_asset_status(*, root: Path, item_id: str) -> dict[str, Any]:
    root = Path(root).resolve()
    item_path = root / "data" / "items" / f"{item_id}.json"
    item = json.loads(item_path.read_text(encoding="utf-8"))

    assets = [
        _asset_entry(root, "concept_image", f"assets/concepts/{item_id}.png"),
        _asset_entry(root, "raw_model", item["model"]["raw_path"]),
        _asset_entry(root, "processed_model", item["model"]["processed_path"]),
        _asset_entry(root, "review_report", f"assets/review/{item_id}_review.md"),
    ]

    return {
        "item_id": item["id"],
        "display_name": item["display_name"],
        "generation_status": item["generation"]["status"],
        "approved": item["generation"]["approved"],
        "assets": assets,
        "missing_stages": [
            asset["stage"] for asset in assets if not asset["exists"]
        ],
    }


def render_asset_status_markdown(status: dict[str, Any]) -> str:
    lines = [
        f"# Asset Status: {status['display_name']}",
        "",
        f"- Item ID: `{status['item_id']}`",
        f"- Generation status: `{status['generation_status']}`",
        f"- Approved: `{str(status['approved']).lower()}`",
        "",
        "## Outputs",
        "",
    ]

    for asset in status["assets"]:
        state = "ready" if asset["exists"] else "missing"
        lines.append(f"- {asset['stage']}: {state} (`{asset['path']}`)")

    if status["missing_stages"]:
        missing = ", ".join(status["missing_stages"])
        lines.extend(["", f"Missing stages: {missing}"])
    else:
        lines.extend(["", "Missing stages: none"])

    return "\n".join(lines) + "\n"


def _asset_entry(root: Path, stage: str, relative_path: str) -> dict[str, Any]:
    normalized_path = relative_path.replace("\\", "/")
    return {
        "stage": stage,
        "path": normalized_path,
        "exists": (root / normalized_path).exists(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report which generated asset outputs exist for an oddity."
    )
    parser.add_argument("--root", default=".", help="Project root directory.")
    parser.add_argument("--item-id", required=True, help="Oddity item id.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of Markdown.",
    )
    args = parser.parse_args()

    status = build_asset_status(root=Path(args.root), item_id=args.item_id)
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        print(render_asset_status_markdown(status), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
