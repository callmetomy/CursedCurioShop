# Second Oddity Batch Evaluation

Status: candidate gate
Updated: 2026-05-31

## Purpose

Evaluate a narrow second oddity batch before adding new playable days. This is a content design gate, not a runtime implementation pass.

Current decision: do not add these candidates to `GameState.DAILY_ITEM_IDS` yet. Promote only after the first candidate passes clue readability, wrong-outcome clarity, local model readability, and Traditional Chinese capture review.

## Batch Size

Limit the first second-batch slice to three candidates:

- `oddity_0011`
- `oddity_0012`
- `oddity_0013`

Do not add a fourth candidate until at least one of these three has a reviewed item JSON, generated or local prototype asset, Godot item scene, smoke coverage, and Traditional Chinese capture evidence.

## Candidate 1: oddity_0011 Cracked Apothecary Scale

Role: value ambiguity and false safety.

Correct handling: `seal`

Player-readable premise:

- A brass apothecary scale balances even when one pan is empty.
- The customer claims it belonged to a pharmacist who never miscounted a debt.
- The object looks commercially valuable, but the clues point to an active weighing curse.

Inspection clues:

- Magnifier: one pan has fine scratches shaped like tally marks, but the matching pan is smooth.
- UV lamp: old fingerprints appear under the empty pan, as if something invisible was weighed there.
- Thermometer: the empty pan is colder than the weighted pan.

Wrong outcomes:

- `sell`: buyer reports every purchase in their shop is undercounted by one coin; outcome should be `outcome.cursed_sale`.
- `discard`: the scale returns balanced with ash in one pan; outcome should be `outcome.uncontained_discard`.

Economy target:

- Sell value: medium-high, tempting but not run-breaking.
- Seal cost: medium, enough to create pressure after a low-cash route.

## Candidate 2: oddity_0012 Tarnished Mourning Locket

Role: emotional bait and correct sale.

Correct handling: `sell`

Player-readable premise:

- A mourning locket contains no portrait, only a clean oval of unfaded velvet.
- The customer wants it appraised quickly before a family dispute.
- The object is unsettling, but the clues indicate provenance rather than an active curse.

Inspection clues:

- Magnifier: the hinge wear is normal and the clasp has no fresh tool marks.
- UV lamp: initials appear inside the case and match a legitimate maker mark.
- Thermometer: the locket warms normally after being handled.

Wrong outcomes:

- `seal`: the legitimate buyer withdraws and rumors spread that the shop hides lawful heirlooms.
- `discard`: the family dispute escalates after the shop destroys the only provenance object.

Economy target:

- Sell value: high enough to reward recognizing a safe object.
- Seal cost: high enough that over-sealing is clearly harmful.

## Candidate 3: oddity_0013 Wax-Sealed Train Ticket

Role: discard/destroy-adjacent decision without adding a new verb.

Correct handling: `discard`

Player-readable premise:

- A century-old train ticket is sealed under black wax but still smells of coal smoke.
- The destination line is blank until the ticket is held under cold light.
- It should leave the shop, but not through sale or containment.

Inspection clues:

- Magnifier: the punched date repeats on the back in a different order.
- UV lamp: a destination appears only as a platform number, not a city.
- Thermometer: the wax gets warmer when the ticket points toward the door.

Wrong outcomes:

- `sell`: buyer hears a train approach every time they open a cash drawer.
- `seal`: the ticket sweats coal dust inside the case and contaminates nearby receipts.

Economy target:

- Sell value: medium, enough to tempt a sale.
- Seal cost: low-medium, so sealing feels plausible but still wrong.

## Gate Checklist

### Clue readability gate

- Each candidate has three inspection clues.
- At least one clue argues for the correct handling.
- At least one clue rules out the most tempting wrong handling.
- Risk hints must not directly name `sell`, `seal`, or `discard`.

### Wrong-outcome clarity gate

- Each wrong path has a consequence that explains why the decision was wrong.
- At least one candidate uses `outcome.cursed_sale`.
- At least one candidate uses `outcome.uncontained_discard`.
- No candidate triggers a bad ending in the first second-batch slice.

### Traditional Chinese capture gate

- The first promoted candidate needs a shop customer brief screenshot.
- The first promoted candidate needs a day-result screenshot for the correct path.
- The first promoted candidate needs a wrong-outcome screenshot for its most tempting wrong path.
- Capture evidence must include `1152x648` and `1280x720`.

## Recommendation

Promote `oddity_0011` first. It exercises the strongest commercial-game decision pattern: a valuable-looking object that should not be sold, with a non-ending wrong outcome that can reuse the existing result-detail and abnormal-event flows.

After `oddity_0011` passes its gate, decide whether to promote `oddity_0012` or `oddity_0013` based on which handling type is underrepresented in the expanded run.
