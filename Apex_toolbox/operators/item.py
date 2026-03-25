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

"""Item spawn operators module for Apex Toolbox addon."""

import bpy
import os
import platform
from ..config import mode, ast_fldr, my_path, fbs, blend_file, ap_object, ap_material, ap_world, ap_action, all_loot_items, all_lobby_other_items, all_heirloom_items, armor_range, helmet_range, meds_range, nades_range, bag_range, ammo_range, other_range, lobby_lobby_range, lobby_other_range


######### Badge Buttons ###########    

class BDG_BUTTON_SPAWN(bpy.types.Operator):
    """Operator for spawning badge items."""
    bl_label = "BDG_BUTTON_SPAWN"
    bl_idname = "object.bdg_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    badge: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        if platform.system() == 'Windows':
            blend_file_local = ("\\Assets.blend")
        else:
            blend_file_local = ("/Assets.blend")

        if mode == 0:
            asset_folder = ast_fldr
        else:
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder

        badge_items = {
            'Badge - 20 Bombs (v2)': [
                {'name': 'Badge - 20 Bombs (v2)'},
                {'name': 'skull_gladcard_LOD0_SEModelMesh'}
            ]
        } 
        
        if bpy.data.objects.get(self.badge) is None:
            if self.badge == 'Badge - 20 Bombs (v2)':
                bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=badge_items.get('Badge - 20 Bombs (v2)'))
            else:
                bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, filename=self.badge)
            print(self.badge + " Appended")
        else:
            print(self.badge + " already inside")
    
        return {'FINISHED'}


######### Legends Effects Seer ###########

class SEER_BUTTON_SPAWN(bpy.types.Operator):
    """Operator for spawning Seer Ultimate effect."""
    bl_label = "SEER_BUTTON_SPAWN"
    bl_idname = "object.seer_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    lgnd_effect: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        lgnd_effect = self.lgnd_effect
        
        lgnd_effect_items = {
            'Seer Ultimate': [
                {'name': 'Seer Ultimate'},
            ],
        }  

    # Main loop for Seer items
        for i in range(len(lgnd_effect_items)):
            item = list(lgnd_effect_items.keys())[i]
            split_item = item.split()
            if lgnd_effect == item:
                
                ### Ultimate ###
                if i == 0:
                    bpy.ops.wm.append(directory=my_path + blend_file + ap_object, files=lgnd_effect_items.get(item))
                    
                print(item + " Appended") 
                break
            
        return {'FINISHED'}


######### Skydive Effects ###########    

class SKY_BUTTON_SPAWN(bpy.types.Operator):
    """Operator for spawning skydive effects."""
    bl_label = "SKY_BUTTON_SPAWN"
    bl_idname = "object.sky_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    sky_effect: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        sky_effect = self.sky_effect
        
        sky_effect_items = {
            'Skydive Ranked S9': [
                {'name': 'Skydive Ranked S9'},
                {'name': 'Skydive Ranked S9 trails'},
                {'name': 'Skydive Ranked S9 Smoke'},
            ],
        } 

        def color():
            selection = [obj.name for obj in bpy.context.selected_objects]
            for obj in bpy.context.selected_objects:
                obj.select_set(False)
            
            if len(selection) > 2:
                bpy.data.objects[selection[2]].select_set(True)
                mat = bpy.data.objects[selection[2]].active_material
                nodes = mat.node_tree.nodes['Skydive Group Color S9'].node_tree.nodes
                links = mat.node_tree.nodes['Skydive Group Color S9'].node_tree.links
                node_output = nodes['Group Output']
                
                colours = {
                    'Diamond': nodes['RGB.001'],
                    'Master': nodes['RGB.002'],
                    'Predator': nodes['RGB.003'],
                } 
                
                split_item = selection[2].split()[-1] if len(selection) > 2 else "Diamond"
                node_color = colours.get(split_item, nodes['RGB.001'])
                links.new(node_color.outputs[0], node_output.inputs[0])

        # Main loop for Skydive items
        for i in range(len(sky_effect_items)):
            item = list(sky_effect_items.keys())[i]
            split_item = item.rsplit(" ", 1)

            if sky_effect == item:
                ### Ranked S9 ###
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, files=sky_effect_items.get(split_item[0]))
                color()
                    
                print(item + " Appended")
        
        # Skydive Parenting
        if sky_effect == "Skydive_parent":
            sel_objects = bpy.context.selected_objects
            sel_names = [obj.name for obj in bpy.context.selected_objects]
            
            if not bpy.context.selected_objects:
                print("Nothing selected. Please select Model Bones in Object Mode")
            else:
                if len(sel_objects) > 1:
                    print("More than 1 Object selected. Please select only 1 Bone Object")
                else:
                    for bones in sel_objects:
                        if bones.type in ["ARMATURE"]:
                            if bpy.data.objects.get('Skydive Ranked S9') is None:
                                print("Skydive not Found. Pls add Effect first")
                            else:
                                # Deselect All and select only bones that were chosen
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                context.view_layer.objects.active = None
                                bpy.data.objects['Skydive Ranked S9'].select_set(True)
                                sel_objects[0].select_set(True)
                                context.view_layer.objects.active = sel_objects[0]

                                arm = bpy.data.objects['Skydive Ranked S9']
                                bpy.ops.object.mode_set(mode='EDIT')
                                bpy.ops.armature.select_all(action='DESELECT')

                                bones_to_select = ['Bone']
                                for bone in arm.data.edit_bones:
                                    if bone.name in bones_to_select:
                                        bone.select = True
                                        
                                arm = sel_objects[0]
                                bones_to_select = ['jx_c_pov']
                                for bone in arm.data.edit_bones:
                                    if bone.name in bones_to_select:
                                        bone.select = True 
                                        
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.parent_set(type='BONE')
                                bpy.ops.object.select_all(action='DESELECT')
                                
                                print("Parenting Skydive Done")
                        else:
                            print("Selected Object is Not a Bone. Pls Select Bones")

        return {'FINISHED'}


