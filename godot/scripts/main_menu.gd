extends Control

@onready var start_button: Button = $MenuPanel/StartButton
@onready var reset_progress_button: Button = $MenuPanel/ResetProgressButton
@onready var settings_button: Button = $MenuPanel/SettingsButton
@onready var quit_button: Button = $MenuPanel/QuitButton
@onready var title_label: Label = $MenuPanel/Title
@onready var menu_panel: VBoxContainer = $MenuPanel
@onready var settings_panel: VBoxContainer = $SettingsPanel
@onready var settings_title: Label = $SettingsPanel/SettingsTitle
@onready var language_label: Label = $SettingsPanel/LanguageLabel
@onready var language_option: OptionButton = $SettingsPanel/LanguageOption
@onready var fullscreen_checkbox: CheckBox = $SettingsPanel/FullscreenCheckBox
@onready var volume_label: Label = $SettingsPanel/VolumeLabel
@onready var volume_slider: HSlider = $SettingsPanel/VolumeSlider
@onready var back_from_settings_button: Button = $SettingsPanel/BackFromSettingsButton

const shop_scene_path := "res://scenes/shop_prototype.tscn"
const LOCALE_OPTIONS := [
	{"code": "en", "label": "English"},
	{"code": "ja", "label": "日本語"},
	{"code": "ko", "label": "한국어"},
	{"code": "es", "label": "Español"},
	{"code": "pt", "label": "Português"},
	{"code": "ru", "label": "Русский"},
	{"code": "zh_CN", "label": "简体中文"},
	{"code": "zh_TW", "label": "繁體中文"},
]


func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	_populate_language_options()
	volume_slider.value = 0.8
	_apply_localized_text()
	start_button.pressed.connect(_on_start_pressed)
	reset_progress_button.pressed.connect(_on_reset_progress_pressed)
	settings_button.pressed.connect(_on_settings_pressed)
	language_option.item_selected.connect(_on_language_selected)
	fullscreen_checkbox.toggled.connect(_on_fullscreen_toggled)
	volume_slider.value_changed.connect(_on_volume_changed)
	back_from_settings_button.pressed.connect(_on_back_from_settings_pressed)
	quit_button.pressed.connect(_on_quit_pressed)


func _apply_localized_text() -> void:
	title_label.text = Localization.text("game.title")
	start_button.text = Localization.text("ui.start_day")
	reset_progress_button.text = Localization.text("ui.reset_progress")
	settings_button.text = Localization.text("ui.settings")
	quit_button.text = Localization.text("ui.quit")
	settings_title.text = Localization.text("ui.settings_title")
	language_label.text = Localization.text("ui.language")
	fullscreen_checkbox.text = Localization.text("ui.fullscreen")
	volume_label.text = Localization.text("ui.master_volume")
	back_from_settings_button.text = Localization.text("ui.back")


func _populate_language_options() -> void:
	language_option.clear()
	var selected_index := 0
	for index in LOCALE_OPTIONS.size():
		var option: Dictionary = LOCALE_OPTIONS[index]
		language_option.add_item(str(option["label"]))
		if str(option["code"]) == Localization.current_locale:
			selected_index = index
	language_option.select(selected_index)


func _on_start_pressed() -> void:
	GameState.start_new_run()
	get_tree().change_scene_to_file(shop_scene_path)


func _on_reset_progress_pressed() -> void:
	GameState.reset_progress()
	get_tree().change_scene_to_file(shop_scene_path)


func _on_settings_pressed() -> void:
	menu_panel.visible = false
	settings_panel.visible = true


func _on_language_selected(index: int) -> void:
	var safe_index: int = clamp(index, 0, LOCALE_OPTIONS.size() - 1)
	Localization.set_locale(str(LOCALE_OPTIONS[safe_index]["code"]))
	_apply_localized_text()


func _on_fullscreen_toggled(enabled: bool) -> void:
	var mode := DisplayServer.WINDOW_MODE_FULLSCREEN if enabled else DisplayServer.WINDOW_MODE_WINDOWED
	DisplayServer.window_set_mode(mode)


func _on_volume_changed(value: float) -> void:
	var master_bus := AudioServer.get_bus_index("Master")
	AudioServer.set_bus_volume_db(master_bus, linear_to_db(max(value, 0.001)))


func _on_back_from_settings_pressed() -> void:
	settings_panel.visible = false
	menu_panel.visible = true


func _on_quit_pressed() -> void:
	get_tree().quit()
