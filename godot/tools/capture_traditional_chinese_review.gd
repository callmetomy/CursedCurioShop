extends SceneTree

const OUTPUT_DIR := "res://../docs/production/playtests/screenshots"
const VIEWPORTS := [
	{"name": "1152x648", "size": Vector2i(1152, 648)},
	{"name": "1280x720", "size": Vector2i(1280, 720)},
]


func _init() -> void:
	_run.call_deferred()


func _run() -> void:
	_localization().call("set_locale", "zh_TW")
	_prepare_output_dir()
	for viewport: Dictionary in VIEWPORTS:
		root.size = viewport["size"]
		await process_frame
		await _capture_shop_customer_brief(viewport["name"])
		await _capture_shop_result_detail(viewport["name"])
		await _capture_day_result(viewport["name"])
		await _capture_final_summary(viewport["name"])
	print("Traditional Chinese review screenshots captured")
	quit(0)


func _capture_shop_customer_brief(viewport_name: String) -> void:
	_clear_runtime_scenes()
	_game_state().call("start_new_run")
	var shop := _instantiate_scene("res://scenes/shop_prototype.tscn")
	await _settle_frames()
	await _save_screenshot("shop_customer_brief", viewport_name)
	root.remove_child(shop)
	shop.free()


func _capture_shop_result_detail(viewport_name: String) -> void:
	_clear_runtime_scenes()
	var game_state := _game_state()
	game_state.call("start_new_run")
	await _resolve_and_close_day("seal")
	game_state.call("advance_day")
	var shop := _instantiate_scene("res://scenes/shop_prototype.tscn")
	await _settle_frames()
	await _save_screenshot("shop_result_detail", viewport_name)
	root.remove_child(shop)
	shop.free()


func _capture_day_result(viewport_name: String) -> void:
	_clear_runtime_scenes()
	_game_state().call("start_new_run")
	var table := _instantiate_scene("res://scenes/inspection_table.tscn")
	await _settle_frames()
	table.call("_resolve_decision", "seal")
	await _settle_frames()
	await _save_screenshot("day_result", viewport_name)
	root.remove_child(table)
	table.free()


func _capture_final_summary(viewport_name: String) -> void:
	_clear_runtime_scenes()
	var game_state := _game_state()
	game_state.call("start_new_run")
	await _resolve_and_close_day("seal")
	game_state.call("advance_day")
	await _resolve_and_close_day("seal")
	game_state.call("advance_day")
	await _resolve_and_close_day("discard")
	game_state.call("advance_day")
	await _resolve_and_close_day("seal")
	game_state.call("advance_day")
	await _resolve_and_close_day("sell")
	game_state.call("advance_day")
	await _resolve_and_close_day("discard")
	game_state.call("advance_day")
	await _resolve_and_close_day("seal")
	game_state.call("advance_day")
	await _resolve_and_close_day("seal")
	game_state.call("advance_day")
	await _resolve_and_close_day("seal")
	game_state.call("advance_day")
	var table := _instantiate_scene("res://scenes/inspection_table.tscn")
	await _settle_frames()
	table.call("_resolve_decision", "sell")
	await _settle_frames()
	await _save_screenshot("final_summary", viewport_name)
	root.remove_child(table)
	table.free()


func _resolve_and_close_day(decision: String) -> void:
	var table := _instantiate_scene("res://scenes/inspection_table.tscn")
	await _settle_frames()
	table.call("_resolve_decision", decision)
	await _settle_frames()
	root.remove_child(table)
	table.free()
	await process_frame


func _instantiate_scene(scene_path: String) -> Node:
	var packed := load(scene_path) as PackedScene
	_assert(packed != null, "Could not load %s" % scene_path)
	var instance := packed.instantiate()
	root.add_child(instance)
	return instance


func _save_screenshot(state_name: String, viewport_name: String) -> void:
	await process_frame
	await process_frame
	var texture := root.get_texture()
	_assert(texture != null, "Viewport texture unavailable. Run without --headless.")
	var image := texture.get_image()
	_assert(image != null, "Viewport image unavailable. Run without --headless.")
	var output_path := "%s/%s-%s.png" % [
		ProjectSettings.globalize_path(OUTPUT_DIR),
		state_name,
		viewport_name,
	]
	var err := image.save_png(output_path)
	_assert(err == OK, "Could not write screenshot %s" % output_path)


func _prepare_output_dir() -> void:
	var err := DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUTPUT_DIR))
	_assert(err == OK, "Could not create screenshot output directory")


func _clear_runtime_scenes() -> void:
	for child: Node in root.get_children():
		if child.name in ["GameState", "Localization"]:
			continue
		root.remove_child(child)
		child.free()


func _settle_frames() -> void:
	await process_frame
	await process_frame


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


func _localization() -> Node:
	var node := root.get_node_or_null("Localization")
	if node != null:
		return node
	var script := load("res://scripts/localization.gd") as Script
	_assert(script != null, "Could not load Localization script")
	node = Node.new()
	node.set_script(script)
	node.name = "Localization"
	root.add_child(node)
	return node


func _assert(condition: bool, message: String) -> void:
	if condition:
		return
	push_error(message)
	quit(1)
