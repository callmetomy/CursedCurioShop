# Demo Completeness Pass Design

Status: approved for implementation
Date: 2026-05-26
Owner direction: pause Steam store preparation and make the game feel more complete first.

## Goal

Improve the existing ten-day demo so it feels less like a prototype and more like a complete small game loop. This pass keeps the owner-approved demo baseline intact, avoids Steam asset work, and does not add a new oddity batch.

## Scope

This pass focuses on two connected areas:

1. First-run onboarding that teaches the appraisal loop inside the game.
2. Explicit run reset and upgrade persistence behavior so progression is understandable across runs.

The work should preserve the current ten-day queue, Sell / Seal / Discard decisions, Ledger Desk upgrade, Containment Cabinet upgrade, and existing automated test coverage.

## Player Experience

On a fresh run, the player should quickly understand:

- how to inspect the current object,
- that the three tools reveal different clues,
- that the notes panel records discovered clues,
- that Sell, Seal, and Discard are consequential choices,
- that upgrades bought after a completed run affect future runs.

The onboarding should be brief and in-world. It should not reveal correct answers, directly name the correct handling for any oddity, or stop the player from experimenting.

## Design

### First-Run Onboarding

Add a small guidance panel to the inspection table for Day 1 until the player has used all three tools at least once. The panel should be localized and show the next practical instruction:

- inspect the object with the Magnifier,
- inspect it with the UV Lamp,
- check the temperature with the Thermometer,
- then choose Sell, Seal, or Discard.

The panel is guidance, not a modal tutorial. It should not block buttons, movement, item rotation, or decisions.

### Upgrade Persistence And Reset Clarity

Keep upgrades persistent across `GameState.start_new_run()`, matching the current behavior and tests. Make that behavior visible from the main menu:

- a start button that begins a new run while keeping purchased upgrades,
- a reset progress button that clears purchased upgrades and starts over from a clean profile.

The reset action should be explicit in wording. For this pass, no confirmation dialog is required because the game is still local prototype software, but the button text must make the destructive behavior clear.

### Run State

Add a small amount of state to `GameState`:

- whether onboarding has been completed,
- which onboarding tools have been used in the current run,
- a `reset_progress()` method that clears persistent upgrades and starts a clean run.

`start_new_run()` should reset day, cash, reputation, handled reports, and current-run onboarding state. It should not clear purchased upgrades.

`reset_progress()` should clear purchased upgrades, onboarding completion, and then call the clean run setup.

## Files

Expected implementation touch points:

- `godot/scripts/game_state.gd`
- `godot/scripts/inspection_table.gd`
- `godot/scripts/main_menu.gd`
- `godot/scripts/localization.gd`
- `godot/scenes/inspection_table.tscn`
- `godot/scenes/main_menu.tscn`
- focused Python text tests under `tests/`

## Non-Goals

- No Steam screenshots, capsules, trailer work, or store page updates.
- No new oddity batch.
- No save-to-disk profile system in this pass.
- No large UI redesign.
- No tutorial popups that reveal the correct decision.

## Testing

Required verification:

- Unit-style text tests for the new `GameState` methods and persistence behavior.
- Scene/script tests proving the onboarding panel and reset progress button exist.
- Localization tests for English and Traditional Chinese tutorial/reset strings.
- Full test suite: `python -m unittest discover -s tests`.
- Project dashboard: `python -m tools.project_status --root . --run-tests`.

## Success Criteria

- A first-time player gets in-game guidance before making the first decision.
- The demo still plays through the existing ten-day loop.
- Purchased upgrades still persist into future runs.
- The player can intentionally reset progression from the main menu.
- All existing tests pass after the change.
