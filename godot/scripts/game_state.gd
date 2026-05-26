extends Node

const SHOP_LEDGER_TITLE := "Shop Ledger"
const LEDGER_DESK_UPGRADE_COST := 120
const CONTAINMENT_CABINET_UPGRADE_COST := 60
const CONTAINMENT_CABINET_SEAL_DISCOUNT := 5
const TOOL_MAGNIFIER := "magnifier"
const TOOL_UV_LAMP := "uv_lamp"
const TOOL_THERMOMETER := "thermometer"
const DAILY_ITEM_IDS := ["oddity_0001", "oddity_0002", "oddity_0003", "oddity_0004", "oddity_0005", "oddity_0006", "oddity_0007", "oddity_0008", "oddity_0009", "oddity_0010"]
const DAILY_ITEM_SCENE_PATHS := {
	"oddity_0001": "res://scenes/items/oddity_0001.tscn",
	"oddity_0002": "res://scenes/items/oddity_0002.tscn",
	"oddity_0003": "res://scenes/items/oddity_0003.tscn",
	"oddity_0004": "res://scenes/items/oddity_0004.tscn",
	"oddity_0005": "res://scenes/items/oddity_0005.tscn",
	"oddity_0006": "res://scenes/items/oddity_0006.tscn",
	"oddity_0007": "res://scenes/items/oddity_0007.tscn",
	"oddity_0008": "res://scenes/items/oddity_0008.tscn",
	"oddity_0009": "res://scenes/items/oddity_0009.tscn",
	"oddity_0010": "res://scenes/items/oddity_0010.tscn",
}
const DAILY_CUSTOMER_BRIEFS := {
	"oddity_0001": {
		"title": "Customer Note: Shivering Heiress",
		"body": "A wrapped teacup arrived before dawn. The courier refused to touch it twice.",
		"risk_hint": "Risk hint: cold transfer",
	},
	"oddity_0002": {
		"title": "Customer Note: Clockmaker",
		"body": "A coin was found in a locked till, reflecting a room that is not there.",
		"risk_hint": "Risk hint: delayed reflection",
	},
	"oddity_0003": {
		"title": "Customer Note: Estate Executor",
		"body": "This music box played during the inventory, though no key was wound.",
		"risk_hint": "Risk hint: intact case prolongs the tune",
	},
	"oddity_0004": {
		"title": "Customer Note: Night Porter",
		"body": "A brass key arrived from a locked cellar door, cold enough to numb the envelope.",
		"risk_hint": "Risk hint: remote lock movement",
	},
	"oddity_0005": {
		"title": "Customer Note: Retired Surgeon",
		"body": "A glass eye was found staring upward inside a sealed instrument case.",
		"risk_hint": "Risk hint: catalogued medical provenance, watchful surface",
	},
	"oddity_0006": {
		"title": "Customer Note: Chapel Caretaker",
		"body": "A black candle was found burning cold beside an unused chapel register.",
		"risk_hint": "Risk hint: heat rises after attention shifts",
	},
	"oddity_0007": {
		"title": "Customer Note: Boarding School Matron",
		"body": "A cloth doll was found in a dormitory trunk, wrapped in shed fabric scraps.",
		"risk_hint": "Risk hint: cold nursery trace, active stitching",
	},
	"oddity_0008": {
		"title": "Customer Note: Funeral Director",
		"body": "A silver bell was found inside a sealed coffin drawer that should have been empty.",
		"risk_hint": "Risk hint: muted clapper, active vibration",
	},
	"oddity_0009": {
		"title": "Customer Note: Theatre Widow",
		"body": "A cracked hand mirror was recovered from a dressing room that reflects applause after midnight.",
		"risk_hint": "Risk hint: covered glass holds the second face",
	},
	"oddity_0010": {
		"title": "Customer Note: Matchmaker",
		"body": "A spool of red thread was found tying two account books together after closing.",
		"risk_hint": "Risk hint: matched accounts, warm thread",
	},
}
const DAILY_CONSEQUENCE_REPORTS := {
	"oddity_0001": {
		"seal": "The customer leaves without the cup",
		"sell": "The buyer complains that frost crept across the receipt",
		"discard": "The discarded cup returns to the doorstep with fresh ice inside.",
	},
	"oddity_0002": {
		"seal": "The clockmaker accepts the sealed packet and stops hearing the delayed echo.",
		"sell": "The buyer pays quickly, but their reflection lags behind them at the door.",
		"discard": "The coin rolls back under the counter after the bell rings once.",
	},
	"oddity_0003": {
		"seal": "The estate executor notes that the tune finally stops in the hallway.",
		"sell": "The buyer reports music from an empty nursery after midnight.",
		"discard": "The music box is removed quietly",
	},
	"oddity_0004": {
		"seal": "The porter reports that the cellar door stays shut and the key stops frosting.",
		"sell": "The buyer says every lock in the house clicks open at 3:04.",
		"discard": "The key returns under the shop mat with a new layer of ice.",
	},
	"oddity_0005": {
		"seal": "The sealed case keeps tapping from the inside until the courier leaves.",
		"sell": "The buyer reports that the eye stays quiet once placed in a display case.",
		"discard": "The glass eye rolls back under the counter before closing time.",
	},
	"oddity_0006": {
		"seal": "The sealed candle stains the case with warm soot before quieting.",
		"sell": "The buyer says the candle lights itself whenever a name is spoken.",
		"discard": "The candle collapses into harmless wax after the wick is pinched out.",
	},
	"oddity_0007": {
		"seal": "The sealed doll stops shedding fabric after the latch is tied shut.",
		"sell": "The buyer reports loose threads spelling names across a nursery wall.",
		"discard": "The doll is found sitting upright in the waste bin after closing.",
	},
	"oddity_0008": {
		"seal": "The sealed bell gives one soft ring, then stays silent in the case.",
		"sell": "The buyer hears a funeral procession outside every locked window.",
		"discard": "The bell rings from the rubbish crate whenever the shop goes quiet.",
	},
	"oddity_0009": {
		"seal": "The sealed mirror fogs once, then the second face stays behind the glass.",
		"sell": "The buyer reports their reflection leaving the room before they do.",
		"discard": "The broken mirror scatters a second eye across every shard.",
	},
	"oddity_0010": {
		"seal": "The sealed spool keeps tying knots around the latch from inside the case.",
		"sell": "The buyer says the red thread quietly guides two lost letters together.",
		"discard": "The discarded thread knots around the waste bin and will not burn.",
	},
}
const WRONG_DECISION_OUTCOMES := {
	"default": {
		"sell": {"outcome_key": "outcome.bad_appraisal", "value_delta": 0, "reputation_delta": -10, "bad_ending": false},
		"seal": {"outcome_key": "outcome.bad_appraisal", "value_delta": -10, "reputation_delta": -8, "bad_ending": false},
		"discard": {"outcome_key": "outcome.uncontained_discard", "value_delta": 0, "reputation_delta": -8, "bad_ending": false},
	},
	"oddity_0001": {
		"sell": {"outcome_key": "outcome.cursed_sale", "value_delta": "sell_value", "reputation_delta": -15, "bad_ending": true},
		"discard": {"outcome_key": "outcome.uncontained_discard", "value_delta": 0, "reputation_delta": -8, "bad_ending": false},
	},
	"oddity_0002": {
		"sell": {"outcome_key": "outcome.bad_appraisal", "value_delta": 35, "reputation_delta": -12, "bad_ending": false},
		"discard": {"outcome_key": "outcome.uncontained_discard", "value_delta": -5, "reputation_delta": -7, "bad_ending": false},
	},
	"oddity_0003": {
		"seal": {"outcome_key": "outcome.bad_appraisal", "value_delta": -25, "reputation_delta": -10, "bad_ending": false},
		"sell": {"outcome_key": "outcome.bad_appraisal", "value_delta": 55, "reputation_delta": -16, "bad_ending": false},
	},
}

