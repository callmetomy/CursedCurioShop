extends Node3D

@onready var item_pivot: Node3D = $ItemPivot
@onready var camera: Camera3D = $InspectionCamera
@onready var key_light: SpotLight3D = $KeyLight
@onready var tool_panel: HBoxContainer = $HUD/ToolPanel
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
@onready var outcome_label: Label = $HUD/DayResultPanel/ResultTextPanel/ResultTextContent/OutcomeLabel
@onready var value_label: Label = $HUD/DayResultPanel/ResultTextPanel/ResultTextContent/ValueLabel
@onready var reputation_label: Label = $HUD/DayResultPanel/ResultTextPanel/ResultTextContent/ReputationLabel
@onready var consequence_report_label: Label = $HUD/DayResultPanel/ResultTextPanel/ResultTextContent/ConsequenceReportLabel
@onready var run_summary_label: Label = $HUD/DayResultPanel/ResultTextPanel/ResultTextContent/RunSummaryLabel
@onready var progression_panel: PanelContainer = $HUD/DayResultPanel/ProgressionPanel
@onready var progression_status_label: Label = $HUD/DayResultPanel/ProgressionPanel/ProgressionContent/ProgressionStatusLabel
@onready var buy_ledger_desk_button: Button = $HUD/DayResultPanel/ProgressionPanel/ProgressionContent/BuyLedgerDeskButton
@onready var buy_containment_cabinet_button: Button = $HUD/DayResultPanel/ProgressionPanel/ProgressionContent/BuyContainmentCabinetButton
@onready var next_day_button: Button = $HUD/DayResultPanel/ResultButtonPanel/NextDayButton
@onready var back_to_shop_button: Button = $HUD/BackToShopButton
@onready var decision_panel: HBoxContainer = $HUD/DecisionPanel
@onready var abnormal_event_panel: VBoxContainer = $HUD/AbnormalEventPanel
@onready var event_label: Label = $HUD/AbnormalEventPanel/EventLabel
@onready var bad_ending_background: ColorRect = $HUD/BadEndingBackground
@onready var bad_ending_card: PanelContainer = $HUD/BadEndingCard
@onready var bad_ending_panel: VBoxContainer = $HUD/BadEndingCard/BadEndingPanel
@onready var ending_title: Label = $HUD/BadEndingCard/BadEndingPanel/EndingTitle
@onready var ending_body: Label = $HUD/BadEndingCard/BadEndingPanel/EndingBody
@onready var return_to_menu_button: Button = $HUD/BadEndingCard/BadEndingPanel/ReturnToMenuButton
@onready var uv_lamp: SpotLight3D = $UVLamp
@onready var tool_audio_player: AudioStreamPlayer = $ToolAudioPlayer
@onready var decision_correct_audio_player: AudioStreamPlayer = $DecisionCorrectAudioPlayer
@onready var decision_wrong_audio_player: AudioStreamPlayer = $DecisionWrongAudioPlayer
@onready var abnormal_event_audio_player: AudioStreamPlayer = $AbnormalEventAudioPlayer
@onready var bad_ending_audio_player: AudioStreamPlayer = $BadEndingAudioPlayer
@onready var uv_clue_marker: MeshInstance3D = $ItemPivot/UVClueMarker
@onready var item_name_label: Label = $HUD/ItemNameLabel
@onready var item_description_label: Label = $HUD/ItemDescriptionLabel
@onready var appraisal_notes_background: TextureRect = $HUD/AppraisalNotesBackground
@onready var appraisal_notes_label: Label = $HUD/AppraisalNotesBackground/AppraisalNotesLabel
@onready var onboarding_panel: PanelContainer = $HUD/OnboardingPanel
@onready var onboarding_hint_label: Label = $HUD/OnboardingPanel/OnboardingHintLabel

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
	_apply_localized_static_text()
	_load_current_day_item()
	magnifier_button.pressed.connect(_on_magnifier_pressed)
	uv_lamp_button.pressed.connect(_on_uv_lamp_pressed)
	thermometer_button.pressed.connect(_on_thermometer_pressed)
	sell_button.pressed.connect(_on_sell_pressed)
	seal_button.pressed.connect(_on_seal_pressed)
	discard_button.pressed.connect(_on_discard_pressed)
	next_day_button.pressed.connect(_on_next_day_pressed)
	buy_ledger_desk_button.pressed.connect(_on_buy_ledger_desk_pressed)
	buy_containment_cabinet_button.pressed.connect(_on_buy_containment_cabinet_pressed)
	back_to_shop_button.pressed.connect(_on_back_to_shop_pressed)
	return_to_menu_button.pressed.connect(_on_return_to_menu_pressed)
	_update_tool_readouts()
	_update_onboarding_hint()
	_update_next_day_button_label()
	_set_active_tool(TOOL_NONE)
	day_result_panel.visible = false
	day_result_background.visible = false
	progression_panel.visible = false
	abnormal_event_panel.visible = false
	bad_ending_background.visible = false
	bad_ending_card.visible = false


