extends Control

@onready var start_button: Button = $MenuPanel/StartButton
@onready var quit_button: Button = $MenuPanel/QuitButton

const shop_scene_path := "res://scenes/shop_prototype.tscn"


func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	start_button.pressed.connect(_on_start_pressed)
	quit_button.pressed.connect(_on_quit_pressed)


func _on_start_pressed() -> void:
	GameState.start_new_run()
	get_tree().change_scene_to_file(shop_scene_path)


func _on_quit_pressed() -> void:
	get_tree().quit()
