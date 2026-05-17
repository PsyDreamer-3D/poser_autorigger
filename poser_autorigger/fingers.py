from .helpers import create_fkik_chains, create_bone, move_bone_along_local_axis, align_bone_to_source
from .constraints import add_limit_scale_constraint, add_copy_rotation_constraint, add_limit_rotation_constraint, add_transformation_constraint
from bpy.types import PoseBone
import bpy

def create_finger_fkik_chains():
    edit_bones = bpy.context.object.data.edit_bones
    ik_collection = bpy.context.object.data.collections_all.get('Fingers IK')
    fk_collection = bpy.context.object.data.collections_all.get('Fingers FK')

    # ofml — finger chains now
    thumb_fkik_chain = [
        'Thumb_1',
        'Thumb_2',
        'Thumb_3',
    ]
    index_fkik_chain = [
        'Index_1',
        'Index_2',
        'Index_3',
    ]
    mid_fkik_chain = [
        'Mid_1',
        'Mid_2',
        'Mid_3',
    ]
    ring_fkik_chain = [
        'Ring_1',
        'Ring_2',
        'Ring_3',
    ]
    pinky_fkik_chain = [
        'Pinky_1',
        'Pinky_2',
        'Pinky_3',
    ]

    finger_ik_chain = []
    finger_ik_chain = create_fkik_chains(thumb_fkik_chain, 'IK-Hand.L', 'IK', '.L', 'THEME01', 0.004, True)
    finger_ik_chain += create_fkik_chains(index_fkik_chain, 'IK-Hand.L', 'IK', '.L', 'THEME01', 0.004, True)
    finger_ik_chain += create_fkik_chains(mid_fkik_chain, 'IK-Hand.L', 'IK', '.L', 'THEME01', 0.004, True)
    finger_ik_chain += create_fkik_chains(ring_fkik_chain, 'IK-Hand.L', 'IK', '.L', 'THEME01', 0.004, True)
    finger_ik_chain += create_fkik_chains(pinky_fkik_chain, 'IK-Hand.L', 'IK', '.L', 'THEME01', 0.004, True)

    finger_fk_chain = []
    finger_fk_chain = create_fkik_chains(thumb_fkik_chain, 'FK-Hand.L', 'FK', '.L', 'THEME03', 0.002)
    finger_fk_chain += create_fkik_chains(index_fkik_chain, 'FK-Hand.L', 'FK', '.L', 'THEME03', 0.002)
    finger_fk_chain += create_fkik_chains(mid_fkik_chain, 'FK-Hand.L', 'FK', '.L', 'THEME03', 0.002)
    finger_fk_chain += create_fkik_chains(ring_fkik_chain, 'FK-Hand.L', 'FK', '.L', 'THEME03', 0.002)
    finger_fk_chain += create_fkik_chains(pinky_fkik_chain, 'FK-Hand.L', 'FK', '.L', 'THEME03', 0.002)

    for ik_bone in finger_ik_chain:
        ik_collection.assign(ik_bone)

    for fk_bone in finger_fk_chain:
        fk_collection.assign(fk_bone)

    # adjust position of middle joints in IK finger chain
    # this eliminates the need for a pole target.
    for bone in edit_bones:
        if bone.name in ['IK-Thumb_2.L', 'IK-Index_2.L', 'IK-Mid_2.L', 'IK-Ring_2.L', 'IK-Pinky_2.L']:
            if bone.name == 'IK-Thumb_2.L':
                head_y_axis = bone.head[1]
                tail_y_axis = bone.tail[1]
                tail_z_axis = bone.tail[2]
                bone.head[1] = head_y_axis - 0.005
                bone.tail[1] = tail_y_axis - 0.005
                bone.tail[2] = tail_z_axis + 0.005
            else:
                head_z_axis = bone.head[2]
                tail_z_axis = bone.tail[2]
                bone.head[2] = head_z_axis + 0.005
                bone.tail[2] = tail_z_axis + 0.005



