extends Node

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
