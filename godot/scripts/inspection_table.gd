extends Node3D

@onready var item_pivot: Node3D = $ItemPivot
@onready var camera: Camera3D = $InspectionCamera
@onready var key_light: SpotLight3D = $KeyLight
@onready var magnifier_button: Button = $HUD/ToolPanel/MagnifierButton
@onready var uv_lamp_button: Button = $HUD/ToolPanel/UVLampButton
@onready var thermometer_button: Button = $HUD/ToolPanel/ThermometerButton
@onready var thermometer_readout: Label = $HUD/ThermometerReadout
@onready var tool_clue_readout: Label = $HUD/ToolClueReadout
@onready var sell_button: Button = $HUD/DecisionPanel/SellButton
@onready var seal_button: Button = $HUD/DecisionPanel/SealButton
@onready var discard_button: Button = $HUD/DecisionPanel/DiscardButton
@onready var decision_result: Label = $HUD/DecisionResult
@onready var day_result_panel: VBoxContainer = $HUD/DayResultPanel
@onready var day_result_background: TextureRect = $HUD/DayResultBackground
@onready var outcome_label: Label = $HUD/DayResultPanel/OutcomeLabel
@onready var value_label: Label = $HUD/DayResultPanel/ValueLabel
@onready var reputation_label: Label = $HUD/DayResultPanel/ReputationLabel
@onready var next_day_button: Button = $HUD/DayResultPanel/NextDayButton
@onready var back_to_shop_button: Button = $HUD/BackToShopButton
@onready var abnormal_event_panel: VBoxContainer = $HUD/AbnormalEventPanel
@onready var event_label: Label = $HUD/AbnormalEventPanel/EventLabel
@onready var bad_ending_panel: VBoxContainer = $HUD/BadEndingPanel
@onready var return_to_menu_button: Button = $HUD/BadEndingPanel/ReturnToMenuButton
@onready var uv_lamp: SpotLight3D = $UVLamp
@onready var uv_clue_marker: MeshInstance3D = $ItemPivot/UVClueMarker
@onready var item_name_label: Label = $HUD/ItemNameLabel
@onready var item_description_label: Label = $HUD/ItemDescriptionLabel
@onready var appraisal_notes_label: Label = $HUD/AppraisalNotesBackground/AppraisalNotesLabel

const MIN_CAMERA_Z := 1.8
const MAX_CAMERA_Z := 4.2
const DEFAULT_CAMERA_Z := 2.7
const DEFAULT_FOV := 42.0
const DEFAULT_KEY_LIGHT_ENERGY := 185.0
const MAGNIFIER_CAMERA_Z := 1.95
const MAGNIFIER_FOV := 26.0
const UV_KEY_LIGHT_ENERGY := 62.0
const UV_LAMP_ENERGY := 920.0
const FALLBACK_TEMPERATURE_C := -7.4
const FALLBACK_CORRECT_HANDLING := "seal"
const FALLBACK_SELL_VALUE := 75
const FALLBACK_SEAL_COST := 20
const TEACUP_INITIAL_ROTATION_DEGREES := Vector3(0.0, -32.0, 0.0)
const shop_scene_path := "res://scenes/shop_prototype.tscn"
const main_menu_scene_path := "res://scenes/main_menu.tscn"
const TOOL_NONE := "none"
const TOOL_MAGNIFIER := "magnifier"
const TOOL_UV_LAMP := "uv_lamp"
const TOOL_THERMOMETER := "thermometer"

var drag_active := false
var rotation_sensitivity := 0.01
var zoom_step := 0.18
var active_tool := TOOL_NONE
var current_item: Node3D
var discovered_tools := {
	TOOL_MAGNIFIER: false,
	TOOL_UV_LAMP: false,
	TOOL_THERMOMETER: false,
}


