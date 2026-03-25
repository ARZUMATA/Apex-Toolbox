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

"""Preferences and property groups module for Apex Toolbox addon."""

import bpy
from bpy.props import BoolProperty, StringProperty, EnumProperty, FloatVectorProperty
import requests
import os
import sys

from .config import mode, ast_fldr, lgn_fdr, my_path, fbs


class apexToolsPreferences(bpy.types.AddonPreferences):
    """Addon preferences class for Apex Toolbox."""
    bl_idname = __name__

    asset_folder: StringProperty(
        name="Folder",
        description="Select Assets folder",
        default="",
        maxlen=1024,
        subtype="DIR_PATH"
    )

    legion_folder: StringProperty(
        name="Folder",
        description="Select Legion folder",
        default="",
        maxlen=1024,
        subtype="DIR_PATH"
    )

    if mode == 0:
        asset_folder = ast_fldr
        legion_folder = lgn_fdr


class PROPERTIES_CUSTOM(bpy.types.PropertyGroup):
    """Custom property group for Apex Toolbox."""

    name: StringProperty(name="ver", default="", maxlen=40) #not in use (??)

    # AutoTex shader selection
    cust_enum: EnumProperty(
        name="Shader",
        description="Shader for recolor",
        default='OP1',
        items=[
            ('OP1', "Apex Shader", ""),
            ('OP2', "Apex Shader+_v3.4", ""),
            ('OP3', "S/G-Blender", "")
        ]
    )

    autotex_folder: StringProperty(
        name="Folder",
        description="Select textures folder",
        default="",
        maxlen=1024,
        subtype="DIR_PATH"
    )

    aut_subf: BoolProperty(
        name="Have Sub-folders?",
        description="Autotex property",
        default=False
    )

    # Recolor shader selection
    cust_enum2: EnumProperty(
        name="Shader",
        description="Shader for Autotex",
        default='OP1',
        items=[
            ('OP1', "Apex Shader", ""),
            ('OP2', "Apex Shader+_v3.4", ""),
            ('OP3', "S/G-Blender", "")
        ]
    )

    texture_folder: StringProperty(
        name="Folder",
        description="Select textures folder",
        default="",
        maxlen=1024,
        subtype="DIR_PATH"
    )

    recolor_folder: StringProperty(
        name="Folder",
        description="Select Recolor textures folder",
        default="",
        maxlen=1024,
        subtype="DIR_PATH"
    )

    rec_alpha: BoolProperty(
        name="Plug Alpha?",
        description="Recolor Alpha property",
        default=True
    )

    # Shader append selection
    cust_enum_shader: EnumProperty(
        name="Shader",
        description="Append Shader",
        default='OP1',
        items=[
            ('OP1', "Apex Shader", ""),
            ('OP2', "Apex Shader+_v3.4", ""),
            ('OP3', "S/G-Blender", ""),
            ('OP4', "Apex Cycles (Blue)", ""),
            ('OP5', "Apex Mobile (Biast12)", "")
        ]
    )

    # HDRI append selection
    cust_enum_hdri: EnumProperty(
        name="Theme",
        description="Append HDRI",
        default='OP1',
        items=[
            ('OP1', "Blender Default", ""),
            ('OP2', "Apex Lobby", ""),
            ('OP3', "Party Crasher", ""),
            ('OP4', "Encore", ""),
            ('OP5', "Habitat", ""),
            ('OP6', "Kings Canyon (Old)", ""),
            ('OP7', "Kings Canyon (New)", ""),
            ('OP8', "Kings Canyon (Night)", ""),
            ('OP9', "Olympus", ""),
            ('OP10', "Phase Runner", ""),
            ('OP11', "Storm Point", ""),
            ('OP12', "Worlds Edge", ""),
            ('OP13', "Sky", ""),
            ('OP14', "-- HDRI from Poly Haven --", ""),
            ('OP15', "Indoor", ""),
            ('OP16', "Outdoor", ""),
            ('OP17', "Outdoor under shade", ""),
            ('OP18', "Morning Forest", ""),
            ('OP19', "-- Blender Built-in HDRI --", ""),
            ('OP20', "City", ""),
            ('OP21', "Courtyard", ""),
            ('OP22', "Forest", ""),
            ('OP23', "Interior", ""),
            ('OP24', "Night", ""),
            ('OP25', "Studio", ""),
            ('OP26', "Sunrise", ""),
            ('OP27', "Sunset", "")
        ]
    )

    # HDRI append selection (without assets)
    cust_enum_hdri_noast: EnumProperty(
        name="HDRI",
        description="Append default HDRI",
        default='OP1',
        items=[
            ('OP1', "Blender Default", ""),
            ('OP2', "City", ""),
            ('OP3', "Courtyard", ""),
            ('OP4', "Forest", ""),
            ('OP5', "Interior", ""),
            ('OP6', "Night", ""),
            ('OP7', "Studio", ""),
            ('OP8', "Sunrise", ""),
            ('OP9', "Sunset", "")
        ]
    )

    # Mirage bone parent property
    my_bool: BoolProperty(
        name="Parent to Bone? (Not done yet)",
        description="Mirage Bone parent property",
        default=False
    )
