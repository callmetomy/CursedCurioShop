# Cursed Curio Shop GDD

## Document Status

- Status: MVP baseline
- Owner: project design
- Source documents:
  - `docs/design/game_direction.md`
  - `docs/production/mvp_backlog.md`
  - `data/items/item_schema.json`
  - `godot/README.md`

This document is the design authority for the playable MVP slice. When a later implementation choice conflicts with this document, update the GDD first or record the reason for the exception.

## High Concept

Cursed Curio Shop is a single-player first-person 3D appraisal game about running a late-night oddity shop. The player receives strange objects, inspects them with tools, chooses how to handle them, and deals with the consequences.

The player is not a combat hero. They are the last person willing to touch objects that should have stayed lost.

## Target Platform

- Primary platform: PC / Steam
- Engine: Godot 4.x
- Initial release target: playable Windows demo slice
- Business model assumption: paid game, with optional future DLC after the core loop proves strong

## Core Pillars

1. Object-first horror: cursed objects are the main characters.
2. Clear decisions: every oddity leads to a meaningful handling choice.
3. Small-shop pressure: cash, reputation, and stability pull against each other.
4. Inspectable details: clues should reward careful looking, not random guessing.
5. Scalable content: new oddities should be addable through structured data and repeatable asset processing.

## MVP Scope

The MVP is a three-day playable demo slice:

- One shop interior
- Ten oddities in structured data
- One fully integrated 3D oddity scene
- Three inspection tools
- Three in-game days
- One scripted abnormal event
- One bad ending
- Main menu
- Windows export

## Non-Goals For MVP

- Multiplayer
- Online economy
- Live in-game generative AI
- Large open world
- Complex human NPC relationships
- Mobile or console release
- Full procedural item generation inside the shipped build

## Player Experience

The intended session rhythm is tense, quiet, and procedural:

1. The player starts a day in the shop.
2. An oddity is presented for appraisal.
3. The player inspects it using available tools.
4. The player chooses Sell, Seal, or Discard.
5. The shop state changes based on the decision.
6. A wrong decision may trigger an abnormal event.
7. The player advances to the next day or reaches an ending.

The experience should feel like an appraisal desk with consequences, not an action game.

## Core Loop

```text
Receive oddity
-> Inspect visual and tool-based clues
-> Interpret risk and value
-> Choose handling action
-> Resolve cash, reputation, and event consequences
-> Advance day
```

The loop works only if clues are legible. The player should be able to explain why the correct handling was correct after seeing the outcome.

## Handling Actions

### Sell

The player accepts profit and transfers the object to a buyer. This is correct for safe or low-risk items, but dangerous for cursed items that should not leave the shop.

Expected effects:

- Increase cash.
- Risk reputation loss if the item harms the buyer.
- May trigger abnormal events for dangerous items.

### Seal

The player pays a cost to contain the object. This is correct for dangerous items that should not circulate.

Expected effects:

- Decrease cash by seal cost.
- Preserve or improve reputation when used correctly.
- Reduce abnormal event risk.

### Discard

The player removes the object without sale or proper containment. This should be a risky fallback, not a dominant strategy.

Expected effects:

- No sale profit.
- Possible reputation or stability penalty.
- May trigger events if the object resists disposal.

## Inspection Tools

### Magnifier

Purpose: reveals close physical details.

Examples:

- Hairline cracks
- Hidden engraving
- Tool marks
- Stains, dust, repairs, altered seams

Design requirement: magnifier clues should be visual and concrete.

### UV Lamp

Purpose: reveals marks invisible under normal light.

Examples:

- Glowing symbols
- Hidden signatures
- Fluids, residues, ritual markings
- False restorations

Design requirement: UV clues should create a clear before/after change.

### Thermometer

Purpose: exposes abnormal temperature.

Examples:

- Object reads below room temperature.
- Object reads unnaturally hot.
- Temperature fluctuates despite stable surroundings.

Design requirement: thermometer clues should return a readable numeric or categorical result.

## Oddity Design Rules

Each oddity should contain:

- A readable silhouette.
- One strong identifying material.
- One or more signs of age or use.
- One uncanny detail.
- Three appraisal clues when possible.
- One correct handling decision.
- One consequence for wrong handling.

Oddities should not rely on lore text alone. The model, texture, UI icon, and tool feedback should all support the same interpretation.

## Current MVP Oddities

The current structured item set is:

- `oddity_0001`: Whispering Teacup
- `oddity_0002`: Mirror Coin
- `oddity_0003`: Ashen Music Box
- `oddity_0004`: Cold Brass Key
- `oddity_0005`: Glass Eye
- `oddity_0006`: Black Wax Candle
- `oddity_0007`: Moth-Eaten Doll
- `oddity_0008`: Silver Funeral Bell
- `oddity_0009`: Cracked Hand Mirror
- `oddity_0010`: Red Thread Spool

All ten MVP oddities currently have Godot item scenes generated from structured data and processed local model assets. The three-day playable loop currently presents `oddity_0001`, `oddity_0002`, and `oddity_0003` as the daily queue. The remaining oddities are ready content reserves for future queue expansion, balance passes, and visual polish.