func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	_load_current_day_item()
	magnifier_button.pressed.connect(_on_magnifier_pressed)
	uv_lamp_button.pressed.connect(_on_uv_lamp_pressed)
	thermometer_button.pressed.connect(_on_thermometer_pressed)
	sell_button.pressed.connect(_on_sell_pressed)
	seal_button.pressed.connect(_on_seal_pressed)
	discard_button.pressed.connect(_on_discard_pressed)
	next_day_button.pressed.connect(_on_next_day_pressed)
	back_to_shop_button.pressed.connect(_on_back_to_shop_pressed)
	return_to_menu_button.pressed.connect(_on_return_to_menu_pressed)
	_update_tool_readouts()
	_update_next_day_button_label()
	_set_active_tool(TOOL_NONE)
	day_result_panel.visible = false
	day_result_background.visible = false
	abnormal_event_panel.visible = false
	bad_ending_panel.visible = false


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		_handle_mouse_button(event)
	elif event is InputEventMouseMotion and drag_active:
		_rotate_item(event.relative)
	elif event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_1:
			_toggle_tool(TOOL_MAGNIFIER)
		elif event.keycode == KEY_2:
			_toggle_tool(TOOL_UV_LAMP)
		elif event.keycode == KEY_3:
			_toggle_tool(TOOL_THERMOMETER)


func _handle_mouse_button(event: InputEventMouseButton) -> void:
	if event.button_index == MOUSE_BUTTON_LEFT:
		drag_active = event.pressed
	elif event.pressed and event.button_index == MOUSE_BUTTON_WHEEL_UP:
		_apply_zoom(-zoom_step)
	elif event.pressed and event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
		_apply_zoom(zoom_step)


func _rotate_item(relative_motion: Vector2) -> void:
	item_pivot.rotate_y(-relative_motion.x * rotation_sensitivity)
	item_pivot.rotate_x(-relative_motion.y * rotation_sensitivity)
	item_pivot.rotation.x = clamp(item_pivot.rotation.x, -1.1, 1.1)


func _apply_zoom(delta_z: float) -> void:
	camera.position.z = clamp(camera.position.z + delta_z, MIN_CAMERA_Z, MAX_CAMERA_Z)


func _load_current_day_item() -> void:
	var item_scene_path: String = GameState.get_current_item_scene_path()
	var packed_scene := load(item_scene_path) as PackedScene
	if packed_scene == null:
		push_error("Could not load current oddity scene: %s" % item_scene_path)
		return

	current_item = packed_scene.instantiate() as Node3D
	if current_item == null:
		push_error("Current oddity scene is not a Node3D: %s" % item_scene_path)
		return
	if current_item.get("item_id") == "oddity_0001":
		current_item.rotation_degrees = TEACUP_INITIAL_ROTATION_DEGREES
	item_pivot.add_child(current_item)
	_reset_discovered_tools()
	_update_item_labels()
	_update_appraisal_notes()


func _on_magnifier_pressed() -> void:
	_toggle_tool(TOOL_MAGNIFIER)


func _on_uv_lamp_pressed() -> void:
	_toggle_tool(TOOL_UV_LAMP)


func _on_thermometer_pressed() -> void:
	_toggle_tool(TOOL_THERMOMETER)


func _on_sell_pressed() -> void:
	_resolve_decision("sell")


func _on_seal_pressed() -> void:
	_resolve_decision("seal")


func _on_discard_pressed() -> void:
	_resolve_decision("discard")


func _on_next_day_pressed() -> void:
	decision_result.visible = false
	day_result_panel.visible = false
	day_result_background.visible = false
	abnormal_event_panel.visible = false
	bad_ending_panel.visible = false
	_set_active_tool(TOOL_NONE)
	if GameState.is_run_complete():
		get_tree().change_scene_to_file(main_menu_scene_path)
	else:
		GameState.advance_day()
		get_tree().change_scene_to_file(shop_scene_path)


func _on_back_to_shop_pressed() -> void:
	get_tree().change_scene_to_file(shop_scene_path)


func _on_return_to_menu_pressed() -> void:
	get_tree().change_scene_to_file(main_menu_scene_path)


func _toggle_tool(tool_name: String) -> void:
	if active_tool == tool_name:
		_set_active_tool(TOOL_NONE)
	else:
		_set_active_tool(tool_name)