var current_day := 1
var max_days := 10
var cash := 100
var reputation := 50
var ledger_desk_upgraded := false
var containment_cabinet_upgraded := false
var onboarding_completed := false
var onboarding_tools_used := {
	TOOL_MAGNIFIER: false,
	TOOL_UV_LAMP: false,
	TOOL_THERMOMETER: false,
}
var handled_reports := []


func start_new_run() -> void:
	_reset_current_run_state()


func reset_progress() -> void:
	ledger_desk_upgraded = false
	containment_cabinet_upgraded = false
	onboarding_completed = false
	_reset_current_run_state()


func _reset_current_run_state() -> void:
	current_day = 1
	cash = 100
	reputation = 50
	handled_reports.clear()
	onboarding_tools_used[TOOL_MAGNIFIER] = false
	onboarding_tools_used[TOOL_UV_LAMP] = false
	onboarding_tools_used[TOOL_THERMOMETER] = false


func apply_result(value_delta: int, reputation_delta: int) -> void:
	cash += value_delta
	reputation += reputation_delta


func advance_day() -> void:
	if current_day < max_days:
		current_day += 1


func is_run_complete() -> bool:
	return current_day >= max_days


func get_current_item_id() -> String:
	var roster_index: int = clamp(current_day - 1, 0, DAILY_ITEM_IDS.size() - 1)
	return DAILY_ITEM_IDS[roster_index]


