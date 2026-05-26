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
        self.assertIn('[node name="QuitButton" type="Button" parent="MenuPanel"]', scene)
        self.assertIn('text = "Start Day"', scene)
        self.assertIn('text = "Reset Progress"', scene)
        self.assertIn('text = "Quit"', scene)

    def test_main_menu_script_starts_shop_or_quits(self):
        script = (ROOT / "godot" / "scripts" / "main_menu.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('const shop_scene_path := "res://scenes/shop_prototype.tscn"', script)
        self.assertIn("start_button", script)
        self.assertIn("reset_progress_button", script)
        self.assertIn("quit_button", script)
        self.assertIn("_on_start_pressed", script)
        self.assertIn("_on_reset_progress_pressed", script)
        self.assertIn("_on_quit_pressed", script)
        self.assertIn("reset_progress_button.pressed.connect(_on_reset_progress_pressed)", script)
        self.assertIn("GameState.reset_progress()", script)
        self.assertIn('Localization.text("ui.reset_progress")', script)
        self.assertIn("change_scene_to_file", script)
        self.assertIn("get_tree().quit", script)


if __name__ == "__main__":
    unittest.main()
