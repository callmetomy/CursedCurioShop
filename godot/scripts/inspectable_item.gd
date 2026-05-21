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
@export var use_fallback_material := false
@export var fallback_material_color := Color(0.48, 0.42, 0.36, 1.0)
@export var fallback_material_metallic := 0.0
@export var fallback_material_roughness := 0.78
@export var material_tint_enabled := false
@export var material_tint_color := Color(1.0, 1.0, 1.0, 1.0)
@export var material_tint_roughness := 0.88
@export var accent_marker_enabled := true
@export var accent_marker_color := Color(0.15, 0.75, 1.0, 1.0)
@export var wear_decal_enabled := false
@export var wear_decal_texture_path := ""
@export var wear_decal_size := Vector3(0.24, 0.16, 0.16)

@onready var model_root: Node3D = $ModelRoot
@onready var collision_shape: CollisionShape3D = $CollisionBody/CollisionShape3D


func _ready() -> void:
	var resolved_model_path: String = _resolve_model_path(model_path)
	var model: Node3D = _load_model_scene(resolved_model_path)
	if model == null:
		return

	model_root.add_child(model)
	_center_model(model)
	_apply_fallback_material(model)
	_apply_material_tint(model)
	_fit_collision_to_model(model)
	_add_accent_marker(model)
	_add_wear_decal(model)


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


func _apply_fallback_material(model: Node3D) -> void:
	if not use_fallback_material:
		return
	var material := _make_readability_material(
		fallback_material_color,
		fallback_material_metallic,
		fallback_material_roughness
	)
	for child: Node in model.find_children("*", "MeshInstance3D", true, false):
		var mesh_instance := child as MeshInstance3D
		mesh_instance.material_override = material


func _apply_material_tint(model: Node3D) -> void:
	if not material_tint_enabled or use_fallback_material:
		return
	for child: Node in model.find_children("*", "MeshInstance3D", true, false):
		var mesh_instance := child as MeshInstance3D
		if mesh_instance.mesh == null:
			continue
		for surface_index: int in mesh_instance.mesh.get_surface_count():
			var material := _tinted_surface_material(mesh_instance, surface_index)
			mesh_instance.set_surface_override_material(surface_index, material)


func _tinted_surface_material(mesh_instance: MeshInstance3D, surface_index: int) -> BaseMaterial3D:
	var source := mesh_instance.get_surface_override_material(surface_index)
	if source == null and mesh_instance.mesh != null:
		source = mesh_instance.mesh.surface_get_material(surface_index)
	var material: BaseMaterial3D
	if source is BaseMaterial3D:
		material = (source as BaseMaterial3D).duplicate() as BaseMaterial3D
	else:
		material = StandardMaterial3D.new()
	material.albedo_color = material_tint_color
	material.roughness = clamp(material_tint_roughness, 0.0, 1.0)
	return material


func _add_accent_marker(model: Node3D) -> void:
	if not accent_marker_enabled:
		return
	var bounds: AABB = _calculate_bounds(model)
	if bounds.size == Vector3.ZERO:
		return

	var marker := MeshInstance3D.new()
	marker.name = "AppraisalAccentMarker"
	var marker_mesh := SphereMesh.new()
	marker_mesh.radius = max(bounds.size.length() * 0.045, 0.025)
	marker_mesh.height = marker_mesh.radius * 2.0
	marker.mesh = marker_mesh
	marker.material_override = _make_readability_material(accent_marker_color)
	model_root.add_child(marker)
	marker.global_position = bounds.get_center() + Vector3(
		bounds.size.x * 0.28,
		bounds.size.y * 0.36,
		bounds.size.z * 0.28
	)


func _add_wear_decal(model: Node3D) -> void:
	if not wear_decal_enabled:
		return
	var bounds: AABB = _calculate_bounds(model)
	if bounds.size == Vector3.ZERO:
		return

	var decal_texture := load(wear_decal_texture_path) as Texture2D
	if decal_texture == null:
		push_error("Could not load item wear decal texture: %s" % wear_decal_texture_path)
		return

	var decal := Decal.new()
	decal.name = "AppraisalWearDecal"
	decal.texture_albedo = decal_texture
	decal.size = _resolved_wear_decal_size(bounds)
	decal.albedo_mix = 0.92
	decal.upper_fade = 0.18
	decal.lower_fade = 0.18
	model_root.add_child(decal)

	var target := bounds.get_center() + Vector3(
		-bounds.size.x * 0.12,
		bounds.size.y * 0.08,
		bounds.size.z * 0.05
	)
	decal.global_position = bounds.get_center() + Vector3(
		-bounds.size.x * 0.24,
		bounds.size.y * 0.1,
		bounds.size.z * 0.62
	)
	decal.look_at(target, Vector3.UP)


func _resolved_wear_decal_size(bounds: AABB) -> Vector3:
	if wear_decal_size.x > 0.0 and wear_decal_size.y > 0.0 and wear_decal_size.z > 0.0:
		return wear_decal_size
	var width: float = max(bounds.size.x * 0.34, 0.12)
	var height: float = max(bounds.size.y * 0.22, 0.08)
	var depth: float = max(bounds.size.z * 0.3, 0.08)
	return Vector3(width, height, depth)


func _make_readability_material(color: Color, metallic := 0.0, roughness := 0.78) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.metallic = metallic
	material.roughness = roughness
	return material


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
