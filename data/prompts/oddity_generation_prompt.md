# Oddity Generation Prompt

Use this prompt to create structured cursed object definitions.

```text
You are designing items for a first-person 3D oddity appraisal shop game.

Create one cursed object.

Constraints:
- The object must be possible to represent as a small 3D prop.
- Avoid human bodies, gore, text labels, logos, and copyrighted designs.
- The object should have 2-3 clear visual features.
- The appraisal should require observation, not random guessing.
- Tone: eerie, strange, restrained, suitable for a Steam indie horror game.

Return JSON with:
- id
- display_name
- rarity
- danger_level from 1 to 5
- visual_theme
- short_description
- concept_prompt
- model_prompt
- clues: tool, clue_result, meaning
- correct_handling: sell, return, seal, destroy
- wrong_handling_consequence
- base_value
```