func _set_active_tool(tool_name: String) -> void:
	active_tool = tool_name
	_remember_tool_clue(active_tool)
	magnifier_button.button_pressed = active_tool == TOOL_MAGNIFIER
	uv_lamp_button.button_pressed = active_tool == TOOL_UV_LAMP
	thermometer_button.button_pressed = active_tool == TOOL_THERMOMETER
	uv_lamp.visible = active_tool == TOOL_UV_LAMP
	uv_lamp.light_energy = UV_LAMP_ENERGY if active_tool == TOOL_UV_LAMP else 0.0
	uv_clue_marker.visible = false
	thermometer_readout.visible = active_tool == TOOL_THERMOMETER
	tool_clue_readout.visible = active_tool != TOOL_NONE
	_update_tool_readouts()
	_update_appraisal_notes()
	if active_tool == TOOL_MAGNIFIER:
		camera.position.z = MAGNIFIER_CAMERA_Z
		camera.fov = MAGNIFIER_FOV
		key_light.light_energy = DEFAULT_KEY_LIGHT_ENERGY
	elif active_tool == TOOL_UV_LAMP:
		camera.position.z = DEFAULT_CAMERA_Z
		camera.fov = DEFAULT_FOV
		key_light.light_energy = UV_KEY_LIGHT_ENERGY
	elif active_tool == TOOL_THERMOMETER:
		camera.position.z = DEFAULT_CAMERA_Z
		camera.fov = DEFAULT_FOV
		key_light.light_energy = DEFAULT_KEY_LIGHT_ENERGY
	else:
		camera.position.z = DEFAULT_CAMERA_Z
		camera.fov = DEFAULT_FOV
		key_light.light_energy = DEFAULT_KEY_LIGHT_ENERGY


func _resolve_decision(decision: String) -> void:
	decision_result.visible = true
	var correct_handling := _get_current_correct_handling()
	var display_name := _get_current_display_name()
	if decision == correct_handling:
		decision_result.text = "Correct: %s is handled safely." % display_name
		_show_day_result("Correct handling", _get_decision_value_delta(decision), 5)
		abnormal_event_panel.visible = false
		bad_ending_panel.visible = false
	else:
		decision_result.text = "Wrong: %s should be %s, not %s." % [display_name, correct_handling, decision]
		_show_abnormal_event(_get_current_wrong_event_text())
		if GameState.get_current_item_id() == "oddity_0001" and decision == "sell":
			_show_day_result("Cursed sale", _get_current_sell_value(), -15)
			_show_bad_ending()
		elif decision == "discard":
			_show_day_result("Uncontained discard", 0, -8)
		else:
			_show_day_result("Bad appraisal", 0, -10)


func _show_day_result(outcome: String, value_delta: int, reputation_delta: int) -> void:
	GameState.apply_result(value_delta, reputation_delta)
	day_result_background.visible = true
	day_result_panel.visible = true
	_update_next_day_button_label()
	outcome_label.text = outcome
	value_label.text = "Cash: %+d" % value_delta
	reputation_label.text = "Reputation: %+d" % reputation_delta


func _show_abnormal_event(event_text: String) -> void:
	abnormal_event_panel.visible = true
	event_label.text = event_text


func _show_bad_ending() -> void:
	bad_ending_panel.visible = true


func _update_next_day_button_label() -> void:
	if GameState.is_run_complete():
		next_day_button.text = "Return to Menu"
	else:
		next_day_button.text = "Next Day"


func _get_current_correct_handling() -> String:
	if current_item == null:
		return FALLBACK_CORRECT_HANDLING
	var handling: Variant = current_item.get("correct_handling")
	if handling is String and not handling.is_empty():
		return handling
	return FALLBACK_CORRECT_HANDLING


func _get_current_display_name() -> String:
	if current_item == null:
		return GameState.get_current_item_id()
	var item_display_name: Variant = current_item.get("display_name")
	if item_display_name is String and not item_display_name.is_empty():
		return item_display_name
	return GameState.get_current_item_id()


