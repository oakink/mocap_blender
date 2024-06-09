import bpy
import copy

# keys:
# ['Base Color', 'Subsurface', 'Subsurface Radius', 'Subsurface Color', 'Metallic', 'Specular', 'Specular Tint', 'Roughness', 'Anisotropic', 'Anisotropic Rotation', 'Sheen', 1Sheen Tint', 'Clearcoat', 'Clearcoat Roughness', 'IOR', 'Transmission', 'Transmission Roughness', 'Emission', 'Emission Strength', 'Alpha', 'Normal', 'Clearcoat Normal', 'Tangent']
__DEFAULT_BSDF_SETTINGS = {
    "Base Color": (1, 1, 1, 1),
    "Subsurface Color": (1, 1, 1, 1),
    "Subsurface": 0.15,
    "Subsurface Radius": [1.1, 0.2, 0.1],
    "Metallic": 0.3,
    "Specular": 0.5,
    "Specular Tint": 0.5,
    "Roughness": 0.75,
    "Anisotropic": 0.25,
    "Anisotropic Rotation": 0.25,
    "Sheen": 0.75,
    "Sheen Tint": 0.5,
    "Clearcoat": 0.5,
    "Clearcoat Roughness": 0.5,
    "IOR": 1.450,
    "Transmission": 0.1,
    "Transmission Roughness": 0.1,
    "Emission": (0, 0, 0, 1),
    "Emission Strength": 0.0,
    "Alpha": 1.0,
}


def clear_material(material):
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()


def colored_material_diffuse_BSDF(r, g, b, a=1, roughness=0.127451, name="diffuse"):
    materials = bpy.data.materials
    material = materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    bsdf.inputs["Base Color"].default_value = (r, g, b, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Alpha"].default_value = a
    return material


def getDefaultSettings():
    settings = copy.deepcopy(__DEFAULT_BSDF_SETTINGS)
    return settings


def setMaterialSettings(key: str, value, settings=None):
    if not settings:
        settings = getDefaultSettings()
    settings[key] = value
    return settings


def bsdf_material(settings, name):
    materials = bpy.data.materials
    material = materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    diffuse = nodes["Principled BSDF"]
    inputs = diffuse.inputs

    settings = settings
    for setting, val in settings.items():
        inputs[setting].default_value = val
    return material


def createDiffuseMaterial(r, g, b, a=1, roughness=0.127451, name="diffuse"):
    material = colored_material_diffuse_BSDF(r, g, b, a=a, roughness=roughness, name=name)
    return material


def getMaterialByName(name):
    mat = bpy.data.materials.get(name)
    return mat


def setMat(obj, mat):
    obj.select_set(True)
    obj.active_material = mat
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    bpy.ops.object.select_all(action="DESELECT")