def create_finger_control_bones():
    edit_bones = bpy.context.object.data.edit_bones
    fk_ctrl_collection = bpy.context.object.data.collections_all.get('Fingers FK CTRL')
    ik_ctrl_collection = bpy.context.object.data.collections_all.get('Fingers IK CTRL')

    # eventually, we'll want to "DRY" this out, but this will do for now
    # finger/thumb curl bones
    # these are the bones to use for naming and positioning
    ctrl_bones = ['Thumb_1', 'Index_1', 'Mid_1', 'Ring_1', 'Pinky_1']
    fk_hand = edit_bones['FK-Hand.L']
    ik_hand = edit_bones['IK-Hand.L']
    fk_fingers_ctrl = create_bone(
        edit_bones=edit_bones,
        name='FK-Fingers-CTRL.L',
        parent=fk_hand,
        head=fk_hand.head,
        tail=fk_hand.tail,
        length=0.05,
        collection=fk_ctrl_collection,
        palette='THEME03'
    )
    ik_fingers_ctrl = create_bone(
        edit_bones=edit_bones,
        name='IK-Fingers-CTRL.L',
        parent=ik_hand,
        head=ik_hand.head,
        tail=ik_hand.tail,
        length=0.05,
        collection=ik_ctrl_collection,
        palette='THEME09'
    )

    # make bones to parent controls to, then parent these bones to their respective layers


    bpy.ops.armature.select_all(action='DESELECT')
    for bone in ctrl_bones:
        name = bone.replace('_1', '')
        fk_finger_bone = edit_bones['FK-' + bone + '.L']
        ik_finger_bone = edit_bones['IK-' + name + '_3.L']

        fk_ctrl_bone = create_bone(
            edit_bones=edit_bones,
            name='CTRL-FK-' + name + '.L',
            head=fk_finger_bone.head,
            tail=fk_finger_bone.tail,
            length=0.025,
            bbone_size=fk_finger_bone.bbone_x * 3,
            palette='THEME09',
            parent=fk_fingers_ctrl,
            collection=fk_ctrl_collection
        )
        ik_ctrl_bone = create_bone(
            edit_bones=edit_bones,
            name='CTRL-IK-' + name + '.L',
            head=ik_finger_bone.head,
            tail=ik_finger_bone.tail,
            length=0.025,
            bbone_size=fk_finger_bone.bbone_x * 3,
            palette='THEME09',
            parent=ik_fingers_ctrl,
            collection=ik_ctrl_collection
        )

        move_bone_along_local_axis(fk_ctrl_bone, -0.025)
        move_bone_along_local_axis(ik_ctrl_bone, 0.025)
        ik_ctrl_bone.head = ik_finger_bone.tail # we want the heads and tails to align
        ik_ctrl_bone.length = 0.025 # make sure length stays the same, though

    # need to do the same thing for thumb_1, because IKs are a bit different here
    thumb_bone = edit_bones['IK-Thumb_1.L']
    ik_thumb_bone = create_bone(
        edit_bones=edit_bones,
        name='CTRL-IK-Thumb-Joint.L',
        head=thumb_bone.tail,
        tail=thumb_bone.head,
        length=0.025,
        bbone_size=0.002,
        palette='THEME09',
        collection=ik_ctrl_collection,
        parent=ik_fingers_ctrl
    )
    align_bone_to_source(ik_thumb_bone, thumb_bone)


