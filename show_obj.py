import trimesh

obj_file = "models_ignition/obj_000001/obj_000001.obj"
texture_file = "models_ignition/obj_000001/obj_000001.png"

obj_file = "models/obj_000001.ply"
texture_file = "models/obj_000001.png"

mesh = trimesh.load(obj_file)
mesh.show()
