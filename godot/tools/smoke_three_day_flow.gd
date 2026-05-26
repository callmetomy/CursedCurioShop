extends SceneTree

const EXPECTED_ITEMS := ["oddity_0001", "oddity_0002", "oddity_0003", "oddity_0004", "oddity_0005", "oddity_0006", "oddity_0007", "oddity_0008", "oddity_0009", "oddity_0010"]
const CORRECT_DECISIONS := ["seal", "seal", "discard", "seal", "sell", "discard", "seal", "seal", "seal", "sell"]


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
	await _verify_item_specific_wrong_outcome()
	game_state.call("start_new_run")
	await _verify_late_game_wrong_outcomes()
	game_state.call("start_new_run")
	await _verify_correct_demo_flow()

	print("Ten-day demo smoke flow passed")
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


func _verify_item_specific_wrong_outcome() -> void:
	var game_state := _game_state()
	game_state.set("current_day", 2)
	var table := await _instantiate_inspection_table()
	_assert(_current_item_id(table) == "oddity_0002", "Item-specific wrong outcome check should load the mirror coin")

	table.call("_resolve_decision", "sell")
	await process_frame

	_assert(_node_visible(table, "HUD/DayResultPanel"), "Item-specific wrong sale should show the day result panel")
	_assert(_node_visible(table, "HUD/AbnormalEventPanel"), "Item-specific wrong sale should show an abnormal event")
	_assert(not _node_visible(table, "HUD/BadEndingCard"), "Item-specific wrong sale should not trigger the bad ending")
	_assert(int(game_state.get("cash")) == 135, "Day 2 wrong sale should use item-specific cash delta")
	_assert(int(game_state.get("reputation")) == 38, "Day 2 wrong sale should use item-specific reputation delta")
	table.queue_free()
	await process_frame


func _verify_late_game_wrong_outcomes() -> void:
	var game_state := _game_state()
	game_state.set("current_day", 8)
	var bell_table := await _instantiate_inspection_table()
	_assert(_current_item_id(bell_table) == "oddity_0008", "Late-game wrong outcome check should load the funeral bell")
	bell_table.call("_resolve_decision", "sell")
	await process_frame
	_assert(_node_visible(bell_table, "HUD/DayResultPanel"), "Day 8 wrong sale should show the day result panel")
	_assert(_node_visible(bell_table, "HUD/AbnormalEventPanel"), "Day 8 wrong sale should show an abnormal event")
	_assert(not _node_visible(bell_table, "HUD/BadEndingCard"), "Day 8 wrong sale should not trigger the bad ending")
	_assert(int(game_state.get("cash")) == 145, "Day 8 wrong sale should use late-game cash delta")
	_assert(int(game_state.get("reputation")) == 36, "Day 8 wrong sale should use late-game reputation delta")
	var bell_detail: Dictionary = game_state.call("get_result_detail", 0)
	_assert(
		str(bell_detail.get("body", "")).contains(_localized("outcome_note.oddity_0008.sell")),
		"Day 8 wrong sale result detail should explain the mistake"
	)
	bell_table.queue_free()
	await process_frame

	game_state.call("start_new_run")
	game_state.set("current_day", 10)
	var thread_table := await _instantiate_inspection_table()
	_assert(_current_item_id(thread_table) == "oddity_0010", "Late-game wrong outcome check should load the red thread spool")
	thread_table.call("_resolve_decision", "discard")
	await process_frame
	_assert(_node_visible(thread_table, "HUD/DayResultPanel"), "Day 10 wrong discard should show the day result panel")
	_assert(_node_visible(thread_table, "HUD/AbnormalEventPanel"), "Day 10 wrong discard should show an abnormal event")
	_assert(not _node_visible(thread_table, "HUD/BadEndingCard"), "Day 10 wrong discard should not trigger the bad ending")
	_assert(int(game_state.get("cash")) == 85, "Day 10 wrong discard should use late-game cash delta")
	_assert(int(game_state.get("reputation")) == 38, "Day 10 wrong discard should use late-game reputation delta")
	thread_table.queue_free()
	await process_frame


