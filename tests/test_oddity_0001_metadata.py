import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Oddity0001MetadataTests(unittest.TestCase):
    def test_teacup_has_appraisal_clues_for_three_tools(self):
        item = json.loads((ROOT / "data" / "items" / "oddity_0001.json").read_text(encoding="utf-8"))

        self.assertTrue(item["appraisal"]["description"])
        self.assertIn("correct_handling", item["appraisal"])
        self.assertEqual(item["appraisal"]["correct_handling"], "seal")
        self.assertGreaterEqual(len(item["appraisal"]["clues"]), 3)
        clue_tools = {clue["tool"] for clue in item["appraisal"]["clues"]}
        self.assertEqual(clue_tools, {"magnifier", "uv_lamp", "thermometer"})
        thermometer = next(clue for clue in item["appraisal"]["clues"] if clue["tool"] == "thermometer")
        self.assertIn("temperature_c", thermometer)
        self.assertLess(thermometer["temperature_c"], 0)


if __name__ == "__main__":
    unittest.main()