func get_current_item_scene_path() -> String:
	return DAILY_ITEM_SCENE_PATHS.get(get_current_item_id(), DAILY_ITEM_SCENE_PATHS["oddity_0001"])


func get_current_customer_brief() -> Dictionary:
	var item_id := get_current_item_id()
	var body := Localization.text("customer.%s.body" % item_id)
	if ledger_desk_upgraded:
		body = "%s\n%s" % [body, Localization.text("upgrade.ledger_desk.provenance")]
	return {
		"title": Localization.text("customer.%s.title" % item_id),
		"body": body,
		"risk_hint": Localization.text("customer.%s.risk_hint" % item_id),
	}


func can_purchase_ledger_desk_upgrade() -> bool:
	return not ledger_desk_upgraded and cash >= LEDGER_DESK_UPGRADE_COST


func purchase_ledger_desk_upgrade() -> bool:
	if not can_purchase_ledger_desk_upgrade():
		return false
	cash -= LEDGER_DESK_UPGRADE_COST
	ledger_desk_upgraded = true
	return true


func can_purchase_containment_cabinet_upgrade() -> bool:
	return not containment_cabinet_upgraded and cash >= CONTAINMENT_CABINET_UPGRADE_COST


func purchase_containment_cabinet_upgrade() -> bool:
	if not can_purchase_containment_cabinet_upgrade():
		return false
	cash -= CONTAINMENT_CABINET_UPGRADE_COST
	containment_cabinet_upgraded = true
	return true


func get_effective_seal_cost(base_cost: int) -> int:
	if containment_cabinet_upgraded:
		return max(5, base_cost - CONTAINMENT_CABINET_SEAL_DISCOUNT)
	return base_cost


func get_progression_status_text() -> String:
	var lines: Array[String] = []
	if ledger_desk_upgraded:
		lines.append(Localization.text("upgrade.ledger_desk.status_unlocked"))
	else:
		lines.append(Localization.format_text("upgrade.ledger_desk.status_locked", [LEDGER_DESK_UPGRADE_COST]))
	if containment_cabinet_upgraded:
		lines.append(Localization.text("upgrade.containment_cabinet.status_unlocked"))
	else:
		lines.append(Localization.format_text("upgrade.containment_cabinet.status_locked", [CONTAINMENT_CABINET_UPGRADE_COST, CONTAINMENT_CABINET_SEAL_DISCOUNT]))
	return "\n".join(lines)


func record_onboarding_tool_used(tool_name: String) -> void:
	if onboarding_completed:
		return
	if onboarding_tools_used.has(tool_name):
		onboarding_tools_used[tool_name] = true


func complete_onboarding() -> void:
	if not onboarding_completed and _all_onboarding_tools_used():
		onboarding_completed = true


func get_onboarding_hint_key() -> String:
	if onboarding_completed or current_day != 1:
		return ""
	if not onboarding_tools_used[TOOL_MAGNIFIER]:
		return "tutorial.inspect_magnifier"
	if not onboarding_tools_used[TOOL_UV_LAMP]:
		return "tutorial.inspect_uv"
	if not onboarding_tools_used[TOOL_THERMOMETER]:
		return "tutorial.inspect_temperature"
	return "tutorial.choose_handling"


func get_current_consequence_report(decision: String) -> String:
	var item_reports: Dictionary = DAILY_CONSEQUENCE_REPORTS.get(
		get_current_item_id(),
		DAILY_CONSEQUENCE_REPORTS["oddity_0001"]
	)
	var key := get_current_consequence_key(decision)
	var translated := Localization.text(key)
	if translated == key:
		return str(item_reports.get(decision, Localization.text("fallback.consequence")))
	return translated