func _get_current_description() -> String:
	return _get_current_string_property("description", "")


func _update_item_labels() -> void:
	item_name_label.text = _get_current_display_name()
	item_description_label.text = _get_current_description()


func _update_tool_readouts() -> void:
	thermometer_readout.text = "Temperature: %.1f C" % _get_current_temperature_c()
	tool_clue_readout.text = _get_current_tool_clue(active_tool)


func _reset_discovered_tools() -> void:
	discovered_tools[TOOL_MAGNIFIER] = false
	discovered_tools[TOOL_UV_LAMP] = false
	discovered_tools[TOOL_THERMOMETER] = false


func _remember_tool_clue(tool_name: String) -> void:
	if tool_name == TOOL_MAGNIFIER:
		discovered_tools[TOOL_MAGNIFIER] = true
	elif tool_name == TOOL_UV_LAMP:
		discovered_tools[TOOL_UV_LAMP] = true
	elif tool_name == TOOL_THERMOMETER:
		discovered_tools[TOOL_THERMOMETER] = true


func _update_appraisal_notes() -> void:
	var lines := ["Appraisal Notes"]
	lines.append("- Mag: %s" % _short_note_for_tool(TOOL_MAGNIFIER))
	lines.append("- UV: %s" % _short_note_for_tool(TOOL_UV_LAMP))
	lines.append("- Temp: %s" % _short_note_for_tool(TOOL_THERMOMETER))
	appraisal_notes_label.text = "\n".join(lines)


func _short_note_for_tool(tool_name: String) -> String:
	var note := _note_for_tool(tool_name)
	if note == "-":
		return note
	return _truncate_note(note, 28)


func _note_for_tool(tool_name: String) -> String:
	if not discovered_tools.get(tool_name, false):
		return "-"
	if tool_name == TOOL_THERMOMETER:
		return "%.1f C" % _get_current_temperature_c()
	return _get_current_tool_clue(tool_name)


func _truncate_note(text: String, max_length: int) -> String:
	if text.length() <= max_length:
		return text
	return text.substr(0, max_length - 3) + "..."


func _get_current_tool_clue(tool_name: String) -> String:
	if current_item == null:
		return ""
	var property_name := ""
	if tool_name == TOOL_MAGNIFIER:
		property_name = "magnifier_clue"
	elif tool_name == TOOL_UV_LAMP:
		property_name = "uv_clue"
	elif tool_name == TOOL_THERMOMETER:
		property_name = "thermometer_clue"
	else:
		return ""
	return _get_current_string_property(property_name, "")


func _get_current_temperature_c() -> float:
	return _get_current_float_property("thermometer_c", FALLBACK_TEMPERATURE_C)


func _get_current_sell_value() -> int:
	return _get_current_int_property("sell_value", FALLBACK_SELL_VALUE)


func _get_current_seal_cost() -> int:
	return _get_current_int_property("seal_cost", FALLBACK_SEAL_COST)


func _get_current_wrong_event_text() -> String:
	return _get_current_string_property(
		"wrong_event_text",
		"%s disturbs the shop after the bad appraisal." % _get_current_display_name()
	)


func _get_decision_value_delta(decision: String) -> int:
	if decision == "sell":
		return _get_current_sell_value()
	if decision == "seal":
		return -_get_current_seal_cost()
	return 0


func _get_current_string_property(property_name: String, fallback: String) -> String:
	if current_item == null:
		return fallback
	var value: Variant = current_item.get(property_name)
	if value is String and not value.is_empty():
		return value
	return fallback


func _get_current_float_property(property_name: String, fallback: float) -> float:
	if current_item == null:
		return fallback
	var value: Variant = current_item.get(property_name)
	if value is float or value is int:
		return float(value)
	return fallback


func _get_current_int_property(property_name: String, fallback: int) -> int:
	if current_item == null:
		return fallback
	var value: Variant = current_item.get(property_name)
	if value is int:
		return value
	if value is float:
		return int(value)
	return fallback
