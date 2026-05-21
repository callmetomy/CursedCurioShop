from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotGameStateTests(unittest.TestCase):
    def test_game_state_autoload_is_registered(self):
        project = (ROOT / "godot" / "project.godot").read_text(encoding="utf-8")

        self.assertIn("[autoload]", project)
        self.assertIn('GameState="*res://scripts/game_state.gd"', project)

    def test_game_state_tracks_three_day_loop_cash_and_reputation(self):
        script = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("extends Node", script)
        self.assertIn("var current_day := 1", script)
        self.assertIn("var max_days := 3", script)
        self.assertIn("var cash := 100", script)
        self.assertIn("var reputation := 50", script)
        self.assertIn("func start_new_run", script)
        self.assertIn("func apply_result", script)
        self.assertIn("func advance_day", script)
        self.assertIn("func is_run_complete", script)

    def test_game_state_maps_three_days_to_demo_oddities(self):
        script = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('const DAILY_ITEM_IDS := ["oddity_0001", "oddity_0002", "oddity_0003"]', script)
        self.assertIn("func get_current_item_id", script)
        self.assertIn("func get_current_item_scene_path", script)
        self.assertIn('res://scenes/items/oddity_0002.tscn', script)
        self.assertIn('res://scenes/items/oddity_0003.tscn', script)

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

    def test_three_day_demo_smoke_script_exercises_core_flow(self):
        script_path = ROOT / "godot" / "tools" / "smoke_three_day_flow.gd"
        self.assertTrue(script_path.exists())

        script = script_path.read_text(encoding="utf-8")
        self.assertIn('load("res://scenes/inspection_table.tscn") as PackedScene', script)
        self.assertIn('const EXPECTED_ITEMS := ["oddity_0001", "oddity_0002", "oddity_0003"]', script)
        self.assertIn("_resolve_decision", script)
        self.assertIn("_on_next_day_pressed", script)
        self.assertIn('_game_state().get("current_day")', script)
        self.assertIn("HUD/AbnormalEventPanel", script)
        self.assertIn("HUD/BadEndingPanel", script)
        self.assertIn("quit(0)", script)


if __name__ == "__main__":
    unittest.main()
