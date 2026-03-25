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

"""Animation and bone operator module for Apex Toolbox addon."""

import bpy

# IK Bones
class BUTTON_IKBONE(bpy.types.Operator):
    """Operator for IK bone setup functionality."""
    bl_label = "BUTTON_IKBONE"
    bl_idname = "object.button_ikbone"
    bl_options = {'REGISTER', 'UNDO'}
    ik_b: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        ik_b = self.ik_b
        
        bones_to_select = [
            'def_l_wrist',
            'def_r_wrist',
            'def_l_elbow',
            'def_r_elbow',
            'def_l_ankle',
            'def_r_ankle',
            'def_l_knee',
            'def_r_knee'
        ]

        constr_bones = [
            'def_l_wrist',
            'def_r_wrist',
            'def_l_ankle',
            'def_r_ankle'
        ]

        adj_bones_f = [
            'def_l_knee',
            'def_r_knee'
            ]
        
        ik_bone_names = [
            'HandIK.L',
            'HandIK.R',
            'LegIK.L',
            'LegIK.R'
            ]
        
        ik_pole_names = [
            'ElbowIK.L',
            'ElbowIK.R',
            'KneeIK.L',
            'KneeIK.R'
            ]
        
        ik_pole_move_f = [
            'KneeIK.L',
            'KneeIK.R'
            ]
        
        ik_pole_move_b = [
            'ElbowIK.L',
            'ElbowIK.R'
            ]

        if bpy.context.selected_objects and bpy.context.selected_objects[0].type == 'ARMATURE': 
            arm = bpy.context.selected_objects[0]
            
            # GOTO Edit Mode
            if context.active_object.mode == 'EDIT':
                pass
            else:
                bpy.ops.object.editmode_toggle()
            
            # Create Poles and Targets
            bpy.ops.armature.select_all(action='DESELECT')
            for bone in arm.data.edit_bones:
                if bone.name in bones_to_select:
                    bone.select_head = True
                    bone.select_tail = True   
            
            bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked": False},
                                          TRANSFORM_OT_translate={
                                              "value": (0, 0.06, 0),
                                              "orient_axis_ortho": 'X',
                                              "orient_type": 'GLOBAL',
                                              "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                              "orient_matrix_type": 'GLOBAL',
                                              "constraint_axis": (False, True, False)
                                          })
            bpy.ops.armature.select_more()
            bpy.ops.armature.parent_clear(type='CLEAR')
            
            # Rename all Selected Bones
            for bone in bpy.context.selected_bones:
                if bone.name == 'def_l_elbow.001':
                    bone.name = 'ElbowIK.L'
                if bone.name == 'def_l_wrist.001':
                    bone.name = 'HandIK.L'
                if bone.name == 'def_r_elbow.001':
                    bone.name = 'ElbowIK.R'
                if bone.name == 'def_r_wrist.001':
                    bone.name = 'HandIK.R'
                if bone.name == 'def_l_ankle.001':
                    bone.name = 'LegIK.L'
                if bone.name == 'def_r_ankle.001':
                    bone.name = 'LegIK.R'
                if bone.name == 'def_l_knee.001':
                    bone.name = 'KneeIK.L'
                if bone.name == 'def_r_knee.001':
                    bone.name = 'KneeIK.R'
            
            # MOVE Pole Bones
            bpy.ops.armature.select_all(action='DESELECT')
            for bone in arm.data.edit_bones:
                if bone.name in ik_pole_move_b:
                    bone.select_head = True
                    bone.select_tail = True
                
                bpy.ops.transform.translate(
                    value=(0, 0.25, 0),
                    orient_axis_ortho='X',
                    orient_type='GLOBAL',
                    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                    orient_matrix_type='GLOBAL',
                    constraint_axis=(False, True, False)
                )
                
                bpy.ops.armature.select_all(action='DESELECT')
                
                if bone.name in ik_pole_move_f:
                    bone.select_head = True
                    bone.select_tail = True
                
                bpy.ops.transform.translate(
                    value=(-0, -0.75, -0),
                    orient_axis_ortho='X',
                    orient_type='GLOBAL',
                    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                    orient_matrix_type='GLOBAL',
                    constraint_axis=(False, True, False)
                )
                
                bpy.ops.armature.select_all(action='DESELECT')
                
                # Small bone adjustments
                if bone.name in adj_bones_f:
                    bone.select_head = True
                    bone.select_tail = True
                
                bpy.ops.transform.translate(
                    value=(-0, -0.002, -0), 
                    orient_axis_ortho='X', 
                    orient_type='GLOBAL', 
                    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                    orient_matrix_type='GLOBAL', 
                    constraint_axis=(False, True, False)
                )
                
                bpy.ops.armature.select_all(action='DESELECT')
            
            # GOTO Pose Mode
            bpy.ops.object.editmode_toggle()
            if context.active_object.mode == 'POSE':
                pass
            else:
                bpy.ops.object.posemode_toggle()

            # Add Constraints
            for x in range(len(constr_bones)):
                ik_bone = arm.pose.bones[constr_bones[x]].bone
                bpy.context.selected_objects[0].pose.bones[ik_bone.name].bone.select = True
                bpy.context.selected_objects[0].data.bones.active = ik_bone
                bpy.ops.pose.constraint_add(type='IK')
                
                constr = bpy.context.object.pose.bones[constr_bones[x]].constraints["IK"]
                constr.target = arm
                constr.subtarget = ik_bone_names[x]
                constr.pole_target = arm
                constr.pole_subtarget = ik_pole_names[x]
                
                if x == 1:
                    constr.pole_angle = 1.5708
                if x == 3:
                    constr.pole_angle = 3.14159
                
                constr.iterations = 500
                
                if x <= 1:
                    constr.chain_count = 4
                else:
                    constr.chain_count = 3
                    
            # Limit Distance IK Poles
            for x in range(len(ik_pole_names)): 
                lim_bone = arm.pose.bones[ik_pole_names[x]].bone 
                bpy.context.selected_objects[0].pose.bones[lim_bone.name].bone.select = True
                bpy.context.selected_objects[0].data.bones.active = lim_bone
                bpy.ops.pose.constraint_add(type='LIMIT_DISTANCE')
                
                limit = bpy.context.object.pose.bones[ik_pole_names[x]].constraints["Limit Distance"]
                limit.target = arm
                limit.subtarget = constr_bones[x]
                
                if x >= 2:
                    limit.distance = 1
                else:
                    limit.distance = 0.5

        return {'FINISHED'}
