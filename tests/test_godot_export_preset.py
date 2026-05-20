from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotExportPresetTests(unittest.TestCase):
    def test_windows_export_preset_exists(self):
        preset = (ROOT / "godot" / "export_presets.cfg").read_text(encoding="utf-8")

        self.assertIn('name="Windows Desktop"', preset)
        self.assertIn('platform="Windows Desktop"', preset)
        self.assertIn('export_path="../exports/windows/CursedCurioShop.exe"', preset)
        self.assertIn('exclude_filter="assets/models_raw/*"', preset)
        self.assertIn("application/file_version", preset)
        self.assertIn("application/product_name", preset)


if __name__ == "__main__":
    unittest.main()
