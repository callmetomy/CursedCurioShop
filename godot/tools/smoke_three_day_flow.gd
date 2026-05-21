extends SceneTree

const EXPECTED_ITEMS := ["oddity_0001", "oddity_0002", "oddity_0003"]
const CORRECT_DECISIONS := ["seal", "seal", "discard"]


func _init() -> void:
	_run.call_deferred()


func _run() -> void:
	var game_state := _game_state()
	game_state.call("start_new_run")
	_assert(game_state.get("current_day") == 1, "New run should start on Day 1")
	_assert(game_state.get("cash") == 100, "New run should start with Cash 100")
	_assert(game_state.get("reputation") == 50, "New run should start with Reputation 50")

	_verify_wrong_teacup_sale_path()
	game_state.call("start_new_run")
	_verify_correct_three_day_flow()

	print("Three-day demo smoke flow passed")
	quit(0)


func _verify_wrong_teacup_sale_path() -> void:
	var table := await _instantiate_inspection_table()
	_assert(_current_item_id(table) == "oddity_0001", "Wrong-path check should start with teacup")

	table.call("_resolve_decision", "sell")
	await process_frame

	_assert(_node_visible(table, "HUD/AbnormalEventPanel"), "Wrong teacup sale should show abnormal event")
	_assert(_node_visible(table, "HUD/BadEndingPanel"), "Wrong teacup sale should show bad ending")
	_assert(_game_state().get("reputation") == 35, "Wrong teacup sale should reduce reputation by 15")
	table.queue_free()


func _verify_correct_three_day_flow() -> void:
	for day_index: int in EXPECTED_ITEMS.size():
		var table := await _instantiate_inspection_table()
		var expected_item_id: String = EXPECTED_ITEMS[day_index]
		var expected_decision: String = CORRECT_DECISIONS[day_index]

		_assert(_game_state().get("current_day") == day_index + 1, "Unexpected current day")
		_assert(_current_item_id(table) == expected_item_id, "Inspection table loaded the wrong oddity")
		_assert(_current_correct_handling(table) == expected_decision, "Oddity correct handling changed")
		_assert(_label_has_text(table, "HUD/ItemNameLabel"), "Inspection table should show item name")
		_assert(_label_has_text(table, "HUD/ItemDescriptionLabel"), "Inspection table should show item description")
		table.call("_on_magnifier_pressed")
		await process_frame
		_assert(
			_label_contains(table, "HUD/AppraisalNotesBackground/AppraisalNotesLabel", table.call("_get_current_tool_clue", "magnifier")),
			"Magnifier clue should persist in appraisal notes"
		)

		table.call("_resolve_decision", expected_decision)
		await process_frame
		_assert(_node_visible(table, "HUD/DayResultPanel"), "Correct decision should show day result")
		_assert(not _node_visible(table, "HUD/AbnormalEventPanel"), "Correct decision should not show abnormal event")

		if day_index < EXPECTED_ITEMS.size() - 1:
			table.call("_on_next_day_pressed")
			await process_frame
			_assert(_game_state().get("current_day") == day_index + 2, "Next Day should advance the run")
		else:
			var next_day_button := table.get_node("HUD/DayResultPanel/NextDayButton") as Button
			_assert(next_day_button.text == "Return to Menu", "Final day should return to menu")
		table.queue_free()


func _instantiate_inspection_table() -> Node:
	var packed := load("res://scenes/inspection_table.tscn") as PackedScene
	_assert(packed != null, "Could not load inspection table scene")

	var table := packed.instantiate()
	root.add_child(table)
	await process_frame

	_assert(table.get("current_item") != null, "Inspection table did not load an oddity")
	return table


func _game_state() -> Node:
	var node := root.get_node_or_null("GameState")
	if node != null:
		return node
	var script := load("res://scripts/game_state.gd") as Script
	_assert(script != null, "Could not load GameState script")
	node = Node.new()
	node.set_script(script)
	node.name = "GameState"
	root.add_child(node)
	return node


func _current_item_id(table: Node) -> String:
	var item := table.get("current_item") as Node
	if item == null:
		return ""
	var item_id: Variant = item.get("item_id")
	return item_id if item_id is String else ""


func _current_correct_handling(table: Node) -> String:
	var item := table.get("current_item") as Node
	if item == null:
		return ""
	var handling: Variant = item.get("correct_handling")
	return handling if handling is String else ""


func _node_visible(table: Node, node_path: NodePath) -> bool:
	var node := table.get_node(node_path) as CanvasItem
	return node != null and node.visible


func _label_has_text(table: Node, node_path: NodePath) -> bool:
	var label := table.get_node(node_path) as Label
	return label != null and not label.text.is_empty()


func _label_contains(table: Node, node_path: NodePath, expected_text: String) -> bool:
	var label := table.get_node(node_path) as Label
	return label != null and label.text.contains(expected_text)


func _assert(condition: bool, message: String) -> void:
	if condition:
		return
	push_error(message)
	quit(1)
