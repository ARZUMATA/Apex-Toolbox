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

"""Shadow operator module for Apex Toolbox addon."""

import bpy
from ..config import mode, ast_fldr, my_path, fbs, blend_file, ap_object, ap_material

# Auto Shadow
class BUTTON_SHADOW(bpy.types.Operator):
    """Operator for shadow material assignment functionality."""
    bl_label = "BUTTON_SHADOW"
    bl_idname = "object.button_shadow"
    bl_options = {'REGISTER', 'UNDO'}
    shadow: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        shadow = self.shadow
        
        shdw_mat = ['Shadow_big', 'Shadow_med', 'Shadow_med_face', 'shadow_black', 'shadow_eye']
        
        body_parts = [
            "eye",       # 0 - eye
            "eyecornea", # 1 - eye
            "glass",     # 2 - eye
            "lense",     # 3 - eye
            "eyeshadow", # 4 - black
            "teeth",     # 5 - black
            "head",      # 6 - face
            "helmet",    # 7 - face
            "hair",      # 8 - face
            "body",      # 9 - big
            "suit",      # 10 - big
            "v_arms",    # 11 - med
            "boots",     # 12 - med
            "gauntlet",  # 13 - med
            "jumpkit",   # 14 - med
            "gear"       # 15 - med
        ]        
        
        shadow_items = {
            'Eyes': [
                {'name': 'Shadow eyes'},
                {'name': 'Shadow fog'}, 
                {'name': 'Shadow left eye'},
                {'name': 'Shadow right eye'},
            ]
        }  
        
        shdw_bones = ['def_c_noseBridge', 'def_c_top_rope_12']
        
        if shadow == "Shadow":
            selection = [obj.name for obj in bpy.context.selected_objects]
            scene.render.fps = 30
            
            print("############# TEXTURING SHADOW START #############")
            
            # Append Shadow eyes objects if they don't exist
            if bpy.data.objects.get('Shadow eyes') is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, files=shadow_items.get("Eyes"))
        
            # Ensure shadow materials exist
            for x in range(len(shdw_mat)):
                mat = bpy.data.materials.get(shdw_mat[x])
                if mat is None:
                    bpy.ops.wm.append(directory=my_path + blend_file + ap_material, filename=shdw_mat[x])
            
            # Select all objects in selection
            for x in range(len(selection)):
                bpy.data.objects[selection[x]].select_set(True)
                x += 1
            
            for o in bpy.context.selected_objects:
                if o.type == 'MESH':
                    mat_exist = False
                    try:
                        mat_part = o.material_slots[0].name.rsplit('_', 1)[1] 
                        mat_name = o.material_slots[0].name
                        mat_exist = True
                    except:
                        print("Unable to find any Material. Shadow Material cannot assign") 
                    
                    if mat_exist is True:
                        if mat_part in body_parts:
                            part_index = body_parts.index(mat_part)
                            if part_index in range(0, 2):
                                mat = bpy.data.materials.get(shdw_mat[4])
                                o.data.materials.clear()
                                o.data.materials.append(mat)
                                print(mat_name + " *Assigned Shadow eye material*")
                            if part_index in range(2, 4):
                                bpy.data.objects[o.name].hide_set(True)
                                bpy.data.objects[o.name].hide_render = True
                                print(mat_name + " *Set as Hidden*")
                            if part_index in range(4, 6):
                                mat = bpy.data.materials.get(shdw_mat[3])
                                o.data.materials.clear()
                                o.data.materials.append(mat)
                                print(mat_name + " *Assigned Shadow black material*") 
                            if part_index in range(6, 9):
                                mat = bpy.data.materials.get(shdw_mat[2])
                                o.data.materials.clear()
                                o.data.materials.append(mat)
                                print(mat_name + " *Assigned Shadow face material*")
                            if part_index in range(9, 11):
                                mat = bpy.data.materials.get(shdw_mat[0])
                                o.data.materials.clear()
                                o.data.materials.append(mat)
                                print(mat_name + " *Assigned Shadow big material*")
                            if part_index in range(11, 16):
                                mat = bpy.data.materials.get(shdw_mat[1])
                                o.data.materials.clear()
                                o.data.materials.append(mat)
                                print(mat_name + " *Assigned Shadow med material*")
                        else:
                            print(mat_name + " *Skipped*")
            print("############# TEXTURING SHADOW END #############")
        
        # ADJUST AND PARENT SHADOW EYE
        if shadow == "Eyes_parent":
            sel_objects = bpy.context.selected_objects
            sel_names = [obj.name for obj in bpy.context.selected_objects]
            
            # Append Shadow eyes objects if they don't exist
            if bpy.data.objects.get('Shadow eyes') is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, files=shadow_items.get("Eyes"))
                bpy.ops.object.select_all(action='DESELECT')
                context.view_layer.objects.active = None
                sel_objects[0].select_set(True)
                context.view_layer.objects.active = sel_objects[0]
            
            if not bpy.context.selected_objects:
                print("Nothing selected. Please select Model Bones in Object Mode")
            else:
                if len(sel_objects) > 1:
                    print("More than 1 Object selected. Please select only 1 Bone Object")
                else: 
                    if sel_objects[0].type == 'ARMATURE':
                        for x in range(len(shdw_bones)):
                            if sel_objects[0].pose.bones.get(shdw_bones[x]) is not None:
                                get_nose_bone = sel_objects[0].pose.bones.get(shdw_bones[x])
                                nose_bone = bpy.data.objects[sel_names[0]].pose.bones[get_nose_bone.name].bone
                                break
                            
                        if nose_bone is not None:
                            bpy.ops.object.posemode_toggle()
                            context.object.data.bones.active = nose_bone
                            nose_bone.select = True
                            bpy.ops.view3d.snap_cursor_to_selected()
                            bpy.ops.object.posemode_toggle()
                            bpy.data.objects['Shadow eyes'].location = context.scene.cursor.location
                            if nose_bone.name == 'def_c_top_rope_12':
                                bpy.data.objects['Shadow eyes'].location = (0.0005311064887791872, -0.15554966032505035, 1.686505675315857)
                            bpy.ops.view3d.snap_cursor_to_center()
                                              
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = None 
                            bpy.data.objects['Shadow eyes'].select_set(True) 
                            context.view_layer.objects.active = bpy.data.objects['Shadow eyes']
                            boneToSelect = bpy.data.objects['Shadow eyes'].pose.bones['Bone'].bone
                            context.object.data.bones.active = boneToSelect
                            
                            context.view_layer.objects.active = None 
                            sel_objects[0].select_set(True) 
                            context.view_layer.objects.active = sel_objects[0]
                            boneToSelect2 = sel_objects[0].pose.bones[nose_bone.name].bone
                            context.object.data.bones.active = boneToSelect2
                            boneToSelect2.select = True  
                            bpy.ops.object.parent_set(type='BONE')
                            
                            bpy.ops.object.select_all(action='DESELECT')
                            sel_objects[0].select_set(True)
                            context.view_layer.objects.active = sel_objects[0] 
                            print("Parenting Shadow Eyes to " + sel_names[0] + " Done")
        
        return {'FINISHED'}
