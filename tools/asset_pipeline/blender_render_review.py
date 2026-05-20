import argparse
import json
from math import cos, radians, sin
from pathlib import Path

import bpy
from mathutils import Vector

REVIEW_ANGLES = {
    "front": 0.0,
    "right": 90.0,
    "back": 180.0,
    "left": 270.0,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Blender-side review renderer.")
    parser.add_argument("--input", required=True, help="Input processed GLB path.")
    parser.add_argument("--output-dir", required=True, help="Directory for review PNGs.")
    parser.add_argument("--item-id", required=True, help="Oddity item id.")
    parser.add_argument("--resolution", type=int, default=768, help="Square PNG resolution.")
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


def center_objects(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    minimum, maximum = calculate_bounds(objects)
    center = (minimum + maximum) * 0.5
    for obj in objects:
        obj.location -= center
    return calculate_bounds(objects)


def look_at(obj: bpy.types.Object, target: Vector) -> None:
    direction = target - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_render_scene(resolution: int) -> None:
    scene = bpy.context.scene
    scene.render.resolution_x = resolution
    scene.render.resolution_y = resolution
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.world.color = (0.035, 0.033, 0.035)

    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
        scene.eevee.taa_render_samples = 32
    except Exception:
        scene.render.engine = "BLENDER_WORKBENCH"


def add_lights(size: Vector) -> None:
    longest_axis = max(size.x, size.y, size.z)
    bpy.ops.object.light_add(type="AREA", location=(-1.4, -2.0, 2.0))
    key = bpy.context.object
    key.name = "ReviewKeyLight"
    key.data.energy = 450
    key.data.size = max(1.4, longest_axis * 4.0)
    look_at(key, Vector((0, 0, 0)))

    bpy.ops.object.light_add(type="POINT", location=(1.7, 1.2, 1.2))
    fill = bpy.context.object
    fill.name = "ReviewFillLight"
    fill.data.energy = 80


def add_camera(size: Vector) -> bpy.types.Object:
    longest_axis = max(size.x, size.y, size.z)
    distance = max(0.9, longest_axis * 3.2)
    height = max(0.22, longest_axis * 0.75)
    bpy.ops.object.camera_add(location=(0, -distance, height))
    camera = bpy.context.object
    camera.name = "ReviewCamera"
    camera.data.lens = 70
    camera.data.dof.use_dof = False
    bpy.context.scene.camera = camera
    return camera


def render_angles(camera: bpy.types.Object, output_dir: Path, item_id: str) -> list[str]:
    output_paths: list[str] = []
    radius = (camera.location.x**2 + camera.location.y**2) ** 0.5
    height = camera.location.z

    for angle_name, degrees in REVIEW_ANGLES.items():
        angle = radians(degrees)
        camera.location = (radius * -sin(angle), radius * -cos(angle), height)
        look_at(camera, Vector((0, 0, 0)))
        output_path = output_dir / f"{item_id}_{angle_name}.png"
        bpy.context.scene.render.filepath = str(output_path)
        bpy.ops.render.render(write_still=True)
        output_paths.append(str(output_path))

    return output_paths


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    clear_scene()
    setup_render_scene(args.resolution)
    import_glb(input_path)
    objects = mesh_objects()
    minimum, maximum = center_objects(objects)
    size = maximum - minimum
    add_lights(size)
    camera = add_camera(size)
    output_paths = render_angles(camera, output_dir, args.item_id)

    print(
        json.dumps(
            {
                "rendered": True,
                "input": str(input_path),
                "output_paths": output_paths,
                "mesh_count": len(objects),
                "bounds_size": [round(value, 4) for value in size],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
