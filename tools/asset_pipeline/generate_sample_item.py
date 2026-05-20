import argparse
import json
from pathlib import Path

from tools.asset_pipeline.config import ProjectPaths
from tools.asset_pipeline.items import build_item_definition, save_item_definition
from tools.asset_pipeline.manifest import AssetManifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a sample oddity definition and manifest without calling paid APIs."
    )
    parser.add_argument("--root", default=".", help="Project root directory.")
    parser.add_argument("--item-id", default="oddity_0001")
    parser.add_argument("--name", default="Whispering Teacup")
    args = parser.parse_args()

    paths = ProjectPaths(Path(args.root))
    paths.ensure_generated_dirs()

    item = build_item_definition(
        item_id=args.item_id,
        display_name=args.name,
        concept_prompt=(
            "A cracked porcelain teacup for a first-person cursed antique shop game, "
            "dark tea stain, faint hairline fractures, readable silhouette, no text."
        ),
        model_prompt=(
            "A cursed porcelain teacup game prop, cracked white ceramic, dark stain, "
            "asymmetrical worn details, game-ready PBR texture, no text, no logo."
        ),
    )
    item_path = save_item_definition(item, paths.data_items)

    manifest = AssetManifest()
    manifest.add_attempt(
        item_id=args.item_id,
        stage="item_definition",
        status="created",
        output_path=str(item_path.relative_to(paths.root)).replace("\\", "/"),
    )
    manifest_path = paths.manifests / f"{args.item_id}_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Created {item_path}")
    print(f"Created {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
