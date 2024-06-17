# # ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
"name": "Tesselate image texture",
"description": "Generate a mesh based on the alpha of an image",
"author": "Henri Hebeisen",
"version": (0, 0, 1),
"blender": (4, 1, 0),
"location": "3D view > Right Toolbar > Tool > Tesselate Image",
"warning": "Experimental version",
"wiki_url": "https://github.com/Maxiriton/Tesselate_texture_plane",
"tracker_url": "https://github.com/Maxiriton/Tesselate_texture_plane/issues",
"category": "3D View"
}

import bpy
from pathlib import Path
from bpy.types import Operator, Panel

from bpy.utils import (register_class,
                       unregister_class,
                       resource_path)

from bpy_extras.io_utils import ImportHelper
from bpy_extras.image_utils import load_image

class TESS_OT_tesselate_texture(Operator, ImportHelper):
    bl_idname = "mesh.tesselate_texture"
    bl_label = "Add a texture and tesselate plane"
    bl_description = "Tesselate selected texture plane objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    def execute(self, context):
        print(self.filepath)

        image = load_image(self.filepath)


        # add a plane
        mesh = bpy.data.meshes.new("Plane")
        plane = bpy.data.objects.new(image.name, mesh)

        context.collection.objects.link(plane)

        #create the material
        mat = bpy.data.materials.new(image.name)
        mat.use_nodes = True
        tree = mat.node_tree

        img_tex_node = tree.nodes.new("ShaderNodeTexImage")
        img_tex_node.image = image

        attribute_node = tree.nodes.new("ShaderNodeAttribute")
        attribute_node.attribute_name = 'UVs'

        principled_bsdf = tree.nodes['Principled BSDF']

        tree.links.new(attribute_node.outputs[0], img_tex_node.inputs[0])
        tree.links.new(img_tex_node.outputs[0], principled_bsdf.inputs[0])

        # load the geo node 
        try: 
            tesselate_group = bpy.data.node_groups['TESSELATE_IMAGE_TEXTURE']
        except:
            USER = Path(resource_path('USER'))
            ADDON = "Tesselate_texture_plane"
            srcPath = USER / "scripts/addons" / ADDON / "blend" / 'nodes.blend'
            library  = Path(srcPath)
            with bpy.data.libraries.load(str(library)) as (data_from, data_to):
                data_to.node_groups = [ name for name in data_from.node_groups if name == 'TESSELATE_IMAGE_TEXTURE']

            tesselate_group = bpy.data.node_groups['TESSELATE_IMAGE_TEXTURE']

        #apply the geo node to plane
        modifier = plane.modifiers.new("Tesselator", "NODES")
        modifier.node_group = tesselate_group

        modifier["Socket_2"] = 3                #Precision
        modifier["Socket_3"] = image            #image reference
        modifier["Socket_4"] = 20.0             #mesh density
        modifier["Socket_5"] = image.size[0]    #resolution X
        modifier["Socket_6"] = image.size[1]    #resolution Y
        modifier["Socket_9"] = 4                #post simplificaton
        modifier["Socket_10"] = 3               #channel used, index of enum,  3 is for Alpha
        modifier["Socket_11"] = mat             #material

        return {"FINISHED"}


class TESS_PT_tesselate_UI(Panel):
    bl_label = "Tesselate Image"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_context = "objectmode"


    def draw(self, context):
        layout = self.layout
       
        row = layout.row(align=True)
        row.scale_y = 2
        row.operator('mesh.tesselate_texture', icon='IMAGE_REFERENCE')
        row = layout.row(align=True)

### --- REGISTER ---

classes = (
TESS_OT_tesselate_texture,
TESS_PT_tesselate_UI,
)

def register():
    for cls in classes:
        register_class(cls)
    

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()