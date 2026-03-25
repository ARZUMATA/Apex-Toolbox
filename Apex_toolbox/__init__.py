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

"""Apex Toolbox - Blender addon for Apex Legends models."""

# Import all modules
from . import config

from . import preferences
from . import operators
from . import character_operators
from . import item_operators
from . import panels

# Re-export classes for registration
from .config import (
    ver, lts_ver, mode, my_path, fbs, blend_file, ap_node, ap_object, 
    ap_collection, ap_material, ap_image, ap_world, ap_action, bldr_hdri_path,
    IMAGE_EXTENSIONS, texSets, all_loot_items, all_lobby_other_items,
    all_heirloom_items, all_seer_items, all_skydive_items, addon_list,
    armor_range, helmet_range, meds_range, nades_range, bag_range, 
    ammo_range, other_range, lobby_lobby_range, lobby_other_range, heirloom_range
)

from .preferences import (
    apexToolsPreferences, PROPERTIES_CUSTOM
)

from .operators import (
    LGNDTRANSLATE_URL, BUTTON_CUSTOM, BUTTON_TOON, BUTTON_SHADOW,
    BUTTON_CUSTOM2, BUTTON_SHADERS, BUTTON_HDRIFULL, BUTTON_IKBONE
)

from .character_operators import (
    WR_BUTTON_PORTAL, GB_BUTTON_ITEMS, MR_BUTTON_DECOY, VK_BUTTON_ITEMS
)

from .item_operators import (
    BDG_BUTTON_SPAWN, SEER_BUTTON_SPAWN, SKY_BUTTON_SPAWN, WPN_BUTTON_SPAWN,
    LT_BUTTON_SPAWN, LB_BUTTON_SPAWN, HL_BUTTON_SPAWN, EF_BUTTON_SPAWN
)

from .panels import (
    AUTOTEX_MENU, EFFECTS_PT_panel, OTHERS_PT_panel, UPDATE_PT_panel
)


# Register classes
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
    VK_BUTTON_ITEMS,
    BDG_BUTTON_SPAWN,
    WPN_BUTTON_SPAWN,
    LT_BUTTON_SPAWN,
    LB_BUTTON_SPAWN,
    HL_BUTTON_SPAWN,
    EF_BUTTON_SPAWN,
    AUTOTEX_MENU,
    EFFECTS_PT_panel,
    OTHERS_PT_panel,
    UPDATE_PT_panel,
)


def register():
    """Register all addon classes."""
    for c in classes:
        bpy.utils.register_class(c)
    
    bpy.types.Scene.my_prefs = bpy.props.PointerProperty(type=PROPERTIES_CUSTOM)
    
    # Panel subpanel properties
    bpy.types.Scene.subpanel_readme = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_status_0 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_shadow = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_toon = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_ikbone = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_status_1 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_status_2 = bpy.props.BoolProperty(default=False)
    
    # Effects panel properties
    bpy.types.Scene.subpanel_effects_wraith = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_wraith_prop1 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_gibby = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_gibby_prop1 = bpy.props.BoolProperty(default=False)    
    bpy.types.Scene.subpanel_effects_mirage = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_mirage_prop1 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_valkyrie = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_valkyrie_prop1 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_seer = bpy.props.BoolProperty(default=False)    
    bpy.types.Scene.subpanel_effects_weapons = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_weapons_laser = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_weapons_prop1 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_heirloom = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_badges = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_loot = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_loot_prop1 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_loot_prop2 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_loot_prop3 = bpy.props.BoolProperty(default=False) 
    bpy.types.Scene.subpanel_effects_loot_prop4 = bpy.props.BoolProperty(default=False) 
    bpy.types.Scene.subpanel_effects_loot_prop5 = bpy.props.BoolProperty(default=False) 
    bpy.types.Scene.subpanel_effects_loot_prop6 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_loot_prop7 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.subpanel_effects_lobby = bpy.props.BoolProperty(default=False) 
    bpy.types.Scene.subpanel_effects_other = bpy.props.BoolProperty(default=False)   
    bpy.types.Scene.subpanel_effects_sky = bpy.props.BoolProperty(default=False)


def unregister():
    """Unregister all addon classes."""
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    
    del bpy.types.Scene.my_prefs
    
    # Delete panel properties
    del bpy.types.Scene.subpanel_readme
    del bpy.types.Scene.subpanel_status_0
    del bpy.types.Scene.subpanel_shadow
    del bpy.types.Scene.subpanel_toon
    del bpy.types.Scene.subpanel_ikbone
    del bpy.types.Scene.subpanel_status_1
    del bpy.types.Scene.subpanel_status_2
    del bpy.types.Scene.subpanel_effects_wraith
    del bpy.types.Scene.subpanel_effects_wraith_prop1
    del bpy.types.Scene.subpanel_effects_gibby
    del bpy.types.Scene.subpanel_effects_gibby_prop1    
    del bpy.types.Scene.subpanel_effects_mirage
    del bpy.types.Scene.subpanel_effects_mirage_prop1
    del bpy.types.Scene.subpanel_effects_valkyrie
    del bpy.types.Scene.subpanel_effects_valkyrie_prop1
    del bpy.types.Scene.subpanel_effects_seer    
    del bpy.types.Scene.subpanel_effects_weapons
    del bpy.types.Scene.subpanel_effects_weapons_laser
    del bpy.types.Scene.subpanel_effects_weapons_prop1
    del bpy.types.Scene.subpanel_effects_heirloom
    del bpy.types.Scene.subpanel_effects_badges
    del bpy.types.Scene.subpanel_effects_loot
    del bpy.types.Scene.subpanel_effects_loot_prop1
    del bpy.types.Scene.subpanel_effects_loot_prop2
    del bpy.types.Scene.subpanel_effects_loot_prop3 
    del bpy.types.Scene.subpanel_effects_loot_prop4 
    del bpy.types.Scene.subpanel_effects_loot_prop5
    del bpy.types.Scene.subpanel_effects_loot_prop6
    del bpy.types.Scene.subpanel_effects_loot_prop7
    del bpy.types.Scene.subpanel_effects_lobby 
    del bpy.types.Scene.subpanel_effects_other
    del bpy.types.Scene.subpanel_effects_sky 


if __name__ == "__main__":
    register()
