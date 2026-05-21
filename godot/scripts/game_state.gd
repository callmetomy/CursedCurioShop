extends Node

const DAILY_ITEM_IDS := ["oddity_0001", "oddity_0002", "oddity_0003"]
const DAILY_ITEM_SCENE_PATHS := {
	"oddity_0001": "res://scenes/items/oddity_0001.tscn",
	"oddity_0002": "res://scenes/items/oddity_0002.tscn",
	"oddity_0003": "res://scenes/items/oddity_0003.tscn",
}

var current_day := 1
var max_days := 3
var cash := 100
var reputation := 50


func start_new_run() -> void:
	current_day = 1
	cash = 100
	reputation = 50


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