func _verify_correct_demo_flow() -> void:
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
		var pressure_key := str(_game_state().call("get_daily_pressure_key", int(_game_state().get("reputation"))))
		_assert(
			_label_contains(table, "HUD/DayResultPanel/ResultTextPanel/ResultTextContent/PressureSummaryLabel", _localized(pressure_key)),
			"Day result should show post-decision pressure summary"
		)
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
			_assert(_node_visible(table, "HUD/DayResultPanel/ProgressionPanel"), "Final day should show the progression panel")
			var final_cash := int(_game_state().get("cash"))
			_assert(bool(_game_state().call("can_purchase_ledger_desk_upgrade")), "Final cash should afford the ledger desk upgrade")
			table.call("_on_buy_ledger_desk_pressed")
			await process_frame
			_assert(bool(_game_state().get("ledger_desk_upgraded")), "Ledger desk upgrade should be purchased")
			_assert(int(_game_state().get("cash")) == final_cash - 120, "Ledger desk upgrade should deduct cash")
			_assert(bool(_game_state().call("can_purchase_containment_cabinet_upgrade")), "Remaining cash should afford the containment cabinet upgrade")
			table.call("_on_buy_containment_cabinet_pressed")
			await process_frame
			_assert(bool(_game_state().get("containment_cabinet_upgraded")), "Containment cabinet upgrade should be purchased")
			_assert(int(_game_state().get("cash")) == final_cash - 180, "Both shop upgrades should deduct cash")
			_assert(
				_label_contains(table, "HUD/DayResultPanel/ProgressionPanel/ProgressionContent/ProgressionStatusLabel", _localized("upgrade.ledger_desk.status_unlocked")),
				"Progression panel should show the upgraded ledger desk status"
			)
			_assert(
				_label_contains(table, "HUD/DayResultPanel/ProgressionPanel/ProgressionContent/ProgressionStatusLabel", _localized("upgrade.containment_cabinet.status_unlocked")),
				"Progression panel should show the upgraded containment cabinet status"
			)
		table.queue_free()
		await process_frame
	_game_state().call("start_new_run")
	await _verify_upgraded_customer_brief()
	await _verify_discounted_seal_cost()
	await _verify_upgraded_second_run_economy()


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
	_assert(
		_label_contains(shop, "HUD/ResultDetailPanel/ResultDetailContent/ResultDetailBody", "壓力"),
		"Shop result detail should show the post-decision pressure summary"
	)
	root.remove_child(shop)
	shop.free()


func _verify_upgraded_customer_brief() -> void:
	var packed := load("res://scenes/shop_prototype.tscn") as PackedScene
	_assert(packed != null, "Could not load shop prototype scene for upgraded customer brief check")

	var shop := packed.instantiate()
	root.add_child(shop)
	await process_frame

	_assert(
		_label_contains(shop, "HUD/CustomerBriefPanel/CustomerBriefContent/CustomerBriefBody", _localized("upgrade.ledger_desk.provenance")),
		"Upgraded ledger desk should add provenance notes to customer briefs"
	)
	_assert(
		_label_contains(shop, "HUD/ShopLedgerPanel/ShopLedgerContent/ProgressionStatus", _localized("upgrade.ledger_desk.status_unlocked")),
		"Shop ledger should show upgraded progression status"
	)
	root.remove_child(shop)
	shop.free()


func _verify_discounted_seal_cost() -> void:
	var table := await _instantiate_inspection_table()
	_assert(int(table.call("_get_current_seal_cost")) == 20, "Containment cabinet should discount the Day 1 seal cost")
	table.queue_free()
	await process_frame


func _verify_upgraded_second_run_economy() -> void:
	var game_state := _game_state()
	game_state.call("start_new_run")
	_assert(bool(game_state.get("ledger_desk_upgraded")), "Ledger desk should persist into the upgraded second run")
	_assert(bool(game_state.get("containment_cabinet_upgraded")), "Containment cabinet should persist into the upgraded second run")
	var lowest_cash := int(game_state.get("cash"))

	for day_index: int in EXPECTED_ITEMS.size():
		var table := await _instantiate_inspection_table()
		var expected_item_id: String = EXPECTED_ITEMS[day_index]
		var expected_decision: String = CORRECT_DECISIONS[day_index]

		_assert(game_state.get("current_day") == day_index + 1, "Upgraded second run should progress through all demo days")
		_assert(_current_item_id(table) == expected_item_id, "Upgraded second run loaded the wrong oddity")
		_assert(_current_correct_handling(table) == expected_decision, "Upgraded second run correct handling changed")

		table.call("_resolve_decision", expected_decision)
		await process_frame
		lowest_cash = min(lowest_cash, int(game_state.get("cash")))

		if day_index < EXPECTED_ITEMS.size() - 1:
			table.call("_on_next_day_pressed")
			await process_frame
			_assert(game_state.get("current_day") == day_index + 2, "Upgraded second run should advance to the next day")

		table.queue_free()
		await process_frame

	_assert(int(game_state.get("cash")) == 210, "Upgraded second run should finish with discounted final cash")
	_assert(int(game_state.get("reputation")) == 100, "Upgraded second run should finish with perfect reputation")
	_assert(lowest_cash >= 35, "Upgraded second run should keep enough cash buffer")


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


func _localized(key: String) -> String:
	var node := root.get_node_or_null("Localization")
	_assert(node != null, "Localization autoload is not available")
	return str(node.call("text", key))


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
