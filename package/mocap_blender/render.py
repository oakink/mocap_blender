import bpy
import os


def render(filename, res_x=640, res_y=480):
    path = filename
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    bpy.context.scene.render.resolution_x = res_x
    bpy.context.scene.render.resolution_y = res_y
    bpy.ops.render.render()
    bpy.data.images["Render Result"].save_render(path)
