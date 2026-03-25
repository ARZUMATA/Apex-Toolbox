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

"""URL handler operator module for Apex Toolbox addon."""

import bpy
import webbrowser
import requests
from ..config import mode, ast_fldr, lgn_fdr, my_path, fbs, legion_lts_ver, io_anim_lts_ver, cast_lts_ver, semodel_lts_ver, mprt_lts_ver, addon_name, addon_ver

# URL handler operator
class LGNDTRANSLATE_URL(bpy.types.Operator):
    """Operator for handling external links and displaying instructions."""
    bl_label = "BUTTON CUSTOM"
    bl_idname = "object.lgndtranslate_url"
    bl_options = {'REGISTER', 'UNDO'}
    link: bpy.props.StringProperty(name="Added")

    def execute(self, context):
        link = self.link

        if link == "check_update":
            global legion_lts_ver
            global io_anim_lts_ver
            global cast_lts_ver
            global semodel_lts_ver
            global mprt_lts_ver
            
            # Check Legion+ version
            legion_url = 'https://github.com/r-ex/LegionPlus/releases.atom'
            try:
                full_text = requests.get(legion_url, allow_redirects=True).text
            except:
                print("Apex Toolbox Addon: Something Went Wrong While checking Legion+ Online version")
            else:
                split_1 = full_text.split('437133675/')[2]
                legion_lts_ver = split_1.split('</id>')[0]
                if legion_lts_ver == 'nightly':
                    legion_lts_ver = '0'

            # Check addon versions
            if addon_name is not None:
                for x in range(len(addon_name)):
                    for i in range(len(addon_name)):
                        if addon_name[x] == addon_name[i]:
                            if i == 0:
                                url = 'https://github.com/SE2Dev/io_anim_seanim/releases.atom'
                                try:
                                    full_text = requests.get(url, allow_redirects=True).text
                                except:
                                    print("Apex Toolbox Addon: Something Went Wrong While checking io_anim_seanim Online version")
                                else:
                                    split_1 = full_text.split('72251837/')[1]
                                    io_anim_lts_ver = split_1.split('</id>')[0] 
                            if i == 1:
                                url = 'https://github.com/dtzxporter/cast/releases.atom'
                                try:
                                    full_text = requests.get(url, allow_redirects=True).text
                                except:
                                    print("Apex Toolbox Addon: Something Went Wrong While checking io_scene_cast Online version")
                                else:
                                    split_1 = full_text.split('<title>[Plugins] Blender ')[1]
                                    cast_lts_ver = split_1.split(', Maya')[0]
                            if i == 2:
                                url = 'https://github.com/dtzxporter/io_model_semodel/tree/blender-28' 
                                semodel_lts_ver = "0.0.3"
                            if i == 3: 
                                url = 'https://github.com/llennoco22/Apex-mprt-importer-for-Blender/releases.atom'
                                try:
                                    full_text = requests.get(url, allow_redirects=True).text
                                except:
                                    print("Apex Toolbox Addon: Something Went Wrong While checking ApexMapImporter Online version")
                                else:
                                    split_1 = full_text.split('433190309/')[1]
                                    mprt_lts_ver = split_1.split('</id>')[0]

        if link == "buy coffee":
            webbrowser.open_new("https://buy.stripe.com/7sI2cd3495IGbYc8wz")

        if link == "garlicus_list":
            webbrowser.open_new("https://docs.google.com/spreadsheets/d/123c1OigzmI4UaSZIEcKbIJFjgXVfAmXFrXQmM1dZMOU/edit#gid=0")

        if link == "biast_archive":
            webbrowser.open_new("https://biast12.site/")

        if link == "io_anim_seanim":
            webbrowser.open_new("https://github.com/SE2Dev/io_anim_seanim/releases")
            
        if link == "cast":
            webbrowser.open_new("https://github.com/dtzxporter/cast/releases")
            
        if link == "io_model_semodel":
            webbrowser.open_new("https://github.com/SE2Dev/io_anim_seanim/releases")
            
        if link == "mprt":
            webbrowser.open_new("https://github.com/llennoco22/Apex-mprt-importer-for-Blender/releases")

        if link == "legion_update":
            webbrowser.open_new("https://github.com/r-ex/LegionPlus/releases")
                     
        if link == "update":
            webbrowser.open_new("https://github.com/Gl2imm/Apex-Toolbox/releases")
            
        if link == "instructions":
            instructions = my_path + fbs + "Credits and Instructions.txt"
            with open(instructions) as f:
                text = f.read()
            t = bpy.data.texts.new("Instructions")
            t.write("To switch back to normal view switch from 'TEXT EDITOR' to '3D Viewport'. Or just press 'Shift+F5' \n \n \n")
            t.write(text)
            bpy.context.area.ui_type = 'TEXT_EDITOR'
            bpy.context.space_data.text = bpy.data.texts['Instructions']
            bpy.ops.text.jump(line=1)
            
        if link == "version":
            instructions = my_path + fbs + "Version_log.txt"
            with open(instructions) as f:
                text = f.read()
            t = bpy.data.texts.new("Version_log")
            t.write("To switch back to normal view switch from 'TEXT EDITOR' to '3D Viewport'. Or just press 'Shift+F5' \n \n \n")
            t.write(text)
            bpy.context.area.ui_type = 'TEXT_EDITOR'
            bpy.context.space_data.text = bpy.data.texts['Version_log']
            bpy.ops.text.jump(line=1)
            
        if link == "toon_shader":
            texts_exist = bpy.data.texts.get('Toon Shader Instructions')
            if texts_exist is not None:
                bpy.context.area.ui_type = 'TEXT_EDITOR'
                bpy.context.space_data.text = bpy.data.texts['Toon Shader Instructions']
            else:
                t = bpy.data.texts.new("Toon Shader Instructions")
                t.write("To switch back to normal view switch from 'TEXT EDITOR' to '3D Viewport'. Or just press 'Shift+F5' \n \n \n")
                t.write("Apex Toon Shader (Beta)\n")
                t.write("This was inspired by Lightning Boy Studio Toon Shader\n")
                t.write("Some nodes and Key light setup were taken from this tutorial https://youtu.be/VmyMbgMh-eQ\n\n")
                t.write("Warning:\n")
                t.write("1. Please do not expect the model look cool out of the box, for the model to look nice\n")
                t.write("   you will have to do some manual adjustments, as well as setting up 'Key Light' and 'Fill Light'\n")
                t.write("   directions. They specify directions for the shadow outlines\n")
                t.write("2. This Setup Works only in Eevee\n")
                t.write("3. This setup does not need Lights or HDRI (Will not work if you add any)\n")
                t.write("4. Currently this works with a model only, you may have custom background, etc.\n")
                t.write("   if you have other models to include together - you will need to manually add 'Apex ToonShader'\n")
                t.write("   and setup model with this shader (no Principal or other shader, as they need lights)\n")
                t.write("5. The Outline for the Head is showing up in the Eyes for some models - Go to Modifiers Tab\n")
                t.write("   and set Solidify modifier Thickness to -0.015m or less (closer to 0)\n\n")
                t.write("Guide:\n")
                t.write("1. Import a New Model (Semodel)\n")
                t.write("2. Select the model parts you want to Toon and click 'Toon it'\n")
                t.write("3. Use 'Key Light' and 'Fill Light' to specify directions for the shadow outlines\n")
                t.write("4. Sometimes Shadows are glitching, you may try set it to 'None' (Material Settings, Shadow Opacity)\n")
                t.write("5. Set 'Key Light Color' and 'Fill Light Color' to your liking\n")
                t.write("6. ToolBox will show only Key settings, more settings is in the Shader Tab\n")
                t.write("7. All the settings needed for this shader to work will be autoset and will be shown in ToolBox\n\n")
                t.write("For now it work only this way\n")
                t.write("Will update if there any solutions found for other objects in the Scene\n\n")
                t.write("Good Luck with your Renders!!")
                bpy.context.area.ui_type = 'TEXT_EDITOR'
                bpy.context.space_data.text = bpy.data.texts['Toon Shader Instructions']
                bpy.ops.text.jump(line=1)

        if link == "asset_file":
            webbrowser.open_new("https://drive.google.com/file/d/14z98OfTWH9Uku2MFssg1bs2qjjVVkOWz/view?usp=sharing")
             
        if link == "discord":
            webbrowser.open_new("https://discord.gg/gFa4mY7")

        return {'FINISHED'}
