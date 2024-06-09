import bpy
from . import objects


def getCameras(collection=None):
    objects.findObjs(type="CAMERA", collection=collection)


def findCameras(name, collection=None):
    return objects.findObjs(name, type="CAMERA", collection=collection)


def getCamera(name, collection=None):
    return objects.findObjs(name, type="CAMERA", collection=collection)[0]


def setActive(cam):
    bpy.context.scene.camera = cam
