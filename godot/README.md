# Godot Project

This folder contains the Godot 4.x project for Cursed Curio Shop.

## Main Menu

The main scene is `res://scenes/main_menu.tscn`.

Use `Start Day` to enter the first-person shop prototype.

Starting a day resets the current prototype run to Day 1, Cash 100, Reputation 50.

## Inspection Table

The inspection scene is `res://scenes/inspection_table.tscn`.

It instances the first tracked oddity scene:

```text
res://scenes/items/oddity_0001.tscn
```

Drag with the left mouse button to rotate the item. Use the mouse wheel to adjust inspection distance. Press `1` or click `Magnifier` to toggle the close inspection tool. Press `2` or click `UV Lamp` to dim the room light and reveal UV-only markings. Press `3` or click `Thermometer` to show the object's temperature clue.

Use `Sell`, `Seal`, or `Discard` to resolve the current appraisal. The first oddity's correct handling is `Seal`. After a decision, the day result panel shows the outcome, cash change, and reputation change.

Wrong decisions trigger a scripted abnormal event. Selling the teacup triggers the current bad ending path.

## Shop Prototype

The first-person shop prototype is `res://scenes/shop_prototype.tscn`.

Use WASD to move, mouse look to turn, and `E` to enter the inspection table from the shop floor. Use `Back to Shop` from the inspection table to return.

The shop HUD shows Day, Cash, and Reputation from the shared `GameState` autoload. `Next Day` advances the run until the three-day prototype loop completes.

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