######### Weapons Buttons ###########    

class WPN_BUTTON_SPAWN(bpy.types.Operator):
    """Operator for spawning weapon effects."""
    bl_label = "WPN_BUTTON_SPAWN"
    bl_idname = "object.wpn_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    weapon: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        weapon = self.weapon
        
        weapon_items = {
            'Laser': [
                {'name': 'Laser'},
                {'name': 'Laser_pt1'},
                {'name': 'Laser_pt2'}
            ]
        }        

        # Flatline flame button normal
        if weapon == "flatline_s4_glow_hex_LOD0_SEModelMesh.125":
            if bpy.data.objects.get(weapon) is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, filename=weapon)
                print("Flatline Flames Effect Appended")
            else:
                print("Flatline Flames Effect already exist")

        # Flatline flame parent button
        if weapon == "flatline_parent_flame":
            if bpy.data.objects.get("flatline_s4_glow_hex_LOD0_SEModelMesh.125") is None:
                print("Flatline Flames Effect not Found. Pls add Effect first")
            else:
                if bpy.data.objects.get("flatline_v20_assim_w_LOD0_skel") is None:
                    print("Flatline model <<flatline_v20_assim_w>> not detected. Add the model then click Parent it")
                else:
                    bpy.ops.object.select_all(action='DESELECT')
                    context.view_layer.objects.active = None
                    bpy.data.objects['flatline_s4_glow_hex_LOD0_skel'].select_set(True) 
                    context.view_layer.objects.active = bpy.data.objects['flatline_s4_glow_hex_LOD0_skel']
                    boneToSelect = bpy.data.objects['flatline_s4_glow_hex_LOD0_skel'].pose.bones['static_prop'].bone
                    context.object.data.bones.active = boneToSelect
                    
                    context.view_layer.objects.active = None
                    bpy.data.objects['flatline_v20_assim_w_LOD0_skel'].select_set(True) 
                    context.view_layer.objects.active = bpy.data.objects['flatline_v20_assim_w_LOD0_skel']
                    boneToSelect2 = bpy.data.objects['flatline_v20_assim_w_LOD0_skel'].pose.bones['def_c_base'].bone
                    context.object.data.bones.active = boneToSelect2
                    boneToSelect2.select = True  
                    bpy.ops.object.parent_set(type='BONE')
                    print("Parenting Flames to Flatline Done")

        # Flatline flame button POV    
        if weapon == "flatline_s4_glow_hex_LOD0_SEModelMesh.001":
            if bpy.data.objects.get(weapon) is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, filename="flatline_s4_glow_hex_LOD0_SEModelMesh.001")
                print("POV Flatline Flames Effect Appended")
            else:
                print("POV Flatline Flames Effect already exist")

        # Flatline flame parent button POV
        if weapon == "flatline_pov_parent_flame":
            if bpy.data.objects.get("flatline_s4_glow_hex_LOD0_SEModelMesh.001") is None:
                print("POV Flatline Flames Effect not Found. Pls add Effect first")
            else:
                if bpy.data.objects.get("flatline_v20_assim_v_LOD0_skel") is None:
                    print("POV Flatline model <<flatline_v20_assim_v>> not detected. Add the model then click Parent it")
                else:
                    bpy.ops.object.select_all(action='DESELECT')
                    context.view_layer.objects.active = None 
                    bpy.data.objects['flatline_s4_glow_hex_LOD0_skel.001'].select_set(True) 
                    context.view_layer.objects.active = bpy.data.objects['flatline_s4_glow_hex_LOD0_skel.001']
                    boneToSelect = bpy.data.objects['flatline_s4_glow_hex_LOD0_skel.001'].pose.bones['static_prop'].bone
                    context.object.data.bones.active = boneToSelect
                    
                    context.view_layer.objects.active = None 
                    bpy.data.objects['flatline_v20_assim_v_LOD0_skel'].select_set(True) 
                    context.view_layer.objects.active = bpy.data.objects['flatline_v20_assim_v_LOD0_skel']
                    boneToSelect2 = bpy.data.objects['flatline_v20_assim_v_LOD0_skel'].pose.bones['def_c_base'].bone
                    context.object.data.bones.active = boneToSelect2
                    boneToSelect2.select = True  
                    bpy.ops.object.parent_set(type='BONE')
                    print("Parenting Flames to POV Flatline Done") 

        # Flatline POV Animation
        if weapon == "idle_reactive_layer_3_Fixed":
            if bpy.data.objects.get("flatline_v20_assim_v_LOD0_skel") is None:
                print("POV Flatline model 'flatline_v20_assim_v_LOD0_skel' not Found. Pls add model first")
            else:
                if bpy.data.objects.get(weapon) is None:
                    bpy.ops.wm.append(directory=my_path + blend_file + ap_action, filename="idle_reactive_layer_3_Fixed")
                    print("POV Reactive Animation Appended")
                else:
                    print("POV Reactive Animation already exist")  
                
                object = bpy.data.objects.get('flatline_v20_assim_v_LOD0_skel')   
                object.animation_data_create()
                action = object.animation_data.action
                object.animation_data.action = bpy.data.actions.get("idle_reactive_layer_3_Fixed")   

        # Laser effect
        if weapon == "Laser":
            if bpy.data.objects.get(weapon) is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, files=weapon_items.get("Laser"))
                print("Laser Effect Appended")
            else:
                print("Laser Effect already exist")

        # Laser Parenting
        if weapon == "Laser_parent":
            if bpy.data.objects.get("Laser") is None:
                print("Laser Effect not Found. Pls add effect first")
            else:
                sel_objects = bpy.context.selected_objects
                sel_names = [obj.name for obj in bpy.context.selected_objects]
                
                if not bpy.context.selected_objects:
                    print("Nothing selected. Please select Model Bones in Object Mode")
                else:
                    if len(sel_objects) > 1:
                        print("More than 1 Object selected. Please select only 1 Bone Object")
                    else: 
                        try:
                            bpy.data.objects['Laser'].location = sel_objects[0].pose.bones['ja_c_propGun'].location
                        except:
                            print("Bone 'ja_c_propGun' not found")
                        else:                                            
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = None 
                            bpy.data.objects['Laser'].select_set(True) 
                            context.view_layer.objects.active = bpy.data.objects['Laser']        
                            boneToSelect = bpy.data.objects['Laser'].pose.bones['Bone'].bone
                            context.object.data.bones.active = boneToSelect
                            
                            context.view_layer.objects.active = None 
                            sel_objects[0].select_set(True) 
                            context.view_layer.objects.active = sel_objects[0]  
                            sel_objects[0].rotation_euler.x = 1.5707963705062866
                            sel_objects[0].rotation_euler.y = 0
                            sel_objects[0].rotation_euler.z = 0                                   
                            boneToSelect2 = sel_objects[0].pose.bones['ja_c_propGun'].bone
                            context.object.data.bones.active = boneToSelect2
                            boneToSelect2.select = True  
                            bpy.ops.object.parent_set(type='BONE')
                            
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = None
                            sel_objects[0].select_set(True)
                            context.view_layer.objects.active = sel_objects[0] 
                            print("Parenting laser to " + sel_names[0] + " Done")

        # Laser Move
        if weapon == "Laser_move":
            if bpy.data.objects.get("Laser") is None:
                print("Laser Effect not Found. Pls add effect first")
            else:
                sel_objects = bpy.context.selected_objects
                sel_names = [obj.name for obj in bpy.context.selected_objects]
                
                if not bpy.context.selected_objects:
                    print("Nothing selected. Please select Model Bones in Object Mode")
                else:
                    if len(sel_objects) > 1:
                        print("More than 1 Object selected. Please select only 1 Bone Object")
                    else:
                        try:
                            bpy.data.objects['Laser'].location = sel_objects[0].pose.bones['ja_c_propGun'].location
                        except:
                            print("Bone 'ja_c_propGun' not found")
                        else:
                            sel_objects[0].rotation_euler.x = 1.5707963705062866
                            sel_objects[0].rotation_euler.y = 0
                            sel_objects[0].rotation_euler.z = 0
                            bpy.data.objects['Laser'].location.z = sel_objects[0].pose.bones['ja_c_propGun'].bone.matrix_local[1][3] * 0.0254 - 0.018
                            bpy.data.objects['Laser'].location.y -= sel_objects[0].pose.bones['ja_c_propGun'].bone.matrix_local[2][3] * 0.0254 + 0.04
                            print("Laser Effect moved") 

        return {'FINISHED'}


