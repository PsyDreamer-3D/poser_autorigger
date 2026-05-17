import bpy
import math
from .constraints import add_transformation_constraint, add_copy_location_constraint, add_limit_rotation_constraint
from .helpers import create_bone
from .colorscheme import bright_blue

def setup_foot_roll_constraints():
    armature = bpy.context.object
    pose_bones = bpy.context.object.pose.bones

    bone_mch_roll_toe = pose_bones['MCH-Roll-Toe.L']
    bone_mch_roll_foot = pose_bones['MCH-Roll-Foot.L']
    bone_ctrl_foot_roll = pose_bones['CTRL-Foot-Roll.L']
    bone_ctrl_foot_roll.lock_rotation = [False, True, True]

    # add_transformation_constraint()
    add_copy_location_constraint(
        pose_bone=bone_mch_roll_foot,
        target_bone=bone_mch_roll_toe,
        target_object=armature,
        head_tail=1.0,
        owner_space='WORLD',
        target_space='WORLD',
    )

    add_transformation_constraint(
        pose_bone=bone_mch_roll_toe,
        target_bone=bone_ctrl_foot_roll,
        target_object=armature,
        target_space='LOCAL',
        owner_space='LOCAL',
        map_from='ROTATION',
        from_max_x_rot=181.0,
        from_min_x_rot=90.0,
        map_to='ROTATION',
        to_min_x_rot=0.0,
        to_max_x_rot=113.0
    )

    add_transformation_constraint(
        pose_bone=bone_mch_roll_foot,
        target_bone=bone_ctrl_foot_roll,
        target_object=armature,
        target_space='LOCAL',
        owner_space='LOCAL',
        map_from='ROTATION',
        from_min_x_rot=0.0,
        from_max_x_rot=90.0,
        map_to='ROTATION',
        to_min_x_rot=0.0,
        to_max_x_rot=90.0
    )

    add_limit_rotation_constraint(
        pose_bone=bone_ctrl_foot_roll,
        use_limit_x=True,
        min_x=0.0,
        max_x=math.radians(179.0)
    )


def create_foot_roll_control_bones():
    all_collections = bpy.context.object.data.collections_all
    collection = bpy.context.object.data.collections
    mch_collection = all_collections.get('MCH')
    leg_collection = all_collections.get('Legs')

    mch_footroll_collection = collection.new('MCH Footroll', parent=mch_collection)
    footroll_ctrl_collection = collection.new('Foot Roll', parent=leg_collection)
    edit_bones = bpy.context.object.data.edit_bones

    # create and position bones for foot roll mechanism
    # Bones (Symmetrized):
    # MCH-Roll-Toe.L (parented to MCH-Foot-Rollback.L)
    # MCH-Roll-Foot.L (parented to MCH-Foot-Rollback.L)
    # Roll-Foot.L (parented to CTRL-IK-Foot.L)
    # MCH-Foot-Rollback.L (parented to Roll-Foot.L)
    # CTRL-Foot-Roll.L (parented to CTRL-IK-Foot.L

    bone_ik_toe = edit_bones['IK-Toe.L']
    bone_ik_foot = edit_bones['IK-Foot.L']
    bone_ctrl_ik_foot = edit_bones['CTRL-IK-Foot.L']

    create_bone(
        edit_bones=edit_bones,
        name='CTRL-Foot-Roll.L',
        custom_color=bright_blue,
        display_type='OCTAHEDRAL',
        parent=bone_ctrl_ik_foot,
        head=[bone_ik_foot.head[0], bone_ik_foot.head[1] + 0.05, bone_ik_foot.head[2]],
        tail=[bone_ik_foot.head[0], bone_ik_foot.head[1] + 0.075, bone_ik_foot.head[2]],
        collection=footroll_ctrl_collection,
    )

    bone_roll_foot = create_bone(
        edit_bones=edit_bones,
        name='Roll-Foot.L',
        custom_color=bright_blue,
        display_type='OCTAHEDRAL',
        parent=bone_ctrl_ik_foot,
        head=bone_ik_foot.head,
        tail=[bone_ik_foot.head[0], -0.05 , bone_ik_foot.head[2]],
        collection=mch_footroll_collection,
    )

    bone_mch_foot_rollback = create_bone(
        edit_bones=edit_bones,
        name='MCH-Foot-Rollback.L',
        custom_color=bright_blue,
        display_type='OCTAHEDRAL',
        parent=bone_roll_foot,
        head=[bone_ik_foot.head[0], bone_ik_foot.head[1], 0.025],
        tail=[bone_ik_foot.head[0], bone_ik_foot.head[1] - 0.025, 0.025],
        collection=mch_footroll_collection,
    )

    bone_mch_roll_toe = create_bone(
        edit_bones=edit_bones,
        name='MCH-Roll-Toe.L',
        custom_color=bright_blue,
        display_type='OCTAHEDRAL',
        parent=bone_mch_foot_rollback,
        head=[bone_ik_toe.tail[0], bone_ik_toe.tail[1], 0],
        tail = bone_ik_toe.head,
        collection=mch_footroll_collection,
    )

    bone_mch_roll_foot = create_bone(
        edit_bones=edit_bones,
        name='MCH-Roll-Foot.L',
        custom_color=bright_blue,
        display_type='OCTAHEDRAL',
        parent=bone_mch_foot_rollback,
        head=bone_ik_foot.tail,
        tail= bone_ik_foot.head,
        collection=mch_footroll_collection,
    )

    # parent existing bones to new ones
    bone_ik_toe.parent = bone_mch_roll_toe
    bone_ik_foot.parent = bone_mch_roll_foot
