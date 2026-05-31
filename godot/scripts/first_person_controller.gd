extends CharacterBody3D

@export var move_speed := 3.5
@export var mouse_sensitivity := 0.0025
@export var inspection_scene_path := "res://scenes/inspection_table.tscn"

@onready var camera: Camera3D = $Camera3D
@onready var prompt_label: Label = $"../HUD/Prompt"
@onready var run_status: Label = $"../HUD/RunStatus"
@onready var customer_brief_title: Label = $"../HUD/CustomerBriefPanel/CustomerBriefContent/CustomerBriefTitle"
@onready var customer_brief_body: Label = $"../HUD/CustomerBriefPanel/CustomerBriefContent/CustomerBriefBody"
@onready var customer_risk_hint: Label = $"../HUD/CustomerBriefPanel/CustomerBriefContent/CustomerRiskHint"
@onready var shop_ledger_title: Label = $"../HUD/ShopLedgerPanel/ShopLedgerContent/ShopLedgerTitle"
@onready var shop_ledger_body: Label = $"../HUD/ShopLedgerPanel/ShopLedgerContent/ShopLedgerBody"
@onready var progression_status: Label = $"../HUD/ShopLedgerPanel/ShopLedgerContent/ProgressionStatus"
@onready var result_detail_panel: PanelContainer = $"../HUD/ResultDetailPanel"
@onready var result_detail_title: Label = $"../HUD/ResultDetailPanel/ResultDetailContent/ResultDetailTitle"
@onready var result_detail_body: Label = $"../HUD/ResultDetailPanel/ResultDetailContent/ResultDetailBody"
@onready var result_detail_previous_button: Button = $"../HUD/ResultDetailPanel/ResultDetailContent/ResultDetailNav/ResultDetailPreviousButton"
@onready var result_detail_next_button: Button = $"../HUD/ResultDetailPanel/ResultDetailContent/ResultDetailNav/ResultDetailNextButton"
@onready var shop_ambience_player: AudioStreamPlayer = $"../ShopAmbiencePlayer"

var look_pitch := 0.0
var result_detail_index := 0


func _ready() -> void:
	result_detail_previous_button.pressed.connect(_on_result_detail_previous_pressed)
	result_detail_next_button.pressed.connect(_on_result_detail_next_pressed)
	_start_shop_ambience()
	_update_shop_hud()


func _start_shop_ambience() -> void:
	if shop_ambience_player.stream is AudioStreamWAV:
		shop_ambience_player.stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	if not shop_ambience_player.playing:
		shop_ambience_player.play()


func _exit_tree() -> void:
	if shop_ambience_player.playing:
		shop_ambience_player.stop()


func _update_shop_hud() -> void:
	prompt_label.text = Localization.text("ui.inspect_prompt")
	run_status.text = Localization.format_text("ui.run_status", [
		GameState.current_day,
		GameState.max_days,
		GameState.cash,
		GameState.reputation,
	])
	var customer_brief: Dictionary = GameState.get_current_customer_brief()
	customer_brief_title.text = str(customer_brief.get("title", Localization.text("fallback.customer_note")))
	customer_brief_body.text = str(customer_brief.get("body", Localization.text("fallback.customer_body")))
	customer_risk_hint.text = str(customer_brief.get("risk_hint", Localization.text("fallback.risk_hint")))
	shop_ledger_title.text = Localization.text("ui.shop_ledger")
	shop_ledger_body.text = GameState.get_shop_ledger()
	progression_status.text = GameState.get_progression_status_text()
	_update_result_detail_panel()


func _update_result_detail_panel() -> void:
	var detail_count := GameState.get_result_detail_count()
	result_detail_panel.visible = detail_count > 0
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE if detail_count > 0 else Input.MOUSE_MODE_CAPTURED)
	if detail_count <= 0:
		result_detail_title.text = Localization.text("ui.result_detail_empty")
		result_detail_body.text = Localization.text("ui.result_detail_empty")
		return
	result_detail_index = clamp(result_detail_index, 0, detail_count - 1)
	var detail: Dictionary = GameState.get_result_detail(result_detail_index)
	result_detail_title.text = str(detail.get("title", Localization.text("ui.result_detail_empty")))
	result_detail_body.text = str(detail.get("body", Localization.text("ui.result_detail_empty")))
	result_detail_previous_button.text = Localization.text("ui.detail_previous")
	result_detail_next_button.text = Localization.text("ui.detail_next")
	result_detail_previous_button.disabled = result_detail_index <= 0
	result_detail_next_button.disabled = result_detail_index >= detail_count - 1


func _on_result_detail_previous_pressed() -> void:
	result_detail_index -= 1
	_update_result_detail_panel()


func _on_result_detail_next_pressed() -> void:
	result_detail_index += 1
	_update_result_detail_panel()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		rotate_y(-event.relative.x * mouse_sensitivity)
		look_pitch = clamp(look_pitch - event.relative.y * mouse_sensitivity, -1.25, 1.25)
		camera.rotation.x = look_pitch
	elif event.is_action_pressed("interact"):
		get_tree().change_scene_to_file(inspection_scene_path)
	elif event.is_action_pressed("ui_cancel"):
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)


func _physics_process(_delta: float) -> void:
	var input_vector := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction := (transform.basis * Vector3(input_vector.x, 0.0, input_vector.y)).normalized()
	velocity.x = direction.x * move_speed
	velocity.z = direction.z * move_speed
	move_and_slide()
