def change_mat_alpha(mat, alpha):
    nodes = mat.node_tree.nodes
    node = nodes.get("Principled BSDF")
    node.inputs.get("Alpha").default_value = alpha


def change_mat_color(mat, r, g, b):
    nodes = mat.node_tree.nodes
    node = nodes.get("Principled BSDF")
    node.inputs.get("Base Color").default_value = (r, g, b, 1)
