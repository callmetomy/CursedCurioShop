import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.asset_pipeline.items import build_item_definition, save_item_definition
from tools.asset_pipeline.process_model_blender import (
    build_blender_command,
    build_blender_process_job,
    resolve_blender_executable,
)


class ProcessModelBlenderTests(unittest.TestCase):
    def test_build_blender_process_job_uses_item_model_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            item = build_item_definition(
                item_id="oddity_0020",
                display_name="Cracked Hand Mirror",
                concept_prompt="A cracked hand mirror concept.",
                model_prompt="A cracked hand mirror model.",
            )
            save_item_definition(item, root / "data" / "items")

            job = build_blender_process_job(root=root, item_id="oddity_0020")

            self.assertEqual(job["item_id"], "oddity_0020")
            self.assertEqual(job["display_name"], "Cracked Hand Mirror")
            self.assertEqual(job["input_path"], str(root / "assets" / "models_raw" / "oddity_0020.glb"))
            self.assertEqual(job["output_path"], str(root / "assets" / "models_processed" / "oddity_0020.glb"))
            self.assertEqual(job["relative_output_path"], "assets/models_processed/oddity_0020.glb")

    def test_resolve_blender_executable_accepts_explicit_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            blender = Path(temp_dir) / "blender.exe"
            blender.write_text("", encoding="utf-8")

            self.assertEqual(resolve_blender_executable(explicit=blender), blender.resolve())

    def test_build_blender_command_passes_script_arguments_after_separator(self):
        command = build_blender_command(
            blender_executable=Path("C:/Blender/blender.exe"),
            script_path=Path("C:/repo/tools/asset_pipeline/blender_process_model.py"),
            input_path=Path("C:/repo/assets/models_raw/oddity_0020.glb"),
            output_path=Path("C:/repo/assets/models_processed/oddity_0020.glb"),
            item_id="oddity_0020",
            target_longest_axis=0.35,
        )

        self.assertEqual(command[0], "C:\\Blender\\blender.exe")
        self.assertIn("--background", command)
        self.assertIn("--factory-startup", command)
        self.assertIn("--python", command)
        separator_index = command.index("--")
        self.assertEqual(
            command[separator_index + 1 :],
            [
                "--input",
                "C:\\repo\\assets\\models_raw\\oddity_0020.glb",
                "--output",
                "C:\\repo\\assets\\models_processed\\oddity_0020.glb",
                "--item-id",
                "oddity_0020",
                "--target-longest-axis",
                "0.35",
            ],
        )


if __name__ == "__main__":
    unittest.main()
