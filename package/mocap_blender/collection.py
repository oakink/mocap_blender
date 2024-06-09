import bpy


def getOrNewCollection(name, parent=None):
    if parent is None:
        parent = sceneCollection()
    if isinstance(parent, str):
        parent = getOrNewCollection(parent)
    if name not in bpy.data.collections:
        coll = bpy.data.collections.new(name)
        parent.children.link(coll)
        return coll
    if name not in parent.children:
        parent.children.link(bpy.data.collections[name])
    return bpy.data.collections[name]


def removeCollection(name, withobject=False):
    if name not in bpy.data.collections:
        return
    collection = bpy.data.collections.get(name)
    if withobject:
        for obj in collection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        for col in collection.children:
            removeCollection(col.name, withobject=True)
    bpy.data.collections.remove(collection)


def moveCollection(obj, collection):
    if isinstance(collection, str):
        collection = getOrNewCollection(collection)
    flag = True
    for old in obj.users_collection:
        if old != collection:
            old.objects.unlink(obj)
        else:
            flag = False
    if flag:
        collection.objects.link(obj)


def sceneCollection():
    return bpy.context.scene.collection
