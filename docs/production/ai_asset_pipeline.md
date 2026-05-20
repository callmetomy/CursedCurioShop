# AI Asset Pipeline

## Goal

Create a repeatable pipeline that lets a solo developer generate, review, and import game-ready oddity assets without manual 3D art skills.

## Pipeline Stages

1. Item brief generation
   - Input: theme, rarity, danger level, target visual style.
   - Output: structured item definition in `data/items/`.

2. Concept image generation
   - Input: item visual prompt.
   - Output: front-facing concept image in `assets/concepts/`.

3. Meshy 3D generation
   - Input: concept image or text prompt.
   - Output: raw `.glb` or `.fbx` in `assets/models_raw/`.

4. Blender processing
   - Normalize scale.
   - Set origin.
   - Reduce polygon count where practical.
   - Rename materials.
   - Generate simple collision mesh.
   - Export processed `.glb` to `assets/models_processed/`.

5. Godot import
   - Create an item scene.
   - Attach collision and metadata.
   - Connect item definition to gameplay systems.

6. Review render
   - Render four standard angles.
   - Create a review report in `assets/review/`.
   - Human decision: approve, regenerate, or reject.

## Quality Gates

An asset is accepted only if:

- The silhouette is readable from two meters away.
- It has no obvious broken mesh holes in normal gameplay view.
- It fits the shop scale after normalization.
- It matches the intended style closely enough.
- It can be inspected without confusing collision.
- Its generated text, icon, and gameplay metadata agree with the model.

## Cost Control

- Generate batches of 10-30 items.
- Keep only approved outputs.
- Prefer Image-to-3D for important hero objects.
- Use Text-to-3D for filler props and background clutter.
- Track every generation attempt in a manifest before scaling production.
