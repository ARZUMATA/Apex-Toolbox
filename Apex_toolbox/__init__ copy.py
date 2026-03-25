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

import bpy
import os
from bpy.types import Scene
from bpy.props import (BoolProperty,FloatProperty)
import requests
import webbrowser
import sys
import platform
import colorsys



    
    
    
    ####   Check for update addon  ####
    url = 'https://github.com/Gl2imm/Apex-Toolbox/releases.atom'
    try:
        full_text = requests.get(url, allow_redirects=True).text
    except:
        pass
    else:
        global lts_ver
        split_1 = full_text.split('521118368/')[1]
        lts_ver = split_1.split('</id>')[0]
    

    global addon_name
    global addon_ver 
    temp_ver = []   
    for mod_name in bpy.context.preferences.addons.keys():
        mod_name_split = mod_name.split("-")[0]
        for x in range(len(addon)):
            if mod_name_split == addon[x]:
                addon_name.append(mod_name_split)
                mod = sys.modules[mod_name]
                mod_ver = mod.bl_info.get('version', (-1, -1, -1))
                for i in range(len(mod_ver)):
                    temp_ver.append(str(mod_ver[i]))
                addon_ver.append('.'.join(temp_ver))
                del temp_ver[:]
         
        
    
############   AUTOTEX   ##############    
class BUTTON_CUSTOM(bpy.types.Operator):
    bl_label = "BUTTON CUSTOM"
    bl_idname = "object.button_custom"
    bl_options = {'REGISTER', 'UNDO'}
    
    dict_textures = {}

    def set_colorspace(self, img, colorspace):
        """Set image colorspace, fallback to 'Non-Color' if unknown."""

        if colorspace == 'Unknown':
            img.colorspace_settings.name = 'Non-Color'
            print(f"Warning: Unknown colorspace for {img} — using 'Non-Color'")
        else:
            img.colorspace_settings.name = colorspace


    def scan_textures(self, folder_path, recursive=True, max_depth=2):
        """Scan folder for image files and map to texture type. Optionally recursively with depth limit."""
        
        # Example output:
        # {
        #     'col.png': (
        #         'col',
        #         'sRGB',
        #         'Albedo',
        #         '/textures/char/loba_lgnd_v24_opbundle_body_col.png',
        #         (0.8, 0.2, 0.2)  # - Red
        #     ),
        #     'nml.png': (
        #         'nml',
        #         'Non-Color',
        #         'Normal Map',
        #         '/textures/char/loba_lgnd_v24_opbundle_body_nml.png',
        #         (0.2, 0.6, 0.8)  # - Light Blue
        #     )
        # }
        
        texture_map = {}  # {filename: (type, colorspace, shader_input, full_path, node_color)}

        if not os.path.isdir(folder_path):
            print(f"Folder not found: {folder_path}")
            return texture_map

        def walk_with_depth(root, current_depth=0):
            """Recursive walk with depth limit."""
            if max_depth is not None and current_depth > max_depth:
                return

            for item in os.listdir(root):
                item_path = os.path.join(root, item)
                if os.path.isfile(item_path):
                    ext = os.path.splitext(item)[1].lower()
                    if ext in IMAGE_EXTENSIONS:
                        # Extract base name (without extension)
                        base_name = os.path.splitext(item)[0]

                        # Try to extract texture type from end (e.g., 'catalyst_lgnd_v22_partybeach_body_col' - 'col')
                        parts = base_name.split('_')
                        texture_type = parts[-1]  # last part

                        # Search texSets for match (long or short name)
                        matched_entry = None

                        for entry in texSets:
                            names = entry[0]  # (long_name, short_name)
                            if texture_type in names:
                                matched_entry = entry
                                break
                        
                        if matched_entry:
                            colorspace, shader_input = matched_entry[1]
                            node_color = matched_entry[2]  # - RGB color from texSets
                        else:
                            colorspace = 'Non-Color' # Fallback here, not later
                            shader_input = 'Unknown'
                            node_color = (0.3, 0.3, 0.3) # Default gray
                            print(f"Unknown texture type: {texture_type} in {item}")

                        texture_map[item] = (texture_type, colorspace, shader_input, item_path, node_color)

                elif os.path.isdir(item_path) and recursive:
                    walk_with_depth(item_path, current_depth + 1)

        walk_with_depth(folder_path)

        return texture_map

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        texture_folder = prefs.texture_folder

        # Get texture folder from prefs
        if not texture_folder:
            print("texture_folder is not set. Skipping texture assignment.")
            return

        texture_map = self.scan_textures(texture_folder)

        # ColorDict
        #   Define Input Mapping Dictionaries. Idx , Input name in the node group.
        #   These names must match exactly the input names in the node group.
        #   Example:
        #   Texture node 0 - links to input "Albedo"
        #   Texture node 1 - links to input "Specular"

        # AlphaDict

        #   Maps texture node index to alpha input names in the node group.
        #   Link Alpha channel (transparency) from texture nodes to specific inputs.
        #   For materials that use alpha for transparency or subsurface scattering.
        #   Example:
        #   Texture node 0 - links its Alpha output to node group input "Alpha"
        #   Texture node 3 - links its Alpha output to node group input "SSS Alpha"

        # Before Gl2imm used:
        # MatNodeTree.node_tree.nodes["Image Texture"] or MatNodeTree.node_tree.nodes["0"]
        # and it's 'imageNode.image.filepath' in order to get path, load all textures and assign them based on their type.
        # Some RSX exports have that part missing and if you recolate textures it all goes wrong.
        # Also it uses same from as recolor one so we can rewrite it and use texture/recolor by simply pointing it to the folder we need.

        # Define shader configurations for each option
        SHADER_CONFIGS = {
            'OP1': {
                'node_group_name': 'Apex Shader',
                'color_dict': {
                    "Albedo" : "Albedo Map",
                    "Specular" : "Specular Map",
                    "Emission" : "Emission",
                    "SSS Map" : "SSS Map",
                    "Alpha" : "Alpha",
                    "Normal Map" : "Normal Map",
                    "Glossiness" : "Glossiness Map",
                    "Ambient Occlusion" : "AO"
                },
                'alpha_dict': {
                    "Alpha": "Alpha",
                    "SSS Alpha": "SSS Alpha",
                }
            },
            'OP2': {
                'node_group_name': 'Apex Shader+_v3.4',
                'color_dict': {
                    "Albedo": "Albedo",
                    "Specular": "Specular",
                    "Emission": "Emission",
                    "SSS Map": "SSS Map",
                    "Alpha": "Alpha",
                    "Normal Map": "Normal Map",
                    "Glossiness": "Glossiness",
                    "Ambient Occlusion": "Ambient Occlusion",
                    "Cavity": "Cavity"
                },
                'alpha_dict': {
                    "Alpha": "Alpha",
                    "SSS Alpha": "SSS Alpha",
                }
            },
            'OP3': {
                'node_group_name': 'S/G-Blender',
                'color_dict': {
                    "Albedo": "Diffuse map",
                    "Specular": "Specular map",
                    "Emission": "Emission input",
                    "Subsurface": "Subsurface",
                    "Alpha input": "Alpha input",
                    "Normal Map": "Normal map",
                    "Glossiness": "Glossiness map",
                    "Ambient Occlusion": "AO map",
                    "Cavity map": "Cavity map",
                },
                'alpha_dict': {
                    "Alpha": "Alpha",
                    "SSS Alpha": "SSS Alpha",
                }
            }
        }

        # Get selected objects once
        selection = [obj.name for obj in bpy.context.selected_objects]

        # Append node group if it doesn't exist
        config = SHADER_CONFIGS.get(prefs.cust_enum2)
        if config:
            node_group_name = config['node_group_name']
            if bpy.data.node_groups.get(node_group_name) is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename=node_group_name)
                for obj_name in selection:
                    bpy.data.objects[obj_name].select_set(True)

        # Loop through every object currently selected in the Blender viewport.
        for o in bpy.context.selected_objects:

            # Only process mesh objects (not lights, cameras, empties, etc.).
            if o.type != 'MESH':
                continue

            # Loop through all material slots assigned to this mesh object.
            # A mesh can have multiple materials (e.g., for different parts of the mesh).
            for mSlot in o.material_slots:
                    
                # Get the actual material from Blender’s global data block.
                MatNodeTree = bpy.data.materials[mSlot.name]
                
                # mSlot.name we need to find our texture based on it's name
                material_name = mSlot.name  # e.g., 'loba_lgnd_v24_opbundle_body'

                # This completely removes all the nodes.
                # Not good especially if you retexture or have custom setup.
                # All existing nodes (Image Texture, Principled BSDF, Mix Shader, etc.) are removed.
                # The material becomes empty — no shader, no textures, no connections.
                # We gotta rebuild the node tree from scratch.
                # TODO: Keep texture nodes and simpy load new texture.
                MatNodeTree.node_tree.nodes.clear()
                
                        # Filter texture_map: only entries where full_path contains material_name
                local_texture_map = {
                    filename: (type_, colorspace, shader_input, full_path, node_color)
                    for filename, (type_, colorspace, shader_input, full_path, node_color) in texture_map.items()
                            if material_name in full_path
                }

                for filename, (type_, colorspace, shader_input, full_path, node_color) in local_texture_map.items():
                    # Now we have:
                    # filename - e.g. 'col.png'
                    # colorspace - e.g. 'sRGB'
                    # shader_input - e.g. 'Albedo'
                    # full_path - e.g. '/textures/char/loba_lgnd_v24_opbundle_body_col.png'
                    print(f"Processing {filename}: {colorspace} - {shader_input}")
                    
                    # If image esists in all loaded images in the current .blend file.
                    texImage = bpy.data.images.get(filename)

                            # Not found. Load it then.
                    if not texImage and loadImages:
                        if os.path.isfile(full_path):
                            texImage = bpy.data.images.load(full_path)

                    if texImage:
                                # Set colorspace
                        self.set_colorspace(texImage, colorspace)
                        texImage.alpha_mode = 'CHANNEL_PACKED'
                        
                                # Create texture node
                        texNode = MatNodeTree.node_tree.nodes.new('ShaderNodeTexImage')
                        texNode.image = texImage
                        texNode.name = str(shader_input)
                        texNode.label = str(shader_input)
                        texNode.location = (-50, 50 - 260 * len(MatNodeTree.node_tree.nodes)) # Auto-position

                                # Apply color
                        texNode.use_custom_color = True
                        texNode.color = node_color

                # Create a material node setup using a ShaderNodeGroup (like Apex Shader), link texture nodes (created earlier) to its inputs, and set the material to use HASHED blend mode.

                # Creates a new ShaderNodeGroup node in the material’s node tree.
                # This node will act as a wrapper for a pre-defined node group (like a custom shader graph).
                NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')

                # Assign the actual node group named 'like Apex Shader' to this node.
                NodeGroup.node_tree = bpy.data.node_groups.get(node_group_name)

                # Set Node Group Location
                NodeGroup.location = (300,0)

                # Creates the final output node where the material’s shader result goes to the renderer.
                # Every material must have at least one ShaderNodeOutputMaterial.
                NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')

                # Set Output Node Location
                NodeOutput.location = (500,0)
                
                # Link Node Group Output to Material Output
                MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])

                # Link Alpha Inputs

                # For each entry in AlphaDict:
                # slot = texture node index (e.g., "0")
                # AlphaDict[slot] = input name in node group (e.g., "Alpha")
                # MatNodeTree.node_tree.nodes[slot] = the texture node at that index
                # .outputs["Alpha"] = the Alpha channel output of that texture node
                # Create a link from texture node’s Alpha - node group’s Alpha input
                # We control transparency or SSS thickness using the alpha channel of a texture.

                for slot, input_name in config['alpha_dict'].items():
                    try:
                        MatNodeTree.node_tree.links.new(
                            NodeGroup.inputs[input_name],
                            MatNodeTree.node_tree.nodes[slot].outputs["Alpha"]
                        )
                    except:
                        pass

                # Link Color Inputs

                # For each entry in ColorDict:
                # Links the Color output of the texture node - the corresponding color input in the node group.
                # Example:
                # Texture node 0 - Color output - node group input "Albedo"
                # Texture node 5 - Color output - node group input "Normal Map"
                for slot, input_name in config['color_dict'].items():
                    try:
                        MatNodeTree.node_tree.links.new(
                            NodeGroup.inputs[input_name],
                            MatNodeTree.node_tree.nodes[slot].outputs["Color"]
                        )
                    except:
                        pass

                # Set Blend Method

                # Sets the material’s blend mode to HASHED.
                # This is used for transparency with alpha testing (like eyelashes).
                # Other common values:
                # 'OPAQUE' - no transparency
                # 'BLEND' - smooth transparency (slower)
                # 'HASHED' - fast alpha testing (good for performance)
                # Required for materials that use alpha maps to cut out parts of the mesh.
                mSlot.material.blend_method = 'HASHED'

                print("Textured", mSlot.name)

        return {'FINISHED'}

    
    #PANEL UI
