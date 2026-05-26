from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotGameStateTests(unittest.TestCase):
    def test_game_state_autoload_is_registered(self):
        project = (ROOT / "godot" / "project.godot").read_text(encoding="utf-8")

        self.assertIn("[autoload]", project)
        self.assertIn('GameState="*res://scripts/game_state.gd"', project)

    def test_game_state_tracks_ten_day_loop_cash_and_reputation(self):
        script = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("extends Node", script)
        self.assertIn("var current_day := 1", script)
        self.assertIn("var max_days := 10", script)
        self.assertIn("var cash := 100", script)
        self.assertIn("var reputation := 50", script)
        self.assertIn("func start_new_run", script)
        self.assertIn("func apply_result", script)
        self.assertIn("func advance_day", script)
        self.assertIn("func is_run_complete", script)

    def test_game_state_maps_ten_days_to_demo_oddities(self):
        script = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('const DAILY_ITEM_IDS := ["oddity_0001", "oddity_0002", "oddity_0003", "oddity_0004", "oddity_0005", "oddity_0006", "oddity_0007", "oddity_0008", "oddity_0009", "oddity_0010"]', script)
        self.assertIn("func get_current_item_id", script)
        self.assertIn("func get_current_item_scene_path", script)
        self.assertIn('res://scenes/items/oddity_0002.tscn', script)
        self.assertIn('res://scenes/items/oddity_0003.tscn', script)
        self.assertIn('res://scenes/items/oddity_0004.tscn', script)
        self.assertIn('res://scenes/items/oddity_0005.tscn', script)
        self.assertIn('res://scenes/items/oddity_0006.tscn', script)
        self.assertIn('res://scenes/items/oddity_0007.tscn', script)
        self.assertIn('res://scenes/items/oddity_0008.tscn', script)
        self.assertIn('res://scenes/items/oddity_0009.tscn', script)
        self.assertIn('res://scenes/items/oddity_0010.tscn', script)

    def test_shop_and_inspection_use_game_state(self):
        shop_scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )
        controller = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )
        inspection = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="RunStatus" type="Label" parent="HUD"]', shop_scene)
        self.assertIn("run_status", controller)
        self.assertIn("GameState.current_day", controller)
        self.assertIn("GameState.apply_result", inspection)
        self.assertIn("GameState.advance_day", inspection)
        self.assertIn("GameState.is_run_complete", inspection)
        self.assertIn("GameState.get_current_item_scene_path", inspection)

    def test_shop_presents_current_customer_brief_before_inspection(self):
        shop_scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )
        controller = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("const DAILY_CUSTOMER_BRIEFS", game_state)
        self.assertIn("func get_current_customer_brief", game_state)
        self.assertIn('[node name="CustomerBriefPanel" type="PanelContainer" parent="HUD"]', shop_scene)
        self.assertIn('[node name="CustomerBriefTitle" type="Label" parent="HUD/CustomerBriefPanel/CustomerBriefContent"]', shop_scene)
        self.assertIn('[node name="CustomerBriefBody" type="Label" parent="HUD/CustomerBriefPanel/CustomerBriefContent"]', shop_scene)
        self.assertIn('[node name="CustomerRiskHint" type="Label" parent="HUD/CustomerBriefPanel/CustomerBriefContent"]', shop_scene)
        self.assertIn("customer_brief_title", controller)
        self.assertIn("customer_brief_body", controller)
        self.assertIn("customer_risk_hint", controller)
        self.assertIn("GameState.get_current_customer_brief", controller)
        self.assertIn('"risk_hint": "Risk hint:', game_state)

    def test_game_state_provides_decision_consequence_reports(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("const DAILY_CONSEQUENCE_REPORTS", game_state)
        self.assertIn("func get_current_consequence_report", game_state)
        self.assertIn('"seal": "The customer leaves without the cup"', game_state)
        self.assertIn('"sell": "The buyer complains that frost crept across the receipt"', game_state)
        self.assertIn('"discard": "The music box is removed quietly"', game_state)

    def test_game_state_provides_item_specific_wrong_decision_outcomes(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("const WRONG_DECISION_OUTCOMES", game_state)
        self.assertIn("func get_current_wrong_decision_outcome(decision: String) -> Dictionary:", game_state)
        self.assertIn('"oddity_0002": {', game_state)
        self.assertIn('"sell": {"outcome_key": "outcome.bad_appraisal", "value_delta": 35, "reputation_delta": -12, "bad_ending": false}', game_state)
        self.assertIn('"discard": {"outcome_key": "outcome.uncontained_discard", "value_delta": -5, "reputation_delta": -7, "bad_ending": false}', game_state)
        self.assertIn('"oddity_0003": {', game_state)
        self.assertIn('"seal": {"outcome_key": "outcome.bad_appraisal", "value_delta": -25, "reputation_delta": -10, "bad_ending": false}', game_state)
        self.assertIn('return _duplicate_decision_outcome(item_outcomes[decision])', game_state)

    def test_game_state_extends_wrong_decision_outcomes_to_late_demo_days(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        for item_id in [
            "oddity_0004",
            "oddity_0005",
            "oddity_0006",
            "oddity_0007",
            "oddity_0008",
            "oddity_0009",
            "oddity_0010",
        ]:
            self.assertIn(f'"{item_id}": {{', game_state)
        self.assertIn('"oddity_0004": {\n\t\t"sell": {"outcome_key": "outcome.bad_appraisal", "value_delta": 80, "reputation_delta": -18, "bad_ending": false}', game_state)
        self.assertIn('"oddity_0005": {\n\t\t"seal": {"outcome_key": "outcome.bad_appraisal", "value_delta": -20, "reputation_delta": -6, "bad_ending": false}', game_state)
        self.assertIn('"oddity_0006": {\n\t\t"seal": {"outcome_key": "outcome.bad_appraisal", "value_delta": -20, "reputation_delta": -14, "bad_ending": false}', game_state)
        self.assertIn('"oddity_0007": {\n\t\t"sell": {"outcome_key": "outcome.bad_appraisal", "value_delta": 40, "reputation_delta": -13, "bad_ending": false}', game_state)
        self.assertIn('"oddity_0008": {\n\t\t"sell": {"outcome_key": "outcome.bad_appraisal", "value_delta": 45, "reputation_delta": -14, "bad_ending": false}', game_state)
        self.assertIn('"oddity_0009": {\n\t\t"sell": {"outcome_key": "outcome.bad_appraisal", "value_delta": 60, "reputation_delta": -16, "bad_ending": false}', game_state)
        self.assertIn('"oddity_0010": {\n\t\t"seal": {"outcome_key": "outcome.bad_appraisal", "value_delta": -25, "reputation_delta": -9, "bad_ending": false}', game_state)

    def test_game_state_records_run_summary_for_final_day(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("var handled_reports := []", game_state)
        self.assertIn("handled_reports.clear()", game_state)
        self.assertIn("func record_decision_result", game_state)
        self.assertIn("func get_run_summary", game_state)
        self.assertIn('Localization.text("ui.run_summary")', game_state)
        self.assertIn('Localization.format_text("ui.final_cash"', game_state)
        self.assertIn('Localization.format_text("ui.final_reputation"', game_state)

    def test_game_state_tracks_first_run_onboarding_without_clearing_upgrades(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("var onboarding_completed := false", game_state)
        self.assertIn('TOOL_MAGNIFIER: false', game_state)
        self.assertIn('TOOL_UV_LAMP: false', game_state)
        self.assertIn('TOOL_THERMOMETER: false', game_state)
        self.assertIn("func start_new_run() -> void:", game_state)
        self.assertIn("func _reset_current_run_state() -> void:", game_state)
        self.assertIn("_reset_current_run_state()", game_state)
        self.assertNotIn("func start_new_run() -> void:\n\tcurrent_day = 1", game_state)
        self.assertNotIn("ledger_desk_upgraded = false\n\tcontainment_cabinet_upgraded = false\n\thandled_reports.clear()", game_state)

    def test_game_state_exposes_progress_reset_and_onboarding_hint_api(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("func reset_progress() -> void:", game_state)
        self.assertIn("ledger_desk_upgraded = false", game_state)
        self.assertIn("containment_cabinet_upgraded = false", game_state)
        self.assertIn("onboarding_completed = false", game_state)
        self.assertIn("func record_onboarding_tool_used(tool_name: String) -> void:", game_state)
        self.assertIn("func get_onboarding_hint_key() -> String:", game_state)
        self.assertIn('return "tutorial.inspect_magnifier"', game_state)
        self.assertIn('return "tutorial.inspect_uv"', game_state)
        self.assertIn('return "tutorial.inspect_temperature"', game_state)
        self.assertIn('return "tutorial.choose_handling"', game_state)

    def test_game_state_exposes_reviewable_result_details(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("func get_result_detail_count", game_state)
        self.assertIn("func get_result_detail", game_state)
        self.assertIn("func _get_decision_label", game_state)
        self.assertIn('"value_delta": value_delta', game_state)
        self.assertIn('"reputation_delta": reputation_delta', game_state)
        self.assertIn('"cash_after": cash', game_state)
        self.assertIn('"reputation_after": reputation', game_state)
        self.assertIn('"pressure_key": get_daily_pressure_key(reputation)', game_state)
        self.assertIn('"outcome_key": outcome_key', game_state)
        self.assertIn('"outcome_note_key": get_outcome_note_key(item_id, decision, outcome_key)', game_state)
        self.assertIn('"consequence_key": consequence_key', game_state)
        self.assertIn("func get_outcome_note_key(item_id: String, decision: String, outcome_key: String) -> String:", game_state)
        self.assertIn("func get_daily_pressure_key(reputation_after: int) -> String:", game_state)
        self.assertIn('return "daily_pressure.critical"', game_state)
        self.assertIn('return "daily_pressure.strained"', game_state)
        self.assertIn('return "daily_pressure.stable"', game_state)
        self.assertIn("func _get_outcome_note_text(report: Dictionary) -> String:", game_state)
        self.assertIn("func _get_pressure_text(report: Dictionary) -> String:", game_state)
        self.assertIn('Localization.format_text("ui.result_detail_title"', game_state)
        self.assertIn('Localization.format_text("ui.result_detail_body"', game_state)
        self.assertIn('Localization.text(str(report.get("outcome_note_key", "outcome_note.none")))', game_state)
        self.assertIn('int(report.get("cash_after", cash))', game_state)
        self.assertIn('int(report.get("reputation_after", reputation))', game_state)
        self.assertIn('Localization.text("outcome_note.none")', game_state)
        self.assertIn('Localization.text("ui.result_detail_empty")', game_state)
        self.assertIn('Localization.text("decision.%s" % decision)', game_state)

    def test_shop_shows_ten_day_ledger_from_handled_reports(self):
        shop_scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )
        controller = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("func get_shop_ledger", game_state)
        self.assertIn('"Shop Ledger"', game_state)
        self.assertIn('Localization.text("ui.no_appraisals")', game_state)
        self.assertIn('[node name="ShopLedgerPanel" type="PanelContainer" parent="HUD"]', shop_scene)
        self.assertIn('[node name="ShopLedgerTitle" type="Label" parent="HUD/ShopLedgerPanel/ShopLedgerContent"]', shop_scene)
        self.assertIn('[node name="ShopLedgerBody" type="Label" parent="HUD/ShopLedgerPanel/ShopLedgerContent"]', shop_scene)
        self.assertIn("shop_ledger_title", controller)
        self.assertIn("shop_ledger_body", controller)
        self.assertIn("GameState.get_shop_ledger", controller)

    def test_shop_exposes_result_detail_review_panel(self):
        shop_scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )
        controller = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="ResultDetailPanel" type="PanelContainer" parent="HUD"]', shop_scene)
        self.assertIn('[node name="ResultDetailTitle" type="Label" parent="HUD/ResultDetailPanel/ResultDetailContent"]', shop_scene)
        self.assertIn('[node name="ResultDetailBody" type="Label" parent="HUD/ResultDetailPanel/ResultDetailContent"]', shop_scene)
        self.assertIn('[node name="ResultDetailNav" type="HBoxContainer" parent="HUD/ResultDetailPanel/ResultDetailContent"]', shop_scene)
        self.assertIn('[node name="ResultDetailPreviousButton" type="Button" parent="HUD/ResultDetailPanel/ResultDetailContent/ResultDetailNav"]', shop_scene)
        self.assertIn('[node name="ResultDetailNextButton" type="Button" parent="HUD/ResultDetailPanel/ResultDetailContent/ResultDetailNav"]', shop_scene)
        self.assertIn("result_detail_panel", controller)
        self.assertIn("result_detail_title", controller)
        self.assertIn("result_detail_body", controller)
        self.assertIn("result_detail_previous_button", controller)
        self.assertIn("result_detail_next_button", controller)
        self.assertIn("var result_detail_index := 0", controller)
        self.assertIn("func _update_result_detail_panel", controller)
        self.assertIn("GameState.get_result_detail_count", controller)
        self.assertIn("GameState.get_result_detail", controller)
        self.assertIn("_on_result_detail_previous_pressed", controller)
        self.assertIn("_on_result_detail_next_pressed", controller)

    def test_shop_hud_panels_use_1152_safe_areas(self):
        shop_scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn("offset_left = 24.0\noffset_top = 72.0\noffset_right = 376.0\noffset_bottom = 238.0", shop_scene)
        self.assertIn("offset_left = -400.0\noffset_top = 24.0\noffset_right = -24.0\noffset_bottom = 210.0", shop_scene)
        self.assertIn("offset_left = 24.0\noffset_top = 24.0\noffset_right = 376.0\noffset_bottom = 58.0", shop_scene)

    def test_ten_day_demo_smoke_script_exercises_core_flow(self):
        script_path = ROOT / "godot" / "tools" / "smoke_three_day_flow.gd"
        self.assertTrue(script_path.exists())

        script = script_path.read_text(encoding="utf-8")
        self.assertIn('load("res://scenes/inspection_table.tscn") as PackedScene', script)
        self.assertIn('const EXPECTED_ITEMS := ["oddity_0001", "oddity_0002", "oddity_0003", "oddity_0004", "oddity_0005", "oddity_0006", "oddity_0007", "oddity_0008", "oddity_0009", "oddity_0010"]', script)
        self.assertIn('const CORRECT_DECISIONS := ["seal", "seal", "discard", "seal", "sell", "discard", "seal", "seal", "seal", "sell"]', script)
        self.assertIn("_resolve_decision", script)
        self.assertIn("_on_next_day_pressed", script)
        self.assertIn('_game_state().get("current_day")', script)
        self.assertIn("_on_magnifier_pressed", script)
        self.assertIn("HUD/AppraisalNotesBackground/AppraisalNotesLabel", script)
        self.assertIn("HUD/AbnormalEventPanel", script)
        self.assertIn("HUD/BadEndingCard", script)
        self.assertIn("HUD/BadEndingCard/BadEndingPanel", script)
        self.assertIn("HUD/ResultDetailPanel", script)
        self.assertIn("HUD/ResultDetailPanel/ResultDetailContent/ResultDetailBody", script)
        self.assertIn("HUD/DayResultPanel/ResultTextPanel/ResultTextContent/PressureSummaryLabel", script)
        self.assertIn("Day result should show post-decision pressure summary", script)
        self.assertIn("Shop result detail should show the post-decision pressure summary", script)
        self.assertIn("_verify_item_specific_wrong_outcome", script)
        self.assertIn('Day 2 wrong sale should use item-specific cash delta', script)
        self.assertIn('Day 2 wrong sale should use item-specific reputation delta', script)
        self.assertIn("_verify_late_game_wrong_outcomes", script)
        self.assertIn('Day 8 wrong sale should use late-game cash delta', script)
        self.assertIn('Day 10 wrong discard should use late-game reputation delta', script)
        self.assertIn('Day 8 wrong sale result detail should explain the mistake', script)
        self.assertIn("_verify_upgraded_second_run_economy", script)
        self.assertIn("Upgraded second run should finish with discounted final cash", script)
        self.assertIn("Upgraded second run should keep enough cash buffer", script)
        self.assertIn("== 210", script)
        self.assertIn(">= 35", script)
        self.assertIn("quit(0)", script)


if __name__ == "__main__":
    unittest.main()
