# Full Release Roadmap

Status: planning baseline
Updated: 2026-05-26

## Current Completion Estimate

| Target | Estimate | Meaning |
| --- | ---: | --- |
| Owner review demo | 90-95% | Playable ten-day baseline is preserved, tested, packaged, and owner-approved. |
| Steam Coming Soon page | 55-65% | Store positioning exists after the first prep pass, but public-ready assets are missing. |
| Paid full release | 25-35% | Core loop works, but content volume, polish, release systems, and commercial QA are incomplete. |

## Completion Model

The paid-release estimate is weighted by what a player expects from a commercial Steam game, not by code volume.

| Area | Weight | Current | Notes |
| --- | ---: | ---: | --- |
| Core loop and mechanics | 20% | 16% | Sell / Seal / Discard loop works; needs onboarding and more replay support. |
| Content volume | 20% | 5% | Ten oddities are a demo slice, not full paid-game depth. |
| Progression and retention | 15% | 5% | Two upgrades exist; broader run structure and longer-term goals are still light. |
| Presentation and UX polish | 15% | 5% | Functional and readable, but still prototype-level in settings, audio, UI polish, and transitions. |
| Store / marketing readiness | 10% | 4% | Store copy drafted; public assets, trailer, and capsules missing. |
| QA / release engineering | 10% | 5% | Good automated baseline, but release-candidate QA and Steam build workflow missing. |
| Legal / platform / business setup | 10% | 2% | AI asset disclosure, credits, pricing, Steam app setup, and policy checks still needed. |

Approximate total: 42/100 for commercial direction maturity, but 25-35% for full paid release because content volume and public polish are the gating risks.

## Phase A: Steam Store Readiness

Goal: make the game credible enough for a Steam Coming Soon page.

- Capture 1920x1080 English screenshots from the owner-approved baseline.
- Generate Steam capsule concepts.
- Produce required store and library graphical assets.
- Draft English and Traditional Chinese store copy.
- Draft AI asset disclosure and credits policy.
- Prepare trailer beat sheet and capture list.

Exit criteria:

- Steam page can be filled without placeholders.
- Store promise does not exceed the implemented demo.
- Public screenshots are readable and representative.

## Phase B: Productization Polish

Goal: move from prototype-feeling demo to paid-game-feeling demo.

- Add settings menu: language, fullscreen/windowed, master volume, text speed if needed.
- Add first-run onboarding without explaining answers.
- Add save / reset behavior for upgrades and run state.
- Improve audio: shop ambience, tool toggles, decision results, abnormal event cues.
- Polish UI transitions and state clarity.
- Verify 1920x1080, 1280x720, and common windowed resolutions.

Exit criteria:

- A new player understands controls and loop within the first two minutes.
- No required action depends on prior project knowledge.
- Settings and state behavior are predictable.

## Phase C: Content Expansion

Goal: increase paid-game content depth without breaking the appraisal loop.

- Decide full-game structure: fixed campaign, run-based loop, or hybrid.
- Add a second batch of oddities.
- Add more abnormal events tied to item logic.
- Add more consequences and endings.
- Add more shop upgrades only after the progression model is clear.
- Add review gates for each oddity: clue readability, model readability, consequence clarity.

Exit criteria:

- Content supports a paid-game session length target.
- More content increases decision variety instead of just item count.

## Phase D: Commercial Release Candidate

Goal: prepare for Steam review and public demo/release.

- Create Steamworks app build pipeline.
- Prepare depot / branch structure.
- Run clean-machine install test.
- Run release-candidate checklist.
- Finalize pricing, launch timing, and language support claim.
- Prepare press kit and trailer.

Exit criteria:

- Build can be installed outside the dev repo.
- Store page and build match each other.
- Known risks are documented and intentionally accepted.

## Immediate Next Slice

Owner direction on 2026-05-31: skip Steam store readiness and real-player playtest for now, then continue product-body work.

Recommended next implementation task:

1. Continue Phase B productization polish.
2. Tighten scene transition readability and HUD safe areas across the shop, inspection table, day result, and return-to-shop loop.
3. Keep the work scoped to current content; do not add another perk or new oddity batch in this pass.

Reason:

- Settings, onboarding, reset behavior, and first audio cues are already present in the current local build.
- Shop ambience has been added as the next small audio polish slice.
- Post-appraisal shop prompt text and day-result next-step guidance are now covered by tests and the Godot smoke flow.
- Distinct hover and pressed button states now cover the main menu, inspection, decision, upgrade, and result navigation buttons.
- Scene transition readability and final safe-area polish remain the next low-risk Phase B items before content expansion.
