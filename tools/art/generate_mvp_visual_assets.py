from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ASSET_SPECS = {
    "ui/main_menu_background.png": (1920, 1080),
    "ui/panel_ledger.png": (512, 256),
    "ui/button_brass.png": (512, 128),
    "ui/tool_magnifier.png": (256, 256),
    "ui/tool_uv_lamp.png": (256, 256),
    "ui/tool_thermometer.png": (256, 256),
    "textures/workbench_walnut.png": (1024, 1024),
    "textures/shop_wallpaper.png": (1024, 1024),
    "textures/cursed_teacup_decal.png": (1024, 1024),
    "textures/mirror_coin_decal.png": (1024, 1024),
    "textures/uv_ring_mark.png": (1024, 1024),
}


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _save(path: Path, image: Image.Image) -> None:
    _ensure_parent(path)
    image.save(path)


def _noise(width: int, height: int, seed: int, low: int = 0, high: int = 255) -> Image.Image:
    rng = random.Random(seed)
    data = bytes(rng.randint(low, high) for _ in range(width * height))
    return Image.frombytes("L", (width, height), data)


def _overlay_noise(base: Image.Image, seed: int, strength: int) -> Image.Image:
    noise = _noise(base.width, base.height, seed, 0, strength).convert("RGBA")
    noise.putalpha(noise.getchannel("R").point(lambda value: int(value * 0.35)))
    return Image.alpha_composite(base.convert("RGBA"), noise)


