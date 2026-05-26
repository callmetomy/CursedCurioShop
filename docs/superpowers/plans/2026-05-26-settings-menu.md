# Settings Menu Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a main-menu Settings panel with language, fullscreen, volume, and back controls.

**Architecture:** Keep the feature inside the existing main menu scene/script. Use `Localization` for labels, `DisplayServer` for fullscreen/windowed mode, and `AudioServer` for Master bus volume.

**Tech Stack:** Godot 4 GDScript scenes/scripts plus Python `unittest` text assertions.

---

## Task 1: Main Menu Settings UI

**Files:**
- Modify: `tests/test_godot_main_menu.py`
- Modify: `godot/scenes/main_menu.tscn`
- Modify: `godot/scripts/main_menu.gd`

- [ ] Write failing tests for `SettingsButton`, `SettingsPanel`, `LanguageOption`, `FullscreenCheckBox`, `VolumeSlider`, and `BackFromSettingsButton`.
- [ ] Run `python -m unittest tests.test_godot_main_menu` and confirm expected failure.
- [ ] Add the scene nodes and script bindings.
- [ ] Run `python -m unittest tests.test_godot_main_menu` and confirm pass.

## Task 2: Settings Localization

**Files:**
- Modify: `tests/test_godot_localization.py`
- Modify: `godot/scripts/localization.gd`

- [ ] Write failing tests for settings localization keys in `en` and `zh_TW`.
- [ ] Run `python -m unittest tests.test_godot_localization` and confirm expected failure.
- [ ] Add labels for settings, language, fullscreen, volume, and back.
- [ ] Run `python -m unittest tests.test_godot_localization` and confirm pass.

## Task 3: Verification

**Files:**
- No new implementation files.

- [ ] Run `python -m unittest discover -s tests`.
- [ ] Run `C:\tomy\Godot\Godot.exe --headless --path godot --script res://tools/smoke_three_day_flow.gd`.
- [ ] Run `python -m tools.project_status --root . --run-tests`.
- [ ] Inspect `git status --short`.
