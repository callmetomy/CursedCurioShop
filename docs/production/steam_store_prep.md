# Steam Store Prep

Status: first prep pass
Updated: 2026-05-26
Baseline build: `demo-owner-review-2026-05-26`

## Goal

Prepare `Cursed Curio Shop` for a Steam Coming Soon / demo-facing store page without over-promising full-release scope.

This document is based on the current owner-approved ten-day demo baseline and Steamworks documentation checked on 2026-05-26.

## Current Store Positioning

**One-line pitch:** Run a late-night oddity shop, inspect cursed objects, and decide whether each one should be sold, sealed, or destroyed.

**Primary audience:**

- Players who like quiet horror, object stories, and deduction.
- Players who enjoy shop-management pressure without action combat.
- Players who enjoy compact indie demos with readable systems and replayable decision pressure.

**Avoid positioning as:**

- Action horror.
- Open-world exploration.
- Online / live-service game.
- Full procedural generation game.
- Casino, gambling, or online entertainment product.

## Steam Store Copy Draft

### Short Description

Run a late-night oddity shop in this first-person appraisal horror game. Inspect cursed objects with practical tools, read the clues, and choose whether to sell, seal, or discard each item before the shop pays the price.

### About This Game

`Cursed Curio Shop` is a single-player first-person appraisal game about handling objects that should have stayed lost.

Each day, a strange item arrives at your shop. You inspect it with tools, read the customer notes, and decide what to do with it:

- **Sell** it for cash and risk what happens to the buyer.
- **Seal** it at your own expense before it can spread harm.
- **Discard** it when keeping the object intact is the real danger.

The current demo focuses on a ten-day run of cursed objects, cash pressure, reputation, and shop upgrades that persist into future runs.

### Key Features

- Inspect ten cursed oddities across a playable demo run.
- Use a magnifier, UV lamp, and thermometer to uncover object-specific clues.
- Make clear handling decisions: Sell, Seal, or Discard.
- Track cash and reputation as each choice changes the shop.
- Unlock shop upgrades such as the Ledger Desk and Containment Cabinet.
- Experience restrained object-first horror without combat or jump-scare dependency.
- Built for PC / Steam as a paid single-player game, with optional future DLC only after the core loop is proven.

### Mature Content / Tone Note

The game contains supernatural horror themes, implied harm from cursed objects, unsettling object descriptions, and bad-ending text. It does not currently include gore, explicit sexual content, real-money gambling, or online wagering mechanics.

## Tags Draft

Primary tags to test:

- Horror
- Simulation
- Investigation
- Mystery
- First-Person
- Singleplayer
- Atmospheric
- Management
- Supernatural
- Choices Matter
- Puzzle
- Dark
- Narrative
- Indie

Tag risks:

- Avoid `Action Horror` unless future builds add action pressure.
- Avoid `Roguelike` unless the run structure becomes meaningfully replay-randomized.
- Avoid `Procedural Generation` unless shipped content actually uses it in-game.

## Languages Draft

Current visible demo localization includes:

- English
- Japanese
- Korean
- Spanish
- Portuguese
- Russian
- Simplified Chinese
- Traditional Chinese

Store-page recommendation:

- List English and Traditional Chinese as primary supported store languages first.
- Treat other runtime languages as provisional until a full translation QA pass is completed.

## Steam Asset Requirements

Official Steamworks graphical asset requirements checked on 2026-05-26:

| Asset | Required | Size | Current Status |
| --- | --- | ---: | --- |
| Header Capsule | Yes | 920 x 430 | Missing |
| Small Capsule | Yes | 462 x 174 | Missing |
| Main Capsule | Yes | 1232 x 706 | Missing |
| Vertical Capsule | Yes | 748 x 896 | Missing |
| Screenshots | Yes | 1920 x 1080 or larger, 16:9 | Missing; current review screenshots are 1152x648 and 1280x720 |
| Page Background | Optional | 1438 x 810 | Missing |
| Shortcut Icon | Yes | 256 x 256 .ico or .png | Missing |
| App Icon | Yes | 184 x 184 .jpg | Missing |
| Library Capsule | Yes | 600 x 900 | Missing |
| Library Hero | Yes | 3840 x 1240 .png | Missing |
| Library Logo | Yes | 1280 wide and/or 720 tall .png | Missing |
| Library Header Capsule | Yes | 920 x 430 | Missing |

Steam capsule rule reminder:

- Base capsule artwork should contain game artwork, the game name, and official subtitle only.
- Do not include review quotes, discounts, awards, release timing, calls to action, or unrelated marketing text in base capsule assets.

## Current Visual Evidence

Existing screenshots under `docs/production/playtests/screenshots/`:

- `shop_customer_brief-1152x648.png`
- `shop_customer_brief-1280x720.png`
- `day_result-1152x648.png`
- `day_result-1280x720.png`
- `shop_result_detail-1152x648.png`
- `shop_result_detail-1280x720.png`
- `final_summary-1152x648.png`
- `final_summary-1280x720.png`

These are useful for internal review but are below Steam's current required screenshot minimum. Next Steam prep slice should capture 1920x1080 screenshots from the current baseline.

## Screenshot Shot List

Capture at 1920x1080, 16:9:

1. Main menu with shop mood and title.
2. Customer brief panel before inspection.
3. Inspection table with object and tools visible.
4. Magnifier clue moment.
5. UV clue moment.
6. Decision panel with Sell / Seal / Discard.
7. Result panel showing cash / reputation consequence.
8. Shop ledger / result detail view.
9. Final summary with Ledger Desk and Containment Cabinet upgrades.
10. Bad ending card.

Screenshot rules:

- No debug overlays.
- No cropped text.
- No text overlap.
- Prefer readable object and UI over dark mood.
- Use Traditional Chinese screenshots for internal owner review, but Steam public screenshots should be English first unless store language strategy changes.

## Trailer Beat Sheet

Target length: 45-75 seconds.

1. Shop exterior / main menu mood.
2. A cursed object arrives.
3. Inspect with magnifier, UV lamp, thermometer.
4. Read conflicting clues.
5. Choose Sell / Seal / Discard.
6. Show cash / reputation consequence.
7. Show an abnormal event or bad-ending hint.
8. End on the hook: the shop remembers what you choose.

Do not show:

- Placeholder file paths.
- Internal test UI.
- Claims about full campaign length that are not implemented.
- Steam UI mockups.

## Store Page Readiness Checklist

- [x] Owner-approved demo baseline committed and tagged.
- [x] Windows owner review build packaged.
- [x] Initial Steam positioning drafted.
- [x] Short description drafted.
- [x] About This Game drafted.
- [x] Tags drafted.
- [ ] Steam 1920x1080 screenshots captured.
- [ ] Capsule key art direction chosen.
- [ ] Header / small / main / vertical capsules generated.
- [ ] Library assets generated.
- [ ] Trailer captured and edited.
- [ ] English store screenshot pass verified.
- [ ] Traditional Chinese store copy prepared.
- [ ] AI asset disclosure / credits policy drafted.
- [ ] Steamworks app checklist filled in.

## Sources

- Steamworks Graphical Assets Overview: https://partner.steamgames.com/doc/store/assets
- Steamworks Store Page Description: https://partner.steamgames.com/doc/store/page/description
- Steamworks Store Page Building and Editing: https://partner.steamgames.com/doc/store/page
