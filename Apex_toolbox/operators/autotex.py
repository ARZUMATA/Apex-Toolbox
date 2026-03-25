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

"""AutoTex operator module for Apex Toolbox addon."""

import bpy
import os
from ..config import mode, ast_fldr, my_path, fbs, blend_file, ap_node, IMAGE_EXTENSIONS, loadImages, texSets


class BUTTON_CUSTOM(bpy.types.Operator):
    """Operator for automatic texture assignment."""
    bl_label = "BUTTON CUSTOM"
    bl_idname = "object.button_custom"
    bl_options = {'REGISTER', 'UNDO'}

    dict_textures = {}

    def set_colorspace(self, img, colorspace):
        """Set image colorspace, fallback to 'Non-Color' if unknown."""
        if colorspace == 'Unknown':
            img.colorspace_settings.name = 'Non-Color'
            print(f"Warning: Unknown colorspace for {img} — using 'Non-Color'")
        else:
            img.colorspace_settings.name = colorspace

    def scan_textures(self, folder_path, recursive=True, max_depth=2):
        """Scan folder for image files and map to texture type. Optionally recursively with depth limit."""
        # Example output:
        # {
        #     'col.png': (
        #         'col',
        #         'sRGB',
        #         'Albedo',
        #         '/textures/char/loba_lgnd_v24_opbundle_body_col.png',
        #         (0.8, 0.2, 0.2)  # - Red
        #     ),
        #     'nml.png': (
        #         'nml',
        #         'Non-Color',
        #         'Normal Map',
        #         '/textures/char/loba_lgnd_v24_opbundle_body_nml.png',
        #         (0.2, 0.6, 0.8)  # - Light Blue
        #     )
        # }
        
        texture_map = {}  # {filename: (type, colorspace, shader_input, full_path, node_color)}

        if not os.path.isdir(folder_path):
            print(f"Folder not found: {folder_path}")
            return texture_map

        def walk_with_depth(root, current_depth=0):
            """Recursive walk with depth limit."""
            if max_depth is not None and current_depth > max_depth:
                return

            for item in os.listdir(root):
                item_path = os.path.join(root, item)
                if os.path.isfile(item_path):
                    ext = os.path.splitext(item)[1].lower()
                    if ext in IMAGE_EXTENSIONS:
                        # Extract base name (without extension)
                        base_name = os.path.splitext(item)[0]

                        # Try to extract texture type from end (e.g., 'catalyst_lgnd_v22_partybeach_body_col' - 'col')
                        parts = base_name.split('_')
                        texture_type = parts[-1]  # last part

                        # Search texSets for match (long or short name)
                        matched_entry = None

                        for entry in texSets:
                            names = entry[0]  # (long_name, short_name)
                            if texture_type in names:
                                matched_entry = entry
                                break
                        
                        if matched_entry:
                            colorspace, shader_input = matched_entry[1]
                            node_color = matched_entry[2]  # - RGB color from texSets
                        else:
                            colorspace = 'Non-Color' # Fallback here, not later
                            shader_input = 'Unknown'
                            node_color = (0.3, 0.3, 0.3) # Default gray
                            print(f"Unknown texture type: {texture_type} in {item}")

                        texture_map[item] = (texture_type, colorspace, shader_input, item_path, node_color)

                elif os.path.isdir(item_path) and recursive:
                    walk_with_depth(item_path, current_depth + 1)

        walk_with_depth(folder_path)

        return texture_map

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        texture_folder = prefs.texture_folder

        # Get texture folder from prefs
        if not texture_folder:
            print("texture_folder is not set. Skipping texture assignment.")
            return {'CANCELLED'}

        texture_map = self.scan_textures(texture_folder)

        # ColorDict
        #   Define Input Mapping Dictionaries. Idx , Input name in the node group.
        #   These names must match exactly the input names in the node group.
        #   Example:
        #   Texture node 0 - links to input "Albedo"
        #   Texture node 1 - links to input "Specular"

        # AlphaDict

        #   Maps texture node index to alpha input names in the node group.
        #   Link Alpha channel (transparency) from texture nodes to specific inputs.
        #   For materials that use alpha for transparency or subsurface scattering.
        #   Example:
        #   Texture node 0 - links its Alpha output to node group input "Alpha"
        #   Texture node 3 - links its Alpha output to node group input "SSS Alpha"

        # Before Gl2imm used:
        # MatNodeTree.node_tree.nodes["Image Texture"] or MatNodeTree.node_tree.nodes["0"]
        # and it's 'imageNode.image.filepath' in order to get path, load all textures and assign them based on their type.
        # Some RSX exports have that part missing and if you recolate textures it all goes wrong.
        # Also it uses same from as recolor one so we can rewrite it and use texture/recolor by simply pointing it to the folder we need.

        # Shader configurations for each option
        SHADER_CONFIGS = {
            'OP1': {
                'node_group_name': 'Apex Shader',
                'color_dict': {
                    "Albedo": "Albedo Map",
                    "Specular": "Specular Map",
                    "Emission": "Emission",
                    "SSS Map": "SSS Map",
                    "Alpha": "Alpha",
                    "Normal Map": "Normal Map",
                    "Glossiness": "Glossiness Map",
                    "Ambient Occlusion": "AO"
                },
                'alpha_dict': {
                    "Alpha": "Alpha",
                    "SSS Alpha": "SSS Alpha",
                }
            },
            'OP2': {
                'node_group_name': 'Apex Shader+_v3.4',
                'color_dict': {
                    "Albedo": "Albedo",
                    "Specular": "Specular",
                    "Emission": "Emission",
                    "SSS Map": "SSS Map",
                    "Alpha": "Alpha",
                    "Normal Map": "Normal Map",
                    "Glossiness": "Glossiness",
                    "Ambient Occlusion": "Ambient Occlusion",
                    "Cavity": "Cavity"
                },
                'alpha_dict': {
                    "Alpha": "Alpha",
                    "SSS Alpha": "SSS Alpha",
                }
            },
            'OP3': {
                'node_group_name': 'S/G-Blender',
                'color_dict': {
                    "Albedo": "Diffuse map",
                    "Specular": "Specular map",
                    "Emission": "Emission input",
                    "Subsurface": "Subsurface",
                    "Alpha input": "Alpha input",
                    "Normal Map": "Normal map",
                    "Glossiness": "Glossiness map",
                    "Ambient Occlusion": "AO map",
                    "Cavity map": "Cavity map",
                },
                'alpha_dict': {
                    "Alpha": "Alpha",
                    "SSS Alpha": "SSS Alpha",
                }
            }
        }

        # Get selected objects once
        selection = [obj.name for obj in bpy.context.selected_objects]

        # Append node group if it doesn't exist
        config = SHADER_CONFIGS.get(prefs.cust_enum2)
        if config:
            node_group_name = config['node_group_name']
            if bpy.data.node_groups.get(node_group_name) is None:
                bpy.ops.wm.append(directory=my_path + blend_file + ap_node, filename=node_group_name)
                for obj_name in selection:
                    bpy.data.objects[obj_name].select_set(True)

        # Loop through every object currently selected in the Blender viewport.
        for o in bpy.context.selected_objects:
            # Only process mesh objects (not lights, cameras, empties, etc.).
            if o.type != 'MESH':
                continue

            # Loop through all material slots assigned to this mesh object.
            # A mesh can have multiple materials (e.g., for different parts of the mesh).
            for mSlot in o.material_slots:
                # Get the actual material from Blender's global data block.
                MatNodeTree = bpy.data.materials[mSlot.name] # e.g., mSlot.name = 'loba_lgnd_v24_opbundle_body'
                
                # Filter texture_map: only entries where full_path contains material_name
                local_texture_map = {
                    filename: (type_, colorspace, shader_input, full_path, node_color)
                    for filename, (type_, colorspace, shader_input, full_path, node_color) in texture_map.items()
                        if mSlot.name in full_path
                }

                for filename, (type_, colorspace, shader_input, full_path, node_color) in local_texture_map.items():
                    print(f"Processing {filename}: {colorspace} - {shader_input}")

                    # Now we have:
                    # filename - e.g. 'col.png'
                    # colorspace - e.g. 'sRGB'
                    # shader_input - e.g. 'Albedo'
                    # full_path - e.g. '/textures/char/loba_lgnd_v24_opbundle_body_col.png'
                    
                    # If image exists in all loaded images in the current .blend file.
                    texImage = bpy.data.images.get(filename)

                    # Not found. Load it then.
                    if not texImage and loadImages:
                        if os.path.isfile(full_path):
                            texImage = bpy.data.images.load(full_path)

                    if texImage:
                        # Set colorspace
                        self.set_colorspace(texImage, colorspace)
                        texImage.alpha_mode = 'CHANNEL_PACKED'
                        
                        # Create texture node
                        texNode = MatNodeTree.node_tree.nodes.new('ShaderNodeTexImage')
                        texNode.image = texImage
                        texNode.name = str(shader_input)
                        texNode.label = str(shader_input)
                        texNode.location = (-50, 50 - 260 * len(MatNodeTree.node_tree.nodes)) # Auto-position

                        # Apply color
                        texNode.use_custom_color = True
                        texNode.color = node_color

                # Create a material node setup using a ShaderNodeGroup (like Apex Shader)
                NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                NodeGroup.node_tree = bpy.data.node_groups.get(node_group_name)
                NodeGroup.location = (300, 0)

                # Creates the final output node where the material's shader result goes to the renderer.
                NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                NodeOutput.location = (500, 0)
                
                # Link Node Group Output to Material Output
                MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])

                # Link Alpha Inputs

                # For each entry in AlphaDict:
                # slot = texture node index (e.g., "0")
                # AlphaDict[slot] = input name in node group (e.g., "Alpha")
                # MatNodeTree.node_tree.nodes[slot] = the texture node at that index
                # .outputs["Alpha"] = the Alpha channel output of that texture node
                # Create a link from texture node’s Alpha - node group’s Alpha input
                # We control transparency or SSS thickness using the alpha channel of a texture.
                for slot, input_name in config['alpha_dict'].items():
                    try:
                        MatNodeTree.node_tree.links.new(
                            NodeGroup.inputs[input_name],
                            MatNodeTree.node_tree.nodes[slot].outputs["Alpha"]
                        )
                    except:
                        pass

                # Link Color Inputs

                # For each entry in ColorDict:
                # Links the Color output of the texture node - the corresponding color input in the node group.
                # Example:
                # Texture node 0 - Color output - node group input "Albedo"
                # Texture node 5 - Color output - node group input "Normal Map"
                for slot, input_name in config['color_dict'].items():
                    try:
                        MatNodeTree.node_tree.links.new(
                            NodeGroup.inputs[input_name],
                            MatNodeTree.node_tree.nodes[slot].outputs["Color"]
                        )
                    except:
                        pass

                # Set Blend Method to HASHED for alpha testing
                # This is used for transparency with alpha testing (like eyelashes).
                # Other common values:
                # 'OPAQUE' - no transparency
                # 'BLEND' - smooth transparency (slower)
                # 'HASHED' - fast alpha testing (good for performance)
                # Required for materials that use alpha maps to cut out parts of the mesh.
                mSlot.material.blend_method = 'HASHED'

                print("Textured", mSlot.name)

        return {'FINISHED'}