func _apply_localized_static_text() -> void:
	back_to_shop_button.text = Localization.text("ui.back_to_shop")
	magnifier_button.text = Localization.text("ui.magnifier")
	uv_lamp_button.text = Localization.text("ui.uv_lamp")
	thermometer_button.text = Localization.text("ui.thermometer")
	sell_button.text = Localization.text("ui.sell")
	seal_button.text = Localization.text("ui.seal")
	discard_button.text = Localization.text("ui.discard")
	next_day_button.text = Localization.text("ui.next_day")
	return_to_menu_button.text = Localization.text("ui.return_to_menu")
	ending_title.text = Localization.text("ending.frost_sale.title")


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
	progression_panel.visible = false
	abnormal_event_panel.visible = false
	bad_ending_background.visible = false
	bad_ending_card.visible = false
	_set_active_tool(TOOL_NONE)
	if GameState.is_run_complete():
		get_tree().change_scene_to_file(main_menu_scene_path)
	else:
		GameState.advance_day()
		get_tree().change_scene_to_file(shop_scene_path)


func _on_back_to_shop_pressed() -> void:
	if bad_ending_card.visible:
		return
	get_tree().change_scene_to_file(shop_scene_path)


func _on_return_to_menu_pressed() -> void:
	get_tree().change_scene_to_file(main_menu_scene_path)


func _on_buy_ledger_desk_pressed() -> void:
	if GameState.purchase_ledger_desk_upgrade():
		run_summary_label.text = GameState.get_run_summary()
	_update_progression_panel()


func _on_buy_containment_cabinet_pressed() -> void:
	if GameState.purchase_containment_cabinet_upgrade():
		run_summary_label.text = GameState.get_run_summary()
	_update_progression_panel()


func _toggle_tool(tool_name: String) -> void:
	if bad_ending_card.visible:
		return
	if active_tool == tool_name:
		_set_active_tool(TOOL_NONE)
	else:
		_set_active_tool(tool_name)


func _set_active_tool(tool_name: String) -> void:
	if tool_name != TOOL_NONE:
		_play_audio_cue(tool_audio_player)
	active_tool = tool_name
	_remember_tool_clue(active_tool)
	GameState.record_onboarding_tool_used(tool_name)
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
	_update_onboarding_hint()
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
	if bad_ending_card.visible:
		return
	GameState.complete_onboarding()
	decision_result.visible = true
	var correct_handling := _get_current_correct_handling()
	var display_name := _get_current_display_name()
	if decision == correct_handling:
		_play_audio_cue(decision_correct_audio_player)
		decision_result.text = Localization.format_text("ui.correct_result", [display_name])
		_show_day_result("outcome.correct", _get_decision_value_delta(decision), 5, decision)
		abnormal_event_panel.visible = false
		bad_ending_card.visible = false
	else:
		_play_audio_cue(decision_wrong_audio_player)
		decision_result.text = Localization.format_text("ui.wrong_result", [display_name, correct_handling, decision])
		var wrong_event_text := _get_current_wrong_event_text()
		if GameState.get_current_item_id() == "oddity_0001" and decision == "sell":
			_show_day_result("outcome.cursed_sale", _get_current_sell_value(), -15, decision)
			_show_bad_ending(wrong_event_text)
		elif decision == "discard":
			_show_abnormal_event(wrong_event_text)
			_show_day_result("outcome.uncontained_discard", 0, -8, decision)
		else:
			_show_abnormal_event(wrong_event_text)
			_show_day_result("outcome.bad_appraisal", 0, -10, decision)


func _show_day_result(outcome_key: String, value_delta: int, reputation_delta: int, decision: String) -> void:
	GameState.apply_result(value_delta, reputation_delta)
	_set_active_tool(TOOL_NONE)
	_set_inspection_controls_visible(false)
	onboarding_panel.visible = false
	day_result_background.visible = true
	day_result_panel.visible = true
	_update_next_day_button_label()
	outcome_label.text = Localization.text(outcome_key)
	value_label.text = Localization.format_text("ui.cash_delta", [value_delta])
	reputation_label.text = Localization.format_text("ui.reputation_delta", [reputation_delta])
	var consequence_key := GameState.get_current_consequence_key(decision)
	var consequence_report: String = GameState.get_current_consequence_report(decision)
	consequence_report_label.text = consequence_report
	GameState.record_decision_result(
		GameState.get_current_item_id(),
		decision,
		outcome_key,
		consequence_key,
		value_delta,
		reputation_delta
	)
	consequence_report_label.visible = not GameState.is_run_complete()
	run_summary_label.visible = GameState.is_run_complete()
	run_summary_label.text = GameState.get_run_summary() if GameState.is_run_complete() else ""
	_update_progression_panel()