######### Loot Items Buttons ###########

class LT_BUTTON_SPAWN(bpy.types.Operator):
    """Operator for spawning loot items."""
    bl_label = "LT_BUTTON_SPAWN"
    bl_idname = "object.lt_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    loot: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        loot = self.loot
        
        if platform.system() == 'Windows':
            blend_file_local = ("\\Assets.blend")
        else:
            blend_file_local = ("/Assets.blend")

        if mode == 0:
            asset_folder = ast_fldr
        else:    
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder

        # Loot items dictionary
        loot_items = {
            'Armor': [
                {'name': 'w_loot_cha_shield_upgrade_body_LOD0_skel'},
                {'name': 'w_loot_cha_shield_upgrade_body_LOD0_SEModelMesh.106'},
                {'name': 'w_loot_cha_shield_upgrade_body_LOD0_SEModelMesh.107'}
            ],
            'Helmet': [
                {'name': 'w_loot_cha_shield_upgrade_head_LOD0_skel'},
                {'name': 'w_loot_cha_shield_upgrade_head_LOD0_SEModelMesh.108'},
                {'name': 'w_loot_cha_shield_upgrade_head_LOD0_SEModelMesh.109'}
            ],
            'Phoenix Kit': [
                {'name': 'w_loot_wep_iso_phoenix_kit_v1_LOD0_skel'},
                {'name': 'w_loot_wep_iso_phoenix_kit_v1_LOD0_SEModelMesh.135'},
                {'name': 'w_loot_wep_iso_phoenix_kit_v1_LOD0_SEModelMesh.136'}
            ],
            'Shield Battery': [
                {'name': 'w_loot_wep_iso_shield_battery_large_LOD0_skel'},
                {'name': 'w_loot_wep_iso_shield_battery_large_LOD0_SEModelMesh.137'},
                {'name': 'w_loot_wep_iso_shield_battery_large_LOD0_SEModelMesh.138'}
            ],
            'Shield Cell': [
                {'name': 'w_loot_wep_iso_shield_battery_small_LOD0_skel'},
                {'name': 'w_loot_wep_iso_shield_battery_small_LOD0_SEModelMesh.139'},
                {'name': 'w_loot_wep_iso_shield_battery_small_LOD0_SEModelMesh.140'}
            ],
            'Med Kit': [
                {'name': 'w_loot_wep_iso_health_main_large_LOD0_skel'},
                {'name': 'w_loot_wep_iso_health_main_large_LOD0_SEModelMesh.133'}
            ],
            'Syringe': [
                {'name': 'w_loot_wep_iso_health_main_small_LOD0_skel'},
                {'name': 'w_loot_wep_iso_health_main_small_LOD0_SEModelMesh.134'}
            ],
            'Health Injector': [
                {'name': 'w_health_injector_LOD0_skel'}, 
                {'name': 'w_health_injector_LOD0_SEModelMesh.084'}
            ],            
            'Grenade': [
                {'name': 'm20_f_grenade_LOD0_skel'}, 
                {'name': 'm20_f_grenade_LOD0_SEModelMesh.147'}
            ],
            'Arc Star': [
                {'name': 'w_loot_wep_iso_shuriken_LOD0_skel'}, 
                {'name': 'w_loot_wep_iso_shuriken_LOD0_SEModelMesh.142'}
            ],
            'Thermite': [
                {'name': 'w_thermite_grenade_LOD0_skel'}, 
                {'name': 'w_thermite_grenade_LOD0_SEModelMesh.143'}
            ], 
            'Backpack Lv.3': [
                {'name': 'w_loot_char_backpack_heavy_LOD0_skel'}, 
                {'name': 'w_loot_char_backpack_heavy_LOD0_SEModelMesh.118'}
            ],    
            'Backpack Lv.2': [
                {'name': 'w_loot_char_backpack_medium_LOD0_skel'}, 
                {'name': 'w_loot_char_backpack_medium_LOD0_SEModelMesh.120'}
            ],    
            'Backpack Lv.1': [
                {'name': 'w_loot_char_backpack_light_LOD0_skel'}, 
                {'name': 'w_loot_char_backpack_light_LOD0_SEModelMesh.119'}
            ], 
            'Light Ammo': [
                {'name': 'w_loot_wep_ammo_sc_LOD0_skel'}, 
                {'name': 'w_loot_wep_ammo_sc_LOD0_SEModelMesh.123'}
            ], 
            'Heavy Ammo': [
                {'name': 'w_loot_wep_ammo_hc_LOD0_skel'}, 
                {'name': 'w_loot_wep_ammo_hc_LOD0_SEModelMesh.121'}
            ], 
            'Energy Ammo': [
                {'name': 'w_loot_wep_ammo_nrg_LOD0_skel'}, 
                {'name': 'w_loot_wep_ammo_nrg_LOD0_SEModelMesh.122'}
            ],
            'Shotgun Ammo': [
                {'name': 'w_loot_wep_ammo_shg_LOD0_skel'}, 
                {'name': 'w_loot_wep_ammo_shg_LOD0_SEModelMesh.124'}
            ], 
            'Respawn Beacon': [
                {'name': 'beacon_capsule_01_LOD0_skel'}, 
                {'name': 'beacon_capsule_01_LOD0_SEModelMesh.144'}
            ],  
            'Knockdown Shield': [
                {'name': 'w_loot_wep_iso_shield_down_v1_LOD0_skel'}, 
                {'name': 'w_loot_wep_iso_shield_down_v1_LOD0_SEModelMesh.141'}
            ],  
            'Heat Shield': [
                {'name': 'loot_void_ring_LOD0_skel'}, 
                {'name': 'loot_void_ring_LOD0_SEModelMesh.146'}
            ],  
            'Death Box': [
                {'name': 'death_box_01_gladcard_LOD0_skel.001'}, 
                {'name': 'death_box_01_gladcard_LOD0_SEModelMesh.145'},
                {'name': 'death_box_02_LOD0_skel'},
                {'name': 'death_box_02_LOD0_SEModelMesh.007'},
                {'name': 'deathbox_banner_line'},
                {'name': 'deathbox_banner_text'}
            ],
        }  

        # Helper function for armor color
        def armor_color():
            selection = [obj.name for obj in bpy.context.selected_objects]
            for obj in bpy.context.selected_objects:
                obj.select_set(False)
            
            if len(selection) > 1:
                bpy.data.objects[selection[1]].select_set(True)
                mat = bpy.data.objects[selection[1]].active_material
                nodes = mat.node_tree.nodes
                links = mat.node_tree.links
                node_output = nodes['Armor shader']
                
                colours = {
                    'Blue': nodes['RGB.001'],
                    'Purple': nodes['RGB.002'],
                    'Gold': nodes['RGB'],
                    'Red': nodes['RGB.003'],
                } 
                
                split_item = selection[1].split()[-1] if len(selection) > 1 else "White"
                if split_item == "White":
                    pass
                else:
                    node_color = colours.get(split_item, nodes['RGB'])
                    links.new(node_color.outputs[0], node_output.inputs[0])

        # Main loop for Loot items
        for i in range(len(loot_items)):
            item = list(loot_items.keys())[i]
            split_item = item.split()

            if loot == item:
                
                ### Body Armor ###
                if i in range(0, 5):
                    bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=loot_items.get('Armor'))
                    armor_color()
                    
                ### Helmet ###
                if i in range(5, 10):
                    bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=loot_items.get('Helmet'))
                    armor_color()
                
                ### Meds ###
                if i in range(10, 16):
                    bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=loot_items.get(item))

                ### Nades ###
                if i in range(16, 19):
                    bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=loot_items.get(item))

                ### Ammo ###
                if i in range(23, 27):
                    bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=loot_items.get(item))

                ### Backpack ###
                if i in range(20, 23):
                    bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=loot_items.get(item))
                   
                ### Other items ###
                if i in range(27, 31):
                    bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=loot_items.get(item))

                print(item + " Appended") 
                break
            
        return {'FINISHED'} 


