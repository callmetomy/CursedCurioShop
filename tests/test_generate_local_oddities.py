import sys
import json
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.asset_pipeline.generate_local_oddities import LOCAL_ODDITY_SPECS, build_local_item


def _read_glb_json(path: Path) -> dict:
    data = path.read_bytes()
    magic, _version, _length = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF":
        raise AssertionError(f"{path} is not a GLB file")
    chunk_length, chunk_type = struct.unpack_from("<I4s", data, 12)
    if chunk_type != b"JSON":
        raise AssertionError(f"{path} first GLB chunk is not JSON")
    return json.loads(data[20 : 20 + chunk_length].decode("utf-8"))


class GenerateLocalOdditiesTests(unittest.TestCase):
    def test_local_oddity_specs_fill_demo_roster(self):
        self.assertEqual(len(LOCAL_ODDITY_SPECS), 9)
        self.assertEqual(LOCAL_ODDITY_SPECS[0]["item_id"], "oddity_0002")
        self.assertEqual(LOCAL_ODDITY_SPECS[-1]["item_id"], "oddity_0010")
        self.assertEqual(len({spec["item_id"] for spec in LOCAL_ODDITY_SPECS}), 9)

    def test_build_local_item_contains_three_tool_clues(self):
        item = build_local_item(LOCAL_ODDITY_SPECS[0])

        self.assertEqual(item["id"], "oddity_0002")
        self.assertEqual(item["generation"]["status"], "local_prototype")
        self.assertEqual(item["generation"]["approved"], True)
        clue_tools = {clue["tool"] for clue in item["appraisal"]["clues"]}
        self.assertEqual(clue_tools, {"magnifier", "uv_lamp", "thermometer"})
        self.assertTrue(item["appraisal"]["description"])

    def test_build_local_item_preserves_visual_overrides(self):
        item = build_local_item(LOCAL_ODDITY_SPECS[0])

        self.assertEqual(
            item["appraisal"]["description"],
            "A tarnished silver coin whose face reflects a room one second out of sync.",
        )
        self.assertEqual(item["fallback_material_metallic"], 0.72)
        self.assertEqual(item["fallback_material_roughness"], 0.42)
        self.assertEqual(item["accent_marker_enabled"], False)
        self.assertEqual(item["wear_decal_enabled"], True)
        self.assertEqual(
            item["wear_decal_texture_path"],
            "res://assets/textures/mirror_coin_decal.png",
        )
        self.assertEqual(item["wear_decal_size"], [0.34, 0.06, 0.34])
        self.assertEqual(item["wear_decal_normal_axis"], "y")
        self.assertEqual(item["initial_rotation_degrees"], [-90.0, 0.0, 0.0])

    def test_runtime_local_oddity_glbs_export_non_default_material_colors(self):
        for spec in LOCAL_ODDITY_SPECS:
            gltf = _read_glb_json(
                ROOT / "godot" / "assets" / "models_processed" / f"{spec['item_id']}.glb"
            )
            materials = gltf.get("materials", [])
            self.assertTrue(materials, spec["item_id"])
            color = materials[0].get("pbrMetallicRoughness", {}).get("baseColorFactor")
            self.assertIsNotNone(color, spec["item_id"])
            self.assertGreater(
                max(abs(channel - 0.8) for channel in color[:3]),
                0.05,
                spec["item_id"],
            )

    def test_music_box_runtime_glb_has_readable_parts(self):
        gltf = _read_glb_json(ROOT / "godot" / "assets" / "models_processed" / "oddity_0003.glb")
        node_names = {node.get("name", "") for node in gltf.get("nodes", [])}

        self.assertIn("oddity_0003_music_box_base", node_names)
        self.assertIn("oddity_0003_music_box_lid", node_names)
        self.assertIn("oddity_0003_music_box_cylinder", node_names)
        self.assertIn("oddity_0003_music_box_crank", node_names)

    def test_music_box_runtime_glb_avoids_loose_fragment_parts(self):
        gltf = _read_glb_json(ROOT / "godot" / "assets" / "models_processed" / "oddity_0003.glb")
        node_names = {node.get("name", "") for node in gltf.get("nodes", [])}

        self.assertNotIn("oddity_0003_music_box_crank_handle", node_names)
        self.assertFalse(any("_foot_" in node_name for node_name in node_names))

        base = next(node for node in gltf.get("nodes", []) if node.get("name") == "oddity_0003_music_box_base")
        self.assertGreaterEqual(base.get("scale", [0.0])[0], 0.32)


if __name__ == "__main__":
    unittest.main()
