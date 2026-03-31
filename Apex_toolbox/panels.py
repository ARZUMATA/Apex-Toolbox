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

"""UI panel classes module for Apex Toolbox addon."""

import bpy
from bpy.props import BoolProperty
from .config import mode, ast_fldr, my_path, fbs, blend_file, ap_object, ap_material, ap_world, ap_image, bldr_hdri_path, lts_ver, ver, all_seer_items, all_heirloom_items, all_loot_items, armor_range, helmet_range, meds_range, nades_range, bag_range, ammo_range, other_range, all_lobby_other_items, lobby_lobby_range, lobby_other_range


######### Main Panel ########### 

class AUTOTEX_MENU(bpy.types.Panel):
    """Main panel for Apex Toolbox."""
    bl_label = "Apex Toolbox (v.3.7_beta-2)"
    bl_idname = "OBJECT_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Apex Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prefs = scene.my_prefs
        
    # Update Notifier
        from .config import lts_ver, ver
        if lts_ver > ver:
            box = layout.box()
            box.operator('object.lgndtranslate_url', text="Addon Update Available: " + lts_ver, icon='IMPORT').link = "update"

    # Assets
        if mode == 0:
            addon_assets = prefs
            folder = 'recolor_folder'
        else:
            addon_assets = bpy.context.preferences.addons['Apex_toolbox'].preferences
            folder = 'asset_folder'
        
    # Check if Asset Folder installed
        import os
        if mode == 0:
            asset_folder = ast_fldr
            asset_folder_set = asset_folder
        else:
            asset_folder_set = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
        
        assets_set = 0
        if os.path.exists(asset_folder_set) is True:
            asset_folder_set_split = asset_folder_set.split(fbs)[-2]
            if asset_folder_set_split == "Apex_Toolbox_Assets":
                assets_set = 1
            
        if assets_set != 1:
            mode_ver = '"Lite"'
            mode_ico = 'PANEL_CLOSE'
        else:
            mode_ver = '"Extended"'
            mode_ico = 'CHECKMARK'
            
        row = layout.row()
        row.label(text="Current Mode:  " + mode_ver, icon=mode_ico)

        # Readme First
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_readme else 'RIGHTARROW'
        row.prop(scene, 'subpanel_readme', icon=icon, icon_only=True)
        row.label(text="Readme First", icon="QUESTION")
        
        if scene.subpanel_readme:
            box = layout.box()
            box.operator('object.lgndtranslate_url', text="Read Instructions, Credits", icon='ARMATURE_DATA').link = "instructions"
            box.operator('object.lgndtranslate_url', text="Read Version Log", icon='CON_ARMATURE').link = "version" 
            
            if assets_set != 1:
                box.label(text="To install extra assets go to")
                box.operator('object.lgndtranslate_url', text="Assets File", icon='IMPORT').link = "asset_file"
                box.label(text="Download, unzip and specify below")
                box.label(text="folder name must be 'Apex_Toolbox_Assets'")
                box.label(text="addon recognize only this folder")
            
            row = layout.row()
            box.prop(addon_assets, folder)
            
            row.label(text="------------------------------------------------------")

        row.operator('object.ef_button_spawn', text="Set Correct Model Size").cool_effect = 'adjust_model'

        # Auto_tex
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_status_0 else 'RIGHTARROW'
        row.prop(scene, 'subpanel_status_0', icon=icon, icon_only=True)
        row.label(text="Auto_tex (by llenoco)", icon="TEXTURE")
        
        if scene.subpanel_status_0:           
            box = layout.box()
            box.prop(prefs, "cust_enum2")

            box = layout.box()
            box.label(text="Select Texture Folder")
            box.prop(prefs, 'texture_folder')

            split = box.split(factor=0.5)
            col = split.column(align=True)
            split.operator("object.button_custom", text="Texture Model")
            row = layout.row()
            row.label(text="------------------------------------------------------")

        # Auto_shadow
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_shadow else 'RIGHTARROW'
        row.prop(scene, 'subpanel_shadow', icon=icon, icon_only=True)
        row.label(text="Auto_shadow (Beta)", icon="GHOST_ENABLED")
        
        if scene.subpanel_shadow:
            box = layout.box()
            split = box.split(factor=0.5)
            col = split.column(align=True)
            col.label(text="Select mesh:")
            split.operator("object.button_shadow", text="Shadow It").shadow = "Shadow"
            
            split = box.split(factor=0.3)
            col = split.column(align=True)
            col.label(text='Eyes:')
            split.operator('object.button_shadow', text="Adjust and Parent").shadow = "Eyes_parent"  
            box.label(text='*Select Only Legend bones for parenting')
            row = layout.row()
            row.label(text="------------------------------------------------------") 

        # Auto_toon
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_toon else 'RIGHTARROW'
        row.prop(scene, 'subpanel_toon', icon=icon, icon_only=True)
        row.label(text="TOON Auto_tex", icon="UV")
        
        if scene.subpanel_toon:
            box = layout.box()
            box.operator('object.lgndtranslate_url', text="Read Instructions", icon='INFO').link = "toon_shader"
            
            split = box.split(factor=0.5)
            col = split.column(align=True)
            col.label(text="Select mesh then:")
            split.operator("object.button_toon", text="Toon It")

            # Toon Shader Settings UI
            key_lights = bpy.data.collections.get('Apex ToonShader')
            if key_lights is not None:
                if len(bpy.context.selected_objects) > 0:
                    try:
                        act_mat = bpy.context.object.active_material
                    except:
                        pass
                    else:
                        try:
                            toon_shader = act_mat.node_tree.nodes['Apex ToonShader']
                        except:
                            pass
                        else:
                            box.label(text="")
                            box.label(text="Shader Key Settings:")
                            
                            # Get shader input values safely
                            try:
                                set_1 = toon_shader.inputs[4]
                                set_2 = toon_shader.inputs[5]
                                set_3 = toon_shader.inputs[6]
                                set_4 = toon_shader.inputs[7]
                                set_5 = toon_shader.inputs[8]
                                set_6 = toon_shader.inputs[11]  # Reflection Color
                                set_7 = toon_shader.inputs[12]
                                set_8 = toon_shader.inputs[13]
                                set_9 = toon_shader.inputs[21]
                                
                                split = box.split(factor=0.5)
                                col = split.column(align=True)
                                col.label(text=set_1.name)
                                split.prop(set_1, "default_value", text="")
                                
                                split = box.split(factor=0.5)
                                col = split.column(align=True)
                                col.label(text=set_2.name)
                                split.prop(set_2, "default_value", text="")
                                
                                split = box.split(factor=0.5)
                                col = split.column(align=True)
                                col.label(text=set_3.name)
                                split.prop(set_3, "default_value", text="")
                                
                                split = box.split(factor=0.5)
                                col = split.column(align=True)
                                col.label(text=set_4.name)
                                split.prop(set_4, "default_value", text="")
                                
                                split = box.split(factor=0.5)
                                col = split.column(align=True)
                                col.label(text=set_5.name)
                                split.prop(set_5, "default_value", text="")
                                
                                split = box.split(factor=0.5)
                                col = split.column(align=True)
                                col.label(text='Reflection Color')
                                split.prop(set_6, "default_value", text="")
                                
                                split = box.split(factor=0.5)
                                col = split.column(align=True)
                                col.label(text=set_7.name)
                                split.prop(set_7, "default_value", text="")
                                
                                split = box.split(factor=0.5)
                                col = split.column(align=True)
                                col.label(text=set_8.name)
                                split.prop(set_8, "default_value", text="")
                                
                                split = box.split(factor=0.5)
                                col = split.column(align=True)
                                col.label(text=set_9.name)
                                split.prop(set_9, "default_value", text="")
                                
                                box.label(text="If Shadow Glitchy - Set 'None'")
                                split = box.split(factor=0.5)
                                col = split.column(align=True)
                                col.label(text='Shadow')
                                split.prop(act_mat, "shadow_method", text="")
                            except Exception as e:
                                box.label(text=f"Error loading shader settings: {e}")

            # Settings Modified by Addon
            box.label(text="")
            box.label(text="Settings Modified by Addon:")
            box.label(text="-- Optional Settings (Can change): --")
            box.prop(scene.render, "film_transparent", text="Transparent background")
            box.prop(scene.view_settings, "view_transform", text="Color")
            box.prop(scene.view_settings, "look")
            
            box.label(text="")
            box.label(text="-- Settings needed for Shader: --")
            
            # Blender 5.0 EEVEE-Next API Compatibility Notes:
            # - Property: Status - New Location/Method
            # - use_bloom: Removed - Glare Node in Compositor (set type to Bloom)
            # - use_gtao: Removed - Set scene.eevee.fast_gi_method = 'AMBIENT_OCCLUSION_ONLY'
            # - gtao_distance: Renamed - Moved to View Layer, renamed to view_layer.eevee.ambient_occlusion_distance
            # - use_shadow_high_bitdepth: Replaced - Controlled via Shadow Resolution or Jittered Shadows
            
            box.prop(scene.render, "engine")
            # Shading visibility
            if hasattr(context.space_data, 'shading'):
                box.prop(context.space_data.shading, "use_scene_lights")
                box.prop(context.space_data.shading, "use_scene_world")

            # Render Samples
            # Legacy: EEVEE used 'taa_samples'
            # 4.2+: Renamed to 'taa_render_samples' to distinguish from Viewport samples
            if hasattr(scene.eevee, "taa_render_samples"):
                box.prop(scene.eevee, "taa_render_samples", text="Render Samples")
            elif hasattr(scene.eevee, "taa_samples"):
                box.prop(scene.eevee, "taa_samples")
            
            # Bloom (The biggest change)
            # Legacy: A simple checkbox on the engine
            # 4.2+: Bloom is removed from EEVEE settings; must be done via 'Glare' node in Compositor
            if hasattr(scene.eevee, "use_bloom"):
                box.prop(scene.eevee, "use_bloom")
            else:
                box.label(text="Bloom: Use Compositor", icon='INFO')
                box.label(text="Glare Node (set type to Bloom)", icon='INFO')

            # Ambient Occlusion (GTAO)
            # Legacy: 'use_gtao' was a standalone toggle
            # 4.2+: AO is now part of the 'Raytracing' or 'Fast GI' systems
            if hasattr(scene.eevee, "use_gtao"):
                box.prop(scene.eevee, "use_gtao")
            elif hasattr(scene.eevee, "use_raytracing"):
                # Toggling Raytracing is the 5.0 equivalent of enabling high-quality AO/Reflections
                # If raytracing is off, EEVEE uses "Fast GI," which can be set to AO-only mode.
                box.prop(scene.eevee, "use_raytracing", text="Raytracing (Inc. AO)")

            # Shadow Quality
            # Legacy: 'use_shadow_high_bitdepth' for 32-bit shadows
            # 4.2+: EEVEE-Next uses Virtual Shadow Maps. Bit-depth is handled automatically 
            # based on the shadow 'method' or 'resolution'. Resolution is the new 'quality' metric.
            if hasattr(scene.eevee, "use_shadow_high_bitdepth"):
                box.prop(scene.eevee, "use_shadow_high_bitdepth")
            elif hasattr(scene.eevee, "shadow_method"):
                # Shows 'Virtual Shadow Maps' or 'Shadow Maps' options
                box.prop(scene.eevee, "shadow_method", text="Shadow Method")

        # Re-color
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_status_1 else 'RIGHTARROW'
        row.prop(scene, 'subpanel_status_1', icon=icon, icon_only=True)
        row.label(text="Re-color", icon="NODE_TEXTURE")
        
        if scene.subpanel_status_1:
            box = layout.box()
            box.label(text="Select Texture Folder")
            box.prop(prefs, 'recolor_folder')
            
            box.prop(prefs, 'rec_alpha')
            box.prop(prefs, 'cust_enum')
            
            split = box.split(factor=0.5)
            col = split.column(align=True)
            split.operator("object.button_custom2", text="Re-Color")
            row = layout.row()
            row.label(text="------------------------------------------------------")

        # Append Shader
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_status_2 else 'RIGHTARROW'
        row.prop(scene, 'subpanel_status_2', icon=icon, icon_only=True)

        row.label(text="Append Shaders & HDRI", icon="NODE_MATERIAL")
        
        if scene.subpanel_status_2:
            box = layout.box()   
            box.prop(prefs, 'cust_enum_shader')
            
            split = box.split(factor=0.6)
            col = split.column(align=True)
            split.operator("object.button_shaders", text="Add Shader")
            
            if assets_set == 0:
                box.prop(prefs, 'cust_enum_hdri_noast', text="HDRI")
                split = box.split(factor=0.5)
                col = split.column(align=True)
                col.label(text="")
                split.operator("object.button_hdrifull", text="Set as HDRI").hdri = "hdri_noast"
            else:
                box.prop(prefs, 'cust_enum_hdri')
                
                split = box.split(factor=0.5)
                col = split.column(align=True)
                col.operator("object.button_hdrifull", text="Set as Sky").hdri = "background"
                split.operator("object.button_hdrifull", text="Set as HDRI").hdri = "hdri"
            
            try:
                wrld = scene.world.name
            except:
                pass
            else:
                box.label(text='** Current World/HDRI Controls: **')
                wrld_0 = bpy.data.worlds[wrld].node_tree.nodes['Background'].inputs['Strength']
                if wrld != 'World':
                    wrld_1 = bpy.data.worlds[wrld].node_tree.nodes['Mapping'].inputs['Rotation']
                
                split = box.split(factor=0.5)
                col = split.column(align=True)
                col.label(text='Brightness:')
                split.prop(wrld_0, "default_value", text="")
                
                if wrld != 'World':
                    split = box.split(factor=0.5)
                    col = split.column(align=True)
                    col.label(text='Rotation:')
                    split.prop(wrld_1, "default_value", text="")
                
                if assets_set == 0:
                    pass
                else:
                    box.label(text="*Set as Sky - just a background")
                    box.label(text="*Set as HDRI - apply lights")
                    box.label(text="*Not all images can set as Sky")

            row = layout.row()
            row.label(text="------------------------------------------------------")

        # Animation
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_ikbone else 'RIGHTARROW'
        row.prop(scene, 'subpanel_ikbone', icon=icon, icon_only=True)

        row.label(text="Animation & Bones", icon="BONE_DATA")
        
        if scene.subpanel_ikbone:
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
                
            box.label(text="Select Legend Bones Then:")
            box.operator("object.button_ikbone", text="Add IK Bones")
            
            row = layout.row()
            row.label(text="------------------------------------------------------")

        row = layout.row()
        row.operator('object.lgndtranslate_url', text="Biast12 Apex PC Assets", icon='URL').link = "biast_archive"
        row = layout.row()
        row.operator('object.lgndtranslate_url', text="Garlicus Skins list", icon='URL').link = "garlicus_list"
        row = layout.row()
        row.operator('object.lgndtranslate_url', text="Toolbox Discord Server", icon='ORIENTATION_GIMBAL').link = "discord"
        row = layout.row()
        row.operator('object.lgndtranslate_url', text="Buy me a Coffee! ;)", icon='URL').link = "buy coffee"


