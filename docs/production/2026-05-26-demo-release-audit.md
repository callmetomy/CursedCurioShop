# Demo Release Audit

Audit date: 2026-05-26
Scope: local Windows demo handoff after agent blind-test tuning and two shop progression upgrades.

## Current Build

- Export path: `exports/windows/CursedCurioShop.exe`
- Console wrapper: `exports/windows/CursedCurioShop.console.exe`
- Export preset: `Windows Desktop`
- Export refreshed: 2026-05-26 10:51 local time
- Export files are intentionally ignored by git under `exports/`.

## Included Scope

- Ten-day playable loop from `oddity_0001` through `oddity_0010`.
- Day 3 and Day 4 clue readability tuned after agent blind-test misses.
- Day 9 correct handling changed from Discard to Seal to match player reasoning.
- Correct first-run route: minimum Cash 20, Final Cash 180, Final Reputation 100.
- Ledger Desk upgrade: costs 120, persists into future runs, adds source clues to customer briefs.
- Containment Cabinet upgrade: costs 60, persists into future runs, reduces each future Seal cost by 5.
- Upgraded second run: Final Cash 210, Final Reputation 100, minimum cash buffer 35.

## Verification Evidence

```powershell
python -m unittest tests.test_godot_game_state tests.test_godot_shop_progression tests.test_godot_inspection_table
python -m unittest discover -s tests
godot --headless --path godot --script res://tools/smoke_three_day_flow.gd
godot --path godot --script res://tools/capture_traditional_chinese_review.gd
godot --headless --path godot --export-release "Windows Desktop" ..\exports\windows\CursedCurioShop.exe
python -m tools.project_status --root . --run-tests
```

Latest verified state:

- Full project tests: 106 passing.
- Asset outputs: 40/40 ready across 10 item(s).
- Godot ten-day smoke: exit 0.
- Traditional Chinese screenshot capture: exit 0.
- Windows export: regenerated on 2026-05-26.
- Owner playtest from the Windows export: OK, reported on 2026-05-26.

## Visual Evidence

Screenshots refreshed under `docs/production/playtests/screenshots/`:

- `shop_customer_brief-1152x648.png`
- `shop_customer_brief-1280x720.png`
- `day_result-1152x648.png`
- `day_result-1280x720.png`
- `shop_result_detail-1152x648.png`
- `shop_result_detail-1280x720.png`
- `final_summary-1152x648.png`
- `final_summary-1280x720.png`

The final summary screenshot at `1152x648` shows both upgrade buttons and Return to Menu after the longer progression copy.

## Release Limitations

- Owner direction on 2026-05-26: skip the real-player blind-test gate for now and proceed to demo baseline stabilization.
- Agent blind tests remain the available evidence for text logic and rule inference; they do not validate real operation, emotion, attention, or pacing.
- The repo working tree is still dirty; this is a local handoff state, not a committed release tag.

## Recommendation

This demo has passed owner playtest validation as a local handoff build. Per owner direction, the next step is:

- commit a demo baseline after final status verification,
- keep the real-player playtest checklist available as an optional later gate,
- avoid new perks or new oddity batches until the baseline is preserved.

Do not add another perk or new oddity batch before the baseline commit is complete.
