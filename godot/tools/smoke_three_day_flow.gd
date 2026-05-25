extends SceneTree

const EXPECTED_ITEMS := ["oddity_0001", "oddity_0002", "oddity_0003", "oddity_0004"]
const CORRECT_DECISIONS := ["seal", "seal", "discard", "seal"]


func _init() -> void:
	_run.call_deferred()


func _run() -> void:
	var game_state := _game_state()
	game_state.call("start_new_run")
	_assert(game_state.get("current_day") == 1, "New run should start on Day 1")
	_assert(game_state.get("cash") == 100, "New run should start with Cash 100")
	_assert(game_state.get("reputation") == 50, "New run should start with Reputation 50")

	await _verify_shop_customer_brief()
	await _verify_wrong_teacup_sale_path()
	game_state.call("start_new_run")
	await _verify_correct_three_day_flow()

	print("Four-day demo smoke flow passed")
	quit(0)


func _verify_shop_customer_brief() -> void:
	var packed := load("res://scenes/shop_prototype.tscn") as PackedScene
	_assert(packed != null, "Could not load shop prototype scene")

	var shop := packed.instantiate()
	root.add_child(shop)
	await process_frame

	_assert(_label_contains(shop, "HUD/CustomerBriefPanel/CustomerBriefContent/CustomerBriefTitle", "顧客備註"), "Shop should show the localized customer brief title")
	_assert(_label_contains(shop, "HUD/CustomerBriefPanel/CustomerBriefContent/CustomerBriefBody", "茶杯"), "Shop should show the localized current customer brief body")
	_assert(_label_contains(shop, "HUD/CustomerBriefPanel/CustomerBriefContent/CustomerRiskHint", "風險提示"), "Shop should show the localized risk hint")
	root.remove_child(shop)
	shop.free()


func _verify_wrong_teacup_sale_path() -> void:
	var table := await _instantiate_inspection_table()
	_assert(_current_item_id(table) == "oddity_0001", "Wrong-path check should start with teacup")

	table.call("_resolve_decision", "sell")
	await process_frame

	_assert(not _node_visible(table, "HUD/AbnormalEventPanel"), "Bad ending should hide the separate abnormal event panel")
	_assert(not _node_visible(table, "HUD/DayResultPanel"), "Bad ending should hide the normal day result panel")
	_assert(not _node_visible(table, "HUD/BackToShopButton"), "Bad ending should hide Back to Shop")
	_assert(not _node_visible(table, "HUD/ToolPanel"), "Bad ending should hide inspection tools")
	_assert(not _node_visible(table, "HUD/DecisionPanel"), "Bad ending should hide decision buttons")
	_assert(not _node_visible(table, "HUD/AppraisalNotesBackground"), "Bad ending should hide appraisal notes")
	_assert(_node_visible(table, "HUD/BadEndingBackground"), "Wrong teacup sale should show bad ending background")
	_assert(_node_visible(table, "HUD/BadEndingCard"), "Wrong teacup sale should show bad ending card")
	_assert(_node_visible(table, "HUD/BadEndingCard/BadEndingPanel"), "Wrong teacup sale should show bad ending content")
	_assert(_label_contains(table, "HUD/BadEndingCard/BadEndingPanel/EndingBody", "最終聲望：35"), "Bad ending should show localized final reputation")
	_assert(_game_state().get("reputation") == 35, "Wrong teacup sale should reduce reputation by 15")

	table.call("_resolve_decision", "discard")
	await process_frame
	_assert(not _node_visible(table, "HUD/AbnormalEventPanel"), "Bad ending should block later decisions")
	_assert(not _node_visible(table, "HUD/DayResultPanel"), "Bad ending should keep the normal result panel hidden")
	_assert(_game_state().get("reputation") == 35, "Later decisions should not change bad ending state")
	table.queue_free()
	await process_frame


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
		var magnifier_clue: String = table.call("_get_current_tool_clue", "magnifier")
		_assert(
			_label_contains(table, "HUD/AppraisalNotesBackground/AppraisalNotesLabel", magnifier_clue.substr(0, 12)),
			"Magnifier clue should persist in appraisal notes"
		)

		table.call("_resolve_decision", expected_decision)
		await process_frame
		_assert(_node_visible(table, "HUD/DayResultPanel"), "Correct decision should show day result")
		_assert(_label_has_text(table, "HUD/DayResultPanel/ResultTextPanel/ResultTextContent/ConsequenceReportLabel"), "Decision result should show a consequence report")
		_assert(not _node_visible(table, "HUD/AbnormalEventPanel"), "Correct decision should not show abnormal event")
		_assert(not _node_visible(table, "HUD/AppraisalNotesBackground"), "Day result should hide appraisal notes")
		_assert(not _node_visible(table, "HUD/DecisionPanel"), "Day result should hide decision buttons")
		_assert(not _node_visible(table, "HUD/ToolPanel"), "Day result should hide tool buttons")

		if day_index < EXPECTED_ITEMS.size() - 1:
			table.call("_on_next_day_pressed")
			await process_frame
			_assert(_game_state().get("current_day") == day_index + 2, "Next Day should advance the run")
			await _verify_shop_ledger_after_decision(day_index + 1)
		else:
			var next_day_button := table.get_node("HUD/DayResultPanel/ResultButtonPanel/NextDayButton") as Button
			_assert(next_day_button.text == "返回選單", "Final day should return to menu")
			_assert(_node_visible(table, "HUD/DayResultPanel/ResultTextPanel/ResultTextContent/RunSummaryLabel"), "Final day should show the run summary")
			_assert(not _node_visible(table, "HUD/DayResultPanel/ResultTextPanel/ResultTextContent/ConsequenceReportLabel"), "Final day should hide duplicate consequence report")
			_assert(_label_contains(table, "HUD/DayResultPanel/ResultTextPanel/ResultTextContent/RunSummaryLabel", "最終現金"), "Run summary should show localized final cash")
			_assert(_label_contains(table, "HUD/DayResultPanel/ResultTextPanel/ResultTextContent/RunSummaryLabel", "最終聲望"), "Run summary should show localized final reputation")
		table.queue_free()
		await process_frame


func _verify_shop_ledger_after_decision(day_number: int) -> void:
	var packed := load("res://scenes/shop_prototype.tscn") as PackedScene
	_assert(packed != null, "Could not load shop prototype scene for ledger check")

	var shop := packed.instantiate()
	root.add_child(shop)
	await process_frame

	_assert(_label_contains(shop, "HUD/ShopLedgerPanel/ShopLedgerContent/ShopLedgerTitle", "店鋪帳本"), "Shop ledger should show a localized title")
	_assert(
		_label_contains(shop, "HUD/ShopLedgerPanel/ShopLedgerContent/ShopLedgerBody", "第 %d 天" % day_number),
		"Shop ledger should show the localized completed day"
	)
	_assert(_node_visible(shop, "HUD/ResultDetailPanel"), "Shop should show result detail panel after a completed appraisal")
	_assert(
		_label_contains(shop, "HUD/ResultDetailPanel/ResultDetailContent/ResultDetailBody", "決策"),
		"Shop result detail should show the localized decision label"
	)
	_assert(
		_label_contains(shop, "HUD/ResultDetailPanel/ResultDetailContent/ResultDetailBody", "後果"),
		"Shop result detail should show the localized consequence label"
	)
	root.remove_child(shop)
	shop.free()


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
