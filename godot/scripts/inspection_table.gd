extends Node3D

@onready var item_pivot: Node3D = $ItemPivot
@onready var camera: Camera3D = $InspectionCamera
@onready var key_light: SpotLight3D = $KeyLight
@onready var magnifier_button: Button = $HUD/ToolPanel/MagnifierButton
@onready var uv_lamp_button: Button = $HUD/ToolPanel/UVLampButton
@onready var thermometer_button: Button = $HUD/ToolPanel/ThermometerButton
@onready var thermometer_readout: Label = $HUD/ThermometerReadout
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

const MIN_CAMERA_Z := 1.8
const MAX_CAMERA_Z := 4.2
const DEFAULT_CAMERA_Z := 2.7
const DEFAULT_FOV := 42.0
const DEFAULT_KEY_LIGHT_ENERGY := 880.0
const MAGNIFIER_CAMERA_Z := 1.95
const MAGNIFIER_FOV := 26.0
const UV_KEY_LIGHT_ENERGY := 160.0
const UV_LAMP_ENERGY := 920.0
const CURSED_TEMPERATURE_C := -7.4
const CORRECT_HANDLING := "seal"
const SELL_VALUE := 75
const SEAL_COST := 20
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


func _ready() -> void:
	magnifier_button.pressed.connect(_on_magnifier_pressed)
	uv_lamp_button.pressed.connect(_on_uv_lamp_pressed)
	thermometer_button.pressed.connect(_on_thermometer_pressed)
	sell_button.pressed.connect(_on_sell_pressed)
	seal_button.pressed.connect(_on_seal_pressed)
	discard_button.pressed.connect(_on_discard_pressed)
	next_day_button.pressed.connect(_on_next_day_pressed)
	back_to_shop_button.pressed.connect(_on_back_to_shop_pressed)
	return_to_menu_button.pressed.connect(_on_return_to_menu_pressed)
	thermometer_readout.text = "Temperature: %.1f C" % CURSED_TEMPERATURE_C
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
	magnifier_button.button_pressed = active_tool == TOOL_MAGNIFIER
	uv_lamp_button.button_pressed = active_tool == TOOL_UV_LAMP
	thermometer_button.button_pressed = active_tool == TOOL_THERMOMETER
	uv_lamp.visible = active_tool == TOOL_UV_LAMP
	uv_lamp.light_energy = UV_LAMP_ENERGY if active_tool == TOOL_UV_LAMP else 0.0
	uv_clue_marker.visible = active_tool == TOOL_UV_LAMP
	thermometer_readout.visible = active_tool == TOOL_THERMOMETER
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
	if decision == CORRECT_HANDLING:
		decision_result.text = "Correct: the teacup is sealed before it can spread frost."
		_show_day_result("Correct handling", -SEAL_COST, 5)
		abnormal_event_panel.visible = false
		bad_ending_panel.visible = false
	else:
		decision_result.text = "Wrong: the teacup should be sealed, not %s." % decision
		_show_abnormal_event("Frost blooms across the counter. The cup has started whispering names.")
		if decision == "sell":
			_show_day_result("Cursed sale", SELL_VALUE, -15)
			_show_bad_ending()
		elif decision == "discard":
			_show_day_result("Uncontained discard", 0, -8)
		else:
			_show_day_result("Bad appraisal", 0, -10)


func _show_day_result(outcome: String, value_delta: int, reputation_delta: int) -> void:
	GameState.apply_result(value_delta, reputation_delta)
	day_result_background.visible = true
	day_result_panel.visible = true
	outcome_label.text = outcome
	value_label.text = "Cash: %+d" % value_delta
	reputation_label.text = "Reputation: %+d" % reputation_delta


func _show_abnormal_event(event_text: String) -> void:
	abnormal_event_panel.visible = true
	event_label.text = event_text


func _show_bad_ending() -> void:
	bad_ending_panel.visible = true
