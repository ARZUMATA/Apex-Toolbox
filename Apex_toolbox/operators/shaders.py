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

"""Shader and HDRI operator module for Apex Toolbox addon."""

import bpy
import os
import platform
from ..config import mode, ast_fldr, my_path, fbs, blend_file, ap_node, ap_world, bldr_hdri_path

# Shaders operator
class BUTTON_SHADERS(bpy.types.Operator):
    """Operator for appending shader node groups."""
    bl_label = "BUTTON_SHADERS"
    bl_idname = "object.button_shaders"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        
        if prefs.cust_enum_shader == 'OP1':
            if bpy.data.node_groups.get('Apex Shader') is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename='Apex Shader')
                print("Apex Shader Appended")
            else:
                print("Apex Shader Already exist")
        
        if prefs.cust_enum_shader == 'OP2':
            if bpy.data.node_groups.get('Apex Shader+_v3.4') is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename='Apex Shader+_v3.4')
                print("Apex Shader+_v3.4 Appended")
            else:
                print("Apex Shader+_v3.4 Already exist")
        
        if prefs.cust_enum_shader == 'OP3':
            if bpy.data.node_groups.get('S/G-Blender') is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename='S/G-Blender')
                print("S/G-Blender Appended")
            else:
                print("S/G-Blender Already exist")
        
        if prefs.cust_enum_shader == 'OP4':
            if bpy.data.node_groups.get('Apex Cycles (Blue)') is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename='Apex Cycles (Blue)')
                print("Apex Cycles (Blue) Appended")
            else:
                print("Apex Cycles (Blue) Already exist")
        
        if prefs.cust_enum_shader == 'OP5':
            if bpy.data.node_groups.get('Apex Mobile Shader (Biast12)') is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename='Apex Mobile Shader (Biast12)')
                print("Apex Mobile Shader (Biast12) Appended")
            else:
                print("Apex Mobile Shader (Biast12) Already exist")
        
        return {'FINISHED'}

