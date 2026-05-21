import argparse
import json
import struct
import zlib
from pathlib import Path
from typing import Any

from tools.asset_pipeline.config import ProjectPaths
from tools.asset_pipeline.items import build_item_definition
from tools.asset_pipeline.manifest import AssetManifest

LOCAL_ODDITY_SPECS = [
    {
        "item_id": "oddity_0002",
        "display_name": "Mirror Coin",
        "shape": "coin",
        "material_color": [0.52, 0.50, 0.62, 1.0],
        "accent_marker_color": [0.25, 0.85, 1.0, 1.0],
        "temperature_c": -2.1,
        "handling": "seal",
    },
    {
        "item_id": "oddity_0003",
        "display_name": "Ashen Music Box",
        "shape": "box",
        "material_color": [0.42, 0.28, 0.22, 1.0],
        "accent_marker_color": [1.0, 0.45, 0.18, 1.0],
        "temperature_c": 13.4,
        "handling": "discard",
    },
    {
        "item_id": "oddity_0004",
        "display_name": "Cold Brass Key",
        "shape": "key",
        "material_color": [0.74, 0.58, 0.28, 1.0],
        "accent_marker_color": [0.2, 0.65, 1.0, 1.0],
        "temperature_c": -11.8,
        "handling": "seal",
    },
    {
        "item_id": "oddity_0005",
        "display_name": "Glass Eye",
        "shape": "sphere",
        "material_color": [0.38, 0.62, 0.68, 1.0],
        "accent_marker_color": [0.9, 0.18, 0.22, 1.0],
        "temperature_c": 4.2,
        "handling": "sell",
    },
    {
        "item_id": "oddity_0006",
        "display_name": "Black Wax Candle",
        "shape": "candle",
        "material_color": [0.08, 0.07, 0.08, 1.0],
        "accent_marker_color": [0.95, 0.28, 0.12, 1.0],
        "temperature_c": 38.6,
        "handling": "discard",
    },
    {
        "item_id": "oddity_0007",
        "display_name": "Moth-Eaten Doll",
        "shape": "doll",
        "material_color": [0.46, 0.36, 0.52, 1.0],
        "accent_marker_color": [0.2, 0.75, 0.95, 1.0],
        "temperature_c": 7.7,
        "handling": "seal",
    },
    {
        "item_id": "oddity_0008",
        "display_name": "Silver Funeral Bell",
        "shape": "bell",
        "material_color": [0.70, 0.68, 0.58, 1.0],
        "accent_marker_color": [0.16, 0.62, 1.0, 1.0],
        "temperature_c": 0.6,
        "handling": "seal",
    },
    {
        "item_id": "oddity_0009",
        "display_name": "Cracked Hand Mirror",
        "shape": "mirror",
        "material_color": [0.34, 0.45, 0.52, 1.0],
        "accent_marker_color": [0.85, 0.15, 0.22, 1.0],
        "temperature_c": 18.9,
        "handling": "discard",
    },
    {
        "item_id": "oddity_0010",
        "display_name": "Red Thread Spool",
        "shape": "spool",
        "material_color": [0.70, 0.18, 0.20, 1.0],
        "accent_marker_color": [0.95, 0.75, 0.18, 1.0],
        "temperature_c": 31.2,
        "handling": "sell",
    },
]


def build_local_item(spec: dict[str, Any]) -> dict[str, Any]:
    item = build_item_definition(
        item_id=spec["item_id"],
        display_name=spec["display_name"],
        concept_prompt=f"Local prototype concept for {spec['display_name']}.",
        model_prompt=f"Local procedural prototype model for {spec['display_name']}.",
    )
    item["appraisal"] = {
        "description": f"A local prototype oddity: {spec['display_name']}.",
        "clues": [
            {
                "tool": "magnifier",
                "result": "Fine scratches form a deliberate appraisal mark.",
            },
            {
                "tool": "uv_lamp",
                "result": "A hidden blue mark appears under UV light.",
            },
            {
                "tool": "thermometer",
                "result": "The reading is inconsistent with the room.",
                "temperature_c": spec["temperature_c"],
            },
        ],
        "correct_handling": spec["handling"],
        "wrong_handling_consequence": "A minor abnormal event is queued for the shop.",
    }
    item["generation"]["status"] = "local_prototype"
    item["generation"]["approved"] = True
    item["generation"]["attempts"] = 1
    item["local_shape"] = spec["shape"]
    item["local_material_color"] = spec["material_color"]
    item["use_fallback_material"] = True
    item["accent_marker_color"] = spec["accent_marker_color"]
    return item


def write_png(path: Path, *, color: tuple[int, int, int]) -> None:
    width = 64
    height = 64
    raw_rows = []
    for y in range(height):
        row = bytearray([0])
        shade = 24 + int(32 * y / height)
        for _x in range(width):
            row.extend((min(color[0] + shade, 255), min(color[1] + shade, 255), min(color[2] + shade, 255)))
        raw_rows.append(bytes(row))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(b"".join(raw_rows), level=9))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def write_review(path: Path, item: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                f"# Review: {item['display_name']}",
                "",
                f"- Item ID: `{item['id']}`",
                "- Review decision: accepted for local prototype demo roster",
                "",
                "## Manual Check",
                "",
                "- Local procedural model placeholder is present.",
                "- Three inspection clues are defined.",
                "- Approved for demo-loop coverage.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_manifest(path: Path, item_id: str) -> None:
    manifest = AssetManifest()
    for stage, output_path in (
        ("item_definition", f"data/items/{item_id}.json"),
        ("concept_image", f"assets/concepts/{item_id}.png"),
        ("local_model", f"assets/models_raw/{item_id}.glb"),
        ("model_processing", f"assets/models_processed/{item_id}.glb"),
        ("manual_review", f"assets/review/{item_id}_review.md"),
    ):
        manifest.add_attempt(
            item_id=item_id,
            stage=stage,
            status="created_locally",
            output_path=output_path,
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def generate_metadata(root: Path) -> None:
    root = Path(root).resolve()
    paths = ProjectPaths(root)
    paths.ensure_generated_dirs()
    colors = [
        (90, 90, 115),
        (120, 82, 70),
        (110, 96, 45),
        (80, 110, 120),
        (105, 65, 72),
        (88, 74, 96),
        (125, 120, 100),
        (76, 94, 108),
        (116, 62, 62),
    ]
    for spec, color in zip(LOCAL_ODDITY_SPECS, colors, strict=True):
        item = build_local_item(spec)
        item_path = paths.data_items / f"{item['id']}.json"
        item_path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_png(paths.concepts / f"{item['id']}.png", color=color)
        write_review(paths.review / f"{item['id']}_review.md", item)
        write_manifest(paths.manifests / f"{item['id']}_manifest.json", item["id"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local prototype oddity metadata and concept placeholders.")
    parser.add_argument("--root", default=".", help="Project root directory.")
    args = parser.parse_args()
    generate_metadata(Path(args.root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