######### Lobby and Other Items Buttons ###########    

class LB_BUTTON_SPAWN(bpy.types.Operator):
    """Operator for spawning lobby and other items."""
    bl_label = "LB_BUTTON_SPAWN"
    bl_idname = "object.lb_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    lobby_other: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        lobby_other = self.lobby_other
        
        if platform.system() == 'Windows':
            blend_file_local = ("\\Assets.blend")
        else:
            blend_file_local = ("/Assets.blend")

        if mode == 0:
            asset_folder = ast_fldr
        else:    
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder

        # Lobby and other items dictionary
        lobby_other_items = {
            'Heirloom Shards': [
                {'name': 'heirloom_LOD0_skel'},
                {'name': 'heirloom_LOD0_SEModelMesh'}
            ],
            'Epic Shards': [
                {'name': 'currency_crafting_epic_LOD0_skel'}, 
                {'name': 'currency_crafting_epic_LOD0_SEModelMesh.003'}
            ], 
            'Rare Shards': [
                {'name': 'currency_crafting_rare_LOD0_skel'}, 
                {'name': 'currency_crafting_rare_LOD0_SEModelMesh.004'}
            ],   
            'Loot Drone': [
                {'name': 'drone_frag_loot_LOD0_skel'}, 
                {'name': 'drone_frag_loot_LOD0_SEModelMesh.005'}
            ],   
            'Respawn Beacon Hologram': [
                {'name': 'goblin_dropship_holo_LOD0_skel'}, 
                {'name': 'goblin_dropship_holo_LOD0_SEModelMesh.001'}, 
                {'name': 'goblin_dropship_holo_LOD0_SEModelMesh.002'}, 
                {'name': 'Respawn Hologram'}, 
                {'name': 'Respawn Spot Light'}
            ],   
            'Loot Ball': [
                {'name': 'loot_sphere_LOD0_skel'}, 
                {'name': 'loot_sphere_LOD0_SEModelMesh.006'}
            ],
            'Animated Staging': [
                {'name': 'Animated Staging With Light'}, 
                {'name': 'Area_left'},
                {'name': 'Area_overhead'},
                {'name': 'Area_right'},
                {'name': 'Floor Plane'},
                {'name': 'Staging Camera'},
            ]
        }   

        # Main loop for Lobby and Other items
        if lobby_other == 'Animated Staging':
            if platform.system() == 'Windows':
                blend_file_local = ("\\ApexShader.blend")
            else:
                blend_file_local = ("/ApexShader.blend")
            bpy.ops.wm.append(directory=my_path + blend_file_local + ap_object, files=lobby_other_items.get(lobby_other))
            print(lobby_other + " Appended")
        else:                        
            for i in range(len(lobby_other_items)):
                item = list(lobby_other_items.keys())[i]
                split_item = item.split()

                if lobby_other == item:
                    
                    ### Lobby Items ###
                    if i in range(0, 4):
                        bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=lobby_other_items.get(item))
                        
                    ### Other Items ###
                    if i in range(20, 22):
                        bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=lobby_other_items.get(item))

                    print(item + " Appended") 
                    break
            
        return {'FINISHED'} 