func _update_progression_panel() -> void:
	progression_panel.visible = GameState.is_run_complete()
	progression_status_label.text = GameState.get_progression_status_text()
	buy_ledger_desk_button.text = Localization.text("upgrade.ledger_desk.buy")
	buy_ledger_desk_button.disabled = not GameState.can_purchase_ledger_desk_upgrade()
	buy_containment_cabinet_button.text = Localization.text("upgrade.containment_cabinet.buy")
	buy_containment_cabinet_button.disabled = not GameState.can_purchase_containment_cabinet_upgrade()


func _show_abnormal_event(event_text: String) -> void:
	_play_audio_cue(abnormal_event_audio_player)
	abnormal_event_panel.visible = true
	event_label.text = event_text


func _show_bad_ending(event_text: String) -> void:
	_play_audio_cue(bad_ending_audio_player)
	_set_active_tool(TOOL_NONE)
	_set_gameplay_hud_visible(false)
	decision_result.visible = false
	day_result_background.visible = false
	day_result_panel.visible = false
	abnormal_event_panel.visible = false
	bad_ending_background.visible = true
	bad_ending_card.visible = true
	ending_body.text = "%s\n\n%s | %s" % [
		event_text,
		Localization.format_text("ui.final_cash", [GameState.cash]),
		Localization.format_text("ui.final_reputation", [GameState.reputation]),
	]


func _set_gameplay_hud_visible(is_visible: bool) -> void:
	item_name_label.visible = is_visible
	item_description_label.visible = is_visible
	back_to_shop_button.visible = is_visible
	onboarding_panel.visible = is_visible and GameState.get_onboarding_hint_key() != ""
	_set_inspection_controls_visible(is_visible)


func _set_inspection_controls_visible(is_visible: bool) -> void:
	tool_panel.visible = is_visible
	decision_panel.visible = is_visible
	appraisal_notes_background.visible = is_visible
	sell_button.disabled = not is_visible
	seal_button.disabled = not is_visible
	discard_button.disabled = not is_visible
	back_to_shop_button.disabled = not is_visible
	magnifier_button.disabled = not is_visible
	uv_lamp_button.disabled = not is_visible
	thermometer_button.disabled = not is_visible
	if not is_visible:
		drag_active = false
		thermometer_readout.visible = false
		tool_clue_readout.visible = false
		uv_lamp.visible = false
		uv_lamp.light_energy = 0.0


func _update_next_day_button_label() -> void:
	if GameState.is_run_complete():
		next_day_button.text = Localization.text("ui.return_to_menu")
	else:
		next_day_button.text = Localization.text("ui.next_day")


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
	var item_id: String = str(current_item.get("item_id"))
	var item_display_name: Variant = current_item.get("display_name")
	var fallback := GameState.get_current_item_id()
	if item_display_name is String and not item_display_name.is_empty():
		fallback = item_display_name
	return Localization.item_text(item_id, "display_name", fallback)


func _get_current_description() -> String:
	return _get_current_localized_item_property("description", "")


func _update_item_labels() -> void:
	item_name_label.text = _get_current_display_name()
	item_description_label.text = _get_current_description()


func _update_tool_readouts() -> void:
	thermometer_readout.text = Localization.format_text("ui.temperature", [_get_current_temperature_c()])
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
	var lines := [Localization.text("ui.appraisal_notes")]
	lines.append(Localization.format_text("ui.note_mag", [_short_note_for_tool(TOOL_MAGNIFIER)]))
	lines.append(Localization.format_text("ui.note_uv", [_short_note_for_tool(TOOL_UV_LAMP)]))
	lines.append(Localization.format_text("ui.note_temp", [_short_note_for_tool(TOOL_THERMOMETER)]))
	appraisal_notes_label.text = "\n".join(lines)


func _update_onboarding_hint() -> void:
	var hint_key := GameState.get_onboarding_hint_key()
	onboarding_panel.visible = hint_key != ""
	if hint_key != "":
		onboarding_hint_label.text = Localization.text(hint_key)


func _play_audio_cue(player: AudioStreamPlayer) -> void:
	player.stop()
	player.play()


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
	return _get_current_localized_item_property(property_name, "")


func _get_current_temperature_c() -> float:
	return _get_current_float_property("thermometer_c", FALLBACK_TEMPERATURE_C)


func _get_current_sell_value() -> int:
	return _get_current_int_property("sell_value", FALLBACK_SELL_VALUE)


func _get_current_seal_cost() -> int:
	return GameState.get_effective_seal_cost(_get_current_base_seal_cost())


func _get_current_base_seal_cost() -> int:
	return _get_current_int_property("seal_cost", FALLBACK_SEAL_COST)


func _get_current_wrong_event_text() -> String:
	return _get_current_localized_item_property(
		"wrong_event_text",
		Localization.format_text("fallback.wrong_event", [_get_current_display_name()])
	)


func _get_current_localized_item_property(property_name: String, fallback: String) -> String:
	if current_item == null:
		return fallback
	var item_id: String = str(current_item.get("item_id"))
	var item_fallback := _get_current_string_property(property_name, fallback)
	return Localization.item_text(item_id, property_name, item_fallback)


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
