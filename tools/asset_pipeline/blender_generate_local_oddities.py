import argparse
import json
from pathlib import Path

import bpy


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Blender-side local oddity model generator.")
    parser.add_argument("--root", required=True, help="Project root directory.")
    return parser.parse_args(_script_args())


def _script_args() -> list[str]:
    import sys

    if "--" not in sys.argv:
        return []
    return sys.argv[sys.argv.index("--") + 1 :]


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def make_mat(name: str, color: tuple[float, float, float, float], roughness: float = 0.72, metallic: float = 0.0) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    if principled is not None:
        principled.inputs["Base Color"].default_value = color
        principled.inputs["Roughness"].default_value = roughness
        principled.inputs["Metallic"].default_value = metallic
    return mat


def add_box_part(name: str, *, location: tuple[float, float, float], scale: tuple[float, float, float], mat: bpy.types.Material) -> None:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new(f"{name}_soft_edges", "BEVEL")
    bevel.width = 0.012
    bevel.segments = 2
    obj.modifiers.new(f"{name}_weighted_normals", "WEIGHTED_NORMAL")


def add_cylinder_part(
    name: str,
    *,
    location: tuple[float, float, float],
    radius: float,
    depth: float,
    mat: bpy.types.Material,
    vertices: int = 32,
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> None:
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)


def add_music_box(item_id: str, mat: bpy.types.Material) -> None:
    dark = make_mat(f"{item_id}_music_box_dark_mat", (0.11, 0.075, 0.055, 1.0), roughness=0.86)
    brass = make_mat(f"{item_id}_music_box_brass_mat", (0.72, 0.43, 0.18, 1.0), roughness=0.48, metallic=0.45)
    add_box_part(f"{item_id}_music_box_base", location=(0, 0, -0.018), scale=(0.38, 0.24, 0.105), mat=mat)
    add_box_part(f"{item_id}_music_box_lid", location=(0.012, 0, 0.082), scale=(0.36, 0.23, 0.034), mat=mat)
    add_box_part(f"{item_id}_music_box_shadow_gap", location=(0, -0.12, 0.045), scale=(0.35, 0.016, 0.03), mat=dark)
    add_box_part(f"{item_id}_music_box_cylinder_bridge", location=(-0.05, -0.108, 0.045), scale=(0.18, 0.022, 0.055), mat=dark)
    add_cylinder_part(
        f"{item_id}_music_box_cylinder",
        location=(-0.05, -0.125, 0.045),
        radius=0.03,
        depth=0.18,
        mat=brass,
        vertices=32,
        rotation=(1.5708, 0, 0),
    )
    add_cylinder_part(
        f"{item_id}_music_box_crank",
        location=(0.205, -0.032, 0.018),
        radius=0.011,
        depth=0.09,
        mat=brass,
        vertices=20,
        rotation=(0, 1.5708, 0),
    )


def add_shape(item_id: str, shape: str, mat: bpy.types.Material) -> None:
    if shape == "coin":
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.18, depth=0.035)
    elif shape == "box":
        add_music_box(item_id, mat)
        return
    elif shape == "key":
        bpy.ops.mesh.primitive_torus_add(major_radius=0.09, minor_radius=0.014)
        bpy.ops.mesh.primitive_cube_add(size=0.08, location=(0.16, 0, 0))
        bpy.context.object.scale = (2.6, 0.28, 0.18)
    elif shape == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.16)
    elif shape == "candle":
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.09, depth=0.32)
    elif shape == "doll":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.1, location=(0, 0, 0.13))
        bpy.ops.mesh.primitive_cube_add(size=0.18, location=(0, 0, -0.06))
        bpy.context.object.scale = (0.75, 0.45, 1.1)
    elif shape == "bell":
        bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.18, radius2=0.07, depth=0.24)
    elif shape == "mirror":
        bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.018)
        bpy.ops.mesh.primitive_cube_add(size=0.08, location=(0, -0.18, 0))
        bpy.context.object.scale = (0.28, 1.8, 0.18)
    elif shape == "spool":
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.12, depth=0.18)
    else:
        bpy.ops.mesh.primitive_cube_add(size=0.2)

    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            if len(obj.data.materials) == 0:
                obj.data.materials.append(mat)


def export_item(root: Path, item: dict) -> None:
    clear_scene()
    color = tuple(item.get("local_material_color", (0.48, 0.42, 0.36, 1.0)))
    mat = make_mat(f"{item['id']}_mat", color)
    add_shape(item["id"], item["local_shape"], mat)
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            if not obj.name.startswith(item["id"]):
                obj.name = f"{item['id']}_{obj.name}"

    for rel_path in (item["model"]["raw_path"], item["model"]["processed_path"]):
        output = root / rel_path
        output.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.export_scene.gltf(filepath=str(output), export_format="GLB")


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    item_paths = sorted((root / "data" / "items").glob("oddity_*.json"))
    generated = []
    for item_path in item_paths:
        item = json.loads(item_path.read_text(encoding="utf-8"))
        if "local_shape" not in item:
            continue
        export_item(root, item)
        generated.append(item["id"])

    print(json.dumps({"generated": generated}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
