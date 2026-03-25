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

"""Configuration and constants module for Apex Toolbox addon."""

import colorsys
import os
import platform
import bpy

bl_info = {
    "name": "Apex Toolbox",
    "author": "Random Blender Dude",
    "version": (3, 6, 2),
    "blender": (2, 90, 0),
    "location": "Operator",
    "description": "Apex models toolbox",
    "warning": "Highly Addictive!",
    "category": "Object"
}

# Version variables
ver = "v.3.7_beta-2"
lts_ver = ver
loadImages = True

# Texture sets configuration
# Alternative names since
# Also texture namings for RSX
texSets = [
    # [
    # (long_name, short_name),           # texture name variants
    # (colorspace, shader_input),        # for image settings + node group input
    # (r, g, b)                          # node color in Blender (0.0–1.0)
    # ]

    [(  'albedoTexture',              'col',  ),       (  'sRGB',       'Albedo'                        ), ],
    [(  'specTexture',                'spc',  ),       (  'sRGB',       'Specular'                      ), ],
    [(  'emissiveTexture',            'ehm',  ),       (  'Non-Color',  'Emission'                      ), ], # ehl
    [(  'scatterThicknessTexture',    'thk',  ),       (  'Non-Color',  'Scatter Thickness (Radius)'    ), ],
    [(  'opacityMultiplyTexture',     None,   ),       (  'Non-Color',  'Alpha (Opacity Multiply)'      ), ],
    [(  'normalTexture',              'nml',  ),       (  'Non-Color',  'Normal Map'                    ), ],
    [(  'glossTexture',               'gls',  ),       (  'Non-Color',  'Glossiness'                    ), ],
    [(  'aoTexture',                   'ao',  ),       (  'Non-Color',  'Ambient Occlusion'             ), ],
    [(  'cavityTexture',              'cav',  ),       (  'Non-Color',  'Cavity'                        ), ],
    [(  'anisoSpecDirTexture',        None,   ),       (  'Non-Color',  'Anis-Spec Dir'                 ), ],
    [(  'iridescenceRampTexture',     'ilm',  ),       (  'Non-Color',  None                            ), ],
]

# Generate rainbow colors for texture sets
# Friendship is magic!
def generate_rainbow_colors(n, saturation=0.8, value=0.4):
    """Generate n distinct rainbow colors (darker for white text)"""
    colors = []
    for i in range(n):
        hue = i / n  # 0.0 to 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        colors.append((r, g, b))
    return colors

# Generate colors for all texSets entries
rainbow_colors = generate_rainbow_colors(len(texSets), saturation=0.8, value=0.4)

# Assign colors to texSets
for i, entry in enumerate(texSets):
    entry.append(rainbow_colors[i])
# Result:
# [(long, short), (colorspace, shader_input), (r, g, b)]

# Define supported image extensions
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tga', '.bmp', '.dds', '.tif', '.tiff', '.exr', '.hdr'}

# Update tracking variables
# Garlicus List vars
lgnd_list = []
ver_list = []
# Legion update vars
legion_cur_ver = '0'
legion_lts_ver = '0'
legion_folder_exist = 0
# Addons update vars
addon_name = []
addon_ver = []
io_anim_lts_ver = '0'
cast_lts_ver = '0'
semodel_lts_ver = '0'
mprt_lts_ver = '0'

# Mode settings (0 - Test Mode, 1 - Live mode)
mode = 1
wh = 0  # 0 - W drive, 1 - H drive
# TODO: REMOVE THIS

