# Demo Build Handoff

Handoff date: 2026-05-26
Build focus: commercial-demo readability tuning, ten-day balance pass, agent blind-test tuning, and two shop progression upgrades.

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
- Correct route balance after agent blind-test tuning: minimum Cash 20, final Cash 180, final Reputation 100.
- Ledger Desk upgrade added: final-day cash spend, persistent next-run state, and provenance notes in customer briefs.
- Containment Cabinet upgrade added on 2026-05-26: final-day cash spend, persistent next-run state, and each future Seal costs 5 less.
- Upgraded second-run smoke validates Final Cash 210, Final Reputation 100, and minimum cash buffer 35.
- Agent blind-test follow-up clarified shop-upgrade text so players see that upgrades persist into future runs.
- Traditional Chinese review screenshots were refreshed after the longer clue text and progression UI; `1152x648` and `1280x720` final summary both show both upgrade buttons and Return to Menu.
- Windows export refreshed on 2026-05-26 at `exports/windows/CursedCurioShop.exe`.

## Verification

```powershell
python -m unittest tests.test_commercial_demo_design
python -m unittest tests.test_godot_shop_progression
python -m unittest tests.test_godot_game_state tests.test_godot_shop_progression tests.test_godot_inspection_table
python -m unittest discover -s tests
godot --headless --path godot --script res://tools/smoke_three_day_flow.gd
godot --path godot --script res://tools/capture_traditional_chinese_review.gd
godot --headless --path godot --export-release "Windows Desktop" ..\exports\windows\CursedCurioShop.exe
python -m tools.project_status --root . --run-tests
```

Latest local verification:

- Full project tests: 106 passing.
- Asset outputs: 40/40 ready across 10 item(s).
- Godot ten-day smoke: exit 0.
- Traditional Chinese screenshot capture: exit 0.
- Windows export: `CursedCurioShop.exe` and console wrapper regenerated on 2026-05-26.
- Owner playtest from the Windows export: OK, reported on 2026-05-26.

## Known Limits

- This build uses agent blind tests in place of three real external players by owner direction. Owner direction on 2026-05-26 is to skip the real-player blind-test gate for now and proceed to demo baseline stabilization.
- Agent blind-test tuning on 2026-05-26 moved Day 9 from Discard to Seal to match player reasoning.
- The second shop perk was added and upgraded-run validation is complete. The next decision should be baseline commit and release-note cleanup, not another perk or a content expansion in the same slice.
