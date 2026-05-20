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


def make_mat(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    return mat


def add_shape(shape: str, mat: bpy.types.Material) -> None:
    if shape == "coin":
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.18, depth=0.035)
    elif shape == "box":
        bpy.ops.mesh.primitive_cube_add(size=0.28)
        bpy.context.object.scale.z = 0.55
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
            obj.data.materials.clear()
            obj.data.materials.append(mat)


def export_item(root: Path, item: dict) -> None:
    clear_scene()
    mat = make_mat(f"{item['id']}_mat", (0.72, 0.68, 0.62, 1.0))
    add_shape(item["local_shape"], mat)
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
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
