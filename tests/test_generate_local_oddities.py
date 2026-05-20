import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.asset_pipeline.generate_local_oddities import LOCAL_ODDITY_SPECS, build_local_item


class GenerateLocalOdditiesTests(unittest.TestCase):
    def test_local_oddity_specs_fill_demo_roster(self):
        self.assertEqual(len(LOCAL_ODDITY_SPECS), 9)
        self.assertEqual(LOCAL_ODDITY_SPECS[0]["item_id"], "oddity_0002")
        self.assertEqual(LOCAL_ODDITY_SPECS[-1]["item_id"], "oddity_0010")
        self.assertEqual(len({spec["item_id"] for spec in LOCAL_ODDITY_SPECS}), 9)

    def test_build_local_item_contains_three_tool_clues(self):
        item = build_local_item(LOCAL_ODDITY_SPECS[0])

        self.assertEqual(item["id"], "oddity_0002")
        self.assertEqual(item["generation"]["status"], "local_prototype")
        self.assertEqual(item["generation"]["approved"], True)
        clue_tools = {clue["tool"] for clue in item["appraisal"]["clues"]}
        self.assertEqual(clue_tools, {"magnifier", "uv_lamp", "thermometer"})
        self.assertTrue(item["appraisal"]["description"])


if __name__ == "__main__":
    unittest.main()
