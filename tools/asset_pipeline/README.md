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

`status.py` reports which generated outputs exist for an item.

```powershell
python -m tools.asset_pipeline.status --root . --item-id oddity_0001
python -m tools.asset_pipeline.status --root . --item-id oddity_0001 --json
```
