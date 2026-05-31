from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SecondOddityBatchPlanTests(unittest.TestCase):
    def test_second_oddity_batch_eval_defines_narrow_candidate_gate(self):
        plan_path = ROOT / "docs" / "production" / "second_oddity_batch_eval.md"
        self.assertTrue(plan_path.exists())

        plan = plan_path.read_text(encoding="utf-8")
        for item_id in ["oddity_0011", "oddity_0012", "oddity_0013"]:
            self.assertIn(item_id, plan)
        self.assertNotIn("oddity_0014", plan)
        for decision in ["sell", "seal", "discard"]:
            self.assertIn(f"`{decision}`", plan)
        for gate in [
            "Clue readability gate",
            "Wrong-outcome clarity gate",
            "Traditional Chinese capture gate",
        ]:
            self.assertIn(gate, plan)

    def test_oddity_0011_candidate_json_is_drafted_but_not_playable(self):
        item_path = ROOT / "data" / "items" / "oddity_0011.json"
        self.assertTrue(item_path.exists())

        item = json.loads(item_path.read_text(encoding="utf-8"))
        self.assertEqual(item["id"], "oddity_0011")
        self.assertEqual(item["display_name"], "Cracked Apothecary Scale")
        self.assertEqual(item["appraisal"]["correct_handling"], "seal")
        self.assertEqual(item["generation"]["status"], "draft")
        self.assertIs(item["generation"]["approved"], False)
        self.assertGreaterEqual(item["danger_level"], 2)
        self.assertEqual(
            {clue["tool"] for clue in item["appraisal"]["clues"]},
            {"magnifier", "uv_lamp", "thermometer"},
        )
        self.assertIn("undercounting", item["appraisal"]["wrong_handling_consequence"])

        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )
        self.assertNotIn('"oddity_0011"', game_state)
        self.assertFalse((ROOT / "godot" / "scenes" / "items" / "oddity_0011.tscn").exists())


if __name__ == "__main__":
    unittest.main()
