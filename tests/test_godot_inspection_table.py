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
        self.assertIn('[node name="ItemNameLabel" type="Label" parent="HUD"]', scene)
        self.assertIn('[node name="ItemDescriptionLabel" type="Label" parent="HUD"]', scene)
        self.assertIn("item_name_label", script)
        self.assertIn("item_description_label", script)
        self.assertIn("_update_item_labels", script)
        self.assertIn("_get_current_description", script)

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
        self.assertIn("uv_clue_marker.visible = active_tool == TOOL_UV_LAMP", script)

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
        self.assertIn('path="res://assets/ui/panel_ledger.png"', scene)
        self.assertIn('path="res://assets/ui/button_brass.png"', scene)
        self.assertIn('[node name="DayResultBackground" type="TextureRect" parent="HUD"]', scene)
        self.assertIn('[node name="OutcomeLabel" type="Label" parent="HUD/DayResultPanel"]', scene)
        self.assertIn('[node name="ValueLabel" type="Label" parent="HUD/DayResultPanel"]', scene)
        self.assertIn('[node name="ReputationLabel" type="Label" parent="HUD/DayResultPanel"]', scene)
        self.assertIn('[node name="NextDayButton" type="Button" parent="HUD/DayResultPanel"]', scene)
        self.assertIn('text = "Next Day"', scene)

    def test_inspection_table_script_updates_day_result_after_decision(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("day_result_panel", script)
        self.assertIn("day_result_background", script)
        self.assertIn("outcome_label", script)
        self.assertIn("value_label", script)
        self.assertIn("reputation_label", script)
        self.assertIn("next_day_button", script)
        self.assertIn("back_to_shop_button", script)
        self.assertIn("FALLBACK_SEAL_COST", script)
        self.assertIn("FALLBACK_SELL_VALUE", script)
        self.assertIn("_get_current_seal_cost", script)
        self.assertIn("_get_current_sell_value", script)
        self.assertIn("_show_day_result", script)
        self.assertIn("_on_next_day_pressed", script)
        self.assertIn("_on_back_to_shop_pressed", script)
        self.assertIn("_update_next_day_button_label", script)
        self.assertIn('next_day_button.text = "Return to Menu"', script)
        self.assertIn('next_day_button.text = "Next Day"', script)
        self.assertIn("shop_scene_path", script)

    def test_inspection_table_scene_has_abnormal_event_and_bad_ending_panels(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="AbnormalEventPanel" type="VBoxContainer" parent="HUD"]', scene)
        self.assertIn('[node name="EventLabel" type="Label" parent="HUD/AbnormalEventPanel"]', scene)
        self.assertIn('[node name="BadEndingPanel" type="VBoxContainer" parent="HUD"]', scene)
        self.assertIn('[node name="EndingTitle" type="Label" parent="HUD/BadEndingPanel"]', scene)
        self.assertIn('[node name="ReturnToMenuButton" type="Button" parent="HUD/BadEndingPanel"]', scene)
        self.assertIn('text = "Return to Menu"', scene)

    def test_inspection_table_script_triggers_abnormal_event_and_bad_ending(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("abnormal_event_panel", script)
        self.assertIn("event_label", script)
        self.assertIn("bad_ending_panel", script)
        self.assertIn("return_to_menu_button", script)
        self.assertIn("_show_abnormal_event", script)
        self.assertIn("_show_bad_ending", script)
        self.assertIn("_on_return_to_menu_pressed", script)
        self.assertIn("main_menu_scene_path", script)


if __name__ == "__main__":
    unittest.main()
