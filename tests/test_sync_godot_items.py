import json
import tempfile
import unittest
from pathlib import Path

from tools.godot.sync_item_scenes import build_item_scene_text, sync_item_scene


class SyncGodotItemsTests(unittest.TestCase):
    def test_build_item_scene_text_uses_item_metadata(self):
        item = {
            "id": "oddity_0099",
            "display_name": "Test Relic",
            "model": {"processed_path": "assets/models_processed/oddity_0099.glb"},
            "appraisal": {
                "clues": [
                    {"tool": "magnifier", "result": "Tiny teeth marks line the rim."},
                    {"tool": "uv_lamp", "result": "A violet sigil appears."},
                    {
                        "tool": "thermometer",
                        "result": "The object reads cold.",
                        "temperature_c": -5.5,
                    },
                ],
                "correct_handling": "seal",
                "wrong_handling_consequence": "The relic knocks from inside the drawer.",
            },
            "economy": {"sell_value": 88, "seal_cost": 33},
        }

        scene = build_item_scene_text(item)

        self.assertIn('item_id = "oddity_0099"', scene)
        self.assertIn('display_name = "Test Relic"', scene)
        self.assertIn('model_path = "res://assets/models_processed/oddity_0099.glb"', scene)
        self.assertIn('correct_handling = "seal"', scene)
        self.assertIn('magnifier_clue = "Tiny teeth marks line the rim."', scene)
        self.assertIn('uv_clue = "A violet sigil appears."', scene)
        self.assertIn('thermometer_clue = "The object reads cold."', scene)
        self.assertIn("thermometer_c = -5.5", scene)
        self.assertIn("sell_value = 88", scene)
        self.assertIn("seal_cost = 33", scene)

    def test_sync_item_scene_writes_scene_and_runtime_model(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data" / "items").mkdir(parents=True)
            (root / "assets" / "models_processed").mkdir(parents=True)
            (root / "assets" / "models_processed" / "oddity_0099.glb").write_bytes(b"glb")
            item = {
                "id": "oddity_0099",
                "display_name": "Test Relic",
                "model": {"processed_path": "assets/models_processed/oddity_0099.glb"},
                "appraisal": {
                    "clues": [],
                    "correct_handling": "discard",
                    "wrong_handling_consequence": "Bad event.",
                },
                "economy": {"sell_value": 40, "seal_cost": 10},
            }
            item_path = root / "data" / "items" / "oddity_0099.json"
            item_path.write_text(json.dumps(item), encoding="utf-8")

            outputs = sync_item_scene(root, item_path)

            self.assertIn(root / "godot" / "scenes" / "items" / "oddity_0099.tscn", outputs)
            self.assertIn(root / "godot" / "assets" / "models_processed" / "oddity_0099.glb", outputs)
            self.assertEqual(
                (root / "godot" / "assets" / "models_processed" / "oddity_0099.glb").read_bytes(),
                b"glb",
            )


if __name__ == "__main__":
    unittest.main()
