"""Color scheme definitions for rig bones."""

import colorsys
from bpy.types import EditBone

# Predefined color schemes for different bone types
bright_red = {
    'normal': colorsys.hsv_to_rgb(0.0, 1, 1),
    'select': colorsys.hsv_to_rgb(0.0, 1, 1),
    'active': colorsys.hsv_to_rgb(0.0, 0.25, 1),
}

bright_orange = {
    'normal': colorsys.hsv_to_rgb(0.0875, 1, 1),
    'select': colorsys.hsv_to_rgb(0.0875, 1, 1),
    'active': colorsys.hsv_to_rgb(0.0875, 0.25, 1),
}

bright_yellow = {
    'normal': colorsys.hsv_to_rgb(0.167, 1, 1),
    'select': colorsys.hsv_to_rgb(0.167, 1, 1),
    'active': colorsys.hsv_to_rgb(0.167, 0.25, 1),
}

bright_green = {
    'normal': colorsys.hsv_to_rgb(0.25, 1, 1),
    'select': colorsys.hsv_to_rgb(0.25, 1, 1),
    'active': colorsys.hsv_to_rgb(0.25, 0.25, 1),
}

bright_blue = {
    'normal': colorsys.hsv_to_rgb(0.625, 1, 1),
    'select': colorsys.hsv_to_rgb(0.625, 1, 1),
    'active': colorsys.hsv_to_rgb(0.625, 0.625, 1),
}


def assign_custom_color(bone: EditBone, color: dict[str, tuple[float, float, float]]) -> None:
    """
    Apply custom color to a bone.
    
    Args:
        bone: EditBone to color
        color: Dictionary with 'normal', 'select', and 'active' RGB tuples
    """
    bone.color.palette = 'CUSTOM'
    bone.color.custom.normal = color['normal']
    bone.color.custom.select = color['select']
    bone.color.custom.active = color['active']
