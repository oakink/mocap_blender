import bpy
from .errors import MeshError
from . import material, utils
import numpy as np
from mathutils import Vector


def createMesh(name, *, vertices, faces=[], edges=[], matrix=None, mat=None, collection=None, smooth=True):

    vertices = utils.ndarray_pydata.parse(vertices)
    if len(faces) > 0:
        faces = utils.ndarray_pydata.parse(faces)

    # 创建mesh
    mesh = bpy.data.meshes.new(name)
    if vertices:
        if matrix is not None:
            vertices = np.transpose(np.matmul(matrix, np.transpose(vertices)))
        mesh.from_pydata(vertices, edges, faces)
        mesh.validate()

    if smooth:
        smoothMesh(mesh)

    # 创建对象
    obj = bpy.data.objects.new(name, mesh)
    if collection is None:
        bpy.context.scene.collection.objects.link(obj)
    else:
        collection.objects.link(obj)

    # 赋材质
    if not mat:
        return obj
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    obj.active_material = mat
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    bpy.ops.object.select_all(action="DESELECT")
    return obj


def smoothMesh(mesh):
    for poly in mesh.polygons:
        poly.use_smooth = True


def getBboxCenter(obj):
    local_bbox_center = 0.125 * sum((Vector(b) for b in obj.bound_box), Vector())
    global_bbox_center = obj.matrix_world @ local_bbox_center
    return global_bbox_center
