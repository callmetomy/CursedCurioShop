from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotItemSceneTests(unittest.TestCase):
    def test_inspectable_item_script_loads_external_processed_model(self):
        script = (ROOT / "godot" / "scripts" / "inspectable_item.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("var model_path", script)
        self.assertIn("GLTFDocument", script)
        self.assertIn("_fit_collision_to_model", script)
        self.assertIn("BoxShape3D", script)

    def test_oddity_item_scene_tracks_teacup_metadata_and_model(self):
        scene = (ROOT / "godot" / "scenes" / "items" / "oddity_0001.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('item_id = "oddity_0001"', scene)
        self.assertIn('display_name = "Whispering Teacup"', scene)
        self.assertIn('model_path = "res://assets/models_processed/oddity_0001.glb"', scene)
        self.assertIn('[node name="ModelRoot" type="Node3D" parent="."]', scene)
        self.assertIn('[node name="CollisionBody" type="StaticBody3D" parent="."]', scene)
        self.assertIn('[node name="CollisionShape3D" type="CollisionShape3D" parent="CollisionBody"]', scene)


if __name__ == "__main__":
    unittest.main()
