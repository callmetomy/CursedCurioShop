from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotGameStateTests(unittest.TestCase):
    def test_game_state_autoload_is_registered(self):
        project = (ROOT / "godot" / "project.godot").read_text(encoding="utf-8")

        self.assertIn("[autoload]", project)
        self.assertIn('GameState="*res://scripts/game_state.gd"', project)

    def test_game_state_tracks_nine_day_loop_cash_and_reputation(self):
        script = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("extends Node", script)
        self.assertIn("var current_day := 1", script)
        self.assertIn("var max_days := 9", script)
        self.assertIn("var cash := 100", script)
        self.assertIn("var reputation := 50", script)
        self.assertIn("func start_new_run", script)
        self.assertIn("func apply_result", script)
        self.assertIn("func advance_day", script)
        self.assertIn("func is_run_complete", script)

    def test_game_state_maps_nine_days_to_demo_oddities(self):
        script = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('const DAILY_ITEM_IDS := ["oddity_0001", "oddity_0002", "oddity_0003", "oddity_0004", "oddity_0005", "oddity_0006", "oddity_0007", "oddity_0008", "oddity_0009"]', script)
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

    def test_game_state_exposes_reviewable_result_details(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("func get_result_detail_count", game_state)
        self.assertIn("func get_result_detail", game_state)
        self.assertIn("func _get_decision_label", game_state)
        self.assertIn('"value_delta": value_delta', game_state)
        self.assertIn('"reputation_delta": reputation_delta', game_state)
        self.assertIn('"outcome_key": outcome_key', game_state)
        self.assertIn('"consequence_key": consequence_key', game_state)
        self.assertIn('Localization.format_text("ui.result_detail_title"', game_state)
        self.assertIn('Localization.format_text("ui.result_detail_body"', game_state)
        self.assertIn('Localization.text("ui.result_detail_empty")', game_state)
        self.assertIn('Localization.text("decision.%s" % decision)', game_state)

    def test_shop_shows_nine_day_ledger_from_handled_reports(self):
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

    def test_nine_day_demo_smoke_script_exercises_core_flow(self):
        script_path = ROOT / "godot" / "tools" / "smoke_three_day_flow.gd"
        self.assertTrue(script_path.exists())

        script = script_path.read_text(encoding="utf-8")
        self.assertIn('load("res://scenes/inspection_table.tscn") as PackedScene', script)
        self.assertIn('const EXPECTED_ITEMS := ["oddity_0001", "oddity_0002", "oddity_0003", "oddity_0004", "oddity_0005", "oddity_0006", "oddity_0007", "oddity_0008", "oddity_0009"]', script)
        self.assertIn('const CORRECT_DECISIONS := ["seal", "seal", "discard", "seal", "sell", "discard", "seal", "seal", "discard"]', script)
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
        self.assertIn("quit(0)", script)


if __name__ == "__main__":
    unittest.main()
