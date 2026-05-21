# Demo Playtest Checklist

Use this checklist for manual Windows demo passes. Record concrete observations, not design guesses.

## Build Under Test

- Commit:
- Export path: `exports/windows/CursedCurioShop.exe`
- Tester:
- Date:

## Startup

- [ ] Game launches from the exported Windows executable.
- [ ] Main menu appears without missing textures, missing fonts, or script errors.
- [ ] Start button enters the playable shop scene.

## Three-Day Flow

- [ ] Day 1 starts with Cash 100 and Reputation 50.
- [ ] The player can enter the inspection table from the shop.
- [ ] The inspection table shows the current oddity name and description.
- [ ] Magnifier, UV lamp, and thermometer each produce readable clue text.
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

For each issue, include the day, oddity id, action taken, expected result, actual result, and whether it blocks demo completion.

| ID | Severity | Day / Oddity | Issue | Repro Steps | Expected | Actual |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Pass Result

- [ ] Pass: demo can be completed without blocking issues.
- [ ] Conditional pass: demo can be completed, but listed issues should be fixed before sharing.
- [ ] Fail: demo cannot be completed.
