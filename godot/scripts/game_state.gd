extends Node

const SHOP_LEDGER_TITLE := "Shop Ledger"
const DAILY_ITEM_IDS := ["oddity_0001", "oddity_0002", "oddity_0003"]
const DAILY_ITEM_SCENE_PATHS := {
	"oddity_0001": "res://scenes/items/oddity_0001.tscn",
	"oddity_0002": "res://scenes/items/oddity_0002.tscn",
	"oddity_0003": "res://scenes/items/oddity_0003.tscn",
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
		"risk_hint": "Risk hint: self-playing mechanism",
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
}

var current_day := 1
var max_days := 3
var cash := 100
var reputation := 50
var handled_reports := []


func start_new_run() -> void:
	current_day = 1
	cash = 100
	reputation = 50
	handled_reports.clear()


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
	return {
		"title": Localization.text("customer.%s.title" % item_id),
		"body": Localization.text("customer.%s.body" % item_id),
		"risk_hint": Localization.text("customer.%s.risk_hint" % item_id),
	}


func get_current_consequence_report(decision: String) -> String:
	var item_reports: Dictionary = DAILY_CONSEQUENCE_REPORTS.get(
		get_current_item_id(),
		DAILY_CONSEQUENCE_REPORTS["oddity_0001"]
	)
	var key := "consequence.%s.%s" % [get_current_item_id(), decision]
	var translated := Localization.text(key)
	if translated == key:
		return str(item_reports.get(decision, Localization.text("fallback.consequence")))
	return translated


func record_decision_result(item_id: String, decision: String, outcome: String, consequence_report: String) -> void:
	handled_reports.append({
		"item_id": item_id,
		"decision": decision,
		"outcome": outcome,
		"consequence_report": consequence_report,
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
			[strongest_report.get("consequence_report", Localization.text("ui.no_consequence"))]
		))
	return "\n".join(lines)


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
				report.get("item_id", "unknown"),
				report.get("decision", "unknown"),
			]
		))
	return "\n".join(lines)
