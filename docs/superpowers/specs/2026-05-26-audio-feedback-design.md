# Audio Feedback Design

Status: approved for implementation
Date: 2026-05-26
Owner direction: continue improving game completeness before Steam store preparation.

## Goal

Add small, readable sound feedback to the appraisal loop so tool usage, decisions, abnormal events, and bad endings feel more responsive. This pass should make the existing Master Volume setting meaningful without adding full music or an external audio pipeline.

## Scope

Add short local WAV cues for:

- tool activation,
- correct decision result,
- wrong decision result,
- abnormal event,
- bad ending.

The sounds should be generated locally and stored under `godot/assets/audio/`. They should be intentionally simple placeholders that are safe to replace later.

## Behavior

- Activating a real inspection tool plays the tool cue.
- Turning tools off does not play a cue.
- Correct handling plays the correct decision cue.
- Wrong handling plays the wrong decision cue.
- Showing an abnormal event plays the abnormal event cue.
- Showing the bad ending plays the bad ending cue.
- All cues use Godot `AudioStreamPlayer` nodes so the existing Master Volume slider affects them through the Master bus.

## Non-Goals

- No background music.
- No adaptive music system.
- No paid or external generated audio.
- No save system for per-sound volume.
- No Steam or trailer audio work.

## Testing

Required verification:

- Text tests proving the inspection scene has audio resources and `AudioStreamPlayer` nodes.
- Text tests proving `inspection_table.gd` plays the right cue from tool, decision, abnormal event, and bad ending paths.
- Full Python test suite.
- Godot ten-day smoke flow.
- Project dashboard.

## Success Criteria

- The current ten-day demo still passes automated smoke.
- Tool and decision actions have audio hooks.
- Wrong handling and bad ending have separate audio hooks.
- Master Volume has real gameplay sounds to control.
