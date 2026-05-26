from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotInspectionTableTests(unittest.TestCase):
    def test_shop_prototype_scene_exists_for_main_menu_start(self):
        scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="ShopPrototype" type="Node3D"]', scene)

    def test_inspection_table_scene_loads_current_day_oddity(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('path="res://assets/textures/workbench_walnut.png"', scene)
        self.assertIn("albedo_texture = ExtResource", scene)
        self.assertIn('[node name="ItemPivot" type="Node3D" parent="."]', scene)
        self.assertIn('[node name="InspectionCamera" type="Camera3D" parent="."]', scene)
        self.assertIn("var current_item: Node3D", script)
        self.assertIn("_load_current_day_item", script)
        self.assertIn("GameState.get_current_item_scene_path", script)
        self.assertIn("const TEACUP_INITIAL_ROTATION_DEGREES := Vector3(0.0, -32.0, 0.0)", script)
        self.assertIn("current_item.rotation_degrees = TEACUP_INITIAL_ROTATION_DEGREES", script)
        self.assertIn('[node name="ItemNameLabel" type="Label" parent="HUD"]', scene)
        self.assertIn('[node name="ItemDescriptionLabel" type="Label" parent="HUD"]', scene)
        self.assertIn("item_name_label", script)
        self.assertIn("item_description_label", script)
        self.assertIn("_update_item_labels", script)
        self.assertIn("_get_current_description", script)

    def test_inspection_table_scene_uses_readable_lighting(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("ambient_light_energy = 0.2", scene)
        self.assertIn("light_energy = 185.0", scene)
        self.assertIn("spot_angle = 32.0", scene)
        self.assertIn("light_energy = 34.0", scene)
        self.assertIn("const DEFAULT_KEY_LIGHT_ENERGY := 185.0", script)
        self.assertIn("const UV_KEY_LIGHT_ENERGY := 62.0", script)

    def test_inspection_table_releases_mouse_for_hud_buttons(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)", script)
        self.assertLess(
            script.index("Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)"),
            script.index("_load_current_day_item()"),
        )

    def test_inspection_table_script_supports_rotation_and_zoom(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("InputEventMouseMotion", script)
        self.assertIn("MOUSE_BUTTON_WHEEL_UP", script)
        self.assertIn("MOUSE_BUTTON_WHEEL_DOWN", script)
        self.assertIn("_apply_zoom", script)
        self.assertIn("item_pivot.rotate_y", script)
        self.assertIn("item_pivot.rotate_x", script)

    def test_inspection_table_scene_has_magnifier_hud_button(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="HUD" type="CanvasLayer" parent="."]', scene)
        self.assertIn('[node name="MagnifierButton" type="Button" parent="HUD/ToolPanel"]', scene)
        self.assertIn('path="res://assets/ui/tool_magnifier.png"', scene)
        self.assertIn('text = "Magnifier"', scene)

    def test_inspection_table_script_supports_magnifier_tool(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('const TOOL_MAGNIFIER := "magnifier"', script)
        self.assertIn("active_tool", script)
        self.assertIn("_set_active_tool", script)
        self.assertIn("_on_magnifier_pressed", script)
        self.assertIn("KEY_1", script)
        self.assertIn("MAGNIFIER_CAMERA_Z", script)
        self.assertIn("MAGNIFIER_FOV", script)

    def test_inspection_table_scene_has_uv_lamp_tool_nodes(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="UVLampButton" type="Button" parent="HUD/ToolPanel"]', scene)
        self.assertIn('path="res://assets/ui/tool_uv_lamp.png"', scene)
        self.assertIn('text = "UV Lamp"', scene)
        self.assertIn('[node name="UVLamp" type="SpotLight3D" parent="."]', scene)
        self.assertIn('[node name="UVClueMarker" type="MeshInstance3D" parent="ItemPivot"]', scene)
        self.assertIn("visible = false", scene)

    def test_inspection_table_script_supports_uv_lamp_tool(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('const TOOL_UV_LAMP := "uv_lamp"', script)
        self.assertIn("uv_lamp_button", script)
        self.assertIn("uv_lamp", script)
        self.assertIn("uv_clue_marker", script)
        self.assertIn("_on_uv_lamp_pressed", script)
        self.assertIn("KEY_2", script)
        self.assertIn("UV_LAMP_ENERGY", script)
        self.assertIn("uv_clue_marker.visible = false", script)
        self.assertNotIn("uv_clue_marker.visible = active_tool == TOOL_UV_LAMP", script)

    def test_inspection_table_scene_has_thermometer_tool_nodes(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="ThermometerButton" type="Button" parent="HUD/ToolPanel"]', scene)
        self.assertIn('path="res://assets/ui/tool_thermometer.png"', scene)
        self.assertIn('text = "Thermometer"', scene)
        self.assertIn('[node name="ThermometerReadout" type="Label" parent="HUD"]', scene)
        self.assertIn('[node name="ToolClueReadout" type="Label" parent="HUD"]', scene)
        self.assertIn("visible = false", scene)

    def test_inspection_table_script_supports_thermometer_tool(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('const TOOL_THERMOMETER := "thermometer"', script)
        self.assertIn("thermometer_button", script)
        self.assertIn("thermometer_readout", script)
        self.assertIn("tool_clue_readout", script)
        self.assertIn("_on_thermometer_pressed", script)
        self.assertIn("KEY_3", script)
        self.assertIn("FALLBACK_TEMPERATURE_C", script)
        self.assertIn("thermometer_readout.visible = active_tool == TOOL_THERMOMETER", script)
        self.assertIn("_get_current_temperature_c", script)
        self.assertIn("_get_current_tool_clue", script)

    def test_inspection_table_has_appraisal_notes_for_discovered_clues(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="AppraisalNotesBackground" type="TextureRect" parent="HUD"]', scene)
        self.assertIn('[node name="AppraisalNotesLabel" type="Label" parent="HUD/AppraisalNotesBackground"]', scene)
        self.assertIn("appraisal_notes_label", script)
        self.assertIn("discovered_tools", script)
        self.assertIn("_remember_tool_clue", script)
        self.assertIn("_update_appraisal_notes", script)
        self.assertIn("_short_note_for_tool", script)
        self.assertIn('discovered_tools[TOOL_MAGNIFIER] = true', script)
        self.assertIn('Localization.text("ui.appraisal_notes")', script)
        self.assertIn('Localization.format_text("ui.note_mag"', script)
        self.assertIn('Localization.format_text("ui.note_uv"', script)
        self.assertIn('Localization.format_text("ui.note_temp"', script)

    def test_inspection_table_has_non_blocking_onboarding_panel(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="OnboardingPanel" type="PanelContainer" parent="HUD"]', scene)
        self.assertIn('[node name="OnboardingHintLabel" type="Label" parent="HUD/OnboardingPanel"]', scene)
        self.assertIn("onboarding_panel", script)
        self.assertIn("onboarding_hint_label", script)
        self.assertIn("GameState.get_onboarding_hint_key()", script)
        self.assertIn("GameState.record_onboarding_tool_used(tool_name)", script)
        self.assertIn("_update_onboarding_hint()", script)

    def test_appraisal_notes_use_right_side_safe_area(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn("offset_left = -344.0", scene)
        self.assertIn("offset_top = 204.0", scene)
        self.assertIn("offset_right = -24.0", scene)
        self.assertIn("offset_bottom = 356.0", scene)
        self.assertIn("theme_override_font_sizes/font_size = 14", scene)
        self.assertIn("theme_override_colors/font_color = Color(0.06, 0.045, 0.03, 1)", scene)
        self.assertIn("theme_override_constants/line_spacing = 4", scene)
        self.assertIn("modulate = Color(0.92, 0.84, 0.66, 0.93)", scene)

    def test_ledger_textures_scale_instead_of_tiling(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="AppraisalNotesBackground" type="TextureRect" parent="HUD"]', scene)
        self.assertIn("offset_left = -344.0\noffset_top = 204.0\noffset_right = -24.0\noffset_bottom = 356.0\ntexture = ExtResource(\"8_panel_ledger\")\nexpand_mode = 1\nstretch_mode = 0", scene)
        self.assertIn('[node name="DayResultBackground" type="TextureRect" parent="HUD"]', scene)
        self.assertIn("offset_left = -270.0\noffset_top = -220.0\noffset_right = 270.0\noffset_bottom = 160.0\ntexture = ExtResource(\"8_panel_ledger\")\nexpand_mode = 1\nstretch_mode = 0", scene)

    def test_inspection_table_scene_has_decision_buttons_and_result_label(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="DecisionPanel" type="HBoxContainer" parent="HUD"]', scene)
        self.assertIn('[node name="SellButton" type="Button" parent="HUD/DecisionPanel"]', scene)
        self.assertIn('[node name="SealButton" type="Button" parent="HUD/DecisionPanel"]', scene)
        self.assertIn('[node name="DiscardButton" type="Button" parent="HUD/DecisionPanel"]', scene)
        self.assertIn('[node name="DecisionResult" type="Label" parent="HUD"]', scene)
        self.assertIn('text = "Sell"', scene)
        self.assertIn('text = "Seal"', scene)
        self.assertIn('text = "Discard"', scene)

    def test_inspection_table_scene_has_back_to_shop_button(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="BackToShopButton" type="Button" parent="HUD"]', scene)
        self.assertIn('text = "Back to Shop"', scene)

    def test_inspection_table_script_scores_item_decisions(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('const FALLBACK_CORRECT_HANDLING := "seal"', script)
        self.assertIn("sell_button", script)
        self.assertIn("seal_button", script)
        self.assertIn("discard_button", script)
        self.assertIn("decision_result", script)
        self.assertIn("_on_sell_pressed", script)
        self.assertIn("_on_seal_pressed", script)
        self.assertIn("_on_discard_pressed", script)
        self.assertIn("_resolve_decision", script)
        self.assertIn("_get_current_correct_handling", script)
        self.assertIn("decision == correct_handling", script)

    def test_inspection_table_scene_has_day_result_panel(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="DayResultPanel" type="VBoxContainer" parent="HUD"]', scene)
        self.assertIn('[sub_resource type="StyleBoxFlat" id="StyleBox_result_text_panel"]', scene)
        self.assertIn('path="res://assets/ui/panel_ledger.png"', scene)
        self.assertIn('path="res://assets/ui/button_brass.png"', scene)
        self.assertIn('[node name="DayResultBackground" type="TextureRect" parent="HUD"]', scene)
        self.assertIn('[node name="ResultTextPanel" type="PanelContainer" parent="HUD/DayResultPanel"]', scene)
        self.assertIn('[node name="ResultTextContent" type="VBoxContainer" parent="HUD/DayResultPanel/ResultTextPanel"]', scene)
        self.assertIn('[node name="OutcomeLabel" type="Label" parent="HUD/DayResultPanel/ResultTextPanel/ResultTextContent"]', scene)
        self.assertIn('[node name="ValueLabel" type="Label" parent="HUD/DayResultPanel/ResultTextPanel/ResultTextContent"]', scene)
        self.assertIn('[node name="ReputationLabel" type="Label" parent="HUD/DayResultPanel/ResultTextPanel/ResultTextContent"]', scene)
        self.assertIn('[node name="ConsequenceReportLabel" type="Label" parent="HUD/DayResultPanel/ResultTextPanel/ResultTextContent"]', scene)
        self.assertIn('[node name="RunSummaryLabel" type="Label" parent="HUD/DayResultPanel/ResultTextPanel/ResultTextContent"]', scene)
        self.assertIn('[node name="ResultButtonPanel" type="MarginContainer" parent="HUD/DayResultPanel"]', scene)
        self.assertIn('[node name="NextDayButton" type="Button" parent="HUD/DayResultPanel/ResultButtonPanel"]', scene)
        self.assertIn('text = "Next Day"', scene)
        self.assertIn("theme_override_styles/panel = SubResource(\"StyleBox_result_text_panel\")", scene)
        self.assertIn("theme_override_constants/margin_bottom = 8", scene)
        self.assertIn("custom_minimum_size = Vector2(420, 150)", scene)
        self.assertIn("custom_minimum_size = Vector2(400, 44)", scene)
        self.assertIn("custom_minimum_size = Vector2(400, 60)", scene)
        self.assertIn("custom_minimum_size = Vector2(420, 96)", scene)
        self.assertIn("custom_minimum_size = Vector2(400, 30)", scene)

    def test_inspection_table_script_updates_day_result_after_decision(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("day_result_panel", script)
        self.assertIn("day_result_background", script)
        self.assertIn("outcome_label", script)
        self.assertIn("value_label", script)
        self.assertIn("reputation_label", script)
        self.assertIn("consequence_report_label", script)
        self.assertIn("run_summary_label", script)
        self.assertIn("next_day_button", script)
        self.assertIn("back_to_shop_button", script)
        self.assertIn("FALLBACK_SEAL_COST", script)
        self.assertIn("FALLBACK_SELL_VALUE", script)
        self.assertIn("_get_current_seal_cost", script)
        self.assertIn("_get_current_sell_value", script)
        self.assertIn("_show_day_result", script)
        self.assertIn("GameState.record_decision_result", script)
        self.assertIn("GameState.get_current_consequence_report", script)
        self.assertIn("GameState.get_run_summary", script)
        self.assertIn("GameState.get_current_consequence_key", script)
        self.assertIn("_show_day_result(\"outcome.correct\"", script)
        self.assertIn("outcome_label.text = Localization.text(outcome_key)", script)
        self.assertIn("_set_inspection_controls_visible(false)", script)
        self.assertIn("consequence_report_label.visible = not GameState.is_run_complete()", script)
        self.assertIn("run_summary_label.visible = GameState.is_run_complete()", script)
        self.assertIn("_on_next_day_pressed", script)
        self.assertIn("_on_back_to_shop_pressed", script)
        self.assertIn("_update_next_day_button_label", script)
        self.assertIn('next_day_button.text = Localization.text("ui.return_to_menu")', script)
        self.assertIn('next_day_button.text = Localization.text("ui.next_day")', script)
        self.assertIn("shop_scene_path", script)

    def test_inspection_table_scene_has_abnormal_event_and_bad_ending_panels(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="AbnormalEventPanel" type="VBoxContainer" parent="HUD"]', scene)
        self.assertIn('[node name="EventLabel" type="Label" parent="HUD/AbnormalEventPanel"]', scene)
        self.assertIn('[node name="BadEndingBackground" type="ColorRect" parent="HUD"]', scene)
        self.assertIn('[node name="BadEndingCard" type="PanelContainer" parent="HUD"]', scene)
        self.assertIn('[node name="BadEndingPanel" type="VBoxContainer" parent="HUD/BadEndingCard"]', scene)
        self.assertIn('[node name="EndingTitle" type="Label" parent="HUD/BadEndingCard/BadEndingPanel"]', scene)
        self.assertIn('[node name="EndingBody" type="Label" parent="HUD/BadEndingCard/BadEndingPanel"]', scene)
        self.assertIn('[node name="ReturnToMenuButton" type="Button" parent="HUD/BadEndingCard/BadEndingPanel"]', scene)
        self.assertIn('theme_override_styles/panel = SubResource("StyleBox_bad_ending_card")', scene)
        self.assertIn('text = "Return to Menu"', scene)

    def test_inspection_table_scene_has_audio_feedback_players(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('path="res://assets/audio/tool_activate.wav"', scene)
        self.assertIn('path="res://assets/audio/decision_correct.wav"', scene)
        self.assertIn('path="res://assets/audio/decision_wrong.wav"', scene)
        self.assertIn('path="res://assets/audio/abnormal_event.wav"', scene)
        self.assertIn('path="res://assets/audio/bad_ending.wav"', scene)
        self.assertIn('[node name="ToolAudioPlayer" type="AudioStreamPlayer" parent="."]', scene)
        self.assertIn('[node name="DecisionCorrectAudioPlayer" type="AudioStreamPlayer" parent="."]', scene)
        self.assertIn('[node name="DecisionWrongAudioPlayer" type="AudioStreamPlayer" parent="."]', scene)
        self.assertIn('[node name="AbnormalEventAudioPlayer" type="AudioStreamPlayer" parent="."]', scene)
        self.assertIn('[node name="BadEndingAudioPlayer" type="AudioStreamPlayer" parent="."]', scene)
        self.assertIn('stream = ExtResource("9_tool_audio")', scene)
        self.assertIn('stream = ExtResource("10_decision_correct_audio")', scene)
        self.assertIn('stream = ExtResource("11_decision_wrong_audio")', scene)
        self.assertIn('stream = ExtResource("12_abnormal_event_audio")', scene)
        self.assertIn('stream = ExtResource("13_bad_ending_audio")', scene)

    def test_inspection_table_script_triggers_abnormal_event_and_bad_ending(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("abnormal_event_panel", script)
        self.assertIn("event_label", script)
        self.assertIn("tool_panel", script)
        self.assertIn("decision_panel", script)
        self.assertIn("appraisal_notes_background", script)
        self.assertIn("bad_ending_background", script)
        self.assertIn("bad_ending_card", script)
        self.assertIn("bad_ending_panel", script)
        self.assertIn("ending_body", script)
        self.assertIn("return_to_menu_button", script)
        self.assertIn("_show_abnormal_event", script)
        self.assertIn("_show_bad_ending", script)
        self.assertIn("_on_return_to_menu_pressed", script)
        self.assertIn("main_menu_scene_path", script)

    def test_inspection_table_script_plays_audio_feedback_for_player_actions(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("tool_audio_player", script)
        self.assertIn("decision_correct_audio_player", script)
        self.assertIn("decision_wrong_audio_player", script)
        self.assertIn("abnormal_event_audio_player", script)
        self.assertIn("bad_ending_audio_player", script)
        self.assertIn("func _play_audio_cue(player: AudioStreamPlayer) -> void:", script)
        self.assertIn("_play_audio_cue(tool_audio_player)", script)
        self.assertIn("_play_audio_cue(decision_correct_audio_player)", script)
        self.assertIn("_play_audio_cue(decision_wrong_audio_player)", script)
        self.assertIn("_play_audio_cue(abnormal_event_audio_player)", script)
        self.assertIn("_play_audio_cue(bad_ending_audio_player)", script)
        self.assertIn("player.stop()", script)
        self.assertIn("player.play()", script)

    def test_bad_ending_uses_exclusive_overlay(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("func _set_gameplay_hud_visible(is_visible: bool) -> void:", script)
        self.assertIn("func _set_inspection_controls_visible(is_visible: bool) -> void:", script)
        self.assertIn("_show_bad_ending(wrong_event_text)", script)
        self.assertIn("_set_active_tool(TOOL_NONE)", script)
        self.assertIn("_set_gameplay_hud_visible(false)", script)
        self.assertIn("decision_result.visible = false", script)
        self.assertIn("day_result_background.visible = false", script)
        self.assertIn("day_result_panel.visible = false", script)
        self.assertIn("abnormal_event_panel.visible = false", script)
        self.assertIn("bad_ending_background.visible = true", script)
        self.assertIn("bad_ending_card.visible = true", script)
        self.assertIn('Localization.format_text("ui.final_cash"', script)
        self.assertIn('Localization.format_text("ui.final_reputation"', script)
        self.assertIn("tool_panel.visible = is_visible", script)
        self.assertIn("decision_panel.visible = is_visible", script)
        self.assertIn("appraisal_notes_background.visible = is_visible", script)
        self.assertIn("sell_button.disabled = not is_visible", script)
        self.assertIn("if bad_ending_card.visible:\n\t\treturn", script)


if __name__ == "__main__":
    unittest.main()
