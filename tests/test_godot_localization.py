from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotLocalizationTests(unittest.TestCase):
    def _locale_block(self, localization: str, locale: str) -> str:
        pattern = rf'\t"{re.escape(locale)}": \{{(?P<body>.*?)\n\t\}},'
        match = re.search(pattern, localization, re.DOTALL)
        self.assertIsNotNone(match, f"Missing locale block: {locale}")
        return match.group("body")

    def test_localization_autoload_supports_required_languages_and_defaults_to_traditional_chinese(self):
        project = (ROOT / "godot" / "project.godot").read_text(encoding="utf-8")
        localization = (ROOT / "godot" / "scripts" / "localization.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('Localization="*res://scripts/localization.gd"', project)
        self.assertIn('const DEFAULT_LOCALE := "zh_TW"', localization)
        for locale in ["en", "ja", "ko", "es", "pt", "ru", "zh_CN", "zh_TW"]:
            self.assertIn(f'"{locale}"', localization)
        self.assertIn("func set_locale(locale_code: String) -> void:", localization)
        self.assertIn("func text(key: String) -> String:", localization)
        self.assertIn("func format_text(key: String, values: Array) -> String:", localization)

    def test_localization_contains_core_ui_and_demo_item_text_for_each_language(self):
        localization = (ROOT / "godot" / "scripts" / "localization.gd").read_text(
            encoding="utf-8"
        )

        required_keys = [
            "ui.start_day",
            "ui.quit",
            "ui.back_to_shop",
            "ui.sell",
            "ui.seal",
            "ui.discard",
            "ui.next_day",
            "ui.return_to_menu",
            "ui.appraisal_notes",
            "ui.shop_ledger",
            "ui.result_detail_title",
            "ui.result_detail_empty",
            "ui.result_detail_body",
            "ui.detail_previous",
            "ui.detail_next",
            "decision.sell",
            "decision.seal",
            "decision.discard",
            "item.oddity_0001.display_name",
            "item.oddity_0001.description",
            "item.oddity_0001.magnifier_clue",
            "item.oddity_0001.uv_clue",
            "item.oddity_0001.thermometer_clue",
            "item.oddity_0001.wrong_event_text",
            "customer.oddity_0001.title",
            "customer.oddity_0001.body",
            "customer.oddity_0001.risk_hint",
            "consequence.oddity_0001.sell",
            "ending.frost_sale.title",
        ]
        for item_id in ["oddity_0002", "oddity_0003", "oddity_0004", "oddity_0005", "oddity_0006", "oddity_0007", "oddity_0008"]:
            required_keys.extend(
                [
                    f"item.{item_id}.display_name",
                    f"item.{item_id}.description",
                    f"item.{item_id}.magnifier_clue",
                    f"item.{item_id}.uv_clue",
                    f"item.{item_id}.thermometer_clue",
                    f"item.{item_id}.wrong_event_text",
                    f"customer.{item_id}.title",
                    f"customer.{item_id}.body",
                    f"customer.{item_id}.risk_hint",
                    f"consequence.{item_id}.seal",
                    f"consequence.{item_id}.sell",
                    f"consequence.{item_id}.discard",
                ]
            )
        for locale in ["en", "ja", "ko", "es", "pt", "ru", "zh_CN", "zh_TW"]:
            locale_block = self._locale_block(localization, locale)
            for key in required_keys:
                self.assertIn(f'"{key}"', locale_block)

    def test_game_scenes_and_scripts_use_localized_text(self):
        main_menu_script = (ROOT / "godot" / "scripts" / "main_menu.gd").read_text(
            encoding="utf-8"
        )
        shop_script = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )
        table_script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('Localization.text("ui.start_day")', main_menu_script)
        self.assertIn('Localization.text("ui.quit")', main_menu_script)
        self.assertIn("Localization.format_text", shop_script)
        self.assertIn("Localization.text", table_script)
        self.assertIn("Localization.item_text", table_script)
        self.assertIn("Localization.text", game_state)


if __name__ == "__main__":
    unittest.main()
