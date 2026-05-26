# Audio Feedback Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add short sound cues for inspection tools, decisions, abnormal events, and bad endings.

**Architecture:** Store generated WAV files in `godot/assets/audio/`, reference them from `inspection_table.tscn`, and play them through dedicated `AudioStreamPlayer` nodes in `inspection_table.gd`.

**Tech Stack:** Godot 4 GDScript scenes/scripts, local WAV assets, Python `unittest` text assertions.

---

## Task 1: Audio Scene And Script Wiring

**Files:**
- Modify: `tests/test_godot_inspection_table.py`
- Modify: `godot/scenes/inspection_table.tscn`
- Modify: `godot/scripts/inspection_table.gd`

- [ ] Write failing tests for audio ext resources, `AudioStreamPlayer` nodes, onready bindings, and playback calls.
- [ ] Run `python -m unittest tests.test_godot_inspection_table` and confirm expected failure.
- [ ] Add audio resources and players to the inspection table scene.
- [ ] Add `_play_audio_cue()` and call it from tool activation, decision result, abnormal event, and bad ending paths.
- [ ] Run `python -m unittest tests.test_godot_inspection_table` and confirm pass.

## Task 2: Generated Local WAV Assets

**Files:**
- Create: `godot/assets/audio/tool_activate.wav`
- Create: `godot/assets/audio/decision_correct.wav`
- Create: `godot/assets/audio/decision_wrong.wav`
- Create: `godot/assets/audio/abnormal_event.wav`
- Create: `godot/assets/audio/bad_ending.wav`

- [ ] Generate five short local WAV files using deterministic PowerShell.
- [ ] Run `Test-Path godot/assets/audio/*.wav` checks.
- [ ] Let Godot import them during headless verification.

## Task 3: Verification

**Files:**
- No new implementation files.

- [ ] Run `python -m unittest discover -s tests`.
- [ ] Run `C:\tomy\Godot\Godot.exe --headless --path godot --script res://tools/smoke_three_day_flow.gd`.
- [ ] Run `python -m tools.project_status --root . --run-tests`.
- [ ] Inspect `git status --short`.
