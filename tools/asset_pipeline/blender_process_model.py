import argparse
import json
from pathlib import Path

import bpy
from mathutils import Matrix, Vector


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Blender-side GLB processing.")
    parser.add_argument("--input", required=True, help="Input raw GLB path.")
    parser.add_argument("--output", required=True, help="Output processed GLB path.")
    parser.add_argument("--item-id", required=True, help="Oddity item id.")
    parser.add_argument(
        "--target-longest-axis",
        type=float,
        required=True,
        help="Target longest bounding-box axis after normalization.",
    )
    return parser.parse_args(_script_args())


def _script_args() -> list[str]:
    import sys

    if "--" not in sys.argv:
        return []
    return sys.argv[sys.argv.index("--") + 1 :]


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def import_glb(path: Path) -> None:
    bpy.ops.import_scene.gltf(filepath=str(path))


def mesh_objects() -> list[bpy.types.Object]:
    return [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]


def calculate_bounds(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    points: list[Vector] = []
    for obj in objects:
        points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
    if not points:
        raise RuntimeError("No mesh objects were imported.")

    minimum = Vector(
        (
            min(point.x for point in points),
            min(point.y for point in points),
            min(point.z for point in points),
        )
    )
    maximum = Vector(
        (
            max(point.x for point in points),
            max(point.y for point in points),
            max(point.z for point in points),
        )
    )
    return minimum, maximum


def normalize_objects(objects: list[bpy.types.Object], target_longest_axis: float) -> dict[str, float]:
    minimum, maximum = calculate_bounds(objects)
    size = maximum - minimum
    longest_axis = max(size.x, size.y, size.z)
    if longest_axis <= 0.0:
        raise RuntimeError("Imported mesh has zero-size bounds.")

    center = (minimum + maximum) * 0.5
    scale = target_longest_axis / longest_axis
    transform = Matrix.Diagonal((scale, scale, scale, 1.0)) @ Matrix.Translation(-center)

    for obj in objects:
        obj.matrix_world = transform @ obj.matrix_world

    return {
        "source_longest_axis": longest_axis,
        "target_longest_axis": target_longest_axis,
        "scale": scale,
    }


def rename_materials(item_id: str) -> int:
    materials = sorted(bpy.data.materials, key=lambda material: material.name)
    for index, material in enumerate(materials, start=1):
        material.name = f"{item_id}_mat_{index:02d}"
    return len(materials)


def export_glb(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(path), export_format="GLB")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    clear_scene()
    import_glb(input_path)
    objects = mesh_objects()
    normalization = normalize_objects(objects, args.target_longest_axis)
    material_count = rename_materials(args.item_id)
    export_glb(output_path)

    print(
        json.dumps(
            {
                "processed": True,
                "input": str(input_path),
                "output": str(output_path),
                "mesh_count": len(objects),
                "material_count": material_count,
                **normalization,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
