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
        mat_blackoutline = bpy.data.materials.get("Black Outline")
        if mat_blackoutline is None:
            bpy.ops.wm.append(directory=my_path + blend_file + ap_material, filename='Black Outline')
            mat_blackoutline = bpy.data.materials.get("Black Outline")
        
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
                        o.data.materials.append(mat_blackoutline)
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
                    
                    # Skip Black Outline material - use simple Color > Material Output without any shaders
                    if mSlot.name == "Black Outline":
                        continue
                    
                    # Define SHADER_CONFIGS for Toon Shader mapping (adapted from autotex.py)
                    TOON_SHADER_CONFIG = {
                        'toon': {
                            'node_group_name': 'Apex ToonShader',
                            'color_dict': {
                                "Albedo": "--- Base Color ---",
                                "Specular": "--- Specular map ---",
                                "Emission": "--- Emission Map ---",
                            },
                            'alpha_dict': {},  # No alpha mapping for toon shader in this context
                        }
                    }
                    
                    config = TOON_SHADER_CONFIG['toon']
                    node_group_name = config['node_group_name']
                    
                    # Apply Toon Shader based on material type (reuse existing image nodes, create fresh output)
                    
                    # Remove old shader nodes but keep image texture nodes
                    # Using list() to avoid modification during iteration issues
                    for node in list(MatNodeTree.node_tree.nodes):
                        should_remove = False
                        
                        # Check if it's a BSDF/SHADER type
                        if node.type == 'BSDF':
                            should_remove = True
                        
                        # Check for common old shader group names - remove them
                        elif node.type == 'GROUP' and node.node_tree:
                            if node.node_tree.name in ['Apex Shader', 'Apex Shader+_v3.4', 'S/G-Blender']:
                                should_remove = True
                            # Keep only Apex ToonShader, check its output type to be sure
                            elif node.node_tree.name == 'Apex ToonShader':
                                # Verify it's actually a ToonShader by checking outputs
                                is_toon_shader = False
                                if hasattr(node.node_tree, 'outputs') and len(node.node_tree.outputs) > 0:
                                    for out in node.node_tree.outputs:
                                        if out.name == 'Shader' or out.type == 'SHADER':
                                            is_toon_shader = True
                                            break
                                # If it's a ToonShader, keep it, otherwise remove
                                if not is_toon_shader:
                                    should_remove = True
                            else:
                                # Unknown group type - keep it
                                print("Unknown group type {1} for {2}. Keeping.", node.type, mSlot.name)
                                should_remove = False
                        
                        # Remove ALL output nodes (type is OUTPUT_MATERIAL) from previous setup
                        elif node.type == 'OUTPUT_MATERIAL':
                            should_remove = True
                        elif node.type == 'MIX_SHADER' and 'Mix' in node.name:
                            should_remove = True
                        elif node.type == 'BSDF_TRANSPARENT':
                            should_remove = True
                        
                        if should_remove:
                            MatNodeTree.node_tree.nodes.remove(node)
                    
                    # Create fresh Material Output node as needed
                    NodeOutput = None
                    
                    if isbase:
                        if mSlot.name == 'wraith_base_eyecornea' or mSlot.name == 'wraith_base_eyeshadow':
                            # Create fresh Material Output node
                            NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                            NodeOutput.location = (800, 0)
                            node_transparency = MatNodeTree.node_tree.nodes.new(type="ShaderNodeBsdfTransparent")
                            node_transparency.location = 300, 200
                            MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], node_transparency.outputs[0])
                        else:
                            # Create Toon Shader node group
                            NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                            NodeGroup.node_tree = bpy.data.node_groups.get(node_group_name)
                            
                            # Rename if duplicate exists
                            if 'Group' in MatNodeTree.node_tree.nodes:
                                MatNodeTree.node_tree.nodes['Group'].name = node_group_name
                            if node_group_name in MatNodeTree.node_tree.nodes:
                                MatNodeTree.node_tree.nodes[node_group_name].label = node_group_name
                            
                            NodeGroup.location = (300, 0)
                            
                            # Reuse existing output node or create new one
                            if NodeOutput is None:
                                NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                                NodeOutput.location = (800, 0)
                            
                            # Setup transparency mix for base materials
                            node_transparency = MatNodeTree.node_tree.nodes.new(type="ShaderNodeBsdfTransparent")
                            node_transparency.location = 300, 200
                            node_mix = MatNodeTree.node_tree.nodes.new(type="ShaderNodeMixShader")
                            node_mix.location = 500, 150
                                
                            MatNodeTree.node_tree.links.new(node_mix.inputs[1], node_transparency.outputs[0])
                            MatNodeTree.node_tree.links.new(node_mix.inputs[2], NodeGroup.outputs[0])
                            MatNodeTree.node_tree.links.new(node_mix.outputs[0], NodeOutput.inputs[0])
                            
                            if mSlot.name == 'wraith_base_eye':
                                node_mix.inputs[0].default_value = 1
                            
                            # Link existing texture nodes to Toon Shader inputs (adapted from autotex.py)
                            for slot_name, input_name in config['color_dict'].items():
                                try:
                                    tex_node = MatNodeTree.node_tree.nodes[slot_name]
                                    if hasattr(tex_node, 'image') and tex_node.image:
                                        MatNodeTree.node_tree.links.new(NodeGroup.inputs[input_name], tex_node.outputs["Color"])
                                except KeyError:
                                    # Texture node not found for this slot, skip
                                    pass
                            
                            # Special case for wraith_base_hair
                            if mSlot.name == 'wraith_base_hair':
                                try:
                                    hair_tex = MatNodeTree.node_tree.nodes['3']
                                    MatNodeTree.node_tree.links.new(node_mix.inputs[0], hair_tex.outputs["Color"])
                                except KeyError:
                                    pass
                    
                    else:
                        # Non-base material - apply Toon Shader with texture remapping (create fresh output node)
                        NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                        NodeGroup.node_tree = bpy.data.node_groups.get(node_group_name)
                        
                        if 'Group' in MatNodeTree.node_tree.nodes:
                            MatNodeTree.node_tree.nodes['Group'].name = node_group_name
                        if node_group_name in MatNodeTree.node_tree.nodes:
                            MatNodeTree.node_tree.nodes[node_group_name].label = node_group_name
                        
                        NodeGroup.location = (300, 0)
                        
                        # Create fresh Material Output node
                        NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                        NodeOutput.location = (500, 0)
                        
                        # Link Node Group Output to Material Output
                        MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                        
                        # Link existing texture nodes to Toon Shader inputs (adapted from autotex.py)
                        for slot_name, input_name in config['color_dict'].items():
                            try:
                                tex_node = MatNodeTree.node_tree.nodes[slot_name]
                                if hasattr(tex_node, 'image') and tex_node.image:
                                    MatNodeTree.node_tree.links.new(NodeGroup.inputs[input_name], tex_node.outputs["Color"])
                            except KeyError:
                                # Texture node not found for this slot, skip
                                pass
                    
                    mSlot.material.blend_method = 'HASHED'
                    print("Textured", mSlot.name)
                                   
        return {'FINISHED'}
