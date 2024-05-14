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
"name": "Tesselate texture plane",
"description": "Triangulate mesh on opaque area of selected texture",
"author": "Henri Hebeisen, Samuel Bernou, Damien Picard",
"version": (3, 0, 0),
"blender": (4, 0, 1),
"location": "3D view > right toolbar > Tesselate tex plane",
"warning": "Full rewrite of previous version",
"wiki_url": "https://github.com/Maxiriton/Tesselate_texture_plane",
"tracker_url": "https://github.com/Maxiriton/Tesselate_texture_plane/issues",
"category": "3D View"
}

import bpy
from pathlib import Path
from bpy.props import (IntProperty,
                        StringProperty,
                        BoolProperty,
                        FloatProperty,
                        EnumProperty,
                        CollectionProperty,
                        PointerProperty,
                        IntVectorProperty,
                        BoolVectorProperty,
                        FloatVectorProperty,
                        RemoveProperty,
                        )

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList,
                       AddonPreferences,
                       )

from bpy.utils import (register_class,
                       unregister_class)

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
        return {"FINISHED"}


class TESS_PT_tesselate_UI(Panel):
    bl_label = "Tex plane tesselation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_context = "objectmode"


    def draw(self, context):
        layout = self.layout
       
        row = layout.row()
        row.label(text='Prout')
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