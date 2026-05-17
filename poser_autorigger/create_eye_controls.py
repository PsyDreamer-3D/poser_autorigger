import bpy
from .constraints import add_copy_rotation_constraint, add_damped_track_constraint
from .helpers import create_bone
from .colorscheme import bright_blue, bright_yellow

def setup_eye_tracking_constraints():
    armature = bpy.context.object
    pose_bones = bpy.context.object.pose.bones
    # assign copy constraint from MCH-Eye.L to DEF-Eye.L
    bone_mch_eye_left = pose_bones['MCH-Eye.L']
    bone_eye_left = pose_bones['DEF-Eye.L']
    bone_ctrl_eye_target_left = pose_bones['CTRL-Eye_Target.L']

    add_copy_rotation_constraint(
        pose_bone=bone_eye_left,
        target_bone=bone_mch_eye_left,
        target_object=armature,
        owner_space='WORLD',
        target_space='WORLD',
    )

    add_damped_track_constraint(
        pose_bone=bone_mch_eye_left,
        target_bone=bone_ctrl_eye_target_left.name,
        target_object=armature,
        track_axis='TRACK_Y'
    )


def create_eye_control_bones():
    collection = bpy.context.object.data.collections_all.get('Eyes CTRL')
    mch_parent_collection = bpy.context.object.data.collections_all.get('MCH')
    mch_eye_collection = bpy.context.object.data.collections.new('MCH Eye', parent=mch_parent_collection)
    edit_bones = bpy.context.object.data.edit_bones
    # create main eye track and two eye track bones
    bone_eye_left = edit_bones['DEF-Eye.L']

    create_bone(
        edit_bones=edit_bones,
        name='MCH-Eye.L',
        head=bone_eye_left.head,
        tail=[bone_eye_left.tail[0], bone_eye_left.tail[1] + 0.005, bone_eye_left.tail[2]],
        use_deform=False,
        parent=bone_eye_left.parent,
        bbone_size=bone_eye_left.bbone_z * 2,
        collection=mch_eye_collection
    )

    bone_ctrl_eye_target = create_bone(
        edit_bones=edit_bones,
        name='CTRL-Eye_Target',
        head=[0, -0.25, bone_eye_left.head[2]],
        tail=[0, -0.27, bone_eye_left.head[2]],
        use_deform=False,
        parent=edit_bones['DEF-Head'],
        bbone_size=bone_eye_left.bbone_x,
        custom_color=bright_blue,
        collection=collection
    )

    create_bone(
        edit_bones=edit_bones,
        name='CTRL-Eye_Target.L',
        parent=bone_ctrl_eye_target,
        head=[bone_eye_left.head[0], -0.25, bone_eye_left.head[2]],
        tail=[bone_eye_left.head[0], -0.27, bone_eye_left.head[2]],
        bbone_size=bone_eye_left.bbone_x,
        custom_color=bright_yellow,
        collection=collection
    )