class BUTTON_HDRIFULL(bpy.types.Operator):
    """Operator for appending HDRI environments."""
    bl_label = "BUTTON_HDRIFULL"
    bl_idname = "object.button_hdrifull"
    bl_options = {'REGISTER', 'UNDO'}
    hdri: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        hdri = self.hdri
        
        bldr_hdri = ['City', 'Courtyard', 'Forest', 'Interior', 'Night', 'Studio', 'Sunrise', 'Sunset']
        
        if mode == 0:
            asset_folder = ast_fldr
        else:
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder

        # Set blend file path based on platform
        if platform.system() == 'Windows':
            blend_file_local = ("\\Assets.blend")
        else:
            blend_file_local = ("/Assets.blend")
                                
        if hdri == 'hdri_noast': 
            # HDRI without assets (Blender built-in)
            hdri_name_map = {
                'OP1': "World",
                'OP2': "City",
                'OP3': "Courtyard",
                'OP4': "Forest",
                'OP5': "Interior",
                'OP6': "Night",
                'OP7': "Studio",
                'OP8': "Sunrise",
                'OP9': "Sunset"
            }

            if platform.system() == 'Windows':
                blend_file_local = ("\\ApexShader.blend")
            else:
                blend_file_local = ("/ApexShader.blend")
            
            hdri_name = hdri_name_map.get(prefs.cust_enum_hdri_noast, "World")
            
            if hdri_name == "World":
                if scene.world != hdri_name:
                    if hdri_name not in bpy.data.worlds:
                        bpy.ops.wm.append(directory=my_path + blend_file_local + ap_world, filename=hdri_name)
                    hdri_obj = bpy.data.worlds[hdri_name]
                    scene.world = hdri_obj
            else:
                if scene.world != 'Blender HDRI':
                    if 'Blender HDRI' not in bpy.data.worlds:
                        bpy.ops.wm.append(directory=my_path + blend_file_local + ap_world, filename='Blender HDRI')
                    hdri_obj = bpy.data.worlds['Blender HDRI']
                    scene.world = hdri_obj
                    hdri_img_path = bldr_hdri_path + hdri_name + '.exr'
                    hdri_image = bpy.data.images.load(hdri_img_path)
                    bpy.data.worlds['Blender HDRI'].node_tree.nodes['Environment Texture'].image = hdri_image

        if hdri == 'hdri':
            # HDRI with assets (Apex-specific HDRIs)
            hdri_name_map = {
                'OP1': "World",
                'OP2': "Apex Lobby HDRI",
                'OP3': "Party crasher HDRI",
                'OP4': "Encore HDRI",
                'OP5': "Habitat HDRI",
                'OP6': "Kings Canyon HDRI",
                'OP7': "Kings Canyon New HDRI",
                'OP8': "Kings Canyon Night HDRI",
                'OP9': "Olympus HDRI",
                'OP10': "Phase Runner HDRI",
                'OP11': "Storm Point HDRI",
                'OP12': "Worlds Edge HDRI",
                'OP13': "Sky HDRI",
                'OP14': "blank",
                'OP15': "Indoor",
                'OP16': "Outdoor",
                'OP17': "Outdoor under shade",
                'OP18': "Morning Forest",
                'OP19': "blank",
                'OP20': "City",
                'OP21': "Courtyard",
                'OP22': "Forest",
                'OP23': "Interior",
                'OP24': "Night",
                'OP25': "Studio",
                'OP26': "Sunrise",
                'OP27': "Sunset"
            }

            hdri_name = hdri_name_map.get(prefs.cust_enum_hdri, "World")
            
            if hdri_name in bldr_hdri:
                # Blender built-in HDRI
                if scene.world != 'Blender HDRI':
                    if 'Blender HDRI' not in bpy.data.worlds:
                        if platform.system() == 'Windows':
                            blend_file_local = ("\\ApexShader.blend")
                        else:
                            blend_file_local = ("/ApexShader.blend")
                        bpy.ops.wm.append(directory=my_path + blend_file_local + ap_world, filename='Blender HDRI')
                    hdri_obj = bpy.data.worlds['Blender HDRI']
                    scene.world = hdri_obj
                    hdri_img_path = bldr_hdri_path + hdri_name + '.exr'
                    hdri_image = bpy.data.images.load(hdri_img_path)
                    bpy.data.worlds['Blender HDRI'].node_tree.nodes['Environment Texture'].image = hdri_image
            else:
                # Apex-specific HDRI from assets
                if hdri_name not in bpy.data.worlds:
                    if hdri_name == 'blank':
                        pass
                    else:
                        bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_world, filename=hdri_name)
                        hdri_obj = bpy.data.worlds[hdri_name]
                        scene.world = hdri_obj
                        print(hdri_name + " has been Appended and applied to the World")
                else:
                    if scene.world != hdri_name:
                        hdri_obj = bpy.data.worlds[hdri_name]
                        scene.world = hdri_obj
                        print(hdri_name + " is already inside and it's been applied to the World")

        if hdri == 'background':
            # Background images (sky sphere)
            hdri_name_map = {
                'OP1': "blank",
                'OP2': "blank",
                'OP3': "party crasher.png",
                'OP4': "encore.png",
                'OP5': "habit.png",
                'OP6': "Kings Canyon.png",
                'OP7': "Kings Canyon_new.png",
                'OP8': "Kings Canyon_night.png",
                'OP9': "olympus.png",
                'OP10': "phase runner.png",
                'OP11': "storm point.png",
                'OP12': "worlds edge.png",
                'OP13': "Sky-1.png",
                'OP14': "blank",
                'OP15': "blank",
                'OP16': "blank",
                'OP17': "blank",
                'OP18': "blank"
            }

            hdri_name = hdri_name_map.get(prefs.cust_enum_hdri, "blank")
            
            if hdri_name == 'blank':
                pass
            else:
                if bpy.data.objects.get('Sky_background') is None:
                    bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_world, filename='Sky_background')
                    print("Sky Sphere Appended")

                for obj in bpy.context.selected_objects:
                    obj.select_set(False)
                
                bpy.data.objects['Sky_background'].select_set(True)
                mat = bpy.data.objects['Sky_background'].active_material
                nodes = mat.node_tree.nodes['Image Texture.001']
                
                if bpy.data.images.get(hdri_name) is None:
                    bpy.ops.wm.append(directory=asset_folder + blend_file_local + ap_world, filename=hdri_name)
                
                img = bpy.data.images[hdri_name]
                nodes.image = img
                print(hdri_name + " image has been set as Sky Texture")

        return {'FINISHED'}
