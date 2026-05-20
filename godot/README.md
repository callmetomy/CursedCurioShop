# Godot Project

This folder contains the Godot 4.x project for Cursed Curio Shop.

## Model Viewer

The main scene is `res://scenes/model_viewer.tscn`.

It loads the tracked asset pipeline model from:

```text
../assets/models_raw/oddity_0001.glb
```

That path points outside the Godot project folder and into the repository-level asset pipeline output. The GLB is intentionally ignored by git, while its generation history is tracked in `../data/manifests/oddity_0001_manifest.json`.

Use this scene for a first manual quality check before creating processed models, collision, review screenshots, or item scenes.
