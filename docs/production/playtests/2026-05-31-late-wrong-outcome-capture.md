# 2026-05-31 Late-Game Wrong Outcome Capture

## Scope

Add a review-facing Traditional Chinese screenshot state for a late-game wrong outcome before starting a new oddity batch.

Covered state:

- Day 8 Silver Funeral Bell wrong sale at `1152x648`
- Day 8 Silver Funeral Bell wrong sale at `1280x720`

## Commands

```powershell
python -m unittest tests.test_godot_inspection_table tests.test_godot_visual_qa_capture
godot --headless --path godot --script res://tools/smoke_three_day_flow.gd
godot --path godot --script res://tools/capture_traditional_chinese_review.gd
python -m unittest discover -s tests
python -m tools.project_status --root . --run-tests
```

## Result

- Added `late_wrong_outcome` to the Traditional Chinese capture script.
- The state uses Day 8 `Silver Funeral Bell` with the wrong `sell` decision.
- Fixed the day-result overlay so the old `DecisionResult` summary label is hidden when the ledger-style result panel is visible.
- Refreshed the Traditional Chinese HUD screenshot set after the overlay fix.

## Evidence

- `docs/production/playtests/screenshots/late_wrong_outcome-1152x648.png`
- `docs/production/playtests/screenshots/late_wrong_outcome-1280x720.png`
- `docs/production/playtests/screenshots/day_result-1152x648.png`
- `docs/production/playtests/screenshots/day_result-1280x720.png`
- `docs/production/playtests/screenshots/final_summary-1152x648.png`
- `docs/production/playtests/screenshots/final_summary-1280x720.png`
- `docs/production/playtests/screenshots/shop_result_detail-1152x648.png`
- `docs/production/playtests/screenshots/shop_result_detail-1280x720.png`

## Next

Phase C now has enough branch and capture evidence to evaluate a small second oddity batch. Keep the first new batch small and require clue readability, wrong-outcome clarity, and Traditional Chinese capture evidence before expanding further.
