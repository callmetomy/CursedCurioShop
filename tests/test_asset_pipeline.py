import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.asset_pipeline.config import ProjectPaths
from tools.asset_pipeline.items import build_item_definition, save_item_definition
from tools.asset_pipeline.manifest import AssetManifest


class AssetPipelineTests(unittest.TestCase):
    def test_project_paths_resolve_expected_workspace_directories(self):
        paths = ProjectPaths(ROOT)

        self.assertEqual(paths.data_items, ROOT / "data" / "items")
        self.assertEqual(paths.concepts, ROOT / "assets" / "concepts")
        self.assertEqual(paths.models_raw, ROOT / "assets" / "models_raw")
        self.assertEqual(paths.models_processed, ROOT / "assets" / "models_processed")
        self.assertEqual(paths.review, ROOT / "assets" / "review")

    def test_build_item_definition_creates_stable_asset_paths(self):
        item = build_item_definition(
            item_id="oddity_0007",
            display_name="Whispering Teacup",
            concept_prompt="A cracked porcelain teacup with a dark stain.",
            model_prompt="A cursed porcelain teacup game prop.",
        )

        self.assertEqual(item["id"], "oddity_0007")
        self.assertEqual(item["display_name"], "Whispering Teacup")
        self.assertEqual(item["model"]["raw_path"], "assets/models_raw/oddity_0007.glb")
        self.assertEqual(
            item["model"]["processed_path"],
            "assets/models_processed/oddity_0007.glb",
        )
        self.assertEqual(item["generation"]["status"], "draft")
        self.assertIs(item["generation"]["approved"], False)

    def test_save_item_definition_writes_pretty_json(self):
        item = build_item_definition(
            item_id="oddity_0008",
            display_name="Cold Brass Key",
            concept_prompt="A cold brass key with a cracked handle.",
            model_prompt="A cursed brass key game prop.",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = save_item_definition(item, Path(temp_dir))

            self.assertEqual(output_path, Path(temp_dir) / "oddity_0008.json")
            saved = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["id"], "oddity_0008")
            self.assertTrue(output_path.read_text(encoding="utf-8").endswith("\n"))

    def test_asset_manifest_tracks_generation_attempts(self):
        manifest = AssetManifest()

        manifest.add_attempt(
            item_id="oddity_0009",
            stage="meshy_model",
            status="queued",
            output_path="assets/models_raw/oddity_0009.glb",
        )

        data = manifest.to_dict()
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["attempts"][0]["item_id"], "oddity_0009")
        self.assertEqual(data["attempts"][0]["stage"], "meshy_model")
        self.assertEqual(data["attempts"][0]["status"], "queued")


if __name__ == "__main__":
    unittest.main()
