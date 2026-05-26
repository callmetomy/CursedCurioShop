# Demo Completeness Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add brief first-run onboarding and explicit progression reset while preserving the current ten-day demo loop.

**Architecture:** Keep state in `GameState`, render non-blocking guidance in `inspection_table`, and expose reset from `main_menu`. Use the repo's existing text-based Python tests for fast coverage before Godot smoke verification.

**Tech Stack:** Godot 4 GDScript scenes/scripts plus Python `unittest` text assertions.

---

## File Map

- Modify `godot/scripts/game_state.gd`: onboarding state, tool tracking, reset progress API.
- Modify `godot/scripts/inspection_table.gd`: guidance label binding and update calls.
- Modify `godot/scenes/inspection_table.tscn`: small `OnboardingPanel` under HUD.
- Modify `godot/scripts/main_menu.gd`: reset button binding and handler.
- Modify `godot/scenes/main_menu.tscn`: reset progress button.
- Modify `godot/scripts/localization.gd`: English and Traditional Chinese strings, with English fallback for other locales.
- Add or modify tests under `tests/`: focused assertions for state, UI wiring, and localization.

## Task 1: GameState Onboarding And Reset API

**Files:**
- Modify: `godot/scripts/game_state.gd`
- Modify: `tests/test_godot_game_state.py`

- [ ] **Step 1: Write failing tests**

Add tests that assert `GameState` contains:

```python
self.assertIn("var onboarding_completed := false", game_state)
self.assertIn('TOOL_MAGNIFIER: false', game_state)
self.assertIn("func start_new_run() -> void:", game_state)
self.assertIn("_reset_current_run_state()", game_state)
self.assertIn("func reset_progress() -> void:", game_state)
self.assertIn("ledger_desk_upgraded = false", game_state)
self.assertIn("containment_cabinet_upgraded = false", game_state)
self.assertIn("func record_onboarding_tool_used(tool_name: String) -> void:", game_state)
self.assertIn("func get_onboarding_hint_key() -> String:", game_state)
```

- [ ] **Step 2: Run focused test**

Run:

```powershell
python -m unittest tests.test_godot_game_state
```

Expected: fail because the new onboarding/reset symbols do not exist.

- [ ] **Step 3: Implement minimal state API**

Add current-run onboarding fields, refactor `start_new_run()` through `_reset_current_run_state()`, add `reset_progress()`, add `record_onboarding_tool_used()`, and add `get_onboarding_hint_key()`.

- [ ] **Step 4: Run focused test again**

Run:

```powershell
python -m unittest tests.test_godot_game_state
```

Expected: pass.

## Task 2: Inspection Table Guidance Panel

**Files:**
- Modify: `godot/scenes/inspection_table.tscn`
- Modify: `godot/scripts/inspection_table.gd`
- Modify: `tests/test_godot_inspection_table.py`

- [ ] **Step 1: Write failing tests**

Assert that the scene has:

```python
self.assertIn('[node name="OnboardingPanel" type="PanelContainer" parent="HUD"]', scene)
self.assertIn('[node name="OnboardingHintLabel" type="Label" parent="HUD/OnboardingPanel"]', scene)
```

Assert that the script has:

```python
self.assertIn("onboarding_panel", script)
self.assertIn("onboarding_hint_label", script)
self.assertIn("GameState.get_onboarding_hint_key()", script)
self.assertIn("GameState.record_onboarding_tool_used(tool_name)", script)
self.assertIn("_update_onboarding_hint()", script)
```

- [ ] **Step 2: Run focused test**

Run:

```powershell
python -m unittest tests.test_godot_inspection_table
```

Expected: fail because the panel and script hooks do not exist.

- [ ] **Step 3: Add scene and script wiring**

Add a compact panel under the top-left HUD area. In `_set_active_tool()`, record used tools and update the hint. Hide the panel when onboarding is complete or when day result / ending panels are visible.

