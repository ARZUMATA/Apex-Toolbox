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

"""Character-specific operators module for Apex Toolbox addon."""

import bpy
from ..config import mode, ast_fldr, my_path, fbs, blend_file, ap_object

######### Wraith Buttons ###########    

class WR_BUTTON_PORTAL(bpy.types.Operator):
    """Operator for spawning Wraith Portal."""
    bl_label = "WR_BUTTON_PORTAL"
    bl_idname = "object.wr_button_portal"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        portal_items = [
            {'name': 'wraith_portal'}, 
            {'name': 'Inner_Ring_1'}, 
            {'name': 'Inner_Ring_1_br'},
            {'name': 'Inner_Ring_2'},
            {'name': 'Inner_Ring_2_br'}
        ]    
        
        if bpy.data.objects.get('wraith_portal') is None:
            bpy.ops.wm.append(directory=my_path + blend_file + ap_object, files=portal_items)
            print("Wraith Portal Appended")
        else:
            print("Wraith Portal already exist")
            
        return {'FINISHED'}      

######### Gibraltar Buttons ###########    

class GB_BUTTON_ITEMS(bpy.types.Operator):
    """Operator for spawning Gibraltar Dome Shield."""
    bl_label = "GB_BUTTON_ITEMS"
    bl_idname = "object.gb_button_items"
    bl_options = {'REGISTER', 'UNDO'}
    gibby: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        gibby = self.gibby
        
        bubble_items_friendly = [
            {'name': 'Gibby bubble friendly'}, 
            {'name': 'Gibby bubble core friendly'}, 
            {'name': 'Gibby bubble image friendly'},
            {'name': 'Gibby bubble rod friendly'}
        ]    
        
        bubble_items_enemy = [
            {'name': 'Gibby bubble enemy'}, 
            {'name': 'Gibby bubble core enemy'}, 
            {'name': 'Gibby bubble image enemy'},
            {'name': 'Gibby bubble rod enemy'}
        ]                   
        
    # Gibby Dome Shield friendly
        if gibby == "Gibby bubble friendly":
            if bpy.data.objects.get(gibby) is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, files=bubble_items_friendly)
                print("Gibby Friendly Bubble Appended")
            else:
                print("Gibby Friendly Bubble already exist")
        
    # Gibby Dome Shield enemy        
        if gibby == "Gibby bubble enemy":
            if bpy.data.objects.get(gibby) is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, files=bubble_items_enemy)
                print("Gibby Enemy Bubble Appended")
            else:
                print("Gibby Enemy Bubble already exist")
                
        return {'FINISHED'} 

######### Mirage Buttons ###########    

class MR_BUTTON_DECOY(bpy.types.Operator):
    """Operator for spawning Mirage Decoy."""
    bl_label = "Decoy Outline Thickness"
    bl_idname = "object.mr_button_decoy"
    bl_options = {'REGISTER', 'UNDO'}
    mr_decoy: bpy.props.StringProperty(name="Added")

    # Operator Properties
    outline_thickness: bpy.props.FloatProperty(
        name="Outline Thickness",
        description="Thickness of the applied outline",
        default=0.23,
        min=0,
        max=1000000
    )

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs   
        sel = bpy.context.selected_objects
        mr_decoy = self.mr_decoy
        
        decoy_items = [
            {'name': 'Decoy'}, 
            {'name': 'Floor_bloom'}, 
            {'name': 'Flare Generator'},
            {'name': 'Decoy Effects'},
            {'name': 'Decoy flare'},
            {'name': 'Decoy Text'},
            {'name': 'Decoy text triangle'},
            {'name': 'Psyche_Out'}
        ]

    # Mirage Decoy Effect Add
        if mr_decoy == "Decoy":
            if bpy.data.objects.get('Decoy') is None:
                # Copy current selection
                selection = [obj.name for obj in bpy.context.selected_objects]
                # Append Objects
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, files=decoy_items)
                # Unselect all in selected
                for obj in bpy.context.selected_objects:
                    obj.select_set(False)
                # Select initially selected
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1 
                # Append Material                
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, filename='Mirage_decoy_Material')
                # Unselect all in selected
                for obj in bpy.context.selected_objects:
                    obj.select_set(False)
                # Select initially selected
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1

                print("Mirage Decoy Effect Appended, Material applied. Adding Modifier")
            else:
                print("Mirage Decoy Effect already exist. Adding Modifier only")

        for obj in sel:
            if obj.type in ["MESH", "CURVE"]:
                context.view_layer.objects.active = obj

                # Material
                mat_missing = True
                for slot in obj.data.materials:
                    if slot is not None:
                        if slot.name == "Mirage_decoy_Material":
                            mat_missing = False

                if mat_missing:
                    mat = bpy.data.materials.get("Mirage_decoy_Material")
                    obj.data.materials.append(mat)

                # Modifier
                exists = False
                for mod in obj.modifiers:
                    if mod.name == "mirage_decoy":
                        exists = True

                if exists:
                    mod = obj.modifiers["mirage_decoy"]
                    mod.thickness = -(self.outline_thickness)
                else: 
                    obj.modifiers.new("mirage_decoy", "SOLIDIFY")
                    mod = obj.modifiers["mirage_decoy"]
                    mod.use_flip_normals = True
                    mod.use_rim = False
                    mod.thickness = -(self.outline_thickness)
                    mod.material_offset = 999
                    
        print("Mirage Decoy Effect Modifier Added") 

    # Mirage Decoy Effect Parenting
        if mr_decoy == "Decoy_parent":
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
                            if bpy.data.objects.get('Decoy') is None:
                                print("Decoy Effect not Found. Pls add Effect first")
                            else:
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                context.view_layer.objects.active = None
                                bpy.data.objects['Decoy'].select_set(True)
                                sel_objects[0].select_set(True)
                                context.view_layer.objects.active = sel_objects[0]

                                arm = bpy.data.objects['Decoy']
                                bpy.ops.object.mode_set(mode='EDIT')
                                bpy.ops.armature.select_all(action='DESELECT')

                                bones_to_select = ['Bone']
                                for bone in arm.data.edit_bones:
                                    if bone.name in bones_to_select:
                                        bone.select = True
                                        
                                arm = sel_objects[0]
                                bones_to_select = ['def_c_spineA']
                                for bone in arm.data.edit_bones:
                                    if bone.name in bones_to_select:
                                        bone.select = True 
                                        
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.parent_set(type='OBJECT')
                                
                                print("Parenting Decoy Effect to Mirage Done")
                        else:
                            print("Selected Object is Not a Bone. Pls Select Bones")

        return {'FINISHED'}


