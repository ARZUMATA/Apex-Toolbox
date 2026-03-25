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
