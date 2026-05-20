# Agent Roster

This project should stay small and role-driven. Add agents only when their work has a clear handoff and a measurable output.

## Current Recommended Team

### Owner / Creative Director

Human-owned role.

- Approves scope, tone, monetization, and final asset quality.
- Chooses whether to prioritize asset pipeline, gameplay prototype, or content.
- Makes final calls when cost, style, and schedule conflict.

### Tech Lead / Implementer

Primary Codex role.

- Builds and maintains the Python asset pipeline.
- Implements Godot prototype systems.
- Keeps tests passing and commits small, reviewable progress.
- Reports status using `python -m tools.project_status --root . --run-tests`.

### PM / Producer Agent

Recommended standing support role.

- Converts `docs/production/mvp_backlog.md` into weekly priorities.
- Tracks phase progress, blockers, risks, and next actions.
- Keeps scope focused on the MVP: asset factory first, gameplay prototype second.
- Produces a short status note after each milestone.

### Pipeline Agent

Use when asset generation work becomes parallel enough to split.

- Owns provider integrations such as Tripo or Meshy.
- Tracks manifests, downloaded assets, processing outputs, and review reports.
- Keeps generated private assets out of source control unless approved.

### Godot Gameplay Agent

Add after the asset factory can reliably produce at least one approved object.

- Owns first-person controller, pickup/rotation, inspection tools, and decision UI.
- Works inside `godot/` and coordinates data contracts with `data/items/`.
- Verifies scenes remain runnable after changes.

## Later Optional Roles

### QA Agent

- Runs repeatable checks after gameplay features land.
- Reports bugs with reproduction steps and affected files.
- Avoids changing code unless explicitly assigned a fix.

### Narrative / Content Agent

- Drafts oddities, clues, handling decisions, and consequences.
- Keeps object fantasy readable and aligned with `docs/design/game_direction.md`.
- Prepares batches for human approval before generation.

### Art Direction Agent

- Reviews generated concepts and models for style consistency.
- Flags assets that look off-genre, unreadable, or too costly to fix.
- Helps define repeatable prompt rules.

## Operating Rhythm

1. Run `python -m tools.project_status --root . --run-tests`.
2. PM / Producer Agent summarizes current state and proposes the next smallest milestone.
3. Owner approves the milestone.
4. Tech Lead / Implementer executes with tests and commits.
5. Pipeline, Gameplay, QA, or Content agents join only when their task can be scoped independently.

## Current Next Milestones

- Link the downloaded Tripo teacup model to `oddity_0001` or regenerate it with a stable item id.
- Add the first review report format for generated oddities.
- Build the Blender processing step for raw-to-processed model handoff.
- After one reviewed object is stable, start the Godot inspectable item prototype.
