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

        self.assertIn("# Demo 試玩報告", report)
        self.assertIn("- Commit: `abc1234`", report)
        self.assertIn("- 匯出路徑: `exports/windows/CursedCurioShop.exe`", report)
        self.assertIn(
            "- 自動 smoke 測試指令: `godot --headless --path godot --script res://tools/smoke_three_day_flow.gd`",
            report,
        )
        self.assertIn("- 測試者: Codex", report)
        self.assertIn("- 日期: 2026-05-21", report)
        self.assertIn("## 啟動流程", report)
        self.assertIn("## 三日流程", report)
        self.assertIn("## 後果與結局", report)
        self.assertIn("## 可讀性紀錄", report)
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

        self.assertIn("- [x] 單元測試通過。", report)
        self.assertIn("- [x] Godot headless 專案載入通過。", report)
        self.assertIn("- [x] 三日流程 smoke script 通過。", report)
        self.assertIn("- [x] Windows 匯出成功。", report)

    def test_build_demo_playtest_report_renders_readability_notes(self):
        report = build_demo_playtest_report(
            commit="abc1234",
            date="2026-05-22",
            tester="Codex",
            readability_notes=[
                {
                    "id": "VIS-001",
                    "severity": "已修正",
                    "day_oddity": "Day 2 / Mirror Coin",
                    "issue": "硬幣正面與刮痕不易閱讀。",
                    "repro_steps": "檢視 Day 2 並使用 Magnifier。",
                    "expected": "刮痕應像表面細節。",
                    "actual": "硬幣目前以正面朝向開始，decal 較容易閱讀。",
                }
            ],
        )

        self.assertIn(
            "| VIS-001 | 已修正 | Day 2 / Mirror Coin | 硬幣正面與刮痕不易閱讀。 | 檢視 Day 2 並使用 Magnifier。 | 刮痕應像表面細節。 | 硬幣目前以正面朝向開始，decal 較容易閱讀。 |",
            report,
        )

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
