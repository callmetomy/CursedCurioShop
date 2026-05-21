from pathlib import Path

SMOKE_COMMAND = "godot --headless --path godot --script res://tools/smoke_three_day_flow.gd"
DEFAULT_EXPORT_PATH = "exports/windows/CursedCurioShop.exe"


def build_demo_playtest_report(
    *,
    commit: str,
    date: str,
    tester: str,
    export_path: str = DEFAULT_EXPORT_PATH,
    preflight: dict[str, bool] | None = None,
) -> str:
    preflight = preflight or {}
    unit_tests = _check(preflight.get("unit_tests", False))
    godot_headless = _check(preflight.get("godot_headless", False))
    three_day_smoke = _check(preflight.get("three_day_smoke", False))
    windows_export = _check(preflight.get("windows_export", False))

    return f"""# Demo Playtest Report

Use this report for a concrete Windows demo pass. Record observations, not design guesses.

## Build Under Test

- Commit: `{commit}`
- Export path: `{export_path}`
- Automated smoke command: `{SMOKE_COMMAND}`
- Tester: {tester}
- Date: {date}

## Automated Preflight

- [{unit_tests}] Unit tests pass.
- [{godot_headless}] Godot headless project load passes.
- [{three_day_smoke}] Three-day smoke script passes.
- [{windows_export}] Windows export succeeds.

## Startup

- [ ] Game launches from the exported Windows executable.
- [ ] Main menu appears without missing textures, missing fonts, or script errors.
- [ ] Start button enters the playable shop scene.

## Three-Day Flow

- [ ] Day 1 starts with Cash 100 and Reputation 50.
- [ ] The player can enter the inspection table from the shop.
- [ ] The inspection table shows the current oddity name and description.
- [ ] Magnifier, UV lamp, and thermometer each produce readable clue text.
- [ ] Appraisal Notes preserve discovered tool clues.
- [ ] Sell, Seal, and Discard buttons are visible and usable.
- [ ] A decision opens the result panel with cash and reputation deltas.
- [ ] Back To Shop returns to the shop scene.
- [ ] Next Day advances to the next daily oddity before the final day.
- [ ] The final day result button reads `Return to Menu`.
- [ ] Return To Menu returns to the main menu after Day 3.

## Consequences

- [ ] Correct handling produces a better result than at least one wrong handling.
- [ ] A wrong handling path can trigger the abnormal event.
- [ ] The bad ending path can be reached through low reputation.
- [ ] Cash and reputation changes remain visible after scene transitions.

## Readability Notes

| ID | Severity | Day / Oddity | Issue | Repro Steps | Expected | Actual |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Pass Result

- [ ] Pass: demo can be completed without blocking issues.
- [ ] Conditional pass: demo can be completed, but listed issues should be fixed before sharing.
- [ ] Fail: demo cannot be completed.
"""


def write_demo_playtest_report(
    *,
    root: Path,
    commit: str,
    date: str,
    tester: str,
    export_path: str = DEFAULT_EXPORT_PATH,
    preflight: dict[str, bool] | None = None,
) -> Path:
    report_dir = root / "docs" / "production" / "playtests"
    report_dir.mkdir(parents=True, exist_ok=True)
    output_path = report_dir / f"{date}-demo-playtest.md"
    output_path.write_text(
        build_demo_playtest_report(
            commit=commit,
            date=date,
            tester=tester,
            export_path=export_path,
            preflight=preflight,
        ),
        encoding="utf-8",
    )
    return output_path


def _check(is_checked: bool) -> str:
    if is_checked:
        return "x"
    return " "
