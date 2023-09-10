import json

import bpy
from bpy.types import Object, Operator, Panel
from bpy.utils import register_class, unregister_class
from mathutils import Vector
import math

bl_info = {
    'name': 'Particle colorizer',
    'author': 'Evgeny Podjachev',
    "version": (1, 0, 0),
    'blender': (3, 5, 0),
    'location': 'File > Export / Shader Editor > Add > EDM',
    'description': 'Encodes particle color in Rand value',
    'warning': '',
    'doc_url': "",
    'category': 'Export',
}

class ParticleColorizer(Panel):
    bl_label = "Object Properties"
    bl_idname = "OBJECT_PT_particle_colorizer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PColorizer"

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        if not context.object.particle_systems:
            return False
        
        return True

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(PCOL_PT_Set_colors.bl_idname)

class PCOL_PT_Set_colors(Operator):
    bl_idname = "pcol.set_colors" 
    bl_label = "Set colors"
    bl_description = "Set colors"

    def execute(self, context):
        object: Object = context.object
        
        
        #bpy.context.scene.frame_set(900)

        degp = bpy.context.evaluated_depsgraph_get()
        pss = object.evaluated_get(degp).particle_systems
        particles = pss.active.particles

        minV = [1000000, 1000000, 1000000]
        maxV = [-1000000, -1000000, -1000000]
        res = {}
        parts = []
        for i in range(len(particles)):
            pt = particles[i]
            loc = pt.location.to_tuple()
            parts.append(loc)
            for j in range(3):
                minV[j] = min(minV[j], loc[j])
            for j in range(3):
                maxV[j] = max(maxV[j], loc[j])

        res['particles'] = parts
        res['min'] = minV
        res['max'] = maxV
        res['size'] = int(math.sqrt(len(particles)))
        
        with open('C:/Users/evgen/sync/blender/balls/balls3.json', 'wt') as f:
            json.dump(res, f)
        

        return {'FINISHED'}

classes = (
    ParticleColorizer,
    PCOL_PT_Set_colors,
)

def register():
    for cls in classes:
        register_class(cls)

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()