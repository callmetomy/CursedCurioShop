from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


SCRIPT_RESOURCE = 'res://scripts/inspectable_item.gd'


def _gd_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _gd_bool(value: bool) -> str:
    return "true" if value else "false"


def _gd_color(values: Any, fallback: list[float]) -> str:
    if not isinstance(values, list) or len(values) != 4:
        values = fallback
    channels = [str(float(channel)) for channel in values]
    return f"Color({', '.join(channels)})"


def _node_name(item_id: str) -> str:
    return "".join(part.capitalize() for part in item_id.split("_"))


def _clue_result(item: dict[str, Any], tool_name: str) -> str:
    for clue in item.get("appraisal", {}).get("clues", []):
        if clue.get("tool") == tool_name:
            return str(clue.get("result", ""))
    return ""


def _thermometer_c(item: dict[str, Any]) -> float:
    for clue in item.get("appraisal", {}).get("clues", []):
        if clue.get("tool") == "thermometer" and "temperature_c" in clue:
            return float(clue["temperature_c"])
    return 20.0


def _model_res_path(item: dict[str, Any]) -> str:
    processed_path = Path(item["model"]["processed_path"])
    return f"res://assets/models_processed/{processed_path.name}"


def _use_fallback_material(item: dict[str, Any]) -> bool:
    if "use_fallback_material" in item:
        return bool(item["use_fallback_material"])
    if "fallback_material_color" in item:
        return True
    return item.get("generation", {}).get("status") == "local_prototype"


def _fallback_material_color(item: dict[str, Any]) -> list[float]:
    if "fallback_material_color" in item:
        return item["fallback_material_color"]
    if "local_material_color" in item:
        return item["local_material_color"]
    return [0.48, 0.42, 0.36, 1.0]


def _accent_marker_color(item: dict[str, Any]) -> list[float]:
    if "accent_marker_color" in item:
        return item["accent_marker_color"]
    return [0.16, 0.72, 1.0, 1.0]


def _accent_marker_enabled(item: dict[str, Any]) -> bool:
    return bool(item.get("accent_marker_enabled", True))


def _wear_marker_enabled(item: dict[str, Any]) -> bool:
    return bool(item.get("wear_marker_enabled", False))


def _wear_marker_color(item: dict[str, Any]) -> list[float]:
    if "wear_marker_color" in item:
        return item["wear_marker_color"]
    return [0.12, 0.075, 0.035, 1.0]


def build_item_scene_text(item: dict[str, Any]) -> str:
    item_id = item["id"]
    appraisal = item.get("appraisal", {})
    economy = item.get("economy", {})
    lines = [
        f'[gd_scene load_steps=2 format=3 uid="uid://{item_id}_item_scene"]',
        "",
        f'[ext_resource type="Script" path="{SCRIPT_RESOURCE}" id="1_script"]',
        "",
        f'[node name="{_node_name(item_id)}" type="Node3D"]',
        'script = ExtResource("1_script")',
        f"item_id = {_gd_string(item_id)}",
        f"display_name = {_gd_string(str(item.get('display_name', item_id)))}",
        f"description = {_gd_string(str(appraisal.get('description', '')))}",
        f"model_path = {_gd_string(_model_res_path(item))}",
        f"correct_handling = {_gd_string(str(appraisal.get('correct_handling', 'seal')))}",
        f"magnifier_clue = {_gd_string(_clue_result(item, 'magnifier'))}",
        f"uv_clue = {_gd_string(_clue_result(item, 'uv_lamp'))}",
        f"thermometer_clue = {_gd_string(_clue_result(item, 'thermometer'))}",
        f"thermometer_c = {_thermometer_c(item):g}",
        f"sell_value = {int(economy.get('sell_value', 75))}",
        f"seal_cost = {int(economy.get('seal_cost', 20))}",
        f"wrong_event_text = {_gd_string(str(appraisal.get('wrong_handling_consequence', '')))}",
        f"use_fallback_material = {_gd_bool(_use_fallback_material(item))}",
        f"fallback_material_color = {_gd_color(_fallback_material_color(item), [0.48, 0.42, 0.36, 1.0])}",
        f"accent_marker_enabled = {_gd_bool(_accent_marker_enabled(item))}",
        f"accent_marker_color = {_gd_color(_accent_marker_color(item), [0.16, 0.72, 1.0, 1.0])}",
        f"wear_marker_enabled = {_gd_bool(_wear_marker_enabled(item))}",
        f"wear_marker_color = {_gd_color(_wear_marker_color(item), [0.12, 0.075, 0.035, 1.0])}",
        "",
        '[node name="ModelRoot" type="Node3D" parent="."]',
        "",
        '[node name="CollisionBody" type="StaticBody3D" parent="."]',
        "",
        '[node name="CollisionShape3D" type="CollisionShape3D" parent="CollisionBody"]',
        "",
    ]
    return "\n".join(lines)


def sync_item_scene(root: Path, item_path: Path) -> list[Path]:
    root = root.resolve()
    item_path = item_path.resolve()
    item = json.loads(item_path.read_text(encoding="utf-8"))
    item_id = item["id"]

    source_model = root / item["model"]["processed_path"]
    if not source_model.exists():
        raise FileNotFoundError(f"Missing processed model for {item_id}: {source_model}")

    scene_path = root / "godot" / "scenes" / "items" / f"{item_id}.tscn"
    runtime_model_path = root / "godot" / "assets" / "models_processed" / source_model.name

    scene_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_model_path.parent.mkdir(parents=True, exist_ok=True)

    scene_path.write_text(build_item_scene_text(item), encoding="utf-8")
    shutil.copyfile(source_model, runtime_model_path)
    return [scene_path, runtime_model_path]


def iter_item_paths(root: Path, item_id: str | None) -> list[Path]:
    item_root = root / "data" / "items"
    if item_id:
        return [item_root / f"{item_id}.json"]
    return sorted(path for path in item_root.glob("oddity_*.json") if path.is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Godot item scenes from item JSON data.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root.")
    parser.add_argument("--item-id", help="Optional single item id to sync.")
    args = parser.parse_args()

    root = args.root.resolve()
    written: list[Path] = []
    for item_path in iter_item_paths(root, args.item_id):
        written.extend(sync_item_scene(root, item_path))

    for path in written:
        print(path.relative_to(root).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
