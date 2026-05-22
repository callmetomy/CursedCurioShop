# Demo Playtest Report

Use this report for a concrete Windows demo pass. Record observations, not design guesses.

## Build Under Test

- Commit: `d5489be`
- Export path: `exports/windows/CursedCurioShop.exe`
- Automated smoke command: `godot --headless --path godot --script res://tools/smoke_three_day_flow.gd`
- Tester: Codex automated preflight + screenshot review notes
- Date: 2026-05-22

## Automated Preflight

- [x] Unit tests pass.
- [x] Godot headless project load passes.
- [x] Three-day smoke script passes.
- [x] Windows export succeeds.

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
| VIS-001 | Fixed | Day 1 / Whispering Teacup | Teacup surface appeared too white and the crack/stain details read like geometry markers instead of surface detail. | Inspect Day 1, rotate the teacup, and use Magnifier/UV Lamp. | Porcelain remains light but shows warm aging, surface cracks, stain, and UV ring detail. | Teacup now uses warmer material response with decal-style crack/stain details and a UV-only ring mark. |
| VIS-002 | Fixed | Day 2 / Mirror Coin | Coin started edge-on or overly bright, making the face and appraisal scratches hard to read. | Advance to Day 2, inspect Mirror Coin, and use Magnifier. | The coin face is readable and scratches appear as surface appraisal marks. | Mirror Coin now starts front-facing and uses a larger y-axis projected surface decal. |
| VIS-003 | Fixed | Day 3 / Ashen Music Box | Music box silhouette was too cube-like to read as a music box in inspection screenshots. | Advance to Day 3 and inspect Ashen Music Box. | The object should read as a music box before relying on text description. | Runtime GLB now contains separate base, lid, cylinder, crank, handle, and feet parts. |

## Pass Result

- [ ] Pass: demo can be completed without blocking issues.
- [ ] Conditional pass: demo can be completed, but listed issues should be fixed before sharing.
- [ ] Fail: demo cannot be completed.
