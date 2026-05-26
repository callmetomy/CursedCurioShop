extends Control

@onready var start_button: Button = $MenuPanel/StartButton
@onready var reset_progress_button: Button = $MenuPanel/ResetProgressButton
@onready var quit_button: Button = $MenuPanel/QuitButton
@onready var title_label: Label = $MenuPanel/Title

const shop_scene_path := "res://scenes/shop_prototype.tscn"


func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	_apply_localized_text()
	start_button.pressed.connect(_on_start_pressed)
	reset_progress_button.pressed.connect(_on_reset_progress_pressed)
	quit_button.pressed.connect(_on_quit_pressed)


func _apply_localized_text() -> void:
	title_label.text = Localization.text("game.title")
	start_button.text = Localization.text("ui.start_day")
	reset_progress_button.text = Localization.text("ui.reset_progress")
	quit_button.text = Localization.text("ui.quit")


func _on_start_pressed() -> void:
	GameState.start_new_run()
	get_tree().change_scene_to_file(shop_scene_path)


func _on_reset_progress_pressed() -> void:
	GameState.reset_progress()
	get_tree().change_scene_to_file(shop_scene_path)


func _on_quit_pressed() -> void:
	get_tree().quit()
