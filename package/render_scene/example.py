import pickle as pkl
import numpy as np
import os
from math import radians
import math

import bpy
import mathutils
from mocap_blender import file, mesh, utils, collection, material, objects

from mocap_blender import path as PATH
from .common import change_mat_alpha, change_mat_color

BLEND_SETUP = os.path.join(PATH.ASSET_PATH, "base.blend")


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

    scene_name = data["process_key"]
    verts_rh = data["verts_rh"]
    faces_rh = data["faces_rh"]

    obj_list = data["obj_list"]
    print("scene_name:", scene_name)
    print("obj_list:", obj_list)
    objects = mocap_anno.loadObjectInfo(scene_name, True)

    if frames is None:
        frames = [0]
    elif isinstance(frames, int):
        frames = [frames]
    print("frames:", frames)
    print([frame_ids[f] for f in frames])
    collection.removeCollection("frames", withobject=True)
    collection.removeCollection("objects", withobject=True)

    collection.getOrNewCollection("objects")
    collection.getOrNewCollection("frames")

    hand_mat = material.getMaterialByName("Hand")
    hand1_mat = material.getMaterialByName("Hand_1")
    interacted_mat = material.getMaterialByName("interacted")
    interacted1_mat = material.getMaterialByName("interacted_1")
    other_mat = material.getMaterialByName("Other")

    for model in objects:
        if model in obj_list:
            continue
        mocap_model.loadModel(model, True)
        for obj in bpy.context.selected_objects:
            collection.moveCollection(obj, "objects")
            trs = mathutils.Matrix(objects[model][frame_ids[0]])
            res = affine @ trs @ affine.inverted() @ offset
            obj.matrix_world = res
            material.setMat(obj, other_mat)
            m = obj.data
            for poly in m.polygons:
                poly.use_smooth = True

    for i, f in enumerate(frames):
        alpha = math.pow(((i + 1) / len(frames) * 0.4 + 0.6), 2)
        hand_mat_copy = hand_mat.copy()
        hand1_mat_copy = hand1_mat.copy()
        interacted_mat_copy = interacted_mat.copy()
        interacted1_mat_copy = interacted1_mat.copy()
        change_mat_alpha(hand_mat_copy, alpha)
        change_mat_alpha(hand1_mat_copy, alpha)
        change_mat_alpha(interacted_mat_copy, alpha)
        change_mat_alpha(interacted1_mat_copy, alpha)

        frame_coll = collection.getOrNewCollection("{:05}".format(frame_ids[f]), "frames")
        lh = mesh.createMesh("lh", vertices=verts_lh[f], faces=faces_lh, matrix=matrix, collection=frame_coll)
        rh = mesh.createMesh("rh", vertices=verts_rh[f], faces=faces_rh, matrix=matrix, collection=frame_coll)
        material.setMat(lh, hand_mat_copy)
        material.setMat(rh, hand1_mat_copy)
        mat = interacted_mat_copy
        for model in obj_list:
            mocap_model.loadModel(model, True)
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
