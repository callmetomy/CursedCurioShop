# Godot Project

This folder contains the Godot 4.x project for Cursed Curio Shop.

## Main Menu

The main scene is `res://scenes/main_menu.tscn`.

Use `Start Day` to enter the first-person shop prototype.

Starting a day resets the current prototype run to Day 1, Cash 100, Reputation 50.

Runtime text is routed through `res://scripts/localization.gd`. The current playable demo supports:

```text
en, ja, ko, es, pt, ru, zh_CN, zh_TW
```

The default locale is `zh_TW`, so local review builds show Traditional Chinese UI, item information, customer notes, consequence reports, and run summaries unless the locale is changed in code.

The local MVP UI and material asset pack is generated under:

```text
res://assets/ui/
res://assets/textures/
```

## Inspection Table

The inspection scene is `res://scenes/inspection_table.tscn`.

It loads the current day's oddity scene through `GameState`:

```text
Day 1: res://scenes/items/oddity_0001.tscn
Day 2: res://scenes/items/oddity_0002.tscn
Day 3: res://scenes/items/oddity_0003.tscn
```

All ten MVP oddity scenes can be regenerated from `data/items/*.json` with:

```powershell
python -m tools.godot.sync_item_scenes --root .
```

Drag with the left mouse button to rotate the item. Use the mouse wheel to adjust inspection distance. Press `1` or click `Magnifier` to toggle the close inspection tool. Press `2` or click `UV Lamp` to dim the room light and reveal UV-only markings. Press `3` or click `Thermometer` to show the object's temperature clue.

Use `Sell`, `Seal`, or `Discard` to resolve the current appraisal. The first oddity's correct handling is `Seal`. After a decision, the day result panel shows the outcome, cash change, and reputation change.

Wrong decisions trigger a scripted abnormal event. Selling the teacup triggers the current bad ending path.

Decision results now include a short customer or consequence report. This keeps the appraisal loop connected to the shop fiction instead of only showing score deltas.

On the final day, the result panel also shows a compact run summary with handled oddity count, final cash, final reputation, and the last consequence report.

## Shop Prototype

The first-person shop prototype is `res://scenes/shop_prototype.tscn`.

Use WASD to move, mouse look to turn, and `E` to enter the inspection table from the shop floor. Use `Back to Shop` from the inspection table to return.

The shop HUD shows Day, Cash, and Reputation from the shared `GameState` autoload. `Next Day` advances the run until the three-day prototype loop completes.

The shop HUD also shows the current day's customer note and risk hint before inspection. Together with the decision consequence reports and final run summary, this is the first post-MVP customer presentation slice: it gives the oddity a source and pressure context without adding character models or new asset dependencies.

After each completed appraisal, the shop HUD ledger lists prior day decisions and a result-detail panel lets the player review the selected oddity, decision, outcome, cash change, reputation change, and consequence before entering the next inspection.

## Windows Export

The export preset is `Windows Desktop`, configured to write:

```text
../exports/windows/CursedCurioShop.exe
```

Godot export currently requires the matching Godot 4.6.2 mono export templates at:

```text
C:/Users/user/AppData/Roaming/Godot/export_templates/4.6.2.stable.mono/
```

The latest verified local export wrote:

```text
../exports/windows/CursedCurioShop.exe
```

The latest local export was refreshed after the Traditional Chinese result-detail review panel pass on 2026-05-25.

## Visual Review Capture

Use the Traditional Chinese visual capture script after HUD layout changes:

```powershell
godot --path godot --script res://tools/capture_traditional_chinese_review.gd
```

This must run without `--headless`; the headless renderer cannot provide viewport screenshots. The script writes review PNGs to:

```text
../docs/production/playtests/screenshots/
```

## Model Viewer

The standalone model viewer is `res://scenes/model_viewer.tscn`.

It loads the tracked asset pipeline model from:

```text
res://assets/models_processed/oddity_0001.glb
```

That path points to the Godot-local copy of the processed model so exported builds can load it. The generation history is tracked in `../data/manifests/oddity_0001_manifest.json`.

Use this scene for a manual quality check after Blender processing and before creating collision, review screenshots, or item scenes.

## Item Scene

The first tracked item scene is:

```text
res://scenes/items/oddity_0001.tscn
```

It loads the same processed GLB, stores the item metadata needed by gameplay, and fits a simple box collision shape to the imported model at runtime.