# Apex Effects Tab

class EFFECTS_PT_panel(bpy.types.Panel):
    """APEX EFFECTS COLLECTION panel."""
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
            asset_folder_set = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
        
        assets_set = 0
        import os
        if os.path.exists(asset_folder_set) is True:
            asset_folder_set_split = asset_folder_set.split(fbs)[-2]
            if asset_folder_set_split == "Apex_Toolbox_Assets":
                assets_set = 1
                        
        # Wraith
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_effects_wraith else 'RIGHTARROW'
        row.prop(scene, 'subpanel_effects_wraith', icon=icon, icon_only=True)
        row.label(text='Wraith')
        
        if scene.subpanel_effects_wraith:
            box = layout.box()
            
            # Wraith subpanel 1
            box.operator("object.wr_button_portal", text="Spawn Portal")
            
            try:
                obj = bpy.data.objects['wraith_portal']
            except:
                pass
            else:
                portal_0 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[0]
                portal_1 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[1]
                portal_2 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[2]
                portal_3 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[3]
                portal_4 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[4]
                portal_5 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[5]
                portal_6 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[6]
                portal_7 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[7]
                portal_8 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[8]
                portal_9 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[9]
                portal_10 = obj.active_material.node_tree.nodes['Wraith Portal'].inputs[10]
                
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Center Transparency:')
                split.prop(portal_0, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Outer Ring-1:')
                split.prop(portal_1, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Brightness:')
                split.prop(portal_2, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Outer Ring-2:')
                split.prop(portal_3, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Brightness:')
                split.prop(portal_4, "default_value", text="")  
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Outer Ring-3:')
                split.prop(portal_5, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Brightness:')
                split.prop(portal_6, "default_value", text="")  
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Inner Ring-1:')
                split.prop(portal_7, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Brightness:')
                split.prop(portal_8, "default_value", text="")  
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Inner Ring-2:')
                split.prop(portal_9, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Brightness:')
                split.prop(portal_10, "default_value", text="")

        # Gibraltar
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_effects_gibby else 'RIGHTARROW'
        row.prop(scene, 'subpanel_effects_gibby', icon=icon, icon_only=True)
        row.label(text='Gibraltar')
        
        if scene.subpanel_effects_gibby:
            box = layout.box()
            
            # Gibraltar subpanel 1
            icon = 'DOWNARROW_HLT' if scene.subpanel_effects_gibby_prop1 else 'RIGHTARROW'
            box.prop(scene, 'subpanel_effects_gibby_prop1', icon=icon, icon_only=False, text='Dome Shield')
            
            if scene.subpanel_effects_gibby_prop1:
                split = box.split(factor=0.08)
                col = split.column(align=True)
                col.label(text='')
                split.operator('object.gb_button_items', text="Friendly").gibby = "Gibby bubble friendly"
                split.operator('object.gb_button_items', text="Enemy").gibby = "Gibby bubble enemy"

        # Mirage
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_effects_mirage else 'RIGHTARROW'
        row.prop(scene, 'subpanel_effects_mirage', icon=icon, icon_only=True)
        row.label(text='Mirage')
        
        if scene.subpanel_effects_mirage:
            box = layout.box()
            
            # Mirage subpanel 1
            icon = 'DOWNARROW_HLT' if scene.subpanel_effects_mirage_prop1 else 'RIGHTARROW'
            box.prop(scene, 'subpanel_effects_mirage_prop1', icon=icon, icon_only=False, text='Decoy')
            
            if scene.subpanel_effects_mirage_prop1:
                split = box.split(factor=0.08)
                col = split.column(align=True)
                col.label(text='')
                split.operator('object.mr_button_decoy', text="Add Effect").mr_decoy = "Decoy"
                split.operator('object.mr_button_decoy', text="Parent it").mr_decoy = "Decoy_parent" 
                box.label(text='*Sel Legend before add Effect')
                box.label(text='*Sel Model Bones before Parenting')

        # Valkyrie
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_effects_valkyrie else 'RIGHTARROW'
        row.prop(scene, 'subpanel_effects_valkyrie', icon=icon, icon_only=True)
        row.label(text='Valkyrie')
        
        if scene.subpanel_effects_valkyrie:
            box = layout.box()
            
            # Valkyrie subpanel 1
            icon = 'DOWNARROW_HLT' if scene.subpanel_effects_valkyrie_prop1 else 'RIGHTARROW'
            box.prop(scene, 'subpanel_effects_valkyrie_prop1', icon=icon, icon_only=False, text='Flames')
            
            if scene.subpanel_effects_valkyrie_prop1:
                split = box.split(factor=0.08)
                col = split.column(align=True)
                col.label(text='')
                split.operator('object.vk_button_items', text="Add Flames").valk = "Flames"
                split.operator('object.vk_button_items', text="Parent them").valk = "Flames_parent" 
                box.label(text='*Sel Model Bones before Parenting')

        # Seer
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_effects_seer else 'RIGHTARROW'
        row.prop(scene, 'subpanel_effects_seer', icon=icon, icon_only=True)
        row.label(text='Seer')
        
        if scene.subpanel_effects_seer:
            box = layout.box()
            
            # Seer subpanel 1
            from .config import all_seer_items
            for n in range(len(all_seer_items)):
                if n == 0:
                    box.operator('object.seer_button_spawn', text=all_seer_items.get(str(n))).lgnd_effect = all_seer_items.get(str(n)) 
            
            try:
                obj = bpy.data.objects['Seer Ultimate']
                obj2 = bpy.data.objects['Seer ult circle']
            except:
                pass
            else:
                seer_ult_0 = obj.material_slots[0].material.node_tree.nodes['Mix.001'].inputs['Color1'] 
                seer_ult_1 = obj.material_slots[0].material.node_tree.nodes['Emission'].inputs['Strength'] 
                seer_ult_2 = obj2.active_material.node_tree.nodes['Mix.001'].inputs['Color1'] 
                seer_ult_3 = obj2.active_material.node_tree.nodes['Emission'].inputs['Strength']
                seer_ult_4 = obj.material_slots[1].material.node_tree.nodes['Mix.001'].inputs['Color1']
                seer_ult_5 = obj.material_slots[1].material.node_tree.nodes['Emission'].inputs['Strength']

                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Cage Color:')
                split.prop(seer_ult_0, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Brightness:')
                split.prop(seer_ult_1, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Cage Bottom Color:')
                split.prop(seer_ult_4, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Brightness:')
                split.prop(seer_ult_5, "default_value", text="")
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Node Color:')
                split.prop(seer_ult_2, "default_value", text="") 
                split = box.split(factor=0.6)
                col = split.column(align=True)
                col.label(text='Brightness:')
                split.prop(seer_ult_3, "default_value", text="")

        # Weapons
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_effects_weapons else 'RIGHTARROW'
        row.prop(scene, 'subpanel_effects_weapons', icon=icon, icon_only=True)
        row.label(text='Weapons')
        
        if scene.subpanel_effects_weapons:
            box = layout.box()
            
            # Laser subpanel
            icon = 'DOWNARROW_HLT' if scene.subpanel_effects_weapons_laser else 'RIGHTARROW'
            box.prop(scene, 'subpanel_effects_weapons_laser', icon=icon, icon_only=False, text='Weapon Laser')
            
            if scene.subpanel_effects_weapons_laser:
                box.operator('object.wpn_button_spawn', text="Add Laser").weapon = "Laser"
                
                try:
                    obj = bpy.data.objects['Laser_pt1']
                except:
                    pass
                else:
                    laser_color = obj.active_material.node_tree.nodes['Mix'].inputs['Color1']
                    laser_emis = obj.active_material.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
                    
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Set Color:')
                    split.prop(laser_color, "default_value", text="")
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Emissive:')
                    split.prop(laser_emis, "default_value", text="")
                
                split = box.split(factor=0.3)
                col = split.column(align=True)
                col.label(text='')
                split.operator('object.wpn_button_spawn', text="1. Parent Laser").weapon = "Laser_parent"
                split = box.split(factor=0.3)
                col = split.column(align=True)
                col.label(text='')
                split.operator('object.wpn_button_spawn', text="2. Adjust Laser").weapon = "Laser_move" 
                box.label(text='*Select weapon bones for 1 & 2') 

            # Flatline Flames (v20_assim)
            icon = 'DOWNARROW_HLT' if scene.subpanel_effects_weapons_prop1 else 'RIGHTARROW'
            box.prop(scene, 'subpanel_effects_weapons_prop1', icon=icon, icon_only=False, text='Flatline Flames (v20_assim)')
            
            if scene.subpanel_effects_weapons_prop1:
                box.operator('object.wpn_button_spawn', text="Add Normal gun Effect (w)").weapon = "flatline_s4_glow_hex_LOD0_SEModelMesh.125"
                
                try:
                    obj = bpy.data.objects['flatline_s4_glow_hex_LOD0_SEModelMesh.125']
                except:
                    pass
                else:
                    w_flames_color = obj.active_material.node_tree.nodes['Group'].inputs['Color']
                    w_flames_emis = obj.active_material.node_tree.nodes['Group'].inputs['Flames Emission']
                    w_bloom_emis = obj.active_material.node_tree.nodes['Group'].inputs['Bloom Emission']
                    
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Color:')
                    split.prop(w_flames_color, "default_value", text="")
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Flames Emission:')
                    split.prop(w_flames_emis, "default_value", text="")
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Bloom Emission:')
                    split.prop(w_bloom_emis, "default_value", text="")
                
                split = box.split(factor=0.5)
                col = split.column(align=True)
                col.label(text='')
                split.operator('object.wpn_button_spawn', text="Parent Flames").weapon = "flatline_parent_flame"
                
                # POV gun Effect
                box.operator('object.wpn_button_spawn', text="Add POV gun Effect (v)").weapon = "flatline_s4_glow_hex_LOD0_SEModelMesh.001" 
                
                try:
                    obj = bpy.data.objects['flatline_s4_glow_hex_LOD0_SEModelMesh.001']
                except:
                    pass
                else:
                    v_flames_color = obj.active_material.node_tree.nodes['Group'].inputs['Color']
                    v_flames_emis = obj.active_material.node_tree.nodes['Group'].inputs['Flames Emission']
                    v_bloom_emis = obj.active_material.node_tree.nodes['Group'].inputs['Bloom Emission']
                    
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Color:')
                    split.prop(v_flames_color, "default_value", text="")
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Flames Emission:')
                    split.prop(v_flames_emis, "default_value", text="")
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Bloom Emission:')
                    split.prop(v_bloom_emis, "default_value", text="")  
                                    
                split = box.split(factor=0.5)
                col = split.column(align=True)
                col.operator('object.wpn_button_spawn', text="Add POV Anim").weapon = "idle_reactive_layer_3_Fixed"
                split.operator('object.wpn_button_spawn', text="Parent Flames").weapon = "flatline_pov_parent_flame"

        if assets_set == 1:
            row = layout.row()
            row.label(text='*** Spawn Items ***')

            # Heirloom Items
            row = layout.row()
            icon = 'DOWNARROW_HLT' if scene.subpanel_effects_heirloom else 'RIGHTARROW'
            row.prop(scene, 'subpanel_effects_heirloom', icon=icon, icon_only=True)
            row.label(text='Heirloom Items')
            
            if scene.subpanel_effects_heirloom:
                row = layout.row()
                row.label(text='Animation is just to open heirloom')
                box = layout.box()
                
                from .config import all_heirloom_items
                for n in range(len(all_heirloom_items)):
                    box.operator('object.hl_button_spawn', text=all_heirloom_items.get(str(n))).heirloom = all_heirloom_items.get(str(n))

            # Badges
            row = layout.row()
            icon = 'DOWNARROW_HLT' if scene.subpanel_effects_badges else 'RIGHTARROW'
            row.prop(scene, 'subpanel_effects_badges', icon=icon, icon_only=True)
            row.label(text='Badges (3D)')
            
            if scene.subpanel_effects_badges:
                box = layout.box()
                box.operator('object.bdg_button_spawn', text="4K Badge").badge = "Badge - 4k Damage"
                box.operator('object.bdg_button_spawn', text="20 Bomb Badge").badge = "Badge - 20 Bombs"
                box.operator('object.bdg_button_spawn', text="20 Bomb Badge (v2)").badge = "Badge - 20 Bombs (v2)"
                box.operator('object.bdg_button_spawn', text="Predator S3 Badge").badge = "Badge - Predator S3"

            # Loot Items
            row = layout.row()
            icon = 'DOWNARROW_HLT' if scene.subpanel_effects_loot else 'RIGHTARROW'
            row.prop(scene, 'subpanel_effects_loot', icon=icon, icon_only=True)
            row.label(text='Loot Items')
            
            if scene.subpanel_effects_loot:
                box = layout.box()
                
            # Body Armor subpanel 1
                icon = 'DOWNARROW_HLT' if scene.subpanel_effects_loot_prop1 else 'RIGHTARROW'
                box.prop(scene, 'subpanel_effects_loot_prop1', icon=icon, icon_only=False, text='Body Armor')
                
                if scene.subpanel_effects_loot_prop1:
                    from .config import all_loot_items, armor_range
                    for n in range(len(all_loot_items)):
                        if n in range(*armor_range):
                            box.operator('object.lt_button_spawn', text=all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))
                
            # Helmet subpanel 2
                icon = 'DOWNARROW_HLT' if scene.subpanel_effects_loot_prop2 else 'RIGHTARROW'
                box.prop(scene, 'subpanel_effects_loot_prop2', icon=icon, icon_only=False, text='Helmet')
                
                if scene.subpanel_effects_loot_prop2:
                    from .config import helmet_range
                    for n in range(len(all_loot_items)):
                        if n in range(*helmet_range):
                            box.operator('object.lt_button_spawn', text=all_loot_items.get(str(n))).loot = all_loot_items.get(str(n)) 
                
                # Heals subpanel 3
                icon = 'DOWNARROW_HLT' if scene.subpanel_effects_loot_prop3 else 'RIGHTARROW'
                box.prop(scene, 'subpanel_effects_loot_prop3', icon=icon, icon_only=False, text='Heals')
                
                if scene.subpanel_effects_loot_prop3:
                    from .config import meds_range
                    for n in range(len(all_loot_items)):
                        if n in range(*meds_range):
                            box.operator('object.lt_button_spawn', text=all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))
                
                # Nades subpanel 4
                icon = 'DOWNARROW_HLT' if scene.subpanel_effects_loot_prop4 else 'RIGHTARROW'
                box.prop(scene, 'subpanel_effects_loot_prop4', icon=icon, icon_only=False, text='Nades')
                
                if scene.subpanel_effects_loot_prop4:
                    from .config import nades_range
                    for n in range(len(all_loot_items)):
                        if n in range(*nades_range):
                            box.operator('object.lt_button_spawn', text=all_loot_items.get(str(n))).loot = all_loot_items.get(str(n)) 
                
                # Ammo subpanel 5
                icon = 'DOWNARROW_HLT' if scene.subpanel_effects_loot_prop5 else 'RIGHTARROW'
                box.prop(scene, 'subpanel_effects_loot_prop5', icon=icon, icon_only=False, text='Ammo')
                
                if scene.subpanel_effects_loot_prop5:
                    from .config import ammo_range
                    for n in range(len(all_loot_items)):
                        if n in range(*ammo_range):
                            box.operator('object.lt_button_spawn', text=all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))
                
                # Backpacks subpanel 6
                icon = 'DOWNARROW_HLT' if scene.subpanel_effects_loot_prop6 else 'RIGHTARROW'
                box.prop(scene, 'subpanel_effects_loot_prop6', icon=icon, icon_only=False, text='Backpacks')
                
                if scene.subpanel_effects_loot_prop6:
                    from .config import bag_range
                    for n in range(len(all_loot_items)):
                        if n in range(*bag_range):
                            box.operator('object.lt_button_spawn', text=all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))  
                
                # Others subpanel 7
                icon = 'DOWNARROW_HLT' if scene.subpanel_effects_loot_prop7 else 'RIGHTARROW'
                box.prop(scene, 'subpanel_effects_loot_prop7', icon=icon, icon_only=False, text='Other')
                
                if scene.subpanel_effects_loot_prop7:
                    from .config import other_range
                    for n in range(len(all_loot_items)):
                        if n in range(*other_range):
                            box.operator('object.lt_button_spawn', text=all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))

            # Lobby Items
            row = layout.row()
            icon = 'DOWNARROW_HLT' if scene.subpanel_effects_lobby else 'RIGHTARROW'
            row.prop(scene, 'subpanel_effects_lobby', icon=icon, icon_only=True)
            row.label(text='Lobby Items')
            
            if scene.subpanel_effects_lobby:
                box = layout.box()
                
                from .config import all_lobby_other_items, lobby_lobby_range
                for n in range(len(all_lobby_other_items)):
                    if n in range(*lobby_lobby_range):
                        box.operator('object.lb_button_spawn', text=all_lobby_other_items.get(str(n))).lobby_other = all_lobby_other_items.get(str(n))

            # Other Items
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
                    
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Ship Top Color:')
                    split.prop(holo_0, "default_value", text="")
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Emissive:')
                    split.prop(holo_1, "default_value", text="") 
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Ship Bottom Color:')
                    split.prop(holo_2, "default_value", text="") 
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Emissive:')
                    split.prop(holo_3, "default_value", text="") 
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Strips Color:')
                    split.prop(holo_4, "default_value", text="") 
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Strips Height:')
                    split.prop(holo_5, "default_value", text="") 
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Strips Brightness:')
                    split.prop(holo_6, "default_value", text="") 
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Cone Color:')
                    split.prop(holo_7, "default_value", text="") 
                    split = box.split(factor=0.6)
                    col = split.column(align=True)
                    col.label(text='Cone Brightness:')
                    split.prop(holo_8, "default_value", text="")
            
            row = layout.row()
            icon = 'DOWNARROW_HLT' if scene.subpanel_effects_other else 'RIGHTARROW'
            row.prop(scene, 'subpanel_effects_other', icon=icon, icon_only=True)
            row.label(text='Other Items')
            
            if scene.subpanel_effects_other:
                box = layout.box()
                
                from .config import lobby_other_range
                for n in range(len(all_lobby_other_items)):
                    if n in range(*lobby_other_range):
                        box.operator('object.lb_button_spawn', text=all_lobby_other_items.get(str(n))).lobby_other = all_lobby_other_items.get(str(n))                
                        
                        if all_lobby_other_items.get(str(n)) == 'Respawn Beacon Hologram': 
                            holo()

        # Skydive
        row = layout.row()
        icon = 'DOWNARROW_HLT' if scene.subpanel_effects_sky else 'RIGHTARROW'
        row.prop(scene, 'subpanel_effects_sky', icon=icon, icon_only=True)
        row.label(text='Skydive (Experimental)')
        
        if scene.subpanel_effects_sky:
            box = layout.box()

            from .config import all_skydive_items
            for n in range(len(all_skydive_items)):
                split = box.split(factor=0.08)
                col = split.column(align=True)
                col.label(text='')
                split.operator('object.sky_button_spawn', text=all_skydive_items.get(str(n))).sky_effect = all_skydive_items.get(str(n))
            
            split = box.split(factor=0.6)
            col = split.column(align=True)
            col.label(text='')         
            split.operator('object.sky_button_spawn', text="Parent it").sky_effect = "Skydive_parent" 
            box.label(text='*Sel Model Bones before Parenting') 
            box.label(text='*Parent before import animation') 


# Other effects Tab
class OTHERS_PT_panel(bpy.types.Panel):
    """OTHER EFFECTS COLLECTION panel."""
    bl_parent_id = "OBJECT_PT_panel"
    bl_label = "OTHER EFFECTS COLLECTION"  
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prefs = scene.my_prefs

        # Animated Staging
        box = layout.box()
        box.operator('object.lb_button_spawn', text='Animated Staging + Camera').lobby_other = 'Animated Staging'
        
        try:
            bpy.data.objects['Staging Camera']
        except:
            pass
        else:
            split = box.split(factor=0.5)
            col = split.column(align=True)
            col.label(text='')
            split.operator('object.ef_button_spawn', text="Set Active").cool_effect = 'Staging Camera'

        # Basic Lights
        box.operator('object.ef_button_spawn', text='Basic Lights Setup').cool_effect = 'basic lights'

        # Wireframe Effect
        box.operator('object.ef_button_spawn', text='Cool Wireframe effect to Model').cool_effect = 'wireframe'
        
        split = box.split(factor=0.6)
        col = split.column(align=True)
        col.label(text='')
        split.operator('object.ef_button_spawn', text='Clear Effect').cool_effect = 'wireframe_clear'


# Updates tracker tab

class UPDATE_PT_panel(bpy.types.Panel):
    """UPDATES TRACKER panel."""
    bl_parent_id = "OBJECT_PT_panel"
    bl_label = "UPDATES TRACKER"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prefs = scene.my_prefs
        
        # Check for update Legion+
        import os
        if mode == 0:
            legion_folder = ast_fldr
        else:
            legion_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.legion_folder

        # Note: Global variables are managed in config.py module
        # The UPDATE_PT_panel uses these values from the config module
        
        if os.path.isdir(legion_folder) is not True:
            print("Apex Toolbox Addon: Legion folder not selected")

        global legion_cur_ver
        global legion_lts_ver
        global legion_folder_exist

        # Legion Settings
        if mode == 0:
            legion_folder = ast_fldr
            legion_folder_prefs = prefs
            lgn_folder = 'recolor_folder'
        else:
            legion_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.legion_folder
            legion_folder_prefs = bpy.context.preferences.addons['Apex_toolbox'].preferences
            lgn_folder = 'legion_folder'

        box = layout.box()
        
        if legion_cur_ver == '0':
            box.label(text="Select Folder with Legion+ FOLDER")
            box.label(text="NOT Folder with LegionPlus.exe")
            box.label(text="Example: MyFolder/Legion+1.4.1/LegionPlus.exe")
            box.label(text="select 'MyFolder'")
            box.prop(legion_folder_prefs, lgn_folder) 
            
            try:
                if os.path.exists(legion_folder) is True:
                    if legion_folder_exist == 0:
                        box.label(text="Legion+ Folder Not Found")
                    if legion_folder_exist == 2:
                        box.label(text="Name of Legion folder should look")
                        box.label(text="like this: 'Legion+1.4.1' (example)")
            except:
                pass
            
            box.label(text="--------------------------------------------------")

        # Installed Addons
        if legion_cur_ver != '0':
            box.label(text="Installed Software:")
            
            from .config import addon_name, addon_ver, io_anim_lts_ver, cast_lts_ver, semodel_lts_ver, mprt_lts_ver
            
            split = box.split(factor=0.7)
            col = split.column(align=True)
            col.label(text="Legion+")  
            split.label(text="v." + legion_cur_ver)
            
            if legion_lts_ver > legion_cur_ver:
                box.operator('object.lgndtranslate_url', text="Legion+ New Ver." + str(legion_lts_ver), icon='IMPORT').link = "legion_update"
            
            box.label(text="")    
        
        if addon_name is not None:
            box.label(text="Installed Addons:")
            
            for x in range(len(addon_name)):
                split = box.split(factor=0.7)
                col = split.column(align=True)
                col.label(text=addon_name[x])
                split.label(text="v." + addon_ver[x])
                
                if addon_name[x] == 'io_anim_seanim':
                    if io_anim_lts_ver > addon_ver[x]:
                        box.operator('object.lgndtranslate_url', text=addon_name[x] + " New Ver." + str(io_anim_lts_ver), icon='IMPORT').link = "io_anim_seanim"
                
                if addon_name[x] == 'io_scene_cast':
                    if cast_lts_ver > addon_ver[x]:
                        box.operator('object.lgndtranslate_url', text=addon_name[x] + " New Ver." + str(cast_lts_ver), icon='IMPORT').link = "cast"
                
                if addon_name[x] == 'io_model_semodel':
                    if semodel_lts_ver > addon_ver[x]:
                        box.operator('object.lgndtranslate_url', text=addon_name[x] + " New Ver." + str(semodel_lts_ver), icon='IMPORT').link = "io_model_semodel"
                
                if addon_name[x] == 'ApexMapImporter':
                    if mprt_lts_ver > addon_ver[x]:
                        box.operator('object.lgndtranslate_url', text=addon_name[x] + " New Ver." + str(mprt_lts_ver), icon='IMPORT').link = "mprt" 
        
        split = box.split(factor=0.2)
        col = split.column(align=True)
        col.label(text="")  
        split.operator('object.lgndtranslate_url', text="Check for Updates", icon='URL').link = "check_update"
