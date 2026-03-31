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

"""Toon AutoTex operator module for Apex Toolbox addon."""

import bpy
import os
from ..config import mode, ast_fldr, my_path, fbs, blend_file, ap_node, ap_collection, ap_material, ap_object, loadImages, texSets

# Toon Autotexture
class BUTTON_TOON(bpy.types.Operator):
    """Operator for Toon shader functionality."""
    bl_label = "BUTTON_TOON"
    bl_idname = "object.button_toon"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        
        skip = ['wraith_base_hair', 'wraith_base_eyecornea', 'wraith_base_eyeshadow', 'wraith_base_eye']
        
        selection = [obj.name for obj in bpy.context.selected_objects]
         
        # Append Toon Shader node group if it doesn't exist
        if bpy.data.node_groups.get('Apex ToonShader') is None:
            bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename='Apex ToonShader')
        
        # Append Toon Shader collection if it doesn't exist
        if bpy.data.collections.get('Apex ToonShader') is None:
            bpy.ops.wm.append(directory=my_path + blend_file + ap_collection, filename='Apex ToonShader')
        
        # Set render settings for Eevee
        scene.render.engine = 'BLENDER_EEVEE'
        context.space_data.shading.use_scene_lights = True
        context.space_data.shading.use_scene_world = True
        scene.eevee.taa_samples = 64
        # Blender 5.0: bloom settings moved to render_passes and tonemapper
        try:
            scene.eevee.use_bloom = True
        except AttributeError:
            pass  # Bloom handled differently in Blender 5.0
        try:
            scene.eevee.use_gtao = True
        except AttributeError:
            pass  # GTAO handled differently in Blender 5.0
        try:
            scene.eevee.use_shadow_high_bitdepth = True
        except AttributeError:
            pass  # Shadow bitdepth handled differently in Blender 5.0
        scene.view_settings.view_transform = 'Standard'
        scene.view_settings.look = 'Medium High Contrast'
        
        # Append Black Outline material if it doesn't exist
        mat = bpy.data.materials.get("Black Outline")
        if mat is None:
            bpy.ops.wm.append(directory=my_path + blend_file + ap_material, filename='Black Outline')
            mat = bpy.data.materials.get("Black Outline")
        
        # Select all objects in selection
        for x in range(len(selection)):
            bpy.data.objects[selection[x]].select_set(True)
            x += 1
            
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                isbase = False

                for i in range(len(skip)):
                    if skip[i] in o.material_slots:
                        isbase = True
                        break
                
                if isbase is False:
                    if "Black Outline" not in o.material_slots:
                        o.data.materials.append(mat)
                        # Add Solidify modifier for outline
                        exists = False
                        for mod in o.modifiers:
                            if mod.name == "OUTLINE_SOLIDIFY":
                                exists = True
                        if exists:
                            mod = o.modifiers["OUTLINE_SOLIDIFY"]
                            mod.thickness = -0.1
                        else: 
                            o.modifiers.new("OUTLINE_SOLIDIFY", "SOLIDIFY")
                            mod = o.modifiers["OUTLINE_SOLIDIFY"]
                            mod.use_flip_normals = True
                            mod.use_rim = False
                            mod.thickness = -0.1
                            mod.material_offset = 999
                    else:
                        pass
                else:
                    pass

                for mSlot in o.material_slots:
                    MatNodeTree = bpy.data.materials[mSlot.name]
                    try:
                        imageNode = MatNodeTree.node_tree.nodes["Image Texture"]
                    except:
                        print(MatNodeTree.name)
                        continue
                    try:
                        image = os.path.basename(os.path.abspath(imageNode.image.filepath))
                    except:
                        print(mSlot.name, "missing texture.")
                        continue
                    imagepath = os.path.dirname(os.path.abspath(imageNode.image.filepath))
                    imageType = imageNode.image.name.split(".")[0].split('_')[-1]
                    imageName = MatNodeTree.name
                    imageFormat = image.split('.')[1]
                    
                    if not any(imageType in x for x in texSets):
                        print(image, "could not be mapped.")
                        continue

                    # Clear existing nodes
                    MatNodeTree.node_tree.nodes.clear()
                    
                    # Load texture images
                    for i in range(len(texSets)):
                        for j in range(len(texSets[i])):
                            texImageName = imageName + '_' + texSets[i][j] + '.' + imageFormat
                            texImage = bpy.data.images.get(texImageName)
                            texFile = imagepath + fbs + texImageName
                            if not texImage and loadImages:
                                if os.path.isfile(texFile):
                                    texImage = bpy.data.images.load(texFile)
                            if texImage:
                                if i > 2:
                                    texImage.colorspace_settings.name = 'Non-Color'
                                texImage.alpha_mode = 'CHANNEL_PACKED'
                                texNode = MatNodeTree.node_tree.nodes.new('ShaderNodeTexImage')
                                texNode.image = texImage
                                texNode.name = str(i)
                                texNode.location = (-50, 50 - 260 * i)
                                break
                    
                    # Apply Toon Shader based on material type
                    if isbase:
                        if mSlot.name == 'wraith_base_eyecornea' or mSlot.name == 'wraith_base_eyeshadow':
                            NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                            NodeOutput.location = (800, 0)
                            node_transparency = MatNodeTree.node_tree.nodes.new(type="ShaderNodeBsdfTransparent")
                            node_transparency.location = 300, 200 
                            MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], node_transparency.outputs[0])
                        else:
                            NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                            NodeGroup.node_tree = bpy.data.node_groups.get('Apex ToonShader')
                            if 'Group' in MatNodeTree.node_tree.nodes:
                                MatNodeTree.node_tree.nodes['Group'].name = 'Apex ToonShader'
                            MatNodeTree.node_tree.nodes['Apex ToonShader'].label = 'Apex ToonShader'
                            NodeGroup.location = (300, 0)
                            NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                            NodeOutput.location = (800, 0)
                            
                            node_transparency = MatNodeTree.node_tree.nodes.new(type="ShaderNodeBsdfTransparent")
                            node_transparency.location = 300, 200
                            node_mix = MatNodeTree.node_tree.nodes.new(type="ShaderNodeMixShader")
                            node_mix.location = 500, 150
                                
                            MatNodeTree.node_tree.links.new(node_mix.inputs[1], node_transparency.outputs[0])
                            MatNodeTree.node_tree.links.new(node_mix.inputs[2], NodeGroup.outputs[0])
                            MatNodeTree.node_tree.links.new(node_mix.outputs[0], NodeOutput.inputs[0])
                            if mSlot.name == 'wraith_base_eye':
                                node_mix.inputs[0].default_value = 1 
                            
                        try:
                            MatNodeTree.node_tree.links.new(NodeGroup.inputs["--- Base Color ---"], MatNodeTree.node_tree.nodes[0].outputs["Color"])
                        except:
                            pass
                        
                        if mSlot.name == 'wraith_base_hair':
                            try:
                                MatNodeTree.node_tree.links.new(node_mix.inputs[0], MatNodeTree.node_tree.nodes[3].outputs["Color"])
                            except:
                                pass

                    else:
                        NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                        NodeGroup.node_tree = bpy.data.node_groups.get('Apex ToonShader')
                        if 'Group' in MatNodeTree.node_tree.nodes:
                            MatNodeTree.node_tree.nodes['Group'].name = 'Apex ToonShader'
                        MatNodeTree.node_tree.nodes['Apex ToonShader'].label = 'Apex ToonShader'
                        NodeGroup.location = (300, 0)
                        NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                        NodeOutput.location = (500, 0)
                        MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                         
                        ColorDict = {
                            "0": "--- Base Color ---",
                            "1": "--- Specular map ---",
                            "2": "--- Emission Map ---",
                        }
                                           
                        for slot in ColorDict:
                            try:
                                MatNodeTree.node_tree.links.new(NodeGroup.inputs[ColorDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Color"])
                            except:
                                pass
                    
                    mSlot.material.blend_method = 'HASHED'
                    print("Textured", mSlot.name)
                                   
        return {'FINISHED'}
