extends CharacterBody3D

@export var move_speed := 3.5
@export var mouse_sensitivity := 0.0025
@export var inspection_scene_path := "res://scenes/inspection_table.tscn"

@onready var camera: Camera3D = $Camera3D
@onready var run_status: Label = $"../HUD/RunStatus"
@onready var customer_brief_title: Label = $"../HUD/CustomerBriefPanel/CustomerBriefContent/CustomerBriefTitle"
@onready var customer_brief_body: Label = $"../HUD/CustomerBriefPanel/CustomerBriefContent/CustomerBriefBody"
@onready var customer_risk_hint: Label = $"../HUD/CustomerBriefPanel/CustomerBriefContent/CustomerRiskHint"
@onready var shop_ledger_title: Label = $"../HUD/ShopLedgerPanel/ShopLedgerContent/ShopLedgerTitle"
@onready var shop_ledger_body: Label = $"../HUD/ShopLedgerPanel/ShopLedgerContent/ShopLedgerBody"

var look_pitch := 0.0


func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	_update_shop_hud()


func _update_shop_hud() -> void:
	run_status.text = "Day %d/%d | Cash %d | Reputation %d" % [
		GameState.current_day,
		GameState.max_days,
		GameState.cash,
		GameState.reputation,
	]
	var customer_brief: Dictionary = GameState.get_current_customer_brief()
	customer_brief_title.text = str(customer_brief.get("title", "Customer Note"))
	customer_brief_body.text = str(customer_brief.get("body", "A customer is waiting for an appraisal."))
	customer_risk_hint.text = str(customer_brief.get("risk_hint", "Risk hint: unknown"))
	shop_ledger_title.text = GameState.SHOP_LEDGER_TITLE
	shop_ledger_body.text = GameState.get_shop_ledger()


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
