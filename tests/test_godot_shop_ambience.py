from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotShopAmbienceTests(unittest.TestCase):
    def test_shop_scene_has_looping_ambience_player(self):
        scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )

        self.assertIn('path="res://assets/audio/shop_ambience.wav"', scene)
        self.assertIn('[node name="ShopAmbiencePlayer" type="AudioStreamPlayer" parent="."]', scene)
        self.assertIn('stream = ExtResource("4_shop_ambience")', scene)
        self.assertIn("volume_db = -18.0", scene)
        self.assertIn("autoplay = true", scene)

    def test_shop_controller_keeps_ambience_looping(self):
        script = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("shop_ambience_player", script)
        self.assertIn("func _start_shop_ambience() -> void:", script)
        self.assertIn("shop_ambience_player.stream.loop_mode = AudioStreamWAV.LOOP_FORWARD", script)
        self.assertIn("if not shop_ambience_player.playing:", script)
        self.assertIn("shop_ambience_player.play()", script)

    def test_shop_controller_stops_ambience_when_scene_exits(self):
        script = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("func _exit_tree() -> void:", script)
        self.assertIn("if shop_ambience_player.playing:", script)
        self.assertIn("shop_ambience_player.stop()", script)

    def test_shop_ambience_asset_exists(self):
        audio = ROOT / "godot" / "assets" / "audio" / "shop_ambience.wav"
        audio_import = ROOT / "godot" / "assets" / "audio" / "shop_ambience.wav.import"

        self.assertTrue(audio.exists())
        self.assertGreater(audio.stat().st_size, 8000)
        self.assertTrue(audio_import.exists())


if __name__ == "__main__":
    unittest.main()
