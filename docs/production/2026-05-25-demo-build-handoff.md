# Demo Build Handoff

Handoff date: 2026-05-25
Build focus: commercial-demo readability tuning, ten-day balance pass, and Ledger Desk progression slice.

## Build

```text
exports/windows/CursedCurioShop.exe
exports/windows/CursedCurioShop.console.exe
```

Godot export preset:

```text
Windows Desktop
```

Export command:

```powershell
godot --headless --path godot --export-release "Windows Desktop" ..\exports\windows\CursedCurioShop.exe
```

## Included Changes

- Ten-day playable loop remains `oddity_0001` through `oddity_0010`.
- Item clues were rewritten to avoid prototype template text.
- Customer risk hints no longer directly name Sell / Seal / Discard.
- Sell values and seal costs now create different cash-pressure profiles.
- Correct route balance: minimum Cash 20, final Cash 195, final Reputation 100.
- Ledger Desk upgrade added: final-day cash spend, persistent next-run state, and provenance notes in customer briefs.
- Traditional Chinese review screenshots were refreshed after the longer clue text and progression UI.

## Verification

```powershell
python -m unittest tests.test_commercial_demo_design
python -m unittest tests.test_godot_shop_progression
python -m unittest discover -s tests
godot --headless --path godot --script res://tools/smoke_three_day_flow.gd
godot --path godot --script res://tools/capture_traditional_chinese_review.gd
python -m tools.project_status --root . --run-tests
```

## Known Limits

- This build skips external blind playtest by owner direction.
- Windows export was refreshed, but no manual full run was performed from the exported `.exe` in this pass.
- The next implementation decision should be either a second shop perk or a content expansion, not both in the same slice.
