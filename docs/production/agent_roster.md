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

- Done: Started the first post-MVP customer presentation slice with daily customer notes in the shop HUD.
- Done: Added lightweight consequence reports after each decision, so the loop has narrative feedback without requiring visible customer characters yet.
- Done: Added a compact end-of-run summary that lists handled oddity count, final cash, final reputation, and the last consequence report.
- Done: Added a simple run ledger in the shop scene after returning from each day, so the player can review prior decisions before continuing.
- Done: Added a small risk hint to the customer note panel so each day has a clearer player hypothesis before inspection.
- Done: Improved 1152x648 HUD safe areas by moving appraisal notes away from centered readouts and giving the shop ledger/customer panels more vertical room.
- Done: Refreshed the local Windows export after the HUD safe-area pass.
- Done: Added a Godot localization layer for `en`, `ja`, `ko`, `es`, `pt`, `ru`, `zh_CN`, and `zh_TW`; review builds now default to Traditional Chinese for visible demo UI and item information.
- Done: Tightened the final-day result panel so the run summary fits inside the ledger frame and duplicate consequence text is hidden on the final day.
- Done: Split result panel text and button areas with a semi-transparent text plate, reducing overlap risk in the Traditional Chinese review layout.
- Done: Captured and recorded a Traditional Chinese visual pass at `1152x648` and `1280x720`.
- Done: Added a reviewable result-detail panel in the shop so players can inspect each handled oddity's decision, outcome, cash delta, reputation delta, and consequence.
- Done: Promoted `oddity_0004` into the playable schedule as a four-day loop and reran the Traditional Chinese visual pass.
- Done: Promoted `oddity_0005` into the playable schedule as a five-day loop and reran the core smoke checks.
- Done: Promoted `oddity_0006` into the playable schedule as a six-day loop and reran the core smoke checks.
- Done: Promoted `oddity_0007` into the playable schedule as a seven-day loop and reran the core smoke checks.
- Done: Promoted `oddity_0008` into the playable schedule as an eight-day loop and reran the core smoke checks.
- Done: Promoted `oddity_0009` into the playable schedule as a nine-day loop and reran the core smoke checks.
- Done: Promoted `oddity_0010` into the playable schedule as a ten-day loop and reran the core smoke and visual checks.
- Done: Applied the first commercial-demo readability tuning pass: unique item clues, non-answer risk hints, and varied sell/seal/discard economy across the ten-day loop.
- Done: Ran the internal ten-day balance pass, fixed the correct-route cash dip, and recorded the balance report in `docs/production/playtests/2026-05-25-ten-day-balance-pass.md`.
- Done: Refreshed the local Windows export after the ten-day balance pass.
- Done: Added the first shop progression slice: the Ledger Desk upgrade spends post-run cash, persists into the next run, and adds provenance notes to customer briefs.
- Done: Ran 3 agent players for the ten-day blind-test pass, then tuned Day 3, Day 4, and Day 9 readability.
- Done: Added the second shop progression slice: Containment Cabinet spends post-run cash, persists into future runs, and reduces each future Seal cost by 5.
- Done: Added upgraded second-run smoke validation for Final Cash 210, Final Reputation 100, and minimum cash buffer 35.
- Done: Ran 3 agent players on the final progression panel and clarified upgrade copy for "each Seal" and future-run persistence.
- Done: Refreshed Traditional Chinese screenshots and the local Windows export after the progression copy pass.
- Done: Preserved the owner-approved demo baseline in git as `a666a95` and tagged it as `demo-owner-review-2026-05-26`.
- Done: Started Steam store prep with `docs/production/steam_store_prep.md` and full-release gap tracking with `docs/production/full_release_roadmap.md`.
- Done: Owner direction on 2026-05-31 is to ignore Steam store work and real-player playtest for now, then continue product-body work.
- Done: Added a low-volume looping shop ambience cue to the shop prototype, with tests covering the scene node, loop startup, and local WAV asset.
- Done: Improved UI transition/state clarity by adding post-appraisal shop prompt text and day-result next-step guidance, with runtime smoke coverage for both.
- Done: Added distinct brass hover and pressed button feedback across the main menu, inspection tools, decision buttons, upgrade buttons, and result navigation.
- Done: Added a lightweight scene transition overlay for shop-to-inspection, inspection-to-shop, and return-to-menu navigation, with smoke cleanup updated to avoid resource leaks.
- Done: Refined the scene transition overlay so it starts transparent and applies the blackout alpha from script before scene changes.
- Done: Started Phase C content expansion with a second bad-ending branch: selling the Ashen Music Box now triggers a localized Empty Nursery Tune ending.
- Done: Ran the focused 1152x648 and 1280x720 HUD safe-area visual pass, fixed the final-summary return button clipping, and recorded evidence in `docs/production/playtests/2026-05-31-hud-safe-area-pass.md`.
- Next recommended slice: continue Phase C with another small wrong-outcome or ending branch before adding a new oddity batch.
