extends Node3D

@onready var model_root: Node3D = $ModelRoot

const MODEL_PATH := "res://assets/models_raw/tripo_teacup.glb"

var rotation_speed := 0.6


func _ready() -> void:
	var model: Node3D = _load_gltf_scene(MODEL_PATH)
	if model == null:
		return
	model_root.add_child(model)
	_center_and_scale_model(model)


func _process(delta: float) -> void:
	model_root.rotate_y(rotation_speed * delta)


func _load_gltf_scene(path: String) -> Node3D:
	var document: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	var error: Error = document.append_from_file(path, state)
	if error != OK:
		push_error("Could not parse GLB model %s. Error code: %s" % [path, error])
		return null

	var scene: Node = document.generate_scene(state)
	if scene == null:
		push_error("GLB parsed but no scene was generated: %s" % path)
		return null
	if not scene is Node3D:
		push_error("Generated GLB scene is not Node3D: %s" % path)
		scene.queue_free()
		return null
	return scene as Node3D


func _center_and_scale_model(model: Node3D) -> void:
	var bounds: AABB = _calculate_bounds(model)
	if bounds.size == Vector3.ZERO:
		return

	model.position -= bounds.get_center()
	var longest_axis: float = max(bounds.size.x, max(bounds.size.y, bounds.size.z))
	if longest_axis > 0.0:
		model.scale = Vector3.ONE * (1.4 / longest_axis)


func _calculate_bounds(root: Node) -> AABB:
	var has_bounds: bool = false
	var bounds: AABB = AABB()
	for child: Node in root.find_children("*", "MeshInstance3D", true, false):
		var mesh_instance: MeshInstance3D = child as MeshInstance3D
		if mesh_instance.mesh == null:
			continue
		var local_bounds: AABB = mesh_instance.global_transform * mesh_instance.mesh.get_aabb()
		if not has_bounds:
			bounds = local_bounds
			has_bounds = true
		else:
			bounds = bounds.merge(local_bounds)
	return bounds
