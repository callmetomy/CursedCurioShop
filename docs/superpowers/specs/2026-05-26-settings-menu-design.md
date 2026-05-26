# Settings Menu Design

Status: approved for implementation
Date: 2026-05-26
Owner direction: continue improving game completeness before Steam store preparation.

## Goal

Add a small settings menu to the main menu so the demo feels closer to a complete game. This pass should stay focused on player-facing options that matter immediately: language, fullscreen/windowed mode, and master volume.

## Scope

The settings menu lives on the existing main menu. It should not interrupt the current ten-day gameplay loop and should not require a save file system.

Controls:

- Settings button on the main menu.
- Language selector with the existing supported locales.
- Fullscreen toggle.
- Master volume slider.
- Back button to return to the main menu buttons.

## Behavior

- Opening Settings hides the main menu action buttons and shows the settings panel.
- Back returns to the normal main menu.
- Changing language calls `Localization.set_locale()` and refreshes visible main-menu text immediately.
- Fullscreen toggle switches between fullscreen and windowed display modes.
- Volume slider updates the Master audio bus volume.

## Non-Goals

- No persistent settings file in this pass.
- No in-game pause menu yet.
- No key rebinding.
- No graphics quality presets.
- No Steam-related work.

## Testing

Required verification:

- Main menu scene test for settings button and settings panel nodes.
- Main menu script test for language, fullscreen, volume, and back handlers.
- Localization test for settings labels in English and Traditional Chinese.
- Full Python test suite.
- Godot ten-day smoke flow to ensure gameplay is unaffected.

## Success Criteria

- Player can open Settings from the main menu.
- Player can change language and see menu text update.
- Player can toggle fullscreen/windowed mode.
- Player can adjust master volume.
- Existing demo flow remains intact.
