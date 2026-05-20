import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.asset_pipeline.items import build_item_definition, save_item_definition
from tools.asset_pipeline.render_review_blender import (
    REVIEW_ANGLES,
    build_blender_review_command,
    build_review_render_job,
)


class RenderReviewBlenderTests(unittest.TestCase):
    def test_build_review_render_job_uses_processed_model_and_standard_outputs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            item = build_item_definition(
                item_id="oddity_0030",
                display_name="Silver Funeral Bell",
                concept_prompt="A silver funeral bell concept.",
                model_prompt="A silver funeral bell model.",
            )
            save_item_definition(item, root / "data" / "items")

            job = build_review_render_job(root=root, item_id="oddity_0030")

            self.assertEqual(job["item_id"], "oddity_0030")
            self.assertEqual(job["display_name"], "Silver Funeral Bell")
            self.assertEqual(job["input_path"], str(root / "assets" / "models_processed" / "oddity_0030.glb"))
            self.assertEqual(
                job["output_paths"],
                {
                    angle: str(root / "assets" / "review" / f"oddity_0030_{angle}.png")
                    for angle in REVIEW_ANGLES
                },
            )
            self.assertEqual(
                job["relative_output_paths"],
                [f"assets/review/oddity_0030_{angle}.png" for angle in REVIEW_ANGLES],
            )

    def test_build_blender_review_command_passes_review_arguments_after_separator(self):
        command = build_blender_review_command(
            blender_executable=Path("C:/Blender/blender.exe"),
            script_path=Path("C:/repo/tools/asset_pipeline/blender_render_review.py"),
            input_path=Path("C:/repo/assets/models_processed/oddity_0030.glb"),
            output_dir=Path("C:/repo/assets/review"),
            item_id="oddity_0030",
            resolution=768,
        )

        self.assertEqual(command[0], "C:\\Blender\\blender.exe")
        separator_index = command.index("--")
        self.assertEqual(
            command[separator_index + 1 :],
            [
                "--input",
                "C:\\repo\\assets\\models_processed\\oddity_0030.glb",
                "--output-dir",
                "C:\\repo\\assets\\review",
                "--item-id",
                "oddity_0030",
                "--resolution",
                "768",
            ],
        )


if __name__ == "__main__":
    unittest.main()