####################################
class AUTOTEX_MENU(bpy.types.Panel):
    bl_label = "Apex Toolbox (" + ver + ")"
    bl_idname = "OBJECT_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Apex Tools"
    
    
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prefs = scene.my_prefs  
            
                   
        ######## Update Notifier ########
        if lts_ver > ver:
            box = layout.box()
            #box.label(text = "Addon Update Available: " + lts_ver, icon='IMPORT') 
            box.operator('object.lgndtranslate_url', text = "Addon Update Available: " + lts_ver, icon='IMPORT').link = "update"
            
        ######## ASSETS ########                
        if mode == 0:
            addon_assets = prefs
            folder = 'recolor_folder'
        else:
            addon_assets =bpy.context.preferences.addons['Apex_toolbox'].preferences
            folder = 'asset_folder'
        
        ######## Check if Asset Folder installed ######## 
        if mode == 0:
            asset_folder = ast_fldr
            asset_folder_set = asset_folder
        else:
            asset_folder_set =bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
        assets_set = 0

        if os.path.exists(asset_folder_set) == True:
            asset_folder_set = asset_folder_set.split(fbs)[-2]
            if asset_folder_set == "Apex_Toolbox_Assets":
                assets_set = 1            
        
        if assets_set != 1:
            mode_ver = '"Lite"'
            mode_ico = 'PANEL_CLOSE'
        else:
            mode_ver = '"Extended"'
            mode_ico = 'CHECKMARK'
            
        row = layout.row()
        row.label(text = "Current Mode:  " + mode_ver, icon=mode_ico)
          
                        
        ######### Readme First ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_readme else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_readme', icon=icon, icon_only=True)
        row.label(text = "Readme First", icon= "QUESTION")
        # some data on the subpanel
        if context.scene.subpanel_readme:
            box = layout.box()
            #box.label(text = "All Credits, Help and Instructions, Credits")
            #box.label(text = "inside this addon .zip file")
            box.operator('object.lgndtranslate_url', text = "Read Instructions, Credits", icon='ARMATURE_DATA').link = "instructions"
            box.operator('object.lgndtranslate_url', text = "Read Version Log", icon='CON_ARMATURE').link = "version" 
            if assets_set != 1:
                box.label(text = "To install extra assets go to")
                box.operator('object.lgndtranslate_url', text = "Assets File", icon='IMPORT').link = "asset_file"
                box.label(text = "Download, unzip and specify below")
                box.label(text = "folder name must be 'Apex_Toolbox_Assets'")
                box.label(text = "addon recognize only this folder")     
            row = layout.row()
            #row = layout.row()
            
            box.prop(addon_assets, folder)
            
            
            row.label(text = "------------------------------------------------------")
        
        row = layout.row()
        row.operator('object.ef_button_spawn', text = "Set Correct Model Size").cool_effect = 'adjust_model'

        ######### Auto_tex ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_status_0 else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_status_0', icon=icon, icon_only=True)
        row.label(text = "Auto_tex (by llenoco)", icon= "TEXTURE")
        # some data on the subpanel
        if context.scene.subpanel_status_0:           
            box = layout.box()
            box.prop(prefs, "cust_enum2")

            box = layout.box()
            box.label(text = "Select Texture Folder")
            box.prop(prefs, 'texture_folder')
            

            split = box.split(factor = 0.5)
            col = split.column(align = True)
            split.operator("object.button_custom", text = "Texture Model")
            row = layout.row()
            row.label(text = "------------------------------------------------------")            
 
 
        ######### Auto_shadow ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_shadow else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_shadow', icon=icon, icon_only=True)
        row.label(text = "Auto_shadow (Beta)", icon= "GHOST_ENABLED")
        # some data on the subpanel
        if context.scene.subpanel_shadow:           
            box = layout.box()
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            col.label(text = "Select mesh:")
            split.operator("object.button_shadow", text = "Shadow It").shadow = "Shadow"
            split = box.split(factor = 0.3)
            col = split.column(align = True)
            col.label(text='Eyes:')
            split.operator('object.button_shadow', text = "Adjust and Parent").shadow = "Eyes_parent"  
            box.label(text='*Select Only Legend bones for parenting')           
            row = layout.row()
            row.label(text = "------------------------------------------------------") 
            
 
        ######### Auto_toon ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_toon else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_toon', icon=icon, icon_only=True)
        row.label(text = "TOON Auto_tex", icon= "UV")
        # some data on the subpanel
        if context.scene.subpanel_toon:           
            box = layout.box()
            box.operator('object.lgndtranslate_url', text = "Read Instructions", icon='INFO').link = "toon_shader"
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            col.label(text = "Select mesh then:")
            split.operator("object.button_toon", text = "Toon It")
            
            key_lights = bpy.data.collections.get('Apex ToonShader')                        
            if key_lights != None:
                if bpy.context.selected_objects != None: 
                    try:
                        act_mat = bpy.context.object.active_material
                    except:
                        pass
                    try:
                        toon_shader = bpy.context.object.active_material.node_tree.nodes['Apex ToonShader']
                    except:
                        pass
                    else:
                        box.label(text="")
                        box.label(text="Shader Key Settings:")
                        set_1 = toon_shader.inputs[4]
                        set_2 = toon_shader.inputs[5]
                        set_3 = toon_shader.inputs[6]
                        set_4 = toon_shader.inputs[7]
                        set_5 = toon_shader.inputs[8]
                        set_6 = toon_shader.inputs[11]
                        set_7 = toon_shader.inputs[12]
                        set_8 = toon_shader.inputs[13]
                        set_9 = toon_shader.inputs[21]                        
                        
                        split = box.split(factor = 0.5)
                        col = split.column(align = True)
                        col.label(text=set_1.name)
                        split.prop(set_1, "default_value", text = "")
                        split = box.split(factor = 0.5)
                        col = split.column(align = True)
                        col.label(text=set_2.name)
                        split.prop(set_2, "default_value", text = "")
                        split = box.split(factor = 0.5)
                        col = split.column(align = True)
                        col.label(text=set_3.name)
                        split.prop(set_3, "default_value", text = "")
                        split = box.split(factor = 0.5)
                        col = split.column(align = True)
                        col.label(text=set_4.name)
                        split.prop(set_4, "default_value", text = "")
                        split = box.split(factor = 0.5)
                        col = split.column(align = True)
                        col.label(text=set_5.name)
                        split.prop(set_5, "default_value", text = "")
                        split = box.split(factor = 0.5)
                        col = split.column(align = True)
                        col.label(text='Reflection Color')
                        split.prop(set_6, "default_value", text = "")
                        split = box.split(factor = 0.5)
                        col = split.column(align = True)
                        col.label(text=set_7.name)
                        split.prop(set_7, "default_value", text = "")
                        split = box.split(factor = 0.5)
                        col = split.column(align = True)
                        col.label(text=set_8.name)
                        split.prop(set_8, "default_value", text = "")
                        split = box.split(factor = 0.5)
                        col = split.column(align = True)
                        col.label(text=set_9.name)
                        split.prop(set_9, "default_value", text = "")
                        box.label(text="If Shadow Glitchy - Set 'None'")
                        split = box.split(factor = 0.5)
                        col = split.column(align = True)
                        col.label(text='Shadow')
                        split.prop(act_mat, "shadow_method", text = "")
                        
    
                
                box.label(text="")
                box.label(text="Settings Modified by Addon:")
                box.label(text="-- Optional Settings (Can change): --")
                box.prop(bpy.context.scene.render, "film_transparent", text = "Transparent background")
                box.prop(bpy.context.scene.view_settings, "view_transform", text = "Color")
                box.prop(bpy.context.scene.view_settings, "look")
                
                box.label(text="")
                box.label(text="-- Settings needed for Shader: --")                
                box.prop(bpy.context.scene.render, "engine")
                box.prop(bpy.context.space_data.shading, "use_scene_lights")
                box.prop(bpy.context.space_data.shading, "use_scene_world")
                box.prop(bpy.context.scene.eevee, "taa_samples")
                box.prop(bpy.context.scene.eevee, "use_bloom")
                box.prop(bpy.context.scene.eevee, "use_gtao")
                box.prop(bpy.context.scene.eevee, "use_shadow_high_bitdepth")

            '''
            wrld_0 = bpy.data.worlds[wrld].node_tree.nodes['Background'].inputs['Strength']
            if wrld != 'World':
                wrld_1 = bpy.data.worlds[wrld].node_tree.nodes['Mapping'].inputs['Rotation']                     
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            col.label(text='Brightness:')
            split.prop(wrld_0, "default_value", text = "")
            '''    
            row = layout.row()
            row.label(text = "------------------------------------------------------")            
                    
        
        ######### Re-color ###########
        # subpanel
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_status_1 else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_status_1', icon=icon, icon_only=True)
        row.label(text = "Re-color", icon = "NODE_TEXTURE")
        # some data on the subpanel
        if context.scene.subpanel_status_1:
            box = layout.box()
            box.label(text = "Select Texture Folder")
            box.prop(prefs, 'recolor_folder')
            
            #aa = bpy.ops.buttons.directory_browse
            #box.prop(bpy.ops.buttons.directory_browse, 'relative_path')
            #box.prop(bpy.context.preferences.filepaths, 'use_relative_paths')
            #print(os.path.realpath(prefs.recolor_folder))
            
            box.prop(prefs, 'rec_alpha')
            box.prop(prefs, 'cust_enum')
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            split.operator("object.button_custom2", text = "Re-Color")
            row = layout.row()
            row.label(text = "------------------------------------------------------")
            
        
        ######### Append Shader ###########
        # subpanel
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_status_2 else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_status_2', icon=icon, icon_only=True)

        row.label(text = "Append Shaders & HDRI", icon= "NODE_MATERIAL")
        # some data on the subpanel
        if context.scene.subpanel_status_2:
            box = layout.box()   
            box.prop(prefs, 'cust_enum_shader')
            split = box.split(factor = 0.6)
            col = split.column(align = True)
            split.operator("object.button_shaders", text = "Add Shader")       
            if assets_set == 0:
                box.prop(prefs, 'cust_enum_hdri_noast', text = "HDRI")
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text = "")
                split.operator("object.button_hdrifull", text = "Set as HDRI").hdri = "hdri_noast"  
            else:
                box.prop(prefs, 'cust_enum_hdri')
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.operator("object.button_hdrifull", text = "Set as Sky").hdri = "background"
                split.operator("object.button_hdrifull", text = "Set as HDRI").hdri = "hdri"    
            try:
                wrld = bpy.context.scene.world.name
            except:
                pass
            else:
                box.label(text='** Current World/HDRI Controls: **')
                wrld_0 = bpy.data.worlds[wrld].node_tree.nodes['Background'].inputs['Strength']
                if wrld != 'World':
                    wrld_1 = bpy.data.worlds[wrld].node_tree.nodes['Mapping'].inputs['Rotation']                     
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(wrld_0, "default_value", text = "")
                if wrld != 'World':
                    split = box.split(factor = 0.5)
                    col = split.column(align = True)
                    col.label(text='Rotation:')
                    split.prop(wrld_1, "default_value", text = "")                    
            
            if assets_set == 0:
                pass
            else:                         
                box.label(text = "*Set as Sky - just a background")
                box.label(text = "*Set as HDRI - apply lights")
                box.label(text = "*Not all images can set as Sky")
                
            row = layout.row()
            row.label(text = "------------------------------------------------------")


        ######### Animation ###########
        # subpanel
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_ikbone else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_ikbone', icon=icon, icon_only=True)

        row.label(text = "Animation & Bones", icon= "BONE_DATA")
        # some data on the subpanel
        if context.scene.subpanel_ikbone:
            box = layout.box() 
            try:
                if len(bpy.context.selected_objects) == 1: 
                    box.prop(bpy.context.object, 'show_in_front', text='Show Bones In Front')
                    box.prop(bpy.context.object.data, 'show_names', text='Show Bones Names')
                else:
                    box.enabled = False
                    box.label(text='Select Bones', icon='ERROR')                    
            except:
                pass
                            
            box.label(text = "Select Legend Bones Then:")
            box.operator("object.button_ikbone", text = "Add IK Bones")  
                
            row = layout.row()
            row.label(text = "------------------------------------------------------")
            
            
            
        row = layout.row()  
        row = layout.row()   
        row.operator('object.lgndtranslate_url', text = "Biast12 Apex PC Assets", icon='URL').link = "biast_archive"
        row = layout.row()   
        row.operator('object.lgndtranslate_url', text = "Garlicus Skins list", icon='URL').link = "garlicus_list"
        row = layout.row()  
        row.operator('object.lgndtranslate_url', text = "Toolbox Discord Server", icon='ORIENTATION_GIMBAL').link = "discord"  
        row = layout.row() 
        row.operator('object.lgndtranslate_url', text = "Buy me a Coffee! ;)", icon='URL').link = "buy coffee"          