def create_finger_fk_ctrl_constraints():
    armature = bpy.context.object
    bones = armature.pose.bones

    thumb_fkik_chain = [
        'Thumb_1',
        'Thumb_2',
        'Thumb_3',
    ]
    index_fkik_chain = [
        'Index_1',
        'Index_2',
        'Index_3',
    ]
    mid_fkik_chain = [
        'Mid_1',
        'Mid_2',
        'Mid_3',
    ]
    ring_fkik_chain = [
        'Ring_1',
        'Ring_2',
        'Ring_3',
    ]
    pinky_fkik_chain = [
        'Pinky_1',
        'Pinky_2',
        'Pinky_3',
    ]

    finger_fk_ctrls = [
        'CTRL-FK-Thumb.L',
        'CTRL-FK-Index.L',
        'CTRL-FK-Mid.L',
        'CTRL-FK-Ring.L',
        'CTRL-FK-Pinky.L',
    ]

    for ctrl_bone in finger_fk_ctrls:
        for i,bone in enumerate(bones):
            if ctrl_bone in bone.name:
                add_limit_scale_constraint_to_ctrl_bone(bone)

            finger_bone_chain, side = ctrl_bone.replace('CTRL-', '').split('.')
            if finger_bone_chain in bone.name and side in bone.name and 'CTRL-' not in bone.name:
                finger_bone_item, finger_bone_position = bone.name.replace('.L', '').split('_')
                finger_bone = bones[bone.name]
                if 'FK-Thumb' in bone.name:
                    fk_thumb_constraints(armature, bone, bones, ctrl_bone, finger_bone_position, i)

                if finger_bone_item in ['FK-Index', 'FK-Mid', 'FK-Ring', 'FK-Pinky']:
                    if 1 == int(finger_bone_position):
                        add_copy_rotation_constraint(
                            pose_bone=finger_bone,
                            target_bone=bones[ctrl_bone],
                            target_object=armature,
                            name='Copy Rotation (Side-Side)',
                            use_y=False,
                            mix_mode='ADD'
                        )
                        add_transformation_constraint(
                            pose_bone=finger_bone,
                            target_bone=bones[ctrl_bone],
                            target_object=armature,
                            name='Transformation (Curl)',
                            map_from='SCALE',
                            from_min_y_scale=0.25,
                            from_max_y_scale=1.0,
                            map_to='ROTATION',
                            map_to_x_from='Y',
                            to_min_x_rot=-70.0,
                            to_max_x_rot=0,
                            mix_mode='ADD'
                        )
                    if 2 == int(finger_bone_position):
                        add_copy_rotation_constraint(
                            pose_bone=finger_bone,
                            target_bone=bones[i - 1],
                            target_object=armature,
                            use_y=False,
                            use_z=False,
                        )
                    if 3 == int(finger_bone_position):
                        add_copy_rotation_constraint(
                            pose_bone=finger_bone,
                            target_bone=bones[i - 1],
                            target_object=armature,
                            use_y=False,
                            use_z=False,
                        )



def fk_thumb_constraints(armature, bone: PoseBone, bones, ctrl_bone: str,
                         finger_bone_position: str, i: int):

    finger_bone = bones[bone.name]
    if 1 == int(finger_bone_position):
        add_copy_rotation_constraint(finger_bone, bones[ctrl_bone], armature, mix_mode='ADD')
        add_limit_rotation_constraint(
            pose_bone=finger_bone,
            min_x=-0.5235987756,
            max_x=0.174533,
            min_y=-0.174533,
            max_y=-0.174533,
            min_z=-0.52359875,
            max_z=0.174533,
            use_limit_x=True,
            use_limit_y=True,
            use_limit_z=True,
        )

    if 2 == int(finger_bone_position):
        add_transformation_constraint(
            pose_bone=finger_bone,
            target_bone=bones[ctrl_bone],
            target_object=armature,
            map_from='SCALE',
            map_to='ROTATION',
            from_min_y_scale=0.25,
            from_max_y_scale=1.0,
            map_to_z_from='Y',
            to_min_z_rot=62.2,
            to_max_z_rot=0.0
        )

    if 3 == int(finger_bone_position):
        add_transformation_constraint(
            pose_bone=finger_bone,
            target_bone=bones[i - 1],
            target_object=armature,
            map_from='ROTATION',
            map_to='ROTATION',
            from_min_z_rot=0,
            from_max_z_rot=25.0,
            map_to_y_from='Z',
            map_to_z_from='Z',
            to_min_y_rot=0.0,
            to_max_y_rot=30.0,
            to_min_z_rot=0,
            to_max_z_rot=73.0
        )


def add_limit_scale_constraint_to_ctrl_bone(bone: PoseBone):
    bone.lock_location[0] = bone.lock_location[1] = bone.lock_location[2] = True
    bone.lock_rotation[0] = bone.lock_rotation[1] = True
    bone.lock_scale[0] = bone.lock_scale[2] = True

    add_limit_scale_constraint(
        pose_bone=bone,
        min_y=0.25,
        max_y=1.0,
        use_min_y=True,
        use_max_y=True,
    )