# Path variables for test modes
if mode == 0:
    if wh == 1:
        my_path = ("E:\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_toolbox")
        ast_fldr = ("E:\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
        lgn_fdr = ("E:\\G-Drive\\Blender\\0. Setups\\Apex\\")
    if wh == 0:
        my_path = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_toolbox")    
        ast_fldr = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
        lgn_fdr = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\")
else:
    my_path = os.path.dirname(os.path.realpath(__file__))
    ast_fldr = os.path.join(my_path, "Apex_Toolbox_Assets")
    lgn_fdr = my_path

# Blender HDRI paths
bldr_path = os.path.dirname(bpy.app.binary_path)
bldr_ver = bpy.app.version_string.split('.')
bldr_fdr = bldr_ver[0] + '.' + bldr_ver[1] 

if platform.system() == 'Windows':
    fbs = '\\'
    blend_file = ("\\ApexShader.blend")
    ap_node = ("\\NodeTree")
    ap_object = ("\\Object")
    ap_collection = ("\\Collection")
    ap_material = ("\\Material")
    ap_image = ("\\Image")
    ap_world = ("\\World")
    ap_action = ("\\Action")
    bldr_hdri_path = (bldr_path + "\\" + bldr_fdr + "\\datafiles\\studiolights\\world\\")
else:
    fbs = '/'   # forward/back slashes (MacOS)
    blend_file = ("/ApexShader.blend")
    ap_node = ("/NodeTree")
    ap_object = ("/Object")
    ap_collection = ("/Collection")
    ap_material = ("/Material")
    ap_image = ("/Image")
    ap_world = ("/World")
    ap_action = ("/Action")
    bldr_hdri_path = (bldr_path + "/" + bldr_fdr + "/datafiles/studiolights/world/")  

# Use absolute paths for filepaths
bpy.context.preferences.filepaths.use_relative_paths = False

print("**********************************************")
print("OS Platform: " + platform.system())
print("**********************************************")

# All loot items dictionary
all_loot_items = {
    '0': 'White Armor',
    '1': 'Blue Armor',
    '2': 'Purple Armor',
    '3': 'Gold Armor',
    '4': 'Red Armor',
    '5': 'White Helmet',
    '6': 'Blue Helmet',
    '7': 'Purple Helmet',
    '8': 'Gold Helmet',
    '9': 'Red Helmet',
    '10': 'Phoenix Kit',
    '11': 'Shield Battery',
    '12': 'Shield Cell',
    '13': 'Med Kit',
    '14': 'Syringe',
    '15': 'Health Injector',
    '16': 'Grenade',
    '17': 'Arc Star',
    '18': 'Thermite',
    '19': 'Backpack Lv.4',
    '20': 'Backpack Lv.3',
    '21': 'Backpack Lv.2',
    '22': 'Backpack Lv.1',
    '23': 'Light Ammo',
    '24': 'Heavy Ammo',
    '25': 'Energy Ammo',
    '26': 'Shotgun Ammo',
    '27': 'Respawn Beacon',
    '28': 'Knockdown Shield',
    '29': 'Heat Shield',
    '30': 'Death Box',
}

# Item ranges
armor_range = (0, 5)
helmet_range = (5, 10)    
meds_range = (10, 16)
nades_range = (16, 19)
bag_range = (20, 23)
ammo_range = (23, 27)
other_range = (27, 31)

# All lobby other items dictionary
all_lobby_other_items = {
    '0': 'Heirloom Shards',
    '1': 'Epic Shards',
    '2': 'Rare Shards',
    '3': 'Loot Drone',
    '4': 'RESERVED',
    '5': 'RESERVED',
    '6': 'RESERVED',
    '7': 'RESERVED',
    '8': 'RESERVED',
    '9': 'RESERVED',
    '10': 'RESERVED',
    '11': 'RESERVED',
    '12': 'RESERVED',
    '13': 'RESERVED',
    '14': 'RESERVED',
    '15': 'RESERVED',
    '16': 'RESERVED',
    '17': 'RESERVED',
    '18': 'RESERVED',
    '19': 'RESERVED',
    '20': 'Respawn Beacon Hologram',
    '21': 'Loot Ball'
}

# Lobby item ranges
lobby_lobby_range = (0, 4)
lobby_other_range = (20, 22)

# All heirloom items dictionary
all_heirloom_items = {
    '0': 'Gibraltar Set',
    '1': 'Bangalore Set',
    '2': 'Lifeline Set (Animated)',
    '3': 'Bloodhound Set',
    '4': 'Caustic Set',
    '5': 'Crypto Set',
    '6': 'Wraith Set',
    '7': 'Mirage Set',
    '8': 'Octane Set',
    '9': 'Pathfinder Set (Animated)',
    '10': 'Rampart Set',
    '11': 'Revenant Set',
    '12': 'Valkyrie Set',
    '13': 'Wattson Set (Animated)'
}

# Heirloom range
heirloom_range = (0, 14)

# All Seer items dictionary
all_seer_items = {
    '0': 'Seer Ultimate',
}

# All skydive items dictionary
all_skydive_items = {
    '0': 'Skydive Ranked S9 Diamond', 
    '1': 'Skydive Ranked S9 Master', 
    '2': 'Skydive Ranked S9 Predator',
}

# Required addons list
addon_list = [
    'io_anim_seanim',
    'io_scene_cast',
    'io_model_semodel',
    'ApexMapImporter'
]