######### Apex effects Tab ########### 
class EFFECTS_PT_panel(bpy.types.Panel):
    bl_parent_id = "OBJECT_PT_panel"
    bl_label = "APEX EFFECTS COLLECTION"  
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_options = {"DEFAULT_CLOSED"}
    

    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prefs = scene.my_prefs
        
        
        if mode == 0:
            asset_folder = ast_fldr
            asset_folder_set = asset_folder
        else:
            asset_folder_set =bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
        assets_set = 0

        if os.path.exists(asset_folder_set) == True:
            asset_folder_set = asset_folder_set.split(fbs)[-2]
            if asset_folder_set == "Apex_Toolbox_Assets":
                assets_set = 1
        
                        
        ######### Wraith #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_wraith else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_wraith', icon=icon, icon_only=True)
        row.label(text='Wraith')
        # some data on the subpanel
        if context.scene.subpanel_effects_wraith:
            box = layout.box()
            
            # Wraith subpanel 1
            box.operator("object.wr_button_portal", text = "Spawn Portal")
            
            try:
                obj = bpy.data.objects['wraith_portal']
            except:
                pass
            else:
                obj = 'wraith_portal'
                portal_0 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[0]
                portal_1 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[1]
                portal_2 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[2]
                portal_3 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[3]
                portal_4 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[4]
                portal_5 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[5]
                portal_6 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[6]
                portal_7 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[7]
                portal_8 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[8]
                portal_9 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[9]
                portal_10 = bpy.data.objects[obj].active_material.node_tree.nodes['Wraith Portal'].inputs[10]
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Center Transparency:')
                split.prop(portal_0, "default_value", text = "")
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Outer Ring-1:')
                split.prop(portal_1, "default_value", text = "")
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(portal_2, "default_value", text = "")
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Outer Ring-2:')
                split.prop(portal_3, "default_value", text = "")
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(portal_4, "default_value", text = "")  
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Outer Ring-3:')
                split.prop(portal_5, "default_value", text = "")
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(portal_6, "default_value", text = "")  
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Inner Ring-1:')
                split.prop(portal_7, "default_value", text = "")
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(portal_8, "default_value", text = "")  
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Inner Ring-2:')
                split.prop(portal_9, "default_value", text = "")
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(portal_10, "default_value", text = "")                                                                                

            """
            # Wraith subpanel 2
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_wraith_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_wraith_prop1', icon=icon, icon_only=False, text='Wraith with properties')
            # some data on the subpanel
            if context.scene.subpanel_effects_wraith_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='1.')
                split.operator("object.wr_button_portal", text = "Spawn Portal") 
            """           

        ######### Gibraltar #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_gibby else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_gibby', icon=icon, icon_only=True)
        row.label(text='Gibraltar')
        # some data on the subpanel
        if context.scene.subpanel_effects_gibby:
            box = layout.box()
            
            # Gibraltar subpanel 1
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_gibby_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_gibby_prop1', icon=icon, icon_only=False, text='Dome Shield                          ')
            # some data on the subpanel
            if context.scene.subpanel_effects_gibby_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.gb_button_items', text = "Friendly").gibby = "Gibby bubble friendly"
                split.operator('object.gb_button_items', text = "Enemy").gibby = "Gibby bubble enemy"
                
                

        ######### Mirage #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_mirage else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_mirage', icon=icon, icon_only=True)
        row.label(text='Mirage')
        # some data on the subpanel
        if context.scene.subpanel_effects_mirage:
            box = layout.box()
            
            # Mirage subpanel 1
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_mirage_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_mirage_prop1', icon=icon, icon_only=False, text='Decoy                                    ')
            # some data on the subpanel
            if context.scene.subpanel_effects_mirage_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.mr_button_decoy', text = "Add Effect").mr_decoy = "Decoy"
                split.operator('object.mr_button_decoy', text = "Parent it").mr_decoy = "Decoy_parent" 
                box.label(text='*Sel Legend before add Effect')
                box.label(text='*Sel Model Bones before Parenting')
                
            
            """
            # Mirage subpanel 2
            box.operator("object.wr_button_portal", text = "Spawn Portal")
            """     


        ######### Valkyrie #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_valkyrie else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_valkyrie', icon=icon, icon_only=True)
        row.label(text='Valkyrie')
        # some data on the subpanel
        if context.scene.subpanel_effects_valkyrie:
            box = layout.box()
            
            # Mirage subpanel 1
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_valkyrie_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_valkyrie_prop1', icon=icon, icon_only=False, text='Flames                                    ')
            # some data on the subpanel
            if context.scene.subpanel_effects_valkyrie_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.vk_button_items', text = "Add Flames").valk = "Flames"
                split.operator('object.vk_button_items', text = "Parent them").valk = "Flames_parent" 
                box.label(text='*Sel Model Bones before Parenting')
                
            
            """
            # Mirage subpanel 2
            box.operator("object.wr_button_portal", text = "Spawn Portal")
            """    
            

        ######### Seer #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_seer else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_seer', icon=icon, icon_only=True)
        row.label(text='Seer')
        # some data on the subpanel
        if context.scene.subpanel_effects_seer:
            box = layout.box()
            
            # Seer subpanel 1
            for n in range(len(all_seer_items)):
                if n == 0:
                    box.operator('object.seer_button_spawn', text = all_seer_items.get(str(n))).lgnd_effect = all_seer_items.get(str(n)) 
            
            try:
                obj = bpy.data.objects['Seer Ultimate']
                obj2 = bpy.data.objects['Seer ult circle']
            except:
                pass
            else:
                obj = 'Seer Ultimate'
                obj2 = 'Seer ult circle'
                seer_ult_0 = bpy.data.objects[obj].material_slots[0].material.node_tree.nodes['Mix.001'].inputs['Color1'] 
                seer_ult_1 = bpy.data.objects[obj].material_slots[0].material.node_tree.nodes['Emission'].inputs['Strength'] 
                seer_ult_2 = bpy.data.objects[obj2].active_material.node_tree.nodes['Mix.001'].inputs['Color1'] 
                seer_ult_3 = bpy.data.objects[obj2].active_material.node_tree.nodes['Emission'].inputs['Strength']
                seer_ult_4 = bpy.data.objects[obj].material_slots[1].material.node_tree.nodes['Mix.001'].inputs['Color1']
                seer_ult_5 = bpy.data.objects[obj].material_slots[1].material.node_tree.nodes['Emission'].inputs['Strength']

                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Cage Color:')
                split.prop(seer_ult_0, "default_value", text = "")
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(seer_ult_1, "default_value", text = "")
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Cage Bottom Color:')
                split.prop(seer_ult_4, "default_value", text = "")
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(seer_ult_5, "default_value", text = "")                  
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Node Color:')
                split.prop(seer_ult_2, "default_value", text = "") 
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(seer_ult_3, "default_value", text = "")                                                                                         


            """
            # Wraith subpanel 2
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_wraith_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_wraith_prop1', icon=icon, icon_only=False, text='Wraith with properties')
            # some data on the subpanel
            if context.scene.subpanel_effects_wraith_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='1.')
                split.operator("object.wr_button_portal", text = "Spawn Portal") 
            """     
            
            
        ######### Weapons #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_weapons else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_weapons', icon=icon, icon_only=True)
        row.label(text='Weapons')
        # some data on the subpanel
        if context.scene.subpanel_effects_weapons:
            box = layout.box()
            
            
            # Laser subpanel
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_weapons_laser else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_weapons_laser', icon=icon, icon_only=False, text='Weapon Laser                        ')
            # some data on the subpanel
            if context.scene.subpanel_effects_weapons_laser:
                box.operator('object.wpn_button_spawn', text = "Add Laser").weapon = "Laser"
                try:
                    obj = bpy.data.objects['Laser_pt1']
                except:
                    pass
                else:
                    laser_color = bpy.data.objects['Laser_pt1'].active_material.node_tree.nodes['Mix'].inputs['Color1']
                    laser_emis = bpy.data.objects['Laser_pt1'].active_material.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Set Color:')
                    split.prop(laser_color, "default_value", text = "")
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Emissive:')
                    split.prop(laser_emis, "default_value", text = "")                                     
                split = box.split(factor = 0.3)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.wpn_button_spawn', text = "1. Parent Laser").weapon = "Laser_parent"
                split = box.split(factor = 0.3)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.wpn_button_spawn', text = "2. Adjust Laser").weapon = "Laser_move" 
                box.label(text='*Select weapon bones for 1 & 2') 
                
          
    
               

            # Flatline subpanel 1
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_weapons_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_weapons_prop1', icon=icon, icon_only=False, text='Flatline Flames (v20_assim)')
            # some data on the subpanel
            if context.scene.subpanel_effects_weapons_prop1:
                box.operator('object.wpn_button_spawn', text = "Add Normal gun Effect (w)").weapon = "flatline_s4_glow_hex_LOD0_SEModelMesh.125"
                try:
                    obj = bpy.data.objects['flatline_s4_glow_hex_LOD0_SEModelMesh.125']
                except:
                    pass
                else:
                    obj = 'flatline_s4_glow_hex_LOD0_SEModelMesh.125'
                    w_flames_color = bpy.data.objects[obj].active_material.node_tree.nodes['Group'].inputs['Color']
                    w_flames_emis = bpy.data.objects[obj].active_material.node_tree.nodes['Group'].inputs['Flames Emission']
                    w_bloom_emis = bpy.data.objects[obj].active_material.node_tree.nodes['Group'].inputs['Bloom Emission']
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Color:')
                    split.prop(w_flames_color, "default_value", text = "")
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Flames Emission:')
                    split.prop(w_flames_emis, "default_value", text = "")
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Bloom Emission:')
                    split.prop(w_bloom_emis, "default_value", text = "")                 
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.wpn_button_spawn', text = "Parent Flames").weapon = "flatline_parent_flame"
                
                #box.label(text='    ')
                box.operator('object.wpn_button_spawn', text = "Add POV gun Effect (v)").weapon = "flatline_s4_glow_hex_LOD0_SEModelMesh.001" 
                try:
                    obj = bpy.data.objects['flatline_s4_glow_hex_LOD0_SEModelMesh.001']
                except:
                    pass
                else:
                    obj = 'flatline_s4_glow_hex_LOD0_SEModelMesh.001'
                    v_flames_color = bpy.data.objects[obj].active_material.node_tree.nodes['Group'].inputs['Color']
                    v_flames_emis = bpy.data.objects[obj].active_material.node_tree.nodes['Group'].inputs['Flames Emission']
                    v_bloom_emis = bpy.data.objects[obj].active_material.node_tree.nodes['Group'].inputs['Bloom Emission']
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Color:')
                    split.prop(v_flames_color, "default_value", text = "")
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Flames Emission:')
                    split.prop(v_flames_emis, "default_value", text = "")
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Bloom Emission:')
                    split.prop(v_bloom_emis, "default_value", text = "")  
                                    
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.operator('object.wpn_button_spawn', text = "Add POV Anim").weapon = "idle_reactive_layer_3_Fixed"
                split.operator('object.wpn_button_spawn', text = "Parent Flames").weapon = "flatline_pov_parent_flame"                                                                 
                            
            
        if assets_set == 1:
            row = layout.row()
            row.label(text='*** Spawn Items ***')


            ######### Heirloom Items #########         
            row = layout.row()
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_heirloom else 'RIGHTARROW'
            row.prop(context.scene, 'subpanel_effects_heirloom', icon=icon, icon_only=True)
            row.label(text='Heirloom Items')
            # some data on the subpanel
            if context.scene.subpanel_effects_heirloom:
                row = layout.row()
                row.label(text='Animation is just to open heirloom')
                box = layout.box()
                for n in range(len(all_heirloom_items)):
                    box.operator('object.hl_button_spawn', text = all_heirloom_items.get(str(n))).heirloom = all_heirloom_items.get(str(n))
                            
                                        
            ######### Badges #########
            row = layout.row()
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_badges else 'RIGHTARROW'
            row.prop(context.scene, 'subpanel_effects_badges', icon=icon, icon_only=True)
            row.label(text='Badges (3D)')
            # some data on the subpanel
            if context.scene.subpanel_effects_badges:
                box = layout.box()
                # Badges
                box.operator('object.bdg_button_spawn', text = "4K Badge").badge = "Badge - 4k Damage"
                box.operator('object.bdg_button_spawn', text = "20 Bomb Badge").badge = "Badge - 20 Bombs"
                box.operator('object.bdg_button_spawn', text = "20 Bomb Badge (v2)").badge = "Badge - 20 Bombs (v2)"
                box.operator('object.bdg_button_spawn', text = "Predator S3 Badge").badge = "Badge - Predator S3"
                
                
            ######### Loot Items #########
            row = layout.row()
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot else 'RIGHTARROW'
            row.prop(context.scene, 'subpanel_effects_loot', icon=icon, icon_only=True)
            row.label(text='Loot Items')
            # some data on the subpanel
            if context.scene.subpanel_effects_loot:
                box = layout.box()
                
                # Body Armor subpanel 1
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop1 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop1', icon=icon, icon_only=False, text='Body Armor                          ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop1:
                    for n in range(len(all_loot_items)):
                        if n in range(*armor_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))
                    
                # Helmet subpanel 2
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop2 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop2', icon=icon, icon_only=False, text='Helmet                                 ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop2:
                     for n in range(len(all_loot_items)):
                        if n in range(*helmet_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n)) 
                    
                # Heals subpanel 3
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop3 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop3', icon=icon, icon_only=False, text='Heals                                    ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop3:
                    for n in range(len(all_loot_items)):
                        if n in range(*meds_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))
                            
                # Nades subpanel 4
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop4 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop4', icon=icon, icon_only=False, text='Nades                                    ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop4:
                    for n in range(len(all_loot_items)):
                        if n in range(*nades_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n)) 
                            
                # Ammo subpanel 5
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop5 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop5', icon=icon, icon_only=False, text='Ammo                                    ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop5:
                    for n in range(len(all_loot_items)):
                        if n in range(*ammo_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))                               
                            
                # Backpacks subpanel 6
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop6 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop6', icon=icon, icon_only=False, text='Backpacks                              ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop6:
                    for n in range(len(all_loot_items)):
                        if n in range(*bag_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))  
                            
                # Others subpanel 7
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop7 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop7', icon=icon, icon_only=False, text='Other                                       ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop7:
                    for n in range(len(all_loot_items)):
                        if n in range(*other_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))    
              
                            
                            
            ######### Lobby Items #########
            row = layout.row()
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_lobby else 'RIGHTARROW'
            row.prop(context.scene, 'subpanel_effects_lobby', icon=icon, icon_only=True)
            row.label(text='Lobby Items')
            # some data on the subpanel
            if context.scene.subpanel_effects_lobby:
                box = layout.box()
                for n in range(len(all_lobby_other_items)):
                    if n in range(*lobby_lobby_range):
                        box.operator('object.lb_button_spawn', text = all_lobby_other_items.get(str(n))).lobby_other = all_lobby_other_items.get(str(n))

            
            ######### Other Items #########
            def holo():
                try:
                    obj = bpy.data.objects['goblin_dropship_holo_LOD0_skel']
                except:
                    pass
                else:
                    obj = 'goblin_dropship_holo_LOD0_SEModelMesh.002'
                    obj1 = 'goblin_dropship_holo_LOD0_SEModelMesh.001'
                    obj2 = 'Respawn Hologram'
                    holo_0 = bpy.data.objects[obj].active_material.node_tree.nodes['Mix.001'].inputs['Color2'] 
                    holo_1 = bpy.data.objects[obj].active_material.node_tree.nodes['Emission'].inputs['Strength']                     
                    holo_2 = bpy.data.objects[obj1].active_material.node_tree.nodes['Mix'].inputs['Color2'] 
                    holo_3 = bpy.data.objects[obj1].active_material.node_tree.nodes['Emission'].inputs['Strength']               
                    holo_4 = bpy.data.objects[obj2].active_material.node_tree.nodes['Respawn Hologram'].inputs[0]
                    holo_5 = bpy.data.objects[obj2].active_material.node_tree.nodes['Respawn Hologram'].inputs[1] 
                    holo_6 = bpy.data.objects[obj2].active_material.node_tree.nodes['Respawn Hologram'].inputs[2] 
                    holo_7 = bpy.data.objects[obj2].active_material.node_tree.nodes['Respawn Hologram'].inputs[3] 
                    holo_8 = bpy.data.objects[obj2].active_material.node_tree.nodes['Respawn Hologram'].inputs[4]  
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Ship Top Color:')
                    split.prop(holo_0, "default_value", text = "")
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Emissive:')
                    split.prop(holo_1, "default_value", text = "") 
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Ship Bottom Color:')
                    split.prop(holo_2, "default_value", text = "") 
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Emissive:')
                    split.prop(holo_3, "default_value", text = "") 
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Strips Color:')
                    split.prop(holo_4, "default_value", text = "") 
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Strips Height:')
                    split.prop(holo_5, "default_value", text = "") 
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Strips Brightness:')
                    split.prop(holo_6, "default_value", text = "") 
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Cone Color:')
                    split.prop(holo_7, "default_value", text = "") 
                    split = box.split(factor = 0.6)
                    col = split.column(align = True)
                    col.label(text='Cone Brightness:')
                    split.prop(holo_8, "default_value", text = "")  
                                   
            
            row = layout.row()
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_other else 'RIGHTARROW'
            row.prop(context.scene, 'subpanel_effects_other', icon=icon, icon_only=True)
            row.label(text='Other Items')
            # some data on the subpanel
            if context.scene.subpanel_effects_other:
                box = layout.box()
                for n in range(len(all_lobby_other_items)):
                    if n in range(*lobby_other_range):
                        box.operator('object.lb_button_spawn', text = all_lobby_other_items.get(str(n))).lobby_other = all_lobby_other_items.get(str(n))                
                        if all_lobby_other_items.get(str(n)) == 'Respawn Beacon Hologram': 
                            holo()
                                                                                                                                  
                        


        ######### Skydive #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_sky else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_sky', icon=icon, icon_only=True)
        row.label(text='Skydive (Experimental)')
        # some data on the subpanel
        if context.scene.subpanel_effects_sky:
            box = layout.box()

            for n in range(len(all_skydive_items)):
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.sky_button_spawn', text = all_skydive_items.get(str(n))).sky_effect = all_skydive_items.get(str(n))
            split = box.split(factor = 0.6)
            col = split.column(align = True)
            col.label(text='')         
            split.operator('object.sky_button_spawn', text = "Parent it").sky_effect = "Skydive_parent" 
            box.label(text='*Sel Model Bones before Parenting') 
            box.label(text='*Parent before import animation')           


            """
            # Wraith subpanel 2
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_wraith_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_wraith_prop1', icon=icon, icon_only=False, text='Wraith with properties')
            # some data on the subpanel
            if context.scene.subpanel_effects_wraith_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='1.')
                split.operator("object.wr_button_portal", text = "Spawn Portal") 
            """ 
             

