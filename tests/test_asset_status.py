import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.asset_pipeline.items import build_item_definition, save_item_definition
from tools.asset_pipeline.status import build_asset_status, render_asset_status_markdown


class AssetStatusTests(unittest.TestCase):
    def test_build_asset_status_reports_existing_and_missing_outputs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            item = build_item_definition(
                item_id="oddity_0042",
                display_name="Cold Brass Key",
                concept_prompt="A cold brass key concept.",
                model_prompt="A cold brass key model.",
            )
            save_item_definition(item, root / "data" / "items")
            (root / "assets" / "models_raw").mkdir(parents=True)
            (root / "assets" / "models_raw" / "oddity_0042.glb").write_bytes(b"glb")

            status = build_asset_status(root=root, item_id="oddity_0042")

            self.assertEqual(status["item_id"], "oddity_0042")
            self.assertEqual(status["display_name"], "Cold Brass Key")
            self.assertEqual(
                [asset["stage"] for asset in status["assets"]],
                ["concept_image", "raw_model", "processed_model", "review_report"],
            )
            self.assertEqual(
                [asset["exists"] for asset in status["assets"]],
                [False, True, False, False],
            )
            self.assertEqual(
                status["missing_stages"],
                ["concept_image", "processed_model", "review_report"],
            )

    def test_render_asset_status_markdown_is_readable_for_production_review(self):
        status = {
            "item_id": "oddity_0042",
            "display_name": "Cold Brass Key",
            "generation_status": "draft",
            "approved": False,
            "assets": [
                {
                    "stage": "raw_model",
                    "path": "assets/models_raw/oddity_0042.glb",
                    "exists": True,
                },
                {
                    "stage": "processed_model",
                    "path": "assets/models_processed/oddity_0042.glb",
                    "exists": False,
                },
            ],
            "missing_stages": ["processed_model"],
        }

        markdown = render_asset_status_markdown(status)

        self.assertIn("# Asset Status: Cold Brass Key", markdown)
        self.assertIn("- raw_model: ready (`assets/models_raw/oddity_0042.glb`)", markdown)
        self.assertIn("- processed_model: missing (`assets/models_processed/oddity_0042.glb`)", markdown)
        self.assertTrue(markdown.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
