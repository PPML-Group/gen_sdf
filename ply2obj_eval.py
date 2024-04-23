import os
import trimesh
import shutil

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

def copy_rename_obj(models_eval_dir, output_dir):
    for filename in os.listdir(models_eval_dir):
        if filename.endswith('.ply'):
            ply_path = os.path.join(models_eval_dir, filename)
            obj_name = os.path.splitext(filename)[0]
            obj_folder = os.path.join(output_dir, obj_name)
            os.makedirs(obj_folder, exist_ok=True)
            
            obj_file = os.path.join(obj_folder, obj_name + '_simple.obj')
            # Load PLY file
            mesh = trimesh.load_mesh(ply_path)
            mesh.export(obj_file, include_texture=True)
        # break

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
    
    # # Copy and rename OBJ files from models_eval directory
    # models_eval_dir = input_dir + '_eval'
    # if os.path.exists(models_eval_dir):
    #     copy_rename_obj(models_eval_dir, output_dir)
        

if __name__ == "__main__":
    input_dir = "models"
    output_dir = "models_ignition"
    main(input_dir, output_dir)