######### Other Effects Tab ########### 
class OTHERS_PT_panel(bpy.types.Panel):
    bl_parent_id = "OBJECT_PT_panel"
    bl_label = "OTHER EFFECTS COLLECTION"  
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_options = {"DEFAULT_CLOSED"}
    

    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prefs = scene.my_prefs

        ######### Animated Staging #########
        box = layout.box()
        box.operator('object.lb_button_spawn', text = 'Animated Staging + Camera').lobby_other = 'Animated Staging'
        try:
            bpy.data.objects['Staging Camera']
        except:
            pass
        else:               
            #box = layout.box()
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            col.label(text='')
            split.operator('object.ef_button_spawn', text = "Set Active").cool_effect = 'Staging Camera'
                
        ######### Basic Lights #########
        box.operator('object.ef_button_spawn', text = 'Basic Lights Setup').cool_effect = 'basic lights'
        
        ######### Wireframe Effect #########                
        box.operator('object.ef_button_spawn', text = 'Cool Wireframe effect to Model').cool_effect = 'wireframe'
        split = box.split(factor = 0.6)
        col = split.column(align = True)
        col.label(text='')
        split.operator('object.ef_button_spawn', text = 'Clear Effect').cool_effect = 'wireframe_clear'

'''
######### Legends/Weapons Translate Tab ########### 
class TRANSLATE_PT_panel(bpy.types.Panel):
    bl_parent_id = "OBJECT_PT_panel"
    bl_label = "LEGION MODELS TRANSLATE"  
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_options = {"DEFAULT_CLOSED"}
    

    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prefs = scene.my_prefs

        
        row = layout.row()
        row.operator('object.lgndtranslate_url', text = "Visit Online Table", icon='URL').link = "garlicus_table" 
        row = layout.row()
        row.operator('object.lgndtranslate_url', text = "Fetch Data", icon='FILE_REFRESH').link = "garlicus" 
        row = layout.row()  

        try: 
            row = layout.row()
            split = row.split(factor = 0.9)
            col = split.column(align = True)
            col.label(text=ver_list[0][0])  
            split.label(text="") 
            row = layout.row()
            split = row.split(factor = 0.9)
            col = split.column(align = True)
            col.label(text=ver_list[0][2])  
            split.label(text="")
        except:
            pass
        
        else:
            for x in range(len(lgnd_list)):
                if lgnd_list[x][0] != "null":
                    row = layout.row()
                    row.prop(prefs, lgnd_list[x][0], text=lgnd_list[x][0], icon = 'DOWNARROW_HLT' if getattr(prefs, lgnd_list[x][0]) else 'RIGHTARROW')
                    if getattr(prefs, lgnd_list[x][0]):
                        try:
                            row = layout.row()
                            split = row.split(factor = 0.4)
                            col = split.column(align = True)
                            col.label(text=lgnd_list[x][1]) 
                            split.label(text=lgnd_list[x][2])
                            x +=1
                        except:
                            pass    
                        else:
                            for x in range(x,len(lgnd_list)):
                                if lgnd_list[x][0] == "null":
                                    row = layout.row()
                                    split = row.split(factor = 0.4)
                                    col = split.column(align = True)
                                    col.label(text=lgnd_list[x][1]) 
                                    split.label(text=lgnd_list[x][2])
                                    if lgnd_list[x][3] != "null":
                                        row = layout.row()
                                        split = row.split(factor = 0.4)
                                        col = split.column(align = True)
                                        col.label(text="") 
                                        split.label(text="*Material*  " + lgnd_list[x][3])                                     
                                    x +=1
                                else:
                                    break                       

        #0 - Legend Name
        #1 - In game name	
        #2 - Legion name	
        #3 - Material (If needed)        
'''