######### Heirloom Buttons ###########    

class HL_BUTTON_SPAWN(bpy.types.Operator):
    """Operator for spawning heirloom items."""
    bl_label = "HL_BUTTON_SPAWN"
    bl_idname = "object.hl_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    heirloom: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        heirloom = self.heirloom
        
        if platform.system() == 'Windows':
            blend_file_local = ("\\Assets.blend")
        else:
            blend_file_local = ("/Assets.blend")

        if mode == 0:
            asset_folder = ast_fldr
        else:    
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder

        # Heirloom items dictionary
        heirloom_items = {
            'Gibraltar Set': [
                {'name': 'gibraltar_heirloom_v_LOD0_skel'},
                {'name': 'gibraltar_heirloom_v_LOD0_SEModelMesh.008'}
            ],
            'Bangalore Set': [
                {'name': 'ptpov_bangalore_heirloom_LOD0_skel'}, 
                {'name': 'ptpov_bangalore_heirloom_LOD0_SEModelMesh.009'},
                {'name': 'ptpov_bangalore_heirloom_LOD0_SEModelMesh.010'}
            ], 
            'Lifeline Set (Animated)': [
                {'name': 'ptpov_baton_lifeline_LOD0_skel'}, 
                {'name': 'ptpov_baton_lifeline_LOD0_SEModelMesh.011'}
            ],   
            'Bloodhound Set': [
                {'name': 'ptpov_bloodhound_axe_LOD0_skel'}, 
                {'name': 'ptpov_bloodhound_axe_LOD0_SEModelMesh.013'}
            ],   
            'Caustic Set': [
                {'name': 'ptpov_caustic_heirloom_LOD0_skel'}, 
                {'name': 'ptpov_caustic_heirloom_LOD0_SEModelMesh.014'}
            ],   
            'Crypto Set': [
                {'name': 'ptpov_crypto_heirloom_LOD0_skel'}, 
                {'name': 'ptpov_crypto_heirloom_LOD0_SEModelMesh.015'},
                {'name': 'ptpov_crypto_heirloom_LOD0_SEModelMesh.016'},
                {'name': 'ptpov_crypto_heirloom_LOD0_SEModelMesh.017'}
            ],
            'Wraith Set': [
                {'name': 'ptpov_kunai_wraith_LOD0_skel'}, 
                {'name': 'ptpov_kunai_wraith_LOD0_SEModelMesh.018'}
            ],  
            'Mirage Set': [
                {'name': 'ptpov_mirage_heirloom_LOD0_skel'}, 
                {'name': 'ptpov_mirage_heirloom_LOD0_SEModelMesh.019'}, 
                {'name': 'ptpov_mirage_heirloom_LOD0_SEModelMesh.020'}, 
                {'name': 'ptpov_mirage_heirloom_LOD0_SEModelMesh.021'}
            ],  
            'Octane Set': [
                {'name': 'ptpov_octane_knife_LOD0_skel'}, 
                {'name': 'ptpov_octane_knife_LOD0_SEModelMesh.022'}, 
                {'name': 'ptpov_octane_knife_LOD0_SEModelMesh.023'}
            ],  
            'Pathfinder Set (Animated)': [
                {'name': 'ptpov_pathfinder_gloves_LOD0_skel'}, 
                {'name': 'ptpov_pathfinder_gloves_LOD0_SEModelMesh.024'},
                {'name': 'ptpov_pathfinder_gloves_LOD0_SEModelMesh.025'},
                {'name': 'ptpov_pathfinder_gloves_LOD0_SEModelMesh.026'},
                {'name': 'ptpov_pathfinder_gloves_LOD0_SEModelMesh.027'},
                {'name': 'ptpov_pathfinder_gloves_LOD0_SEModelMesh.028'},
                {'name': 'ptpov_pathfinder_gloves_LOD0_SEModelMesh.029'},
                {'name': 'ptpov_pathfinder_gloves_LOD0_SEModelMesh.030'},
                {'name': 'ptpov_pathfinder_gloves_LOD0_SEModelMesh.031'} 
            ],  
            'Rampart Set': [
                {'name': 'ptpov_rampart_heirloom_LOD0_skel'}, 
                {'name': 'ptpov_rampart_heirloom_LOD0_SEModelMesh.032'}, 
                {'name': 'ptpov_rampart_heirloom_LOD0_SEModelMesh.033'},
                {'name': 'ptpov_rampart_heirloom_LOD0_SEModelMesh.034'}
            ],  
            'Revenant Set': [
                {'name': 'revenant_heirloom_v21_base_v_LOD0_skel'}, 
                {'name': 'revenant_heirloom_v21_base_v_LOD0_SEModelMesh.035'}
            ],  
            'Valkyrie Set': [
                {'name': 'valkyrie_heirloom_v22_base_v_LOD0_skel'}, 
                {'name': 'valkyrie_heirloom_v22_base_v_LOD0_SEModelMesh.036'}
            ],  
            'Wattson Set (Animated)': [
                {'name': 'wattson_heirloom_v21_base_v_LOD0_skel'}, 
                {'name': 'wattson_heirloom_v21_base_v_LOD0_SEModelMesh.037'}
            ]
        }   

        # Main loop for Heirloom items    
        for i in range(len(heirloom_items)):
            item = list(heirloom_items.keys())[i]
            split_item = item.split()

            if heirloom == item:
                
                ### Heirloom Items ###
                if i in range(len(heirloom_items)):
                    bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_object, files=heirloom_items.get(item))

                print(item + " Appended") 
                break
            
        return {'FINISHED'} 


