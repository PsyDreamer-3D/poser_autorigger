"""Driver setup functions for FK/IK switching."""

import bpy


def _add_fkik_driver(constraint, armature, data_path: str) -> None:
    """
    Add an FK/IK switch driver to a constraint.
    
    Args:
        constraint: Constraint to add driver to
        armature: Armature object
        data_path: Property data path for the driver variable
    """
    fcurve = constraint.driver_add("influence")
    driver = fcurve.driver
    driver.type = 'SCRIPTED'
    driver.use_self = True
    
    var = driver.variables.new()
    var.name = 'fkik_switch'
    var.type = 'SINGLE_PROP'
    
    target = var.targets[0]
    target.id_type = 'OBJECT'
    target.id = armature
    target.data_path = data_path
    
    driver.expression = 'fkik_switch'
    driver.use_self = False


def create_limb_fkik_switch_drivers(chain: list[str], prop_name: str) -> None:
    """
    Create FK/IK switch drivers for limb bones (arms/legs).
    
    Limbs have separate left and right properties.
    
    Args:
        chain: List of bone names in the FK/IK chain
        prop_name: Name of the custom property (e.g., 'arms_fkik', 'legs_fkik')
    """
    armature = bpy.context.object
    pose_bones = armature.pose.bones

    for bone_name in chain:
        for bone in pose_bones:
            if bone_name not in bone.name:
                continue

            is_left = '.L' in bone.name
            side_index = 0 if is_left else 1
            
            for constraint in bone.constraints:
                if 'IK' in constraint.name and constraint.type == 'COPY_TRANSFORMS':
                    data_path = f'pose.bones["PROPERTIES"]["{prop_name}"][{side_index}]'
                    _add_fkik_driver(constraint, armature, data_path)


def create_spine_fkik_switch_drivers(chain: list[str], prop_name: str) -> None:
    """
    Create FK/IK switch drivers for spine bones.
    
    Spine has a single property for the entire chain.
    
    Args:
        chain: List of bone names in the FK/IK chain
        prop_name: Name of the custom property (e.g., 'spine_fkik')
    """
    armature = bpy.context.object
    pose_bones = armature.pose.bones

    for bone_name in chain:
        for bone in pose_bones:
            if bone_name not in bone.name:
                continue

            for constraint in bone.constraints:
                if 'IK' in constraint.name and constraint.type == 'COPY_TRANSFORMS':
                    data_path = f'pose.bones["PROPERTIES"]["{prop_name}"]'
                    _add_fkik_driver(constraint, armature, data_path)


def create_finger_fkik_switch_drivers(prop_name: str) -> None:
    """
    Create FK/IK switch drivers for finger bones.
    
    Fingers have separate properties for each finger on each side.
    
    Args:
        prop_name: Base name of the custom property (e.g., 'fingers_fkik')
                   Will be suffixed with '_l' or '_r' for left/right
    """
    armature = bpy.context.object
    pose_bones = armature.pose.bones

    # Define all finger chains
    finger_chains = [
        ['FK-Thumb_1', 'FK-Thumb_2', 'FK-Thumb_3'],
        ['FK-Index_1', 'FK-Index_2', 'FK-Index_3'],
        ['FK-Mid_1', 'FK-Mid_2', 'FK-Mid_3'],
        ['FK-Ring_1', 'FK-Ring_2', 'FK-Ring_3'],
        ['FK-Pinky_1', 'FK-Pinky_2', 'FK-Pinky_3'],
    ]
    
    chain = [bone for finger_chain in finger_chains for bone in finger_chain]
    finger_names = ['Thumb', 'Index', 'Mid', 'Ring', 'Pinky']
    
    for bone_name in chain:
        for bone in pose_bones:
            if bone_name not in bone.name:
                continue

            is_left = '.L' in bone.name
            prop_name_side = f"{prop_name}_{'l' if is_left else 'r'}"

            for finger_index, finger_name in enumerate(finger_names):
                if finger_name not in bone.name:
                    continue

                for constraint in bone.constraints:
                    if 'IK' in constraint.name and constraint.type == 'COPY_TRANSFORMS':
                        data_path = f'pose.bones["PROPERTIES"]["{prop_name_side}"][{finger_index}]'
                        _add_fkik_driver(constraint, armature, data_path)
