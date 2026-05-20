import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.asset_pipeline.items import build_item_definition, save_item_definition
from tools.project_status import (
    build_project_status,
    render_project_status_markdown,
    summarize_item_assets,
)


class ProjectStatusTests(unittest.TestCase):
    def test_summarize_item_assets_counts_ready_outputs_for_each_item(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            item = build_item_definition(
                item_id="oddity_0003",
                display_name="Mirror Coin",
                concept_prompt="A mirror coin concept.",
                model_prompt="A mirror coin model.",
            )
            save_item_definition(item, root / "data" / "items")
            (root / "data" / "items" / "item_schema.json").write_text(
                '{"id": "oddity_example", "display_name": "Schema Example"}\n',
                encoding="utf-8",
            )
            (root / "assets" / "concepts").mkdir(parents=True)
            (root / "assets" / "concepts" / "oddity_0003.png").write_bytes(b"png")

            summaries = summarize_item_assets(root)

            self.assertEqual(len(summaries), 1)
            self.assertEqual(summaries[0]["item_id"], "oddity_0003")
            self.assertEqual(summaries[0]["display_name"], "Mirror Coin")
            self.assertEqual(summaries[0]["ready_outputs"], 1)
            self.assertEqual(summaries[0]["total_outputs"], 4)
            self.assertEqual(
                summaries[0]["missing_stages"],
                ["raw_model", "processed_model", "review_report"],
            )

    def test_build_project_status_combines_git_tests_and_item_progress(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            item = build_item_definition(
                item_id="oddity_0004",
                display_name="Ashen Music Box",
                concept_prompt="An ashen music box concept.",
                model_prompt="An ashen music box model.",
            )
            save_item_definition(item, root / "data" / "items")

            status = build_project_status(
                root=root,
                git_info={
                    "branch": "master",
                    "is_dirty": False,
                    "changes": [],
                    "recent_commits": ["abc1234 Add dashboard"],
                },
                test_info={"ran": True, "passed": True, "summary": "Ran 9 tests"},
            )

            self.assertEqual(status["git"]["branch"], "master")
            self.assertEqual(status["tests"]["passed"], True)
            self.assertEqual(status["asset_totals"]["items"], 1)
            self.assertEqual(status["asset_totals"]["ready_outputs"], 0)
            self.assertEqual(status["asset_totals"]["total_outputs"], 4)

    def test_render_project_status_markdown_is_a_compact_dashboard(self):
        status = {
            "git": {
                "branch": "master",
                "is_dirty": True,
                "changes": ["M README.md"],
                "recent_commits": ["abc1234 Add dashboard"],
            },
            "tests": {"ran": False, "passed": None, "summary": "not run"},
            "asset_totals": {"items": 1, "ready_outputs": 2, "total_outputs": 4},
            "items": [
                {
                    "item_id": "oddity_0005",
                    "display_name": "Glass Eye",
                    "ready_outputs": 2,
                    "total_outputs": 4,
                    "missing_stages": ["processed_model", "review_report"],
                }
            ],
        }

        markdown = render_project_status_markdown(status)

        self.assertIn("# Project Status", markdown)
        self.assertIn("- Branch: `master`", markdown)
        self.assertIn("- Working tree: dirty", markdown)
        self.assertIn("- Tests: not run", markdown)
        self.assertIn("- Asset outputs: 2/4 ready across 1 item(s)", markdown)
        self.assertIn("- oddity_0005 Glass Eye: 2/4 ready", markdown)
        self.assertTrue(markdown.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