######### Other Effects Buttons ###########    

class EF_BUTTON_SPAWN(bpy.types.Operator):
    """Operator for other effects."""
    bl_label = "EF_BUTTON_SPAWN"
    bl_idname = "object.ef_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    cool_effect: bpy.props.StringProperty(name="Added")

    # Operator Properties
    wfrm_thickness: bpy.props.FloatProperty(
        name="Wireframe Thickness",
        description="Thickness of the applied wireframe",
        default=0.07,
        min=0,
        max=0.15
    ) 

    def execute(self, context):
        cool_effect = self.cool_effect
        wfrm_thickness = self.wfrm_thickness
        sel = bpy.context.selected_objects 
        
        # Wireframe Effect
        if cool_effect == 'wireframe':
            if not bpy.context.selected_objects:
                print("Nothing selected. Please select Object to apply Effect")
            else:
                for obj in sel:
                    if obj.type in ["MESH"]:
                        context.view_layer.objects.active = obj

                        exists = False
                        for mod in obj.modifiers:
                            if mod.name == "Wireframe":
                                exists = True

                        if exists:
                            mod = obj.modifiers["Wireframe"]
                            mod.thickness = wfrm_thickness
                        else: 
                            obj.modifiers.new("Wireframe", "WIREFRAME")
                            mod = obj.modifiers["Wireframe"]
                            mod.thickness = wfrm_thickness
                                
                print("Cool Wireframe Effect Applied") 
        
        # Wireframe Clear Effect
        if cool_effect == 'wireframe_clear':
            if not bpy.context.selected_objects:
                print("Nothing selected. Please select Object to apply Effect")
            else:
                for obj in sel:
                    if obj.type in ["MESH"]:
                        context.view_layer.objects.active = obj

                        exists = False
                        for mod in obj.modifiers:
                            if mod.name == "Wireframe":
                                exists = True

                        if exists:
                            mod = obj.modifiers["Wireframe"]
                            obj.modifiers.remove(mod)
                                
                print("Cool Wireframe Effect Cleared")

        # Set Active (Staging spawn in Lobby Other Items)
        if cool_effect == 'Staging Camera':
            cam = bpy.data.objects['Staging Camera']
            bpy.data.scenes['Scene'].camera = cam
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = None
            bpy.data.objects['Staging Camera'].select_set(True)
            context.view_layer.objects.active = bpy.data.objects['Staging Camera']
            print("'Staging Camera' Set as Active")
            del cam
            
        # Add Basic Lights
        if cool_effect == 'basic lights':
            bpy.ops.wm.append(directory=my_path + blend_file + ap_collection, filename='Basic Lights Setup')
            
        # Adjust Model
        if cool_effect == 'adjust_model':
            if not bpy.context.selected_objects:
                print("Nothing selected. Please select Model Bones in Object Mode")
            else:
                selection = [obj.name for obj in bpy.context.selected_objects]
                for o in bpy.context.selected_objects:
                    if o.type == 'ARMATURE':
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = None
                        o.select_set(True)
                        context.view_layer.objects.active = o
                        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))
                        bpy.ops.transform.resize(value=(0.0254, 0.0254, 0.0254), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
                        bpy.ops.view3d.view_all()
                        for x in range(len(selection)):
                            bpy.data.objects[selection[x]].select_set(True)
                            x += 1
                        break
                    else:
                        print("No Armature found in selected objects")    
        
        return {'FINISHED'}