######### Updates Tracker ########### 
class UPDATE_PT_panel(bpy.types.Panel):
    bl_parent_id = "OBJECT_PT_panel"
    bl_label = "UPDATES TRACKER"  
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_options = {"DEFAULT_CLOSED"}
    

    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prefs = scene.my_prefs

        
        ####   Check for update Legion+  #### 
        if mode == 0:
            legion_folder = lgn_fldr
        else:
            legion_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.legion_folder
        

        if os.path.isdir(legion_folder) != True:
            print("Apex Toolbox Addon: Legion folder not selected")
        else: 
            global legion_cur_ver
            global legion_lts_ver
            global legion_folder_exist             
            if legion_folder_exist == 0:                   
                dir = os.listdir(legion_folder)
                for x in range(len(dir)):
                    if "+" in dir[x]:
                        i = dir[x].split("+")[0]
                        if i == 'Legion':
                            legion_cur_ver = dir[x].split("+")[1]
                            print("Apex Toolbox Addon: Installed Legion+ Version: " + legion_cur_ver)
                            legion_folder_exist = 1
                            break
                    else:
                        legion_folder_exist = 2    
               
 
        if legion_folder_exist == 0:
            print("Apex Toolbox Addon: Legion folder not found")
                
                
        ######## Legion Settings ########                               
        if mode == 0:
            legion_folder = lgn_fldr
            legion_folder_prefs = prefs
            lgn_folder = 'recolor_folder'
        else:
            legion_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.legion_folder
            legion_folder_prefs =bpy.context.preferences.addons['Apex_toolbox'].preferences
            lgn_folder = 'legion_folder'

        box = layout.box()
        if legion_cur_ver == '0':
            box.label(text = "Select Folder with Legion+ FOLDER")
            box.label(text = "NOT Folder with LegionPlus.exe")
            box.label(text = "Example: MyFolder/Legion+1.4.1/LegionPlus.exe")
            box.label(text = "select 'MyFolder'")
            box.prop(legion_folder_prefs, lgn_folder) 
            try:
                if os.path.exists(legion_folder) == True:
                    if legion_folder_exist == 0:
                        box.label(text = "Legion+ Folder Not Found")
                    if legion_folder_exist == 2:
                        box.label(text = "Name of Legion folder should look")
                        box.label(text = "like this: 'Legion+1.4.1' (example)")
            except:
                pass
            box.label(text = "--------------------------------------------------")
     

        ######## Installed Addons ########
        if legion_cur_ver != '0':
            box.label(text="Installed Software:")
            split = box.split(factor = 0.7)
            col = split.column(align = True)
            col.label(text="Legion+")  
            split.label(text="v." + legion_cur_ver)
            if legion_lts_ver > legion_cur_ver:
                box.operator('object.lgndtranslate_url', text = "Legion+ New Ver." + str(legion_lts_ver), icon='IMPORT').link = "legion_update"
            box.label(text="")    
        if addon_name != None:
            box.label(text = "Installed Addons:")
            for x in range(len(addon_name)):
                split = box.split(factor = 0.7)
                col = split.column(align = True)
                col.label(text=addon_name[x])  
                split.label(text="v." + addon_ver[x])
                if addon_name[x] == addon[0]:
                    if io_anim_lts_ver > addon_ver[x]:
                        box.operator('object.lgndtranslate_url', text = addon_name[x] + " New Ver." + str(io_anim_lts_ver), icon='IMPORT').link = "io_anim_seanim"
                if addon_name[x] == addon[1]:
                    if cast_lts_ver > addon_ver[x]:
                        box.operator('object.lgndtranslate_url', text = addon_name[x] + " New Ver." + str(cast_lts_ver), icon='IMPORT').link = "cast"
                if addon_name[x] == addon[2]:
                    if semodel_lts_ver > addon_ver[x]:
                        box.operator('object.lgndtranslate_url', text = addon_name[x] + " New Ver." + str(semodel_lts_ver), icon='IMPORT').link = "io_model_semodel"
                if addon_name[x] == addon[3]:
                    if mprt_lts_ver > addon_ver[x]:
                        box.operator('object.lgndtranslate_url', text = addon_name[x] + " New Ver." + str(mprt_lts_ver), icon='IMPORT').link = "mprt" 
        split = box.split(factor = 0.2)
        col = split.column(align = True)
        col.label(text="")  
        split.operator('object.lgndtranslate_url', text ="Check for Updates", icon='URL').link = "check_update"  
                                                                                                         


    #CLASS REGISTER 