func get_current_consequence_key(decision: String) -> String:
	return "consequence.%s.%s" % [get_current_item_id(), decision]


func get_current_wrong_decision_outcome(decision: String) -> Dictionary:
	var item_outcomes: Dictionary = WRONG_DECISION_OUTCOMES.get(get_current_item_id(), {})
	if item_outcomes.has(decision):
		return _duplicate_decision_outcome(item_outcomes[decision])
	var default_outcomes: Dictionary = WRONG_DECISION_OUTCOMES["default"]
	if default_outcomes.has(decision):
		return _duplicate_decision_outcome(default_outcomes[decision])
	return _duplicate_decision_outcome(default_outcomes["sell"])


func record_decision_result(
	item_id: String,
	decision: String,
	outcome_key: String,
	consequence_key: String,
	value_delta: int,
	reputation_delta: int
) -> void:
	handled_reports.append({
		"item_id": item_id,
		"decision": decision,
		"outcome_key": outcome_key,
		"consequence_key": consequence_key,
		"value_delta": value_delta,
		"reputation_delta": reputation_delta,
	})


func get_run_summary() -> String:
	var lines := [
		Localization.text("ui.run_summary"),
		Localization.format_text("ui.handled_count", [handled_reports.size(), max_days]),
		Localization.format_text("ui.final_cash", [cash]),
		Localization.format_text("ui.final_reputation", [reputation]),
	]
	if not handled_reports.is_empty():
		var strongest_report: Dictionary = handled_reports[handled_reports.size() - 1]
		lines.append(Localization.format_text(
			"ui.last_report",
			[_get_consequence_text(strongest_report)]
		))
	return "\n".join(lines)


func get_result_detail_count() -> int:
	return handled_reports.size()


func get_result_detail(index: int) -> Dictionary:
	if handled_reports.is_empty():
		return {
			"title": Localization.text("ui.result_detail_empty"),
			"body": Localization.text("ui.result_detail_empty"),
		}
	var safe_index: int = clamp(index, 0, handled_reports.size() - 1)
	var report: Dictionary = handled_reports[safe_index]
	var item_id := str(report.get("item_id", "unknown"))
	var decision := str(report.get("decision", "unknown"))
	var value_delta := int(report.get("value_delta", 0))
	var reputation_delta := int(report.get("reputation_delta", 0))
	var title := Localization.format_text("ui.result_detail_title", [safe_index + 1, handled_reports.size()])
	var body := Localization.format_text("ui.result_detail_body", [
		_get_item_display_name(item_id),
		_get_decision_label(decision),
		Localization.text(str(report.get("outcome_key", "outcome.bad_appraisal"))),
		value_delta,
		reputation_delta,
		_get_consequence_text(report),
	])
	return {
		"title": title,
		"body": body,
	}


func get_shop_ledger() -> String:
	if handled_reports.is_empty():
		return Localization.text("ui.no_appraisals")
	var lines: Array[String] = []
	for index in handled_reports.size():
		var report: Dictionary = handled_reports[index]
		lines.append(Localization.format_text(
			"ui.ledger_entry",
			[
				index + 1,
				_get_item_display_name(str(report.get("item_id", "unknown"))),
				_get_decision_label(str(report.get("decision", "unknown"))),
			]
		))
	return "\n".join(lines)


func _get_item_display_name(item_id: String) -> String:
	return Localization.item_text(item_id, "display_name", item_id)


func _get_decision_label(decision: String) -> String:
	return Localization.text("decision.%s" % decision)


func _duplicate_decision_outcome(outcome: Dictionary) -> Dictionary:
	return outcome.duplicate()


func _all_onboarding_tools_used() -> bool:
	return (
		onboarding_tools_used[TOOL_MAGNIFIER]
		and onboarding_tools_used[TOOL_UV_LAMP]
		and onboarding_tools_used[TOOL_THERMOMETER]
	)


func _get_consequence_text(report: Dictionary) -> String:
	var consequence_key := str(report.get("consequence_key", ""))
	var consequence_text := Localization.text(consequence_key)
	if consequence_text == consequence_key:
		return Localization.text("ui.no_consequence")
	return consequence_text
