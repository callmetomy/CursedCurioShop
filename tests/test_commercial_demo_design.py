import json
import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CommercialDemoDesignTests(unittest.TestCase):
    def _items(self) -> list[dict]:
        item_paths = sorted((ROOT / "data" / "items").glob("oddity_*.json"))
        return [
            json.loads(path.read_text(encoding="utf-8"))
            for path in item_paths
        ]

    def _locale_block(self, locale: str) -> str:
        localization = (ROOT / "godot" / "scripts" / "localization.gd").read_text(
            encoding="utf-8"
        )
        pattern = rf'\t"{re.escape(locale)}": \{{(?P<body>.*?)\n\t\}},'
        match = re.search(pattern, localization, re.DOTALL)
        self.assertIsNotNone(match, f"Missing locale block: {locale}")
        return match.group("body")

    def test_demo_items_use_specific_clues_instead_of_template_placeholders(self):
        banned_phrases = [
            "A local prototype oddity",
            "Fine scratches form a deliberate appraisal mark.",
            "A hidden blue mark appears under UV light.",
            "The reading is inconsistent with the room.",
            "A minor abnormal event is queued for the shop.",
        ]

        for item in self._items():
            appraisal = item["appraisal"]
            combined_text = " ".join(
                [
                    appraisal["description"],
                    appraisal["wrong_handling_consequence"],
                    *[clue["result"] for clue in appraisal["clues"]],
                ]
            )
            for phrase in banned_phrases:
                self.assertNotIn(phrase, combined_text, item["id"])

    def test_customer_risk_hints_do_not_directly_name_the_correct_action(self):
        forbidden = [
            "seal",
            "sell",
            "sale",
            "resale",
            "discard",
            "containment",
            "封存",
            "出售",
            "轉售",
            "丟棄",
            "建议",
            "建議",
        ]

        for locale in ["en", "zh_TW"]:
            block = self._locale_block(locale)
            hints = re.findall(
                r'"customer\.oddity_\d+\.risk_hint": "([^"]+)"',
                block,
            )
            self.assertEqual(len(hints), 10)
            for hint in hints:
                lowered = hint.lower()
                for word in forbidden:
                    self.assertNotIn(word, lowered, hint)

    def test_sell_values_and_seal_costs_create_real_economic_tradeoffs(self):
        items = self._items()
        sell_values = {item["economy"]["sell_value"] for item in items}
        seal_costs = {item["economy"]["seal_cost"] for item in items}
        base_values = {item["economy"]["base_value"] for item in items}

        self.assertGreaterEqual(len(sell_values), 5)
        self.assertGreaterEqual(len(seal_costs), 4)
        self.assertGreaterEqual(len(base_values), 5)
        self.assertTrue(any(item["economy"]["seal_cost"] >= 35 for item in items))
        self.assertTrue(any(item["economy"]["sell_value"] <= 45 for item in items))

    def test_correct_ten_day_path_preserves_cash_pressure_without_debt(self):
        cash = 100
        daily_cash = []
        for item in self._items():
            handling = item["appraisal"]["correct_handling"]
            economy = item["economy"]
            if handling == "sell":
                cash += economy["sell_value"]
            elif handling == "seal":
                cash -= economy["seal_cost"]
            daily_cash.append(cash)

        self.assertGreaterEqual(min(daily_cash), 20)
        self.assertLessEqual(min(daily_cash), 50)
        self.assertGreaterEqual(cash, 180)
        self.assertLessEqual(cash, 260)


if __name__ == "__main__":
    unittest.main()
