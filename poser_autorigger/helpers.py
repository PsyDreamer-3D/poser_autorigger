"""Helper functions for bone manipulation and rig creation."""

from collections.abc import Sequence
from typing import Literal

import bpy
from bpy.types import ArmatureEditBones, BoneCollection, EditBone
from mathutils import Matrix, Vector

from .colorscheme import assign_custom_color


def rename_all_bones(prefix: str = '') -> None:
    """
    Rename all bones in the active armature with the given prefix.

    Args:
        prefix: String to prepend to bone names (e.g., 'DEF-')
    """
    edit_bones = bpy.context.object.data.edit_bones
    for bone in edit_bones:
        new_name = rename_bone(bone.name, prefix)
        if new_name != "":
            edit_bones[bone.name].name = new_name


def rename_bone(name: str, prefix: str = '') -> str:
    """
    Rename a bone following Blender naming conventions.

    Converts Poser naming (Left_/Right_ or l/r prefix) to Blender naming (.L/.R suffix).
    Skips special bones like 'root' and 'PROPERTIES'.

    Args:
        name: Original bone name
        prefix: Optional prefix to add (e.g., 'DEF-')

    Returns:
        New bone name with appropriate suffix, or empty string if bone should not be renamed
    """
    if "root" in name or "PROPERTIES" in name:
        return ""

    new_name = name
    if name.find('Left_') != -1:
        new_name = name[5:] + '.L'
    elif name.find('Right_') != -1:
        new_name = name[6:] + '.R'

    if name.find('l', 0, 1) != -1:
        new_name = name[1:] + '.L'
    elif name.find('r', 0, 1) != -1:
        new_name = name[1:] + '.R'

    return prefix + new_name


def create_bone(
    edit_bones: ArmatureEditBones,
    name: str,
    bbone_size: float = 0.001,
    head: Vector | Sequence[float] = 0.0,
    tail: Vector | Sequence[float] = 0.0,
    length: float = None,
    parent: EditBone = None,
    display_type: Literal[
        "ARMATURE_DEFINED", "OCTAHEDRAL", "STICK", "BBONE", "ENVELOPE", "WIRE"
    ] = "ARMATURE_DEFINED",
    use_deform: bool = False,
    use_connect: bool = False,
    palette: Literal[
        "DEFAULT", "THEME01", "THEME02", "THEME03", "THEME04", "THEME05",
        "THEME06", "THEME07", "THEME08", "THEME09", "THEME10", "THEME11",
        "THEME12", "THEME13", "THEME14", "THEME15", "THEME16", "THEME17",
        "THEME18", "THEME19", "THEME20", "CUSTOM"
    ] = 'CUSTOM',
    custom_color: dict[str, tuple[float, float, float]] = None,
    collection: BoneCollection = None,
) -> EditBone:
    """
    Create a new bone with specified properties.

    Args:
        edit_bones: Armature edit bones collection
        name: Name for the new bone
        bbone_size: B-Bone display size
        head: Head position (3D vector or sequence)
        tail: Tail position (3D vector or sequence)
        length: Override bone length
        parent: Parent bone
        display_type: Bone display type in viewport
        use_deform: Whether bone deforms mesh
        use_connect: Whether bone is connected to parent
        palette: Color palette theme
        custom_color: Custom color dict with 'normal', 'select', 'active' keys
        collection: Bone collection to assign to

    Returns:
        Newly created EditBone
    """
    new_bone = edit_bones.new(name)
    new_bone.head = head
    new_bone.tail = tail
    new_bone.parent = parent
    new_bone.use_deform = use_deform
    new_bone.use_connect = use_connect
    new_bone.display_type = display_type
    new_bone.bbone_x = new_bone.bbone_z = bbone_size

    if length is not None:
        new_bone.length = length

    if palette == 'CUSTOM' and custom_color is not None:
        assign_custom_color(new_bone, custom_color)
    else:
        new_bone.color.palette = palette

    if collection is not None:
        collection.assign(new_bone)

    return new_bone

def align_bone_to_source(source_bone: EditBone, target_bone: EditBone) -> None:
    """
    Align source bone's orientation to match target bone.

    Args:
        source_bone: Bone to be aligned
        target_bone: Bone to align to
    """
    target_dir = target_bone.tail - target_bone.head
    source_dir = source_bone.tail - source_bone.head

    rotation_q = source_dir.rotation_difference(target_dir)

    location, rotation, scale = source_bone.matrix.decompose()
    new_rotation = rotation_q @ rotation
    source_bone.matrix = Matrix.LocRotScale(location, new_rotation, scale)


def move_bone_along_local_axis(bone: EditBone, distance: float) -> None:
    """
    Move a bone along its local axis direction.

    Args:
        bone: Bone to move
        distance: Distance to move (positive for tail direction, negative for head)
    """
    normal = (bone.tail - bone.head).normalized()

    # Calculate the new head and tail positions
    translation_vector = normal * distance

    bone.head += translation_vector
    bone.tail += translation_vector


def create_fkik_chains(
    bone_chains: list[str],
    parent: str = '',
    prefix: str = 'IK',
    suffix: str = '.L',
    palette: Literal[
        "DEFAULT", "THEME01", "THEME02", "THEME03", "THEME04", "THEME05",
        "THEME06", "THEME07", "THEME08", "THEME09", "THEME10", "THEME11",
        "THEME12", "THEME13", "THEME14", "THEME15", "THEME16", "THEME17",
        "THEME18", "THEME19", "THEME20", "CUSTOM"
    ] = 'THEME01',
    bone_size: float = 0.002,
    use_connect: bool = False,
) -> list[EditBone]:
    """
    Create FK or IK chains from deform bones.

    Args:
        bone_chains: List of bone names to create chains for
        parent: Parent bone name for the first bone in chain
        prefix: Prefix for new bones (e.g., 'IK-', 'FK-')
        suffix: Side suffix (e.g., '.L', '.R', or '')
        palette: Color palette theme
        bone_size: B-Bone display size
        use_connect: Whether to connect bones in the chain

    Returns:
        List of created EditBone objects
    """
    edit_bones = bpy.context.object.data.edit_bones

    fkik_chains = []
    completed_fkik_chains = []
    for bone_chain_name in bone_chains:
        for bone in edit_bones:
            deform_bone_name = 'DEF-' + bone_chain_name + suffix
            if bone.name.find(bone_chain_name) == -1:
                continue

            if deform_bone_name != bone.name:
                continue

            bone_name = bone.name
            fkik_bone_name = bone_name.replace('DEF', prefix)
            fkik_chains.append(fkik_bone_name)

    for i, fkik_chain_item in enumerate(fkik_chains):
        # parenting
        fkik_bone_parent = edit_bones[parent] if i == 0 else edit_bones[fkik_chains[i - 1]]

        connect_bone = use_connect and i != 0
        deform_bone_name = fkik_chain_item.replace(prefix, 'DEF')
        fkik_bone = create_bone(
            edit_bones=edit_bones,
            name=fkik_chain_item,
            parent=fkik_bone_parent,
            palette=palette,
            head=edit_bones[deform_bone_name].head,
            tail=edit_bones[deform_bone_name].tail,
            bbone_size=bone_size,
            use_connect=connect_bone,
        )

        completed_fkik_chains.append(fkik_bone)

    return completed_fkik_chains
