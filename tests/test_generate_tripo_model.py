import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.asset_pipeline.generate_tripo_model import (
    append_manifest_attempt,
    build_tripo_model_job,
)
from tools.asset_pipeline.items import build_item_definition, save_item_definition


class GenerateTripoModelTests(unittest.TestCase):
    def test_build_tripo_model_job_uses_item_prompt_and_raw_model_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            item = build_item_definition(
                item_id="oddity_0010",
                display_name="Moth-Eaten Doll",
                concept_prompt="A moth-eaten doll concept.",
                model_prompt="A moth-eaten doll game prop.",
            )
            save_item_definition(item, root / "data" / "items")

            job = build_tripo_model_job(root=root, item_id="oddity_0010")

            self.assertEqual(job["item_id"], "oddity_0010")
            self.assertEqual(job["display_name"], "Moth-Eaten Doll")
            self.assertEqual(job["payload"]["type"], "text_to_model")
            self.assertEqual(job["payload"]["prompt"], "A moth-eaten doll game prop.")
            self.assertEqual(job["output_path"], "assets/models_raw/oddity_0010.glb")
            self.assertEqual(job["manifest_path"], "data/manifests/oddity_0010_manifest.json")

    def test_append_manifest_attempt_preserves_existing_item_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_path = root / "data" / "manifests" / "oddity_0011_manifest.json"
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "attempts": [
                            {
                                "item_id": "oddity_0011",
                                "stage": "item_definition",
                                "status": "created",
                                "output_path": "data/items/oddity_0011.json",
                                "created_at": "2026-05-20T00:00:00+00:00",
                            }
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            append_manifest_attempt(
                root=root,
                item_id="oddity_0011",
                stage="tripo_text_to_model",
                status="submitted",
                output_path="tripo:task_123",
            )

            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(len(data["attempts"]), 2)
            self.assertEqual(data["attempts"][0]["stage"], "item_definition")
            self.assertEqual(data["attempts"][1]["stage"], "tripo_text_to_model")
            self.assertEqual(data["attempts"][1]["output_path"], "tripo:task_123")


if __name__ == "__main__":
    unittest.main()