######### Valkyrie Buttons ###########    

class VK_BUTTON_ITEMS(bpy.types.Operator):
    """Operator for spawning Valkyrie Flames."""
    bl_label = "VK_BUTTON_ITEMS"
    bl_idname = "object.vk_button_items"
    bl_options = {'REGISTER', 'UNDO'}
    valk: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        valk = self.valk
        
        flames_items = [
            {'name': 'Flames left'}, 
            {'name': 'Flames right'} 
        ]    
        
    # Valk Flames
        if valk == "Flames":
            if bpy.data.objects.get('Flames left') is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_object, files=flames_items)
                print("Valkyrie Flames Bubble Appended")
            else:
                print("Valkyrie Flames Bubble already exist")

    # Valk Flames Parenting
        if valk == "Flames_parent":
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
                            if bpy.data.objects.get('Flames left') is None:
                                print("Flames Effect not Found. Pls add Effect first")
                            else:
                                # Deselect All and select only bones that were chosen
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                context.view_layer.objects.active = None
                                sel_objects[0].select_set(True)
                                context.view_layer.objects.active = sel_objects[0]
                                
                                # Select left turbine bone in Bone Edit Mode
                                arm = sel_objects[0]
                                bpy.ops.object.mode_set(mode='EDIT')
                                bones_to_select = ['def_l_turbine']
                                for bone in arm.data.edit_bones:
                                    if bone.name in bones_to_select:
                                        bone.select = True 
                                        
                                # Exit out Edit Mode and Deselect All
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                
                                # Select Flames, Select bones that were chosen, set bones active and parent to them
                                bpy.data.objects['Flames left'].select_set(True)
                                sel_objects[0].select_set(True)
                                context.view_layer.objects.active = sel_objects[0]
                                bpy.ops.object.parent_set(type='BONE')
                                
                                # Deselect All and select only bones that were chosen
                                bpy.ops.object.select_all(action='DESELECT')
                                sel_objects[0].select_set(True)
                                context.view_layer.objects.active = sel_objects[0] 
                                
                                # Select right turbine bone in Bone Edit Mode
                                arm = sel_objects[0]
                                bpy.ops.object.mode_set(mode='EDIT')
                                bones_to_select = ['def_r_turbine']
                                for bone in arm.data.edit_bones:
                                    if bone.name in bones_to_select:
                                        bone.select = True 
                                        
                                # Exit out Edit Mode and Deselect All
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                
                                # Select Flames, Select bones that were chosen, set bones active and parent to them
                                bpy.data.objects['Flames right'].select_set(True)
                                sel_objects[0].select_set(True)
                                context.view_layer.objects.active = sel_objects[0]
                                bpy.ops.object.parent_set(type='BONE') 
                                
                                bpy.ops.object.select_all(action='DESELECT')                                                              
                                
                                print("Parenting Flames to Valkyrie Done")
                        else:
                            print("Selected Object is Not a Bone. Pls Select Bones")

        return {'FINISHED'}
