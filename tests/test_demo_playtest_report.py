import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.demo_playtest_report import (
    build_demo_playtest_report,
    write_demo_playtest_report,
)


class DemoPlaytestReportTests(unittest.TestCase):
    def test_build_demo_playtest_report_prefills_build_under_test(self):
        report = build_demo_playtest_report(
            commit="abc1234",
            date="2026-05-21",
            tester="Codex",
            export_path="exports/windows/CursedCurioShop.exe",
        )

        self.assertIn("# Demo Playtest Report", report)
        self.assertIn("- Commit: `abc1234`", report)
        self.assertIn("- Export path: `exports/windows/CursedCurioShop.exe`", report)
        self.assertIn(
            "- Automated smoke command: `godot --headless --path godot --script res://tools/smoke_three_day_flow.gd`",
            report,
        )
        self.assertIn("- Tester: Codex", report)
        self.assertIn("- Date: 2026-05-21", report)
        self.assertIn("## Startup", report)
        self.assertIn("## Three-Day Flow", report)
        self.assertIn("## Consequences", report)
        self.assertIn("## Readability Notes", report)
        self.assertTrue(report.endswith("\n"))

    def test_build_demo_playtest_report_can_mark_automated_preflight(self):
        report = build_demo_playtest_report(
            commit="abc1234",
            date="2026-05-21",
            tester="Codex",
            preflight={
                "unit_tests": True,
                "godot_headless": True,
                "three_day_smoke": True,
                "windows_export": True,
            },
        )

        self.assertIn("- [x] Unit tests pass.", report)
        self.assertIn("- [x] Godot headless project load passes.", report)
        self.assertIn("- [x] Three-day smoke script passes.", report)
        self.assertIn("- [x] Windows export succeeds.", report)

    def test_write_demo_playtest_report_uses_date_based_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            output_path = write_demo_playtest_report(
                root=root,
                commit="abc1234",
                date="2026-05-21",
                tester="Codex",
            )

            self.assertEqual(
                output_path,
                root / "docs" / "production" / "playtests" / "2026-05-21-demo-playtest.md",
            )
            self.assertTrue(output_path.exists())
            self.assertIn("- Commit: `abc1234`", output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
