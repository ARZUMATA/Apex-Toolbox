# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Recolor operator module for Apex Toolbox addon."""

import bpy
import os
from ..config import mode, ast_fldr, my_path, fbs, blend_file, ap_node, loadImages, texSets

# Recolor
class BUTTON_CUSTOM2(bpy.types.Operator):
    """Operator for recoloring functionality."""
    bl_label = "BUTTON CUSTOM2"
    bl_idname = "object.button_custom2"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        rec_alpha = prefs.rec_alpha
        
        texSets_recolor = [
            ['albedoTexture'],
            ['specTexture'],
            ['emissiveTexture'],
            ['scatterThicknessTexture'],
            ['opacityMultiplyTexture'],
            ['normalTexture'],
            ['glossTexture'],
            ['aoTexture'],
            ['cavityTexture'],
            ['anisoSpecDirTexture'],
            ['iridescenceRampTexture']
        ]

        ttf_texSets = [
            ['col'],
            ['spc'],
            ['ilm'],
            ['nml'],
            ['gls'],
            ['ao']
        ]
        
        recolor_folder = prefs.recolor_folder
        
        # Check if Asset Folder installed
        if mode == 0:
            asset_folder_set = ast_fldr
        else:
            asset_folder_set = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
        
        assets_set = 0
        if os.path.exists(asset_folder_set) is True:
            asset_folder_set_split = asset_folder_set.split(fbs)[-2]
            if asset_folder_set_split == "Apex_Toolbox_Assets":
                if mode == 0:
                    asset_folder_set = ast_fldr
                else:
                    asset_folder_set = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
                assets_set = 1
        
        print("asset_folder_set: " + str(asset_folder_set))
        
        body_parts = [
            "head",
            "helmet",
            "hair",
            "eye",
            "eyecornea",
            "eyeshadow",
            "teeth",
            "body",
            "v_arms",
            "boots",
            "gauntlet",
            "jumpkit",
            "gear"
        ]
    
    # OPTION - 1 (Apex Shader)
        if prefs.cust_enum == 'OP1':
            print("\n######## RECOLORING MODEL: ########")
            if bpy.data.node_groups.get('Apex Shader') is None:
                selection = [obj.name for obj in bpy.context.selected_objects]
                bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename='Apex Shader')
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1
                print("Appended Apex Shader")

    # OPTION - 2 (Apex Shader+)
        if prefs.cust_enum == 'OP2':
            print("\n######## RECOLORING MODEL: ########")
            if bpy.data.node_groups.get('Apex Shader+_v3.4') is None:
                selection = [obj.name for obj in bpy.context.selected_objects]
                bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename='Apex Shader+_v3.4')
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1
                print("Apex Shader+ v3.4 Shader")
                
    # OPTION - 3 (S/G-Blender)
        if prefs.cust_enum == 'OP3':
            print("\n######## RECOLORING MODEL: ########")
            if bpy.data.node_groups.get('S/G-Blender') is None:
                selection = [obj.name for obj in bpy.context.selected_objects]
                bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename='S/G-Blender')
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1
                print("S/G Blender Shader")
                
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                for mSlot in o.material_slots:
                    MatNodeTree = bpy.data.materials[mSlot.name]
                    
                    mSlot_clean = mSlot.name
                    if "." in mSlot.name:
                        mSlot_clean = mSlot.name.split(".")[0]

                    try: 
                        foldername = recolor_folder.split(fbs)[-2] # folder name
                    except:
                        print("Materials Folder not selected")
                    else:    
                        foldernameSplit = foldername.split("_")[-1] # folder suffix _main _body to check for attachments
                        folderpath = recolor_folder 
                        imgBodyPart = mSlot_clean.split('_')[-1] # part name 
                        try:
                            ttf = mSlot_clean.split('_')[-2]  # TTF2 models
                        except:
                            continue
                        
                        exist = 0
                        weapon = 1
                        
                        for b in range(len(body_parts)):
                            if body_parts[b] in mSlot_clean:
                                weapon = 0
                                break

                        # Weapon Codes
                        if weapon == 1:
                            if foldername == "_images": # normal autotex
                                foldername = mSlot_clean
                                
                            if foldernameSplit != imgBodyPart: # check if this is attachment
                                foldername = mSlot_clean

                        # Legend Codes
                        if weapon == 0:
                            
                            # Check folders in the recolor folder
                            body_part_found = 0
                            subf_name = None
                            rec_dir = os.listdir(recolor_folder)
                            for x in range(len(rec_dir)):
                                if body_part_found == 1:
                                    break
                                else:
                                    for i in range(len(body_parts)):
                                        if body_parts[i] in rec_dir[x]:
                                            print("Found: " + body_parts[i] + " in " + rec_dir[x])
                                            body_part_found = 1
                                            subf_name = rec_dir[x].rsplit('_' + body_parts[i])[0]
                                            break  
                            
                            if foldername == "_images":              # normal autotex
                                foldername = mSlot_clean  
                            else:                                    # with sub folders
                                if body_parts[b] == "v_arms":        # with sub folders and check for v_arms in name
                                    folderpath = recolor_folder + foldername + "_" + body_parts[b]
                                    foldername = foldername + "_" + body_parts[b]  
                                else: 
                                    if subf_name is not None:
                                        if foldername != subf_name:
                                            foldername = subf_name
                                    folderpath = recolor_folder + foldername + "_" + imgBodyPart
                                    foldername = foldername + "_" + imgBodyPart
                                    if ttf == "skn":   # TTF Texturing
                                        folderpath = recolor_folder + mSlot_clean
                                        foldername = mSlot_clean
                                        texSets_recolor = ttf_texSets
            
                        # Check if albedo image exists, if not don't proceed clear nodes
                        texFile = folderpath + fbs + foldername + '_' + texSets_recolor[0][0] + ".png"

                        if os.path.isfile(texFile):
                            exist = 1
                        else:
                            if weapon == 0:
                                if assets_set == 1:
                                    texFile = asset_folder_set + "0. Legend_base" + fbs + mSlot_clean + '_' + texSets_recolor[0][0] + ".png" # Set path for Base files from assets folder
                                else:
                                    texFile = recolor_folder + "base" + fbs + mSlot_clean + '_' + texSets_recolor[0][0] + ".png" # check legend base files in the "Base" folder
                                if os.path.isfile(texFile):
                                    if assets_set == 1:
                                        folderpath = asset_folder_set + "0. Legend_base"
                                        foldername = mSlot_clean                                        
                                    else:
                                        folderpath = recolor_folder + "base"
                                        foldername = mSlot_clean
                                    exist = 1
                                if ttf == "skn":                                # TTF Try look different skin folders
                                    skn_name = mSlot_clean.rsplit('_', 2)[0]
                                    for s in ("_skn_02", "_skn_31"):
                                        texFile = recolor_folder + skn_name + s + fbs + skn_name + s + '_' + texSets_recolor[0][0] + ".png" # Set path for Base files from assets folder
                                        if os.path.isfile(texFile):
                                            print(texFile)
                                            folderpath = recolor_folder + skn_name + s
                                            foldername = skn_name + s
                                            exist = 1
                                            break

                        if exist == 1: 
                            MatNodeTree.node_tree.nodes.clear()
                            
                            for i in range(len(texSets_recolor)):
                                for j in range(len(texSets_recolor[i])):
                                    texFile = folderpath + fbs + foldername + '_' + texSets_recolor[i][j] + ".png"
                                    if os.path.isfile(texFile):                         # if texture is absent - skip it
                                        texImage = bpy.data.images.load(texFile)
                                    else:
                                        print(foldername + '_' + texSets_recolor[i][j] + ".png" + " Not in folder. Skipping.")
                                        texImage = None
                                    if texImage:
                                        ird_tex = False
                                        if i > 2:
                                            texImage.colorspace_settings.name = 'Non-Color'
                                        texImage.alpha_mode = 'CHANNEL_PACKED'
                                        texNode = MatNodeTree.node_tree.nodes.new('ShaderNodeTexImage')
                                        texNode.image = texImage
                                        texNode.name = str(i)
                                        if i == 10:
                                            ird_tex = True
                                            texNode.location = (750, -200)
                                        else:
                                            texNode.location = (-50, 50 - 260 * i)
                                        break 
                                    
                            # OPTION - 1 (Apex Shader)
                            if prefs.cust_enum == 'OP1':
                                NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                                NodeGroup.node_tree = bpy.data.node_groups.get('Apex Shader')
                                NodeGroup.location = (300, 0)
                                NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                                NodeOutput.location = (500, 0)
                                MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                                
                                if ttf == "skn":
                                    ColorDict = {
                                        "0": "Albedo Map",
                                        "1": "Specular Map",
                                        "2": "Emission",
                                        "3": "Normal Map",
                                        "4": "Glossiness Map",
                                        "5": "AO"
                                    }
                                else:
                                    ColorDict = {
                                        "0": "Albedo Map",
                                        "1": "Specular Map",
                                        "2": "Emission",
                                        "3": "SSS Map",
                                        "4": "Alpha",
                                        "5": "Normal Map",
                                        "6": "Glossiness Map",
                                        "7": "AO"
                                    }
                                AlphaDict = {
                                    "0": "Alpha",
                                    "3": "SSS Alpha",
                                }
                                
                            # OPTION - 2 (Apex Shader+)
                            if prefs.cust_enum == 'OP2':
                                NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                                NodeGroup.node_tree = bpy.data.node_groups.get('Apex Shader+_v3.4')
                                NodeGroup.location = (300, 0)
                                NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                                NodeOutput.location = (500, 0)
                                MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                                  
                                ColorDict = {
                                    "0": "Albedo",
                                    "1": "Specular",
                                    "2": "Emission",
                                    "3": "SSS Map",
                                    "4": "Alpha",
                                    "5": "Normal Map",
                                    "6": "Glossiness",
                                    "7": "Ambient Occlusion",
                                    "8": "Cavity"
                                }
                                AlphaDict = {
                                    "0": "Alpha",
                                    "3": "SSS Alpha",
                                }

                            # OPTION - 3 (S/G-Blender)
                            if prefs.cust_enum == 'OP3': 
                                NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                                NodeGroup.node_tree = bpy.data.node_groups.get('S/G-Blender')
                                NodeGroup.location = (300, 0)
                                NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                                NodeOutput.location = (500, 0)
                                MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                                
                                if ttf == "skn":
                                    ColorDict = {
                                        "0": "Diffuse map",
                                        "1": "Specular map",
                                        "2": "Emission input",
                                        "3": "Normal map",
                                        "4": "Glossiness map",
                                        "5": "AO map"
                                    }
                                else:
                                    ColorDict = {
                                        "0": "Diffuse map",
                                        "1": "Specular map",
                                        "2": "Emission input",
                                        "3": "Subsurface",
                                        "4": "Alpha input",
                                        "5": "Normal map",
                                        "6": "Glossiness map",
                                        "7": "AO map",
                                        "8": "Cavity map",
                                    }
                                AlphaDict = {
                                    "0": "Alpha input",
                                    "3": "SSS Alpha",
                                }
                                
                            if rec_alpha is True:
                                for slot in AlphaDict:
                                    try:
                                        MatNodeTree.node_tree.links.new(NodeGroup.inputs[AlphaDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Alpha"])
                                    except:
                                        pass
                            else:
                                pass

                            for slot in ColorDict:
                                try:
                                    MatNodeTree.node_tree.links.new(NodeGroup.inputs[ColorDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Color"])
                                except:
                                    pass
                            
                            mSlot.material.blend_method = 'HASHED'
                            print("Textured", mSlot_clean) 
                            print("  ")

                        else:
                            print("Material '" + mSlot_clean + "' Cannot be Textured") 
                            print("Image '" + foldername + '_' + texSets_recolor[0][0] + ".png' Not found in '" + folderpath + "'")
                            print("######### LOG FOR DEBUGGING #########")
                            print("recolor_folder: " + recolor_folder)
                            print("mSlot_clean: " + mSlot_clean)
                            print("foldername: " + foldername)
                            print("foldernameSplit: " + foldernameSplit)
                            print("imgBodyPart: " + imgBodyPart)
                            print("ttf: " + ttf)
                            print("texFile: " + texFile)
                            print("  ")  

        return {'FINISHED'}
