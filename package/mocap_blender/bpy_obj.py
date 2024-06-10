import bpy


class TYPE:
    MESH = "MESH"
    CURVE = "CURVE"
    SURFACE = "SURFACE"
    META = "META"
    FONT = "FONT"
    ARMATURE = "ARMATURE"
    LATTICE = "LATTICE"
    EMPTY = "EMPTY"
    GPENCIL = "GPENCIL"
    CAMERA = "CAMERA"
    LIGHT = "LIGHT"
    SPEAKER = "SPEAKER"
    LIGHT_PROBE = "LIGHT_PROBE"


def findObjs(name=None, type=None, collection=None):
    if collection is None:
        objs = bpy.data.objects
    else:
        objs = collection.objects
    ls = []
    for o in objs:
        match = True
        if name and not o.name == name:
            match = False
        if type and not o.type == type:
            match = False
        if match:
            ls.append(o)
    return ls


def getObj(name=None, type=None, collection=None):
    ls = findObjs(name, type, collection)
    if len(ls) > 0:
        return ls[0]
    return None


def clearObjs(name=None, type=None):
    objs = bpy.data.objects
    ls = findObjs(name, type)
    for o in ls:
        objs.remove(o, do_unlink=True)


def createEmpty(name=None, collection=None):
    bpy.ops.object.empty_add(location=(1, 1, 1))
    obj = bpy.context.object
    if name:
        obj.name = name
    if collection:
        from .collection import moveCollection

        moveCollection(obj, collection)
    return obj


def removeObj(obj, do_unlink=True):
    data_type = obj.type
    if data_type == TYPE.MESH:
        bpy.data.meshes.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.CURVE:
        bpy.data.curves.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.SURFACE:
        bpy.data.surfaces.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.META:
        bpy.data.metaballs.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.FONT:
        bpy.data.fonts.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.ARMATURE:
        bpy.data.armatures.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.LATTICE:
        bpy.data.lattices.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.GPENCIL:
        bpy.data.grease_pencils.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.LIGHT:
        bpy.data.lights.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.CAMERA:
        bpy.data.cameras.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.SPEAKER:
        bpy.data.speakers.remove(obj.data, do_unlink=do_unlink)
    elif data_type == TYPE.LIGHT_PROBE:
        bpy.data.lightprobes.remove(obj.data, do_unlink=do_unlink)
    else:
        bpy.data.objects.remove(obj, do_unlink=do_unlink)
