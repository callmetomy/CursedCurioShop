from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotItemSceneTests(unittest.TestCase):
    def test_inspectable_item_script_loads_external_processed_model(self):
        script = (ROOT / "godot" / "scripts" / "inspectable_item.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("var model_path", script)
        self.assertIn("var description", script)
        self.assertIn("var magnifier_clue", script)
        self.assertIn("var uv_clue", script)
        self.assertIn("var thermometer_clue", script)
        self.assertIn("var thermometer_c", script)
        self.assertIn("var sell_value", script)
        self.assertIn("var seal_cost", script)
        self.assertIn("load(path) as PackedScene", script)
        self.assertIn("_load_imported_scene", script)
        self.assertIn("var use_fallback_material", script)
        self.assertIn("var fallback_material_color", script)
        self.assertIn("var fallback_material_metallic", script)
        self.assertIn("var fallback_material_roughness", script)
        self.assertIn("var material_tint_color", script)
        self.assertIn("var material_tint_roughness", script)
        self.assertIn("var accent_marker_color", script)
        self.assertIn("var wear_decal_texture_path", script)
        self.assertIn("var wear_decal_size", script)
        self.assertIn("var wear_decal_normal_axis", script)
        self.assertIn("var initial_rotation_degrees", script)
        self.assertIn("const ITEM_DECAL_LAYER := 2", script)
        self.assertIn("_apply_fallback_material", script)
        self.assertIn("material.metallic = metallic", script)
        self.assertIn("_apply_material_tint", script)
        self.assertIn("_assign_model_visual_layers", script)
        self.assertIn("mesh_instance.layers = ITEM_DECAL_LAYER", script)
        self.assertIn("set_surface_override_material", script)
        self.assertIn("_add_accent_marker", script)
        self.assertIn("_add_wear_decal", script)
        self.assertIn("AppraisalAccentMarker", script)
        self.assertIn("AppraisalWearDecal", script)
        self.assertIn("Decal.new()", script)
        self.assertIn("decal.cull_mask = ITEM_DECAL_LAYER", script)
        self.assertIn("_apply_initial_rotation", script)
        self.assertIn("if initial_rotation_degrees == Vector3.ZERO", script)
        self.assertIn("_wear_decal_target_offset", script)
        self.assertNotIn("AppraisalWearMarker", script)
        self.assertIn("GLTFDocument", script)
        self.assertIn("_fit_collision_to_model", script)
        self.assertIn("BoxShape3D", script)

    def test_oddity_item_scene_tracks_teacup_metadata_and_model(self):
        scene = (ROOT / "godot" / "scenes" / "items" / "oddity_0001.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('item_id = "oddity_0001"', scene)
        self.assertIn('display_name = "Whispering Teacup"', scene)
        self.assertIn("description =", scene)
        self.assertIn('model_path = "res://assets/models_processed/oddity_0001.glb"', scene)
        self.assertIn('[node name="ModelRoot" type="Node3D" parent="."]', scene)
        self.assertIn('[node name="CollisionBody" type="StaticBody3D" parent="."]', scene)
        self.assertIn('[node name="CollisionShape3D" type="CollisionShape3D" parent="CollisionBody"]', scene)

    def test_demo_day_item_scenes_track_metadata_and_models(self):
        expected = {
            "oddity_0002": ("Mirror Coin", "seal"),
            "oddity_0003": ("Ashen Music Box", "discard"),
        }

        for item_id, (display_name, correct_handling) in expected.items():
            scene_path = ROOT / "godot" / "scenes" / "items" / f"{item_id}.tscn"
            model_path = ROOT / "godot" / "assets" / "models_processed" / f"{item_id}.glb"

            self.assertTrue(scene_path.exists(), f"Missing {scene_path}")
            self.assertTrue(model_path.exists(), f"Missing {model_path}")

            scene = scene_path.read_text(encoding="utf-8")
            self.assertIn(f'item_id = "{item_id}"', scene)
            self.assertIn(f'display_name = "{display_name}"', scene)
            self.assertIn("description =", scene)
            self.assertIn(f'model_path = "res://assets/models_processed/{item_id}.glb"', scene)
            self.assertIn(f'correct_handling = "{correct_handling}"', scene)
            self.assertIn("magnifier_clue =", scene)
            self.assertIn("uv_clue =", scene)
            self.assertIn("thermometer_clue =", scene)
            self.assertIn("thermometer_c =", scene)
            self.assertIn("sell_value =", scene)
            self.assertIn("seal_cost =", scene)
            self.assertIn("use_fallback_material = true", scene)
            self.assertIn("fallback_material_color = Color(", scene)
            self.assertIn("accent_marker_enabled =", scene)
            self.assertIn("accent_marker_color = Color(", scene)

    def test_teacup_scene_has_surface_wear_decal(self):
        scene = (ROOT / "godot" / "scenes" / "items" / "oddity_0001.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn("use_fallback_material = false", scene)
        self.assertIn("material_tint_enabled = true", scene)
        self.assertIn("material_tint_color = Color(0.62, 0.52, 0.38, 1.0)", scene)
        self.assertIn("material_tint_roughness = 0.94", scene)
        self.assertIn("accent_marker_enabled = false", scene)
        self.assertIn("wear_decal_enabled = true", scene)
        self.assertIn(
            'wear_decal_texture_path = "res://assets/textures/cursed_teacup_decal.png"',
            scene,
        )
        self.assertIn("wear_decal_size = Vector3(", scene)
        self.assertNotIn("wear_marker_enabled = true", scene)

    def test_remaining_prototype_item_scenes_have_readability_markers(self):
        scene = (ROOT / "godot" / "scenes" / "items" / "oddity_0004.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn("fallback_material_color = Color(", scene)
        self.assertIn("accent_marker_enabled = true", scene)
        self.assertIn("accent_marker_color = Color(", scene)

    def test_mirror_coin_uses_surface_decal_instead_of_debug_marker(self):
        scene = (ROOT / "godot" / "scenes" / "items" / "oddity_0002.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn("fallback_material_color = Color(0.36, 0.35, 0.4, 1.0)", scene)
        self.assertIn("fallback_material_metallic = 0.72", scene)
        self.assertIn("fallback_material_roughness = 0.42", scene)
        self.assertIn("accent_marker_enabled = false", scene)
        self.assertIn("wear_decal_enabled = true", scene)
        self.assertIn(
            'wear_decal_texture_path = "res://assets/textures/mirror_coin_decal.png"',
            scene,
        )
        self.assertIn("wear_decal_size = Vector3(0.34, 0.06, 0.34)", scene)
        self.assertIn('wear_decal_normal_axis = "y"', scene)
        self.assertIn("initial_rotation_degrees = Vector3(-90.0, 0.0, 0.0)", scene)

    def test_ashen_music_box_uses_surface_decal_instead_of_debug_marker(self):
        scene = (ROOT / "godot" / "scenes" / "items" / "oddity_0003.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'description = "A scorched music box whose intact case keeps the tune alive even when the lid is shut."',
            scene,
        )
        self.assertIn("fallback_material_color = Color(0.26, 0.18, 0.14, 1.0)", scene)
        self.assertIn("fallback_material_metallic = 0.08", scene)
        self.assertIn("fallback_material_roughness = 0.86", scene)
        self.assertIn("accent_marker_enabled = false", scene)
        self.assertIn("wear_decal_enabled = true", scene)
        self.assertIn(
            'wear_decal_texture_path = "res://assets/textures/music_box_ash_decal.png"',
            scene,
        )
        self.assertIn("wear_decal_size = Vector3(0.3, 0.08, 0.22)", scene)


if __name__ == "__main__":
    unittest.main()