def _draw_main_menu_background(path: Path) -> None:
    width, height = ASSET_SPECS["ui/main_menu_background.png"]
    image = Image.new("RGBA", (width, height), (28, 24, 19, 255))
    draw = ImageDraw.Draw(image, "RGBA")

    for y in range(height):
        warm = int(28 + 36 * (1 - y / height))
        draw.line((0, y, width, y), fill=(warm, max(18, warm - 8), max(14, warm - 16), 255))

    for x in range(0, width, 155):
        draw.rectangle((x, 0, x + 80, height), fill=(22, 18, 15, 80))

    shelf_y = [210, 430, 660, 875]
    for y in shelf_y:
        draw.rectangle((0, y, width, y + 18), fill=(52, 35, 22, 210))
        draw.rectangle((0, y + 18, width, y + 28), fill=(15, 11, 9, 170))
        for x in range(95, width - 80, 180):
            draw.rectangle((x, y - 88, x + 42, y), fill=(56, 43, 32, 170))
            draw.rectangle((x + 54, y - 62, x + 105, y), fill=(38, 45, 48, 150))
            draw.ellipse((x + 118, y - 72, x + 176, y - 16), outline=(102, 85, 54, 120), width=4)

    lamp_center = (width // 2, 105)
    for radius, alpha in [(520, 22), (380, 32), (230, 52)]:
        draw.ellipse(
            (
                lamp_center[0] - radius,
                lamp_center[1] - radius // 2,
                lamp_center[0] + radius,
                lamp_center[1] + radius // 2,
            ),
            fill=(198, 150, 88, alpha),
        )
    draw.rectangle((width // 2 - 120, 84, width // 2 + 120, 104), fill=(76, 56, 35, 230))
    draw.polygon(
        [(width // 2 - 95, 104), (width // 2 + 95, 104), (width // 2 + 58, 170), (width // 2 - 58, 170)],
        fill=(92, 68, 42, 230),
    )

    image = _overlay_noise(image, 101, 42).filter(ImageFilter.GaussianBlur(0.35))
    _save(path, image)


def _draw_panel_ledger(path: Path) -> None:
    width, height = ASSET_SPECS["ui/panel_ledger.png"]
    image = Image.new("RGBA", (width, height), (188, 164, 119, 238))
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle((8, 8, width - 9, height - 9), radius=8, fill=(194, 171, 126, 238), outline=(72, 48, 28, 255), width=4)
    draw.rounded_rectangle((20, 20, width - 21, height - 21), radius=5, outline=(96, 69, 40, 170), width=2)
    for y in range(54, height - 28, 28):
        draw.line((35, y, width - 35, y), fill=(91, 65, 41, 62), width=1)
    for x in range(64, width - 60, 72):
        draw.line((x, 34, x, height - 34), fill=(91, 65, 41, 34), width=1)
    image = _overlay_noise(image, 202, 30)
    _save(path, image)


def _draw_button_brass(path: Path) -> None:
    width, height = ASSET_SPECS["ui/button_brass.png"]
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    for inset in range(0, 16):
        color = (136 + inset * 3, 95 + inset * 2, 43 + inset, 255)
        draw.rounded_rectangle((inset, inset, width - inset - 1, height - inset - 1), radius=8, outline=color, width=2)
    draw.rounded_rectangle((18, 18, width - 19, height - 19), radius=6, fill=(125, 86, 38, 245), outline=(222, 171, 89, 210), width=2)
    draw.line((36, 34, width - 36, 34), fill=(245, 204, 122, 110), width=2)
    draw.line((36, height - 36, width - 36, height - 36), fill=(39, 24, 12, 145), width=2)
    image = _overlay_noise(image, 303, 24)
    _save(path, image)


def _draw_tool_magnifier(path: Path) -> None:
    image = Image.new("RGBA", ASSET_SPECS["ui/tool_magnifier.png"], (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    draw.ellipse((45, 35, 156, 146), fill=(64, 83, 87, 82), outline=(214, 181, 105, 255), width=12)
    draw.ellipse((62, 52, 139, 129), outline=(225, 237, 232, 110), width=4)
    draw.line((136, 134, 213, 211), fill=(86, 54, 25, 255), width=20)
    draw.line((136, 134, 213, 211), fill=(188, 139, 71, 255), width=8)
    _save(path, image)


def _draw_tool_uv_lamp(path: Path) -> None:
    image = Image.new("RGBA", ASSET_SPECS["ui/tool_uv_lamp.png"], (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle((55, 70, 184, 127), radius=18, fill=(36, 38, 50, 255), outline=(153, 129, 82, 255), width=5)
    draw.rectangle((82, 126, 157, 201), fill=(47, 43, 39, 255), outline=(151, 113, 70, 255), width=4)
    for offset, alpha in [(0, 210), (18, 110), (36, 55)]:
        draw.arc((24 - offset, 22 - offset, 216 + offset, 188 + offset), 200, 340, fill=(92, 114, 255, alpha), width=5)
    draw.rectangle((75, 84, 164, 104), fill=(88, 101, 217, 230))
    _save(path, image)


def _draw_tool_thermometer(path: Path) -> None:
    image = Image.new("RGBA", ASSET_SPECS["ui/tool_thermometer.png"], (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle((106, 34, 142, 168), radius=18, fill=(230, 229, 212, 230), outline=(92, 66, 38, 255), width=5)
    draw.ellipse((82, 145, 166, 229), fill=(163, 42, 38, 255), outline=(92, 66, 38, 255), width=5)
    draw.rounded_rectangle((116, 76, 132, 180), radius=8, fill=(161, 42, 40, 255))
    for y in range(52, 140, 20):
        draw.line((146, y, 168, y), fill=(222, 197, 126, 220), width=3)
    _save(path, image)


def _draw_workbench_walnut(path: Path) -> None:
    width, height = ASSET_SPECS["textures/workbench_walnut.png"]
    image = Image.new("RGBA", (width, height), (78, 46, 25, 255))
    draw = ImageDraw.Draw(image, "RGBA")
    rng = random.Random(404)
    for y in range(height):
        wave = int(18 * math.sin(y / 31.0) + 9 * math.sin(y / 9.0))
        color = (72 + wave // 2, 43 + wave // 3, 24, 255)
        draw.line((0, y, width, y), fill=color)
    for _ in range(90):
        y = rng.randint(0, height - 1)
        thickness = rng.randint(1, 4)
        shade = rng.randint(14, 42)
        draw.arc((-80, y - 80, width + 80, y + 80), 2, 178, fill=(110 + shade, 68 + shade // 2, 34, 90), width=thickness)
    image = _overlay_noise(image, 405, 45)
    _save(path, image)


def _draw_shop_wallpaper(path: Path) -> None:
    width, height = ASSET_SPECS["textures/shop_wallpaper.png"]
    image = Image.new("RGBA", (width, height), (83, 73, 57, 255))
    draw = ImageDraw.Draw(image, "RGBA")
    for x in range(0, width, 96):
        draw.rectangle((x, 0, x + 48, height), fill=(75, 66, 52, 255))
    for x in range(48, width, 96):
        for y in range(48, height, 128):
            draw.ellipse((x - 16, y - 28, x + 16, y + 28), outline=(125, 108, 75, 76), width=3)
            draw.line((x, y - 45, x, y + 45), fill=(126, 109, 75, 54), width=2)
    image = _overlay_noise(image, 505, 42)
    _save(path, image)


def _draw_cursed_teacup_decal(path: Path) -> None:
    width, height = ASSET_SPECS["textures/cursed_teacup_decal.png"]
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    center = (width // 2, height // 2)
    rng = random.Random(606)
    for i in range(44):
        angle = i * 0.31
        radius = 36 + i * 11
        x = center[0] + int(math.cos(angle) * radius)
        y = center[1] + int(math.sin(angle) * radius * 0.72)
        next_angle = angle + rng.uniform(0.18, 0.55)
        next_radius = radius + rng.randint(22, 58)
        x2 = center[0] + int(math.cos(next_angle) * next_radius)
        y2 = center[1] + int(math.sin(next_angle) * next_radius * 0.72)
        draw.line((x, y, x2, y2), fill=(64, 34, 26, 238), width=rng.randint(4, 9))
        if i % 3 == 0:
            draw.line((x2, y2, x2 + rng.randint(-80, 80), y2 + rng.randint(-46, 46)), fill=(52, 28, 23, 205), width=4)
        if i % 5 == 0:
            draw.ellipse((x2 - 18, y2 - 10, x2 + 18, y2 + 10), fill=(63, 33, 22, 92))
    for radius, alpha, thickness in [(98, 168, 8), (148, 150, 9), (220, 128, 10), (304, 112, 12)]:
        draw.ellipse(
            (center[0] - radius, center[1] - radius // 2, center[0] + radius, center[1] + radius // 2),
            outline=(50, 27, 22, alpha),
            width=thickness,
        )
    for offset_y, radius_x, radius_y, alpha in [(-330, 330, 34, 150), (330, 240, 28, 135)]:
        draw.ellipse(
            (
                center[0] - radius_x,
                center[1] + offset_y - radius_y,
                center[0] + radius_x,
                center[1] + offset_y + radius_y,
            ),
            outline=(76, 43, 25, alpha),
            width=14,
        )
    image = image.filter(ImageFilter.GaussianBlur(0.25))
    _save(path, image)


def _draw_mirror_coin_decal(path: Path) -> None:
    width, height = ASSET_SPECS["textures/mirror_coin_decal.png"]
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    center = (width // 2, height // 2)
    rng = random.Random(616)

    for radius, alpha, thickness in [(360, 120, 14), (292, 92, 8), (188, 70, 5)]:
        draw.ellipse(
            (
                center[0] - radius,
                center[1] - int(radius * 0.82),
                center[0] + radius,
                center[1] + int(radius * 0.82),
            ),
            outline=(28, 24, 20, alpha),
            width=thickness,
        )

    for i in range(58):
        angle = rng.uniform(-0.15, math.tau + 0.15)
        radius = rng.randint(50, 330)
        length = rng.randint(42, 150)
        skew = rng.uniform(-0.65, 0.65)
        x1 = center[0] + int(math.cos(angle) * radius)
        y1 = center[1] + int(math.sin(angle) * radius * 0.82)
        x2 = x1 + int(math.cos(angle + skew) * length)
        y2 = y1 + int(math.sin(angle + skew) * length * 0.42)
        draw.line((x1, y1, x2, y2), fill=(36, 30, 24, rng.randint(105, 210)), width=rng.randint(3, 7))

    for i in range(10):
        angle = i * math.tau / 10
        inner = 170
        outer = 280
        p1 = (center[0] + math.cos(angle) * inner, center[1] + math.sin(angle) * inner * 0.82)
        p2 = (center[0] + math.cos(angle) * outer, center[1] + math.sin(angle) * outer * 0.82)
        draw.line((p1[0], p1[1], p2[0], p2[1]), fill=(52, 147, 190, 132), width=7)

    draw.ellipse((center[0] - 42, center[1] - 34, center[0] + 42, center[1] + 34), outline=(64, 166, 210, 172), width=7)
    image = image.filter(ImageFilter.GaussianBlur(0.35))
    _save(path, image)


def _draw_uv_ring_mark(path: Path) -> None:
    width, height = ASSET_SPECS["textures/uv_ring_mark.png"]
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    center = (width // 2, height // 2)
    for radius, alpha, thickness in [(300, 70, 18), (245, 120, 12), (190, 170, 9), (138, 210, 6)]:
        draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), outline=(76, 138, 255, alpha), width=thickness)
    for i in range(18):
        angle = i * math.tau / 18
        inner = 210
        outer = 286
        p1 = (center[0] + math.cos(angle) * inner, center[1] + math.sin(angle) * inner)
        p2 = (center[0] + math.cos(angle) * outer, center[1] + math.sin(angle) * outer)
        draw.line((p1[0], p1[1], p2[0], p2[1]), fill=(95, 165, 255, 135), width=4)
    image = image.filter(ImageFilter.GaussianBlur(1.2))
    _save(path, image)


DRAWERS = {
    "ui/main_menu_background.png": _draw_main_menu_background,
    "ui/panel_ledger.png": _draw_panel_ledger,
    "ui/button_brass.png": _draw_button_brass,
    "ui/tool_magnifier.png": _draw_tool_magnifier,
    "ui/tool_uv_lamp.png": _draw_tool_uv_lamp,
    "ui/tool_thermometer.png": _draw_tool_thermometer,
    "textures/workbench_walnut.png": _draw_workbench_walnut,
    "textures/shop_wallpaper.png": _draw_shop_wallpaper,
    "textures/cursed_teacup_decal.png": _draw_cursed_teacup_decal,
    "textures/mirror_coin_decal.png": _draw_mirror_coin_decal,
    "textures/uv_ring_mark.png": _draw_uv_ring_mark,
}


def generate_assets(root: Path) -> list[Path]:
    output_root = root / "godot" / "assets"
    written: list[Path] = []
    for relative_path, drawer in DRAWERS.items():
        path = output_root / relative_path
        drawer(path)
        written.append(path)

    manifest_path = output_root / "visual_asset_manifest.json"
    manifest = {
        "status": "local_generated",
        "source": "tools.art.generate_mvp_visual_assets",
        "assets": [
            {
                "path": str(path.relative_to(root)).replace("\\", "/"),
                "size": ASSET_SPECS[str(path.relative_to(output_root)).replace("\\", "/")],
            }
            for path in written
        ],
    }
    _save_manifest(manifest_path, manifest)
    written.append(manifest_path)
    return written


def _save_manifest(path: Path, manifest: dict) -> None:
    _ensure_parent(path)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic MVP UI and texture assets.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root.")
    args = parser.parse_args()

    root = args.root.resolve()
    written = generate_assets(root)
    for path in written:
        print(path.relative_to(root).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
