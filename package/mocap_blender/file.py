def createTmpFile(path, content=""):
    import os

    path = os.path.abspath(path)
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(path, "w") as f:
        f.write(content)


def importFile(path, **kwargs):
    import bpy

    if not path:
        raise Exception(f"文件未找到：{path}")
    if path.endswith(".obj"):
        bpy.ops.import_scene.obj(filepath=path, **kwargs)
    elif path.endswith(".ply"):
        bpy.ops.import_mesh.ply(filepath=path, **kwargs)
    else:
        raise Exception(f"文件格式未支持：{path}")


def exportFile(path, **kwargs):
    import bpy
    import os

    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    if path.endswith(".obj"):
        bpy.ops.export_scene.obj(filepath=path, **kwargs)
    else:
        raise Exception(f"文件格式未支持：{path}")


def newFile(postAction=None):
    import bpy

    @bpy.app.handlers.persistent
    def deleteCube(dummy):
        bpy.app.handlers.load_post.remove(deleteCube)
        objs = bpy.data.objects
        ls = []
        for o in objs:
            ls.append(o)
        for o in ls:
            objs.remove(o, do_unlink=True)
        if postAction is not None:
            postAction()

    bpy.app.handlers.load_post.append(deleteCube)
    bpy.ops.wm.read_homefile()


def openFile(filePath, postAction=None):
    import bpy

    @bpy.app.handlers.persistent
    def __postAction(dummy):
        bpy.app.handlers.load_post.remove(__postAction)
        if postAction is not None:
            postAction()

    bpy.app.handlers.load_post.append(__postAction)
    bpy.ops.wm.open_mainfile(filepath=filePath)


def saveFile(filePath=None):
    import bpy
    import os

    if filePath is None:
        bpy.ops.wm.save_mainfile()
    else:
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=filePath)


def appendFile(filePath, contentPath):
    import bpy
    import os

    fullpath = os.path.abspath(os.path.join(filePath, contentPath))
    filename = os.path.basename(fullpath)
    directory = os.path.dirname(fullpath)
    bpy.ops.wm.append(filename=filename, directory=directory)
