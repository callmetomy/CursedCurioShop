import json
from pathlib import Path
from typing import Any


def build_item_definition(
    *,
    item_id: str,
    display_name: str,
    concept_prompt: str,
    model_prompt: str,
    rarity: str = "common",
    danger_level: int = 1,
) -> dict[str, Any]:
    return {
        "id": item_id,
        "display_name": display_name,
        "rarity": rarity,
        "danger_level": danger_level,
        "visual_theme": ["antique", "cursed", "shop_prop"],
        "model": {
            "raw_path": f"assets/models_raw/{item_id}.glb",
            "processed_path": f"assets/models_processed/{item_id}.glb",
            "scale_meters": 0.35,
        },
        "appraisal": {
            "description": "",
            "clues": [],
            "correct_handling": "seal",
            "wrong_handling_consequence": "",
        },
        "economy": {
            "base_value": 50,
            "sell_value": 75,
            "seal_cost": 20,
        },
        "generation": {
            "status": "draft",
            "concept_prompt": concept_prompt,
            "model_prompt": model_prompt,
            "attempts": 0,
            "approved": False,
        },
    }


def save_item_definition(item: dict[str, Any], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{item['id']}.json"
    output_path.write_text(
        json.dumps(item, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path
