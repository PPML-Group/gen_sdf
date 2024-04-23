import os
import trimesh

def generate_sdf_and_config(folder_path):
    # 获取子文件夹名字
    folder_name = os.path.basename(folder_path)
    
    obj_file = os.path.join(folder_path, folder_name + '.obj')
    mesh = trimesh.load_mesh(obj_file)
    inertia = mesh.moment_inertia/(1000**4)
    # print(inertia)
    
    # 构建SDF文件内容
    sdf_content = f'''<?xml version="1.0" ?>
<sdf version="1.7">
<!--
This SDF file was automatically generated using a template modified 
and authored by Jinjian Li. The moment of interia is not supposed to be changed.
-->
    <model name="{folder_name}">
      <pose>0.0 0.0 0.0 0.0 0.0 0.0</pose> 
      <link name="link">
        <inertial>
          <inertia>
           <ixx>{inertia[0, 0]}</ixx>
           <ixy>{inertia[0, 1]}</ixy>
           <ixz>{inertia[0, 2]}</ixz>
           <iyy>{inertia[1, 1]}</iyy>
           <iyz>{inertia[1, 2]}</iyz>
           <izz>{inertia[2, 2]}</izz>
          </inertia>
          <mass>1.0</mass>
        </inertial>
        <collision name="collision">
          <geometry>
            <mesh>
             <uri>{folder_name}.obj</uri>
             <scale>0.001 0.001 0.001</scale>
            </mesh>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <mesh>
             <uri>{folder_name}.obj</uri>
             <scale>0.001 0.001 0.001</scale>
            </mesh>
          </geometry>
        </visual>
      </link>
    </model>
</sdf>'''

    # 将SDF内容写入文件
    with open(os.path.join(folder_path, 'model.sdf'), 'w') as sdf_file:
        sdf_file.write(sdf_content)

    # 构建配置文件内容
    config_content = f'''<?xml version="1.0" ?>
<model>
    <name>{folder_name}</name>
    <version>1.0</version>
    <sdf version="1.7">model.sdf</sdf>
    <author>
        <name>jinjian li</name>
        <email>jinjian_l@163.com</email>
    </author>
    <description>{folder_name} in YCB-V Dataset</description>
</model>'''

    # 将配置文件内容写入文件
    with open(os.path.join(folder_path, 'model.config'), 'w') as config_file:
        config_file.write(config_content)

# 遍历每个子文件夹并生成对应的SDF文件和配置文件
models_dir = 'models_ignition'
for subdir in os.listdir(models_dir):
    subdir_path = os.path.join(models_dir, subdir)
    if os.path.isdir(subdir_path):
        generate_sdf_and_config(subdir_path)
