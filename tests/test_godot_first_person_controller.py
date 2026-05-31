from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotFirstPersonControllerTests(unittest.TestCase):
    def test_first_person_controller_supports_movement_mouse_look_and_interaction(self):
        script = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("extends CharacterBody3D", script)
        self.assertIn("move_speed", script)
        self.assertIn("mouse_sensitivity", script)
        self.assertIn("InputEventMouseMotion", script)
        self.assertIn("Input.get_vector", script)
        self.assertIn("move_and_slide", script)
        self.assertIn("interact", script)
        self.assertIn("change_scene_to_file", script)

    def test_shop_prototype_scene_instances_player_and_inspection_prompt(self):
        scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('path="res://scripts/first_person_controller.gd"', scene)
        self.assertIn('[node name="Player" type="CharacterBody3D" parent="."]', scene)
        self.assertIn('[node name="Camera3D" type="Camera3D" parent="Player"]', scene)
        self.assertIn('[node name="InspectionTableProxy" type="StaticBody3D" parent="."]', scene)
        self.assertIn('[node name="Prompt" type="Label" parent="HUD"]', scene)

    def test_shop_prompt_changes_after_returning_from_an_appraisal(self):
        script = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("func _get_shop_prompt_text() -> String:", script)
        self.assertIn("GameState.get_result_detail_count() > 0", script)
        self.assertIn('Localization.text("ui.inspect_prompt_after_appraisal")', script)
        self.assertIn('Localization.text("ui.inspect_prompt")', script)
        self.assertIn("prompt_label.text = _get_shop_prompt_text()", script)

    def test_shop_transition_overlay_marks_inspection_scene_change(self):
        scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )
        script = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="SceneTransitionOverlay" type="ColorRect" parent="HUD"]', scene)
        self.assertIn("visible = false", scene)
        self.assertIn("anchors_preset = 15", scene)
        self.assertIn("mouse_filter = 2", scene)
        self.assertIn("color = Color(0, 0, 0, 0)", scene)
        self.assertIn("scene_transition_overlay", script)
        self.assertIn("func _show_scene_transition() -> void:", script)
        self.assertLess(
            script.index("_show_scene_transition()"),
            script.index("get_tree().change_scene_to_file(inspection_scene_path)"),
        )

    def test_shop_transition_overlay_uses_fade_ready_alpha(self):
        scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )
        script = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("color = Color(0, 0, 0, 0)", scene)
        self.assertIn("const SCENE_TRANSITION_ALPHA := 0.34", script)
        self.assertIn("scene_transition_overlay.color.a = SCENE_TRANSITION_ALPHA", script)

    def test_shop_prototype_scene_uses_mvp_material_assets(self):
        scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('path="res://assets/textures/workbench_walnut.png"', scene)
        self.assertIn('path="res://assets/textures/shop_wallpaper.png"', scene)
        self.assertIn('[node name="BackWall" type="MeshInstance3D" parent="."]', scene)
        self.assertIn('[node name="LeftWall" type="MeshInstance3D" parent="."]', scene)
        self.assertIn('[node name="RightWall" type="MeshInstance3D" parent="."]', scene)

    def test_shop_prototype_scene_uses_readable_lighting_and_camera(self):
        scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn("ambient_light_energy = 0.3", scene)
        self.assertIn("light_energy = 260.0", scene)
        self.assertIn("spot_angle = 34.0", scene)
        self.assertIn('[node name="FillLight" type="OmniLight3D" parent="."]', scene)
        self.assertIn("light_energy = 85.0", scene)
        self.assertIn("omni_range = 4.2", scene)
        self.assertIn("fov = 58.0", scene)

    def test_project_defines_first_person_input_actions(self):
        project = (ROOT / "godot" / "project.godot").read_text(encoding="utf-8")

        for action in ("move_forward", "move_back", "move_left", "move_right", "interact"):
            self.assertIn(f"{action}=", project)


if __name__ == "__main__":
    unittest.main()
