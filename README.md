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

Maintain a playable ten-day commercial demo slice:

1. Run the ten-day Sell / Seal / Discard loop from `oddity_0001` through `oddity_0010`.
2. Keep Traditional Chinese review screenshots current at `1152x648` and `1280x720`.
3. Verify the final-day shop progression upgrades: Ledger Desk and Containment Cabinet.
4. Refresh the local Windows export before each handoff.
5. Record playtest findings under `docs/production/playtests/`.

Do not commit API keys or downloaded private assets unless intentionally cleared for source control.

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
