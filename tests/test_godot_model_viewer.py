from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotModelViewerTests(unittest.TestCase):
    def test_model_viewer_loads_tracked_oddity_processed_model(self):
        script = (ROOT / "godot" / "scripts" / "model_viewer.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("res://assets/models_processed/oddity_0001.glb", script)
        self.assertNotIn("../assets/models_raw/oddity_0001.glb", script)
        self.assertNotIn("tripo_teacup.glb", script)

    def test_godot_readme_points_to_processed_pipeline_output(self):
        readme = (ROOT / "godot" / "README.md").read_text(encoding="utf-8")

        self.assertIn("res://assets/models_processed/oddity_0001.glb", readme)
        self.assertNotIn("../assets/models_raw/oddity_0001.glb", readme)


if __name__ == "__main__":
    unittest.main()