- [ ] **Step 4: Run focused test again**

Run:

```powershell
python -m unittest tests.test_godot_inspection_table
```

Expected: pass.

## Task 3: Main Menu Reset Progress Button

**Files:**
- Modify: `godot/scenes/main_menu.tscn`
- Modify: `godot/scripts/main_menu.gd`
- Modify: `tests/test_godot_main_menu.py`

- [ ] **Step 1: Write failing tests**

Assert that the scene has:

```python
self.assertIn('[node name="ResetProgressButton" type="Button" parent="MenuPanel"]', scene)
self.assertIn('text = "Reset Progress"', scene)
```

Assert that the script has:

```python
self.assertIn("reset_progress_button", script)
self.assertIn("reset_progress_button.pressed.connect(_on_reset_progress_pressed)", script)
self.assertIn("GameState.reset_progress()", script)
self.assertIn('Localization.text("ui.reset_progress")', script)
```

- [ ] **Step 2: Run focused test**

Run:

```powershell
python -m unittest tests.test_godot_main_menu
```

Expected: fail because the reset button does not exist.

- [ ] **Step 3: Add button and handler**

Add `ResetProgressButton` between Start and Quit. Bind it in `main_menu.gd` and call `GameState.reset_progress()` before changing to the shop scene.

- [ ] **Step 4: Run focused test again**

Run:

```powershell
python -m unittest tests.test_godot_main_menu
```

Expected: pass.

## Task 4: Localization

**Files:**
- Modify: `godot/scripts/localization.gd`
- Modify: `tests/test_godot_localization.py`

- [ ] **Step 1: Write failing tests**

Require the new keys for `en` and `zh_TW`:

```python
for key in [
    "ui.reset_progress",
    "tutorial.inspect_magnifier",
    "tutorial.inspect_uv",
    "tutorial.inspect_temperature",
    "tutorial.choose_handling",
]:
    self.assertIn(f'"{key}"', self._locale_block(localization, "en"))
    self.assertIn(f'"{key}"', self._locale_block(localization, "zh_TW"))
```

- [ ] **Step 2: Run focused test**

Run:

```powershell
python -m unittest tests.test_godot_localization
```

Expected: fail because the new keys are missing.

- [ ] **Step 3: Add strings**

Add readable English strings to every locale table to preserve fallback-free key lookup. Add Traditional Chinese strings to `zh_TW`:

```gdscript
"ui.reset_progress": "Reset Progress",
"tutorial.inspect_magnifier": "Use the Magnifier to inspect close physical marks.",
"tutorial.inspect_uv": "Use the UV Lamp to check for hidden marks.",
"tutorial.inspect_temperature": "Use the Thermometer to record the temperature clue.",
"tutorial.choose_handling": "Review the notes, then choose Sell, Seal, or Discard.",
```

```gdscript
"ui.reset_progress": "重置進度",
"tutorial.inspect_magnifier": "先用放大鏡檢查近距離痕跡。",
"tutorial.inspect_uv": "再用 UV 燈確認是否有隱藏標記。",
"tutorial.inspect_temperature": "用溫度計記錄溫度線索。",
"tutorial.choose_handling": "看完筆記後，選擇出售、封存或丟棄。",
```

- [ ] **Step 4: Run focused test again**

Run:

```powershell
python -m unittest tests.test_godot_localization
```

Expected: pass.

## Task 5: Full Verification

**Files:**
- No new implementation files.

- [ ] **Step 1: Run full Python suite**

Run:

```powershell
python -m unittest discover -s tests
```

Expected: all tests pass.

- [ ] **Step 2: Run project dashboard**

Run:

```powershell
python -m tools.project_status --root . --run-tests
```

Expected: branch is `main`, tests pass, and asset outputs remain `40/40`.

- [ ] **Step 3: Check git state**

Run:

```powershell
git status --short
```

Expected: only the intended spec, plan, script, scene, and test changes are present.
