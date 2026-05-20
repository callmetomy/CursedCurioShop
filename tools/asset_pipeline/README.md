# Asset Pipeline Tools

This folder will hold scripts that automate AI generation and asset processing.

Planned scripts:

- `generate_item_briefs` - create structured oddity JSON.
- `generate_concepts` - call an image API and save concept art.
- `generate_meshy_models` - call Meshy and download raw models.
- `process_models_blender` - run Blender cleanup in batch mode.
- `build_review_sheet` - render review screenshots and status pages.

Scripts should read secrets from `.env` and should not print API keys.

## Current Script

`generate_sample_item.py` creates one local item definition and one manifest file without calling paid APIs.

```powershell
python -m tools.asset_pipeline.generate_sample_item --root . --item-id oddity_0001 --name "Whispering Teacup"
```

`tripo_smoke_test.py` verifies the Tripo provider. By default it only previews the payload.

```powershell
python -m tools.asset_pipeline.tripo_smoke_test --root .
python -m tools.asset_pipeline.tripo_smoke_test --root . --submit
```

`generate_tripo_model.py` uses an item's `generation.model_prompt`, submits it to Tripo when requested, and downloads the finished model to the item's tracked raw model path.

```powershell
python -m tools.asset_pipeline.generate_tripo_model --root . --item-id oddity_0001
python -m tools.asset_pipeline.generate_tripo_model --root . --item-id oddity_0001 --submit --wait --download
```

`process_model_blender.py` runs Blender in background mode to normalize a tracked raw GLB and export the processed GLB.

```powershell
python -m tools.asset_pipeline.process_model_blender --root . --item-id oddity_0001 --dry-run
python -m tools.asset_pipeline.process_model_blender --root . --item-id oddity_0001
```

It finds Blender from `--blender`, `BLENDER_PATH`, `PATH`, or common Windows install paths.

`render_review_blender.py` renders four standard PNG review angles from the processed GLB.

```powershell
python -m tools.asset_pipeline.render_review_blender --root . --item-id oddity_0001 --dry-run
python -m tools.asset_pipeline.render_review_blender --root . --item-id oddity_0001
```

`generate_local_oddities.py` creates the local prototype roster metadata, concept placeholders, reviews, and manifests for `oddity_0002` through `oddity_0010`.

```powershell
python -m tools.asset_pipeline.generate_local_oddities --root .
```

Generate their local procedural GLBs through Blender:

```powershell
blender --background --factory-startup --python tools/asset_pipeline/blender_generate_local_oddities.py -- --root .
```

`status.py` reports which generated outputs exist for an item.

```powershell
python -m tools.asset_pipeline.status --root . --item-id oddity_0001
python -m tools.asset_pipeline.status --root . --item-id oddity_0001 --json
```
