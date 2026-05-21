extends Node3D

@export var item_id := ""
@export var display_name := ""
@export var description := ""
@export var model_path := ""
@export var correct_handling := "seal"
@export var magnifier_clue := ""
@export var uv_clue := ""
@export var thermometer_clue := ""
@export var thermometer_c := 20.0
@export var sell_value := 75
@export var seal_cost := 20
@export var wrong_event_text := ""

@onready var model_root: Node3D = $ModelRoot
@onready var collision_shape: CollisionShape3D = $CollisionBody/CollisionShape3D


func _ready() -> void:
	var resolved_model_path: String = _resolve_model_path(model_path)
	var model: Node3D = _load_model_scene(resolved_model_path)
	if model == null:
		return

	model_root.add_child(model)
	_center_model(model)
	_fit_collision_to_model(model)


func _resolve_model_path(path: String) -> String:
	if path.begins_with("res://") or path.is_absolute_path():
		return path
	return "res://" + path


func _load_model_scene(path: String) -> Node3D:
	var imported_scene := _load_imported_scene(path)
	if imported_scene != null:
		return imported_scene
	return _load_gltf_scene(path)


func _load_imported_scene(path: String) -> Node3D:
	var packed_scene := load(path) as PackedScene
	if packed_scene == null:
		return null
	var scene := packed_scene.instantiate()
	if scene == null:
		push_error("Imported item scene could not be instantiated: %s" % path)
		return null
	if not scene is Node3D:
		push_error("Imported item scene is not Node3D: %s" % path)
		scene.queue_free()
		return null
	return scene as Node3D


func _load_gltf_scene(path: String) -> Node3D:
	var document: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	var error: Error = document.append_from_file(path, state)
	if error != OK:
		push_error("Could not parse item GLB %s. Error code: %s" % [path, error])
		return null

	var scene: Node = document.generate_scene(state)
	if scene == null:
		push_error("Item GLB parsed but no scene was generated: %s" % path)
		return null
	if not scene is Node3D:
		push_error("Generated item GLB scene is not Node3D: %s" % path)
		scene.queue_free()
		return null
	return scene as Node3D


func _center_model(model: Node3D) -> void:
	var bounds: AABB = _calculate_bounds(model)
	if bounds.size == Vector3.ZERO:
		return
	model.position -= bounds.get_center()


func _fit_collision_to_model(model: Node3D) -> void:
	var bounds: AABB = _calculate_bounds(model)
	if bounds.size == Vector3.ZERO:
		return

	var shape := BoxShape3D.new()
	shape.size = bounds.size
	collision_shape.shape = shape
	collision_shape.position = bounds.get_center()


func _calculate_bounds(root: Node) -> AABB:
	var has_bounds := false
	var bounds := AABB()
	for child: Node in root.find_children("*", "MeshInstance3D", true, false):
		var mesh_instance := child as MeshInstance3D
		if mesh_instance.mesh == null:
			continue
		var local_bounds: AABB = mesh_instance.global_transform * mesh_instance.mesh.get_aabb()
		if not has_bounds:
			bounds = local_bounds
			has_bounds = true
		else:
			bounds = bounds.merge(local_bounds)
	return bounds
