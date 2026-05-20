from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotModelViewerTests(unittest.TestCase):
    def test_model_viewer_loads_tracked_oddity_raw_model(self):
        script = (ROOT / "godot" / "scripts" / "model_viewer.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("../assets/models_raw/oddity_0001.glb", script)
        self.assertNotIn("tripo_teacup.glb", script)


if __name__ == "__main__":
    unittest.main()
