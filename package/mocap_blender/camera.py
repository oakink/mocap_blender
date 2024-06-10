import bpy
from . import bpy_obj
import math


def getCameras(collection=None):
    bpy_obj.findObjs(type="CAMERA", collection=collection)


def findCameras(name, collection=None):
    return bpy_obj.findObjs(name, type="CAMERA", collection=collection)


def getCamera(name, collection=None):
    ls = bpy_obj.findObjs(name, type="CAMERA", collection=collection)
    if len(ls) > 0:
        return ls[0]
    return None


def setActive(cam):
    bpy.context.scene.camera = cam


def createCamera(name, matrix=None, cam_intr=None, cam_size=None, collection=None):
    cam = bpy.data.cameras.new(name)
    obj = bpy.data.objects.new(name, cam)
    if collection is None:
        bpy.context.scene.collection.objects.link(obj)
    else:
        collection.objects.link(obj)
    
    if matrix is not None:
        obj.matrix_world = matrix
    
    if cam_intr is not None and cam_size is not None:
        cam_x = cam_size[0]
        cam_y = cam_size[1]
        assert cam_x >= cam_y
        aspect_ratio = cam_x / cam_y
        fov = 2 * math.atan2(cam_x, 2 * cam_intr[0,0])
        offset_x = -((cam_intr[0, 2]/cam_x)-0.5)
        offset_y = (cam_intr[1, 2]/cam_y)-0.5
        cam.lens_unit = 'FOV'
        cam.angle = fov
        cam.shift_x = offset_x
        cam.shift_y = offset_y / aspect_ratio # blender express units in x if aspect > 1.0
        cam.clip_start = 0.001
        cam.clip_end = 10.000
        
    return obj

def removeCamera(cam):
    bpy.data.cameras.remove(cam.data)