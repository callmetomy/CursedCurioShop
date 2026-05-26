# Cursed Curio Shop

Single-player 3D oddity appraisal shop game prototype built with Godot and an AI-assisted asset pipeline.

## Current Direction

- Platform: PC / Steam first
- Engine: Godot
- Business model: paid game, optional future DLC
- Production style: AI-generated concepts, 3D props, text drafts, and audio drafts with human approval
- Core loop: receive cursed objects, inspect clues, choose a handling decision, survive consequences, upgrade the shop
- Design baseline: `docs/design/gdd.md`

## Workspace Layout

- `docs/` - design, production, and marketing documents
- `tools/` - automation scripts for AI generation, asset processing, and Godot import
- `godot/` - Godot project files
- `assets/concepts/` - generated concept images
- `assets/models_raw/` - raw AI-generated 3D model downloads
- `assets/models_processed/` - cleaned and Godot-ready models
- `assets/audio/` - generated or sourced audio
- `assets/review/` - approval screenshots and review reports
- `assets/steam/` - Steam capsule, key art, and trailer materials
- `data/items/` - item definitions and gameplay metadata
- `data/prompts/` - reusable prompts for generation
- `exports/` - local builds
- `scripts/` - project utility scripts

## Near-Term Goal

Move the owner-approved ten-day demo baseline toward Steam store readiness:

1. Preserve the tagged baseline `demo-owner-review-2026-05-26`.
2. Prepare Steam store copy, screenshots, capsule requirements, and trailer planning.
3. Capture Steam-ready `1920x1080` screenshots from the current baseline.
4. Keep release scope honest: do not add another perk or oddity batch before store readiness work is complete.
5. Track full-release gaps in `docs/production/full_release_roadmap.md`.

Do not commit API keys or downloaded private assets unless intentionally cleared for source control.

Key production docs:

- `docs/production/full_release_roadmap.md`
- `docs/production/steam_store_prep.md`
- `docs/production/2026-05-26-demo-baseline-decision.md`
- `docs/production/2026-05-26-demo-release-audit.md`

## Local Commands

Print the current project dashboard:

```powershell
python -m tools.project_status --root . --run-tests
```

Use JSON output for automation or agent handoff:

```powershell
python -m tools.project_status --root . --run-tests --json
```

Run tests:

```powershell
python -m unittest discover -s tests
```

Run the Godot ten-day smoke flow:

```powershell
godot --headless --path godot --script res://tools/smoke_three_day_flow.gd
```

Capture Traditional Chinese review screenshots:

```powershell
godot --path godot --script res://tools/capture_traditional_chinese_review.gd
```

Steam store prep starts with:

```powershell
Get-Content docs/production/steam_store_prep.md
```

Refresh the local Windows export:

```powershell
godot --headless --path godot --export-release "Windows Desktop" ..\exports\windows\CursedCurioShop.exe
```

Create a sample oddity definition without calling paid APIs:

```powershell
python -m tools.asset_pipeline.generate_sample_item --root . --item-id oddity_0001 --name "Whispering Teacup"
```

The sample command writes:

- `data/items/oddity_0001.json`
- `data/manifests/oddity_0001_manifest.json`

Preview the Tripo text-to-3D API payload without spending credits:

```powershell
python -m tools.asset_pipeline.tripo_smoke_test --root .
```

Preview the tracked Tripo payload for a real oddity without spending credits:

```powershell
python -m tools.asset_pipeline.generate_tripo_model --root . --item-id oddity_0001
```

Check which outputs exist for an oddity:

```powershell
python -m tools.asset_pipeline.status --root . --item-id oddity_0001
```

Generate the local MVP UI and material asset pack:

```powershell
python -m tools.art.generate_mvp_visual_assets --root .
```

Sync item JSON and processed models into Godot runtime item scenes:

```powershell
python -m tools.godot.sync_item_scenes --root .
```

Submit one Tripo text-to-3D smoke test:

```powershell
python -m tools.asset_pipeline.tripo_smoke_test --root . --submit
```

Free Tripo Studio generations may not include OpenAPI credits. If the command returns `not enough credit`, the integration is reaching Tripo correctly, but the account needs API credits before generation can run.

Poll and download an existing task if it is finished:

```powershell
python -m tools.asset_pipeline.tripo_smoke_test --root . --task-id YOUR_TASK_ID --download
```

Submit, wait, and download a tracked oddity model after approving credit usage:

```powershell
python -m tools.asset_pipeline.generate_tripo_model --root . --item-id oddity_0001 --submit --wait --download
```
