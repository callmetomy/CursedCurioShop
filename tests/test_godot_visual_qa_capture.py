import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GodotVisualQACaptureTests(unittest.TestCase):
    def test_capture_script_records_traditional_chinese_review_states(self):
        script_path = ROOT / "godot" / "tools" / "capture_traditional_chinese_review.gd"
        self.assertTrue(script_path.exists())

        script = script_path.read_text(encoding="utf-8")
        self.assertIn('const OUTPUT_DIR := "res://../docs/production/playtests/screenshots"', script)
        self.assertIn('{"name": "1152x648", "size": Vector2i(1152, 648)}', script)
        self.assertIn('{"name": "1280x720", "size": Vector2i(1280, 720)}', script)
        self.assertIn('_capture_shop_customer_brief', script)
        self.assertIn('_capture_shop_result_detail', script)
        self.assertIn('_capture_day_result', script)
        self.assertIn('_capture_final_summary', script)
        self.assertIn('_localization().call("set_locale", "zh_TW")', script)
        self.assertIn('func _localization() -> Node:', script)
        self.assertIn('shop_customer_brief', script)
        self.assertIn('shop_result_detail', script)
        self.assertIn('day_result', script)
        self.assertIn('final_summary', script)
        self.assertIn('save_png', script)
        self.assertIn("Run without --headless", script)
        self.assertIn('quit(0)', script)


if __name__ == "__main__":
    unittest.main()
