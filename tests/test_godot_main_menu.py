from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotMainMenuTests(unittest.TestCase):
    def test_project_main_scene_is_main_menu(self):
        project = (ROOT / "godot" / "project.godot").read_text(encoding="utf-8")

        self.assertIn('run/main_scene="res://scenes/main_menu.tscn"', project)

    def test_main_menu_scene_has_start_and_quit_actions(self):
        scene = (ROOT / "godot" / "scenes" / "main_menu.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('path="res://scripts/main_menu.gd"', scene)
        self.assertIn('path="res://assets/ui/main_menu_background.png"', scene)
        self.assertIn('path="res://assets/ui/button_brass.png"', scene)
        self.assertIn('[node name="Background" type="TextureRect" parent="."]', scene)
        self.assertIn('[node name="StartButton" type="Button" parent="MenuPanel"]', scene)
        self.assertIn('[node name="ResetProgressButton" type="Button" parent="MenuPanel"]', scene)
        self.assertIn('[node name="SettingsButton" type="Button" parent="MenuPanel"]', scene)
        self.assertIn('[node name="QuitButton" type="Button" parent="MenuPanel"]', scene)
        self.assertIn('text = "Start Day"', scene)
        self.assertIn('text = "Reset Progress"', scene)
        self.assertIn('text = "Settings"', scene)
        self.assertIn('text = "Quit"', scene)

    def test_main_menu_buttons_have_hover_and_pressed_feedback(self):
        scene = (ROOT / "godot" / "scenes" / "main_menu.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[sub_resource type="StyleBoxTexture" id="StyleBox_button_hover"]', scene)
        self.assertIn('[sub_resource type="StyleBoxTexture" id="StyleBox_button_pressed"]', scene)
        self.assertIn("modulate_color = Color(0.95, 0.86, 0.56, 1)", scene)
        self.assertIn("modulate_color = Color(0.72, 0.56, 0.32, 1)", scene)
        self.assertIn('theme_override_styles/hover = SubResource("StyleBox_button_hover")', scene)
        self.assertIn('theme_override_styles/pressed = SubResource("StyleBox_button_pressed")', scene)

    def test_main_menu_scene_has_settings_panel_controls(self):
        scene = (ROOT / "godot" / "scenes" / "main_menu.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="SettingsPanel" type="VBoxContainer" parent="."]', scene)
        self.assertIn('[node name="SettingsTitle" type="Label" parent="SettingsPanel"]', scene)
        self.assertIn('[node name="LanguageLabel" type="Label" parent="SettingsPanel"]', scene)
        self.assertIn('[node name="LanguageOption" type="OptionButton" parent="SettingsPanel"]', scene)
        self.assertIn('[node name="FullscreenCheckBox" type="CheckBox" parent="SettingsPanel"]', scene)
        self.assertIn('[node name="VolumeLabel" type="Label" parent="SettingsPanel"]', scene)
        self.assertIn('[node name="VolumeSlider" type="HSlider" parent="SettingsPanel"]', scene)
        self.assertIn('[node name="BackFromSettingsButton" type="Button" parent="SettingsPanel"]', scene)
        self.assertIn("visible = false", scene)

    def test_main_menu_script_starts_shop_or_quits(self):
        script = (ROOT / "godot" / "scripts" / "main_menu.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('const shop_scene_path := "res://scenes/shop_prototype.tscn"', script)
        self.assertIn("start_button", script)
        self.assertIn("reset_progress_button", script)
        self.assertIn("settings_button", script)
        self.assertIn("quit_button", script)
        self.assertIn("settings_panel", script)
        self.assertIn("language_option", script)
        self.assertIn("fullscreen_checkbox", script)
        self.assertIn("volume_slider", script)
        self.assertIn("_on_start_pressed", script)
        self.assertIn("_on_reset_progress_pressed", script)
        self.assertIn("_on_settings_pressed", script)
        self.assertIn("_on_language_selected", script)
        self.assertIn("_on_fullscreen_toggled", script)
        self.assertIn("_on_volume_changed", script)
        self.assertIn("_on_back_from_settings_pressed", script)
        self.assertIn("_on_quit_pressed", script)
        self.assertIn("reset_progress_button.pressed.connect(_on_reset_progress_pressed)", script)
        self.assertIn("settings_button.pressed.connect(_on_settings_pressed)", script)
        self.assertIn("language_option.item_selected.connect(_on_language_selected)", script)
        self.assertIn("fullscreen_checkbox.toggled.connect(_on_fullscreen_toggled)", script)
        self.assertIn("volume_slider.value_changed.connect(_on_volume_changed)", script)
        self.assertIn("GameState.reset_progress()", script)
        self.assertIn('Localization.text("ui.reset_progress")', script)
        self.assertIn('Localization.text("ui.settings")', script)
        self.assertIn("Localization.set_locale", script)
        self.assertIn("DisplayServer.window_set_mode", script)
        self.assertIn("AudioServer.set_bus_volume_db", script)
        self.assertIn("change_scene_to_file", script)
        self.assertIn("get_tree().quit", script)


if __name__ == "__main__":
    unittest.main()