## Example Item Baseline

`oddity_0001`, the Whispering Teacup, defines the current integration standard:

- Visual identity: cracked white porcelain, dark tea stain, cold cursed presence.
- Magnifier clue: hairline cracks form a spiral.
- UV clue: a hidden ring-shaped mark glows blue near the rim.
- Thermometer clue: the cup reads below room temperature.
- Correct handling: Seal.
- Wrong handling: selling harms the buyer and damages shop reputation.

Future integrated oddities should reach at least this level of data completeness.

## Shop State

The MVP shop state tracks:

- Day
- Cash
- Reputation

Current prototype baseline:

- Starts on Day 1.
- Starts with Cash 100.
- Starts with Reputation 50.
- Advances through a three-day loop.

Future versions may add mental stability, customer trust, insurance, storage space, curse contamination, and shop upgrades. Those should not be added until the Sell / Seal / Discard loop is consistently readable.

## Events And Endings

The MVP includes:

- One scripted abnormal event.
- One bad ending path.

Event goals:

- Confirm that wrong handling has visible consequences.
- Break the static appraisal rhythm.
- Teach the player that decisions affect more than score.

Events should be short and tied to specific item logic. Avoid generic jump scares that could happen after any decision.

## UX Flow

Primary flow:

```text
Main Menu
-> Start Day
-> Shop Prototype
-> Inspection Table
-> Decision Result
-> Back To Shop / Next Day
-> Ending or loop continuation
```

The UI should stay functional and restrained. The player should spend most attention on the object, not on decorative interface frames.

## Visual Direction

The art direction should support late-night appraisal horror:

- Antique materials: porcelain, tarnished metal, stained wood, wax, old paper, worn cloth.
- Controlled lighting: warm shop lamps contrasted with cold cursed highlights.
- Practical surfaces: desk, shelves, drawers, labels, receipts, containment tools.
- Clear object readability: each oddity must remain identifiable in a screenshot.

Avoid overusing fog, heavy blur, dark silhouettes, or decorative noise if they make item inspection harder.

## UI Art Direction

UI should look like working shop equipment, not a fantasy HUD.

Recommended UI materials:

- Paper tags
- Ledger entries
- Brass labels
- Small tool icons
- Wax seal marks
- Receipt-like result panels

UI requirements:

- Tool states must be obvious.
- Sell, Seal, and Discard must remain visually distinct.
- Result screens must state the mechanical outcome clearly.
- Text must remain readable at desktop resolution.

## Texture And Material Direction

Generated or authored textures should prioritize:

- Base color clarity.
- Physical aging marks.
- Tool-readable clue details.
- Moderate roughness variation.
- Nonuniform stains, scratches, cracks, tarnish, and patina.

For curse markings:

- Keep symbols simple enough to read from inspection distance.
- Use UV or emissive variants only when gameplay needs them.
- Do not let decorative markings conflict with appraisal clues.

When creating precise model textures, use the model UV layout. Without a UV layout, generated images should be treated as material references, decals, icons, or tileable surfaces rather than final fitted textures.

## Audio Direction

MVP audio can remain minimal, but the target direction is:

- Quiet shop ambience.
- Small object handling sounds.
- Tool toggles with clear feedback.
- Subtle cursed object loops.
- Short event stingers tied to specific decisions.

Avoid constant loud ambience. Silence is part of the appraisal pressure.

## Content Pipeline

New oddity content should follow this path:

1. Create or update `data/items/<item_id>.json`.
2. Generate concept image.
3. Generate or author raw 3D model.
4. Process model through Blender automation.
5. Render review screenshots.
6. Approve or revise.
7. Create Godot item scene.
8. Connect item data to inspection and decision logic.

Generated assets are acceptable for production acceleration, but each oddity still requires human approval for readability and tone.

## Acceptance Criteria For A New Integrated Oddity

An oddity is integrated when:

- Its JSON data exists and follows the schema.
- Its processed model loads in Godot.
- It has a Godot item scene.
- It can be inspected at the table.
- At least two tool clues are visible or readable.
- A correct handling decision is defined.
- Wrong handling has a consequence.
- Review screenshots or notes exist.
- The item does not break Windows export.

## Release Slice Definition

The current playable slice is acceptable when:

- The game starts from the main menu.
- The player can enter the shop.
- The player can access the inspection table.
- The player can inspect the teacup with three tools.
- The player can Sell, Seal, or Discard.
- Correct and wrong decisions produce different outcomes.
- The abnormal event and bad ending path can be reached.
- Windows export succeeds.

## Open Design Questions

These are intentionally unresolved:

- Should each day contain one oddity or multiple oddities?
- Should cash or reputation be the primary fail condition?
- Should sealed items be stored and revisitable?
- Should customers be visible characters or represented through notes and calls?
- Should the full game use a fixed campaign, procedural daily queue, or hybrid structure?
- How much direct horror should happen inside the shop versus through aftermath reports?

Do not answer these prematurely in implementation. Prototype the appraisal loop first, then resolve these based on playtest evidence.
