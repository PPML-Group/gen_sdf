import os
import trimesh

def simplify_mesh(mesh, target_faces):
    """
    使用 Trimesh 库中的简化算法来减少网格的面数。

    参数：
    - mesh: Trimesh 网格对象
    - target_faces: 目标面数

    返回值：
    - simplified_mesh: 简化后的 Trimesh 网格对象
    """
    # 确保目标面数不超过当前网格的面数
    target_faces = min(len(mesh.faces)/10, len(mesh.faces))

    # 使用 Quadric Decimation 算法进行简化
    simplified_mesh = mesh.simplify_quadric_decimation(target_faces)
    
    # 如果简化后的网格不是水密的，则尝试修复
    if not simplified_mesh.is_watertight:
        # 尝试使用修复算法来修复网格的水密性
        simplified_mesh, info = trimesh.repair.fix_winding(simplified_mesh)

    return simplified_mesh

def convert_ply_to_obj(ply_path, texture_path, output_dir):
    # Load PLY file
    mesh = trimesh.load(ply_path)
    
    # Create folder for the object
    obj_name = os.path.splitext(os.path.basename(ply_path))[0]
    obj_folder = os.path.join(output_dir, obj_name)
    os.makedirs(obj_folder, exist_ok=True)
    
    # Export OBJ file
    obj_file = os.path.join(obj_folder, obj_name + '.obj')
    mesh.export(obj_file, include_texture=True)
    
    # Simplify mesh
    # simplified_mesh = simplify_mesh(mesh, 1000)
    simplified_mesh = mesh.convex_hull
    
    # Export simplified OBJ file
    simple_obj_file = os.path.join(obj_folder, obj_name + '_simple.obj')
    simplified_mesh.export(simple_obj_file, include_normals=True, include_texture=False)
    
    # Get the texture file name without extension
    texture_filename = os.path.splitext(os.path.basename(texture_path))[0]
    
    # Rename the generated MTL file
    mtl_file = os.path.join(obj_folder, 'material.mtl')
    new_mtl_file = os.path.join(obj_folder, texture_filename + '.mtl')
    os.rename(mtl_file, new_mtl_file)
    
    # Update the MTL file content
    with open(new_mtl_file, 'r') as f:
        mtl_content = f.read()
    new_mtl_content = mtl_content.replace('material_0', texture_filename)
    with open(new_mtl_file, 'w') as f:
        f.write(new_mtl_content)
        
    # # Rename the texture file
    old_texture_file = os.path.join(obj_folder, 'material_0.png')
    new_texture_file = os.path.join(obj_folder, texture_filename + '.png')
    os.rename(old_texture_file, new_texture_file)
    
    with open(obj_file, 'r') as f:
        obj_content = f.read()
    new_obj_content = obj_content.replace('material_0', texture_filename)
    new_obj_content = new_obj_content.replace('material', texture_filename)
    with open(obj_file, 'w') as f:
        f.write(new_obj_content)

def main(input_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate through files in input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.ply'):
            ply_path = os.path.join(input_dir, filename)
            # ply_path = os.path.join(f"{input_dir}_eval", filename)
            # Check if corresponding texture file exists
            texture_filename = filename.replace('.ply', '.png')
            texture_path = os.path.join(input_dir, texture_filename)
            if os.path.isfile(texture_path):
                print(ply_path)
                convert_ply_to_obj(ply_path, texture_path, output_dir)
        # break

if __name__ == "__main__":
    input_dir = "models"
    output_dir = "models_ignition"
    main(input_dir, output_dir)

