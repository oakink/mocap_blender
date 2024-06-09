import pickle as pkl
import numpy as np
import os
from math import radians
import math

import bpy
import mathutils
from mocap_blender import file, mesh, utils, collection, material

from mocap_blender import path as PATH


def build_scene(data, action=None, frames=None):
    if isinstance(data, str):
        data = load_data(data)

    def _action():
        load_data_to_scene(data, frames=frames)
        if action is not None:
            action()

    print(BLEND_SETUP)
    file.openFile(BLEND_SETUP, _action)


def load_data(path):
    with open(path, "rb") as f:
        data = pkl.load(f)
    return data


def load_data_to_scene(data, *, frames=None):
    if isinstance(data, str):
        data = load_data(data)

    matrix = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    affine_mat = utils.getAffineMat(matrix)
    offset = mathutils.Matrix.Rotation(radians(90), 4, "X")
    affine = mathutils.Matrix(affine_mat)

    scene_name = data["name"]
    print("scene_name:", scene_name)

    verts = data["verts_rh"]
    faces = data["faces_rh"]

    obj_list = data["obj_list"]
    print("obj_list:", obj_list)
    obj_attr = data["obj_attr"]

    collection.removeCollection("objects", withobject=True)
    collection.removeCollection("hand", withobject=True)

    collection.getOrNewCollection("objects")
    collection.getOrNewCollection("hand")

    hand_mat = material.getMaterialByName("Hand")  # TODO replace with api
    interacted_mat = material.getMaterialByName("interacted")
    interacted1_mat = material.getMaterialByName("interacted_1")
    other_mat = material.getMaterialByName("Other")

    obj_coll = collection.getOrNewCollection("obj")
    for obj_id in obj_list:
        _v = obj_attr["verts"]
        _f = obj_attr["faces"]
        obj = mesh.createMesh(obj_id, vertices=_v, faces=_f, matrix=matrix, collection=obj_coll)
        material.setMat(obj, other_mat)
        m = obj.data
        for poly in m.polygons:
            poly.use_smooth = True

    # alpha = math.pow(((i + 1) / len(frames) * 0.4 + 0.6), 2)
    alpha = 1.0
    hand_mat_copy = hand_mat.copy()
    interacted_mat_copy = interacted_mat.copy()
    interacted1_mat_copy = interacted1_mat.copy()
    change_mat_alpha(hand_mat_copy, alpha)
    change_mat_alpha(interacted_mat_copy, alpha)
    change_mat_alpha(interacted1_mat_copy, alpha)

    hand_coll = collection.getOrNewCollection("hand")
    h = mesh.createMesh("hand", vertices=verts[f], faces=faces, matrix=matrix, collection=hand_coll)
    material.setMat(h, hand_mat_copy)
    mat = interacted_mat_copy
    for model in obj_list:
        for obj in bpy.context.selected_objects:
            collection.moveCollection(obj, frame_coll)
            trs = mathutils.Matrix(objects[model][frame_ids[f]])
            res = affine @ trs @ affine.inverted() @ offset
            obj.matrix_world = res
            m = obj.data
            material.setMat(obj, mat)
            for poly in m.polygons:
                poly.use_smooth = True
        if mat == interacted_mat_copy:
            mat = interacted1_mat_copy
        else:
            mat = interacted_mat_copy


if __name__ == "__main__":
    load_data_to_scene("./data/example/example_000000.pkl")
