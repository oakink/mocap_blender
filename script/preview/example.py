import pickle as pkl
import numpy as np
import os
from math import radians
import math

import bpy
import mathutils
from mocap_blender import bpy_obj, file, mesh, util, collection, material, camera

from mocap_blender import path as PATH


def load_data(path):
    with open(path, "rb") as f:
        data = pkl.load(f)
    return data


def load_data_to_scene(data, *, frames=None):
    if isinstance(data, str):
        data = load_data(data)

    matrix = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    affine_mat = util.getAffineMat(matrix)
    offset = mathutils.Matrix.Rotation(radians(90), 4, "X")
    affine = mathutils.Matrix(affine_mat)

    scene_name = data["name"]
    print("scene_name:", scene_name)

    verts = data["vert"]
    faces = data["face"]

    obj_list = data["obj_list"]
    print("obj_list:", obj_list)
    obj_attr = data["obj_attr"]

    collection.removeCollection("object", withobject=True)
    collection.removeCollection("hand", withobject=True)
    cam = camera.getCamera(name="camera_main")
    if cam:
        camera.removeCamera(cam)

    collection.getOrNewCollection("object")
    collection.getOrNewCollection("hand")

    #hand_mat = material.getMaterialByName("Hand")  # TODO replace with api
    #interacted_mat = material.getMaterialByName("interacted")
    #interacted1_mat = material.getMaterialByName("interacted_1")
    #other_mat = material.getMaterialByName("Other")

    obj_coll = collection.getOrNewCollection("object")
    for obj_id in obj_list:
        _v = obj_attr[obj_id]["vert"]
        _f = obj_attr[obj_id]["face"]
        obj = mesh.createMesh(obj_id, vertices=_v, faces=_f, matrix=matrix, collection=obj_coll)
        #material.setMat(obj, other_mat)
        m = obj.data
        mesh.smoothMesh(m)

    # alpha = math.pow(((i + 1) / len(frames) * 0.4 + 0.6), 2)
    alpha = 1.0
    #hand_mat_copy = hand_mat.copy()
    #interacted_mat_copy = interacted_mat.copy()
    #interacted1_mat_copy = interacted1_mat.copy()
    #change_mat_alpha(hand_mat_copy, alpha)
    #change_mat_alpha(interacted_mat_copy, alpha)
    #change_mat_alpha(interacted1_mat_copy, alpha)

    hand_coll = collection.getOrNewCollection("hand")
    h = mesh.createMesh("hand", vertices=verts, faces=faces, matrix=matrix, collection=hand_coll)
    
    # create camera
    cam_extr = data["cam_extr"]
    cam_intr = data["cam_intr"]
    cam_transf = mathutils.Matrix(cam_extr).inverted()
    cam_transf = affine @ cam_transf @ affine.inverted() @ offset.inverted()
    
    CAM_SIZE=(848,480)
    cam = camera.createCamera("camera_main", matrix=cam_transf, cam_intr=cam_intr, cam_size=CAM_SIZE)
    
    for _el in bpy.data.images:
        if _el.name == "bg":
            bpy.data.images.remove(_el)    
    background = data.get("bg", None)
    if background is not None:
        cam.data.show_background_images = True
        bg = cam.data.background_images.new()
        # background = background.astype(np.float16)
        _background = np.zeros((background.shape[0], background.shape[1], 4), dtype=np.float16)
        _background[:, :, 0:3] = background[:, :, (2,1,0)] / 255
        _background[:, :, 3] = 1.0
        _background = np.flip(_background, axis=0)
        bg_img = bpy.data.images.new('bg', background.shape[1], background.shape[0], alpha=True, float_buffer=False)
        bg_img.pixels = _background.ravel()
        bg.image = bg_img
        
        # actual render needs compositor
        tree = bpy.context.scene.node_tree
        for n in tree.nodes:
            if n.type == 'IMAGE' and n.label == 'BackgroundCompositor':
                n.image = bg_img
    

if __name__ == "__main__":
    load_data_to_scene("./data/example/example__000000.pkl")
