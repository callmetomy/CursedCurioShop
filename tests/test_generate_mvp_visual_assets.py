import tempfile
import unittest
from pathlib import Path

from PIL import Image

from tools.art.generate_mvp_visual_assets import ASSET_SPECS, generate_assets


class GenerateMvpVisualAssetsTests(unittest.TestCase):
    def test_generate_assets_writes_expected_pngs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            written = generate_assets(root)

            written_paths = {path.relative_to(root).as_posix() for path in written}
            for relative_path, expected_size in ASSET_SPECS.items():
                output_path = root / "godot" / "assets" / relative_path
                self.assertIn(output_path.relative_to(root).as_posix(), written_paths)
                self.assertTrue(output_path.exists())

                with Image.open(output_path) as image:
                    self.assertEqual(image.size, expected_size)
                    self.assertEqual(image.mode, "RGBA")

            self.assertTrue((root / "godot" / "assets" / "visual_asset_manifest.json").exists())

    def test_transparent_decals_include_alpha(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generate_assets(root)

            for relative_path in ["textures/cursed_teacup_decal.png", "textures/uv_ring_mark.png"]:
                with Image.open(root / "godot" / "assets" / relative_path) as image:
                    alpha = image.getchannel("A")
                    self.assertLess(alpha.getextrema()[0], 10)
                    self.assertGreater(alpha.getextrema()[1], 100)


if __name__ == "__main__":
    unittest.main()