##########################################
classes = (
        apexToolsPreferences,
        PROPERTIES_CUSTOM, 
        LGNDTRANSLATE_URL,
        BUTTON_CUSTOM,
        BUTTON_TOON, 
        BUTTON_SHADOW,
        BUTTON_CUSTOM2, 
        BUTTON_SHADERS, 
        BUTTON_HDRIFULL,
        BUTTON_IKBONE, 
        WR_BUTTON_PORTAL,
        SEER_BUTTON_SPAWN,
        SKY_BUTTON_SPAWN, 
        GB_BUTTON_ITEMS, 
        MR_BUTTON_DECOY, 
        AUTOTEX_MENU, 
        EFFECTS_PT_panel, 
        VK_BUTTON_ITEMS, 
        BDG_BUTTON_SPAWN, 
        WPN_BUTTON_SPAWN,
        LT_BUTTON_SPAWN,
        LB_BUTTON_SPAWN,
        HL_BUTTON_SPAWN,
        EF_BUTTON_SPAWN,
        OTHERS_PT_panel,
        UPDATE_PT_panel
        )
        

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.my_prefs = bpy.props.PointerProperty(type= PROPERTIES_CUSTOM)
    Scene.subpanel_readme = BoolProperty(default=False)
    Scene.subpanel_status_0 = BoolProperty(default=False)
    Scene.subpanel_shadow = BoolProperty(default=False)
    Scene.subpanel_toon = BoolProperty(default=False)
    Scene.subpanel_ikbone = BoolProperty(default=False)
    Scene.subpanel_status_1 = BoolProperty(default=False)
    Scene.subpanel_status_2 = BoolProperty(default=False)
    Scene.subpanel_effects_wraith = BoolProperty(default=False)
    Scene.subpanel_effects_wraith_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_gibby = BoolProperty(default=False)
    Scene.subpanel_effects_gibby_prop1 = BoolProperty(default=False)    
    Scene.subpanel_effects_mirage = BoolProperty(default=False)
    Scene.subpanel_effects_mirage_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_valkyrie = BoolProperty(default=False)
    Scene.subpanel_effects_valkyrie_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_seer = BoolProperty(default=False)    
    Scene.subpanel_effects_weapons = BoolProperty(default=False)
    Scene.subpanel_effects_weapons_laser = BoolProperty(default=False)
    Scene.subpanel_effects_weapons_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_heirloom = BoolProperty(default=False)
    Scene.subpanel_effects_badges = BoolProperty(default=False)
    Scene.subpanel_effects_loot = BoolProperty(default=False)
    Scene.subpanel_effects_loot_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_loot_prop2 = BoolProperty(default=False)
    Scene.subpanel_effects_loot_prop3 = BoolProperty(default=False) 
    Scene.subpanel_effects_loot_prop4 = BoolProperty(default=False) 
    Scene.subpanel_effects_loot_prop5 = BoolProperty(default=False) 
    Scene.subpanel_effects_loot_prop6 = BoolProperty(default=False)
    Scene.subpanel_effects_loot_prop7 = BoolProperty(default=False)
    Scene.subpanel_effects_lobby = BoolProperty(default=False) 
    Scene.subpanel_effects_other = BoolProperty(default=False)   
    Scene.subpanel_effects_sky = BoolProperty(default=False)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.my_prefs
    del Scene.subpanel_readme
    del Scene.subpanel_status_0
    del Scene.subpanel_shadow
    del Scene.subpanel_toon
    del Scene.subpanel_ikbone
    del Scene.subpanel_status_1
    del Scene.subpanel_status_2
    del Scene.subpanel_effects_wraith
    del Scene.subpanel_effects_wraith_prop1
    del Scene.subpanel_effects_gibby
    del Scene.subpanel_effects_gibby_prop1    
    del Scene.subpanel_effects_mirage
    del Scene.subpanel_effects_mirage_prop1
    del Scene.subpanel_effects_valkyrie
    del Scene.subpanel_effects_valkyrie_prop1
    del Scene.subpanel_effects_seer    
    del Scene.subpanel_effects_weapons
    del Scene.subpanel_effects_weapons_laser
    del Scene.subpanel_effects_weapons_prop1
    del Scene.subpanel_effects_heirloom
    del Scene.subpanel_effects_badges
    del Scene.subpanel_effects_loot
    del Scene.subpanel_effects_loot_prop1
    del Scene.subpanel_effects_loot_prop2
    del Scene.subpanel_effects_loot_prop3 
    del Scene.subpanel_effects_loot_prop4 
    del Scene.subpanel_effects_loot_prop5
    del Scene.subpanel_effects_loot_prop6
    del Scene.subpanel_effects_loot_prop7
    del Scene.subpanel_effects_lobby 
    del Scene.subpanel_effects_other
    del Scene.subpanel_effects_sky 
        

if __name__ == "__main__":
    register()
