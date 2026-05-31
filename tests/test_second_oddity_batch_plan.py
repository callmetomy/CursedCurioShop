from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
