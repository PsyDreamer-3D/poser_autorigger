"""Custom shape (widget) assignment for rig control bones."""

from bpy.types import PoseBone, Object
from pathlib import Path
import bpy


def assign_all_custom_shapes(armature: Object) -> None:
    """
    Assign custom shapes (widgets) to all control bones in the armature.
    
    Widgets are imported from WGTS.blend file and matched to bone names.
    Some finger controls use override transforms to position widgets correctly.
    
    Args:
        armature: The armature object to assign shapes to
    """
    pose_bones = armature.pose.bones
    shape_collection_name = 'WGTS_' + armature.name
    shape_collection = bpy.data.collections[shape_collection_name]
    
    # Finger controls need custom transform override
    override_bones = {
        'CTRL-IK-Thumb.L': 'IK-Thumb_3.L',
        'CTRL-IK-Index.L': 'IK-Index_3.L',
        'CTRL-IK-Mid.L': 'IK-Mid_3.L',
        'CTRL-IK-Ring.L': 'IK-Ring_3.L',
        'CTRL-IK-Pinky.L': 'IK-Pinky_3.L',
        'CTRL-IK-Thumb.R': 'IK-Thumb_3.R',
        'CTRL-IK-Index.R': 'IK-Index_3.R',
        'CTRL-IK-Mid.R': 'IK-Mid_3.R',
        'CTRL-IK-Ring.R': 'IK-Ring_3.R',
        'CTRL-IK-Pinky.R': 'IK-Pinky_3.R',
    }

    for bone in pose_bones:
        # Skip deform and mechanism bones
        if 'DEF' in bone.name or 'MCH' in bone.name:
            continue

        shape_name = 'WGT_' + armature.name + '_' + bone.name
        found = shape_collection.all_objects.find(shape_name)

        if found != -1:
            override_bone = None
            if bone.name in override_bones:
                override_bone = pose_bones[override_bones[bone.name]]

            assign_custom_shape(bone, shape_collection.all_objects[found], override_bone)


def assign_custom_shape(pose_bone: PoseBone, shape: Object | None, 
                       override_transform: PoseBone = None) -> None:
    """
    Assign a custom shape (widget) to a pose bone.
    
    Args:
        pose_bone: Bone to assign shape to
        shape: Custom shape object
        override_transform: Optional bone to use for shape's transform
    """
    pose_bone.custom_shape = shape
    pose_bone.custom_shape_transform = override_transform


def import_custom_shapes(collection_name: str) -> None:
    """
    Import custom bone shapes from WGTS.blend file.
    
    Imports the widget collection and renames it to match the armature.
    The collection is hidden in the viewport after import.
    
    Args:
        collection_name: Name of the armature to create widgets for
        
    Raises:
        FileNotFoundError: If WGTS.blend file is not found
        RuntimeError: If the WGTS collection fails to load
    """
    blend_path = Path(__file__).with_name("WGTS.blend")
    
    if not blend_path.exists():
        raise FileNotFoundError(f"Widget file not found: {blend_path}")
    
    with bpy.data.libraries.load(str(blend_path), link=False) as (data_from, data_to):
        data_to.collections = ["WGTS"]

    # Link into the scene tree so it's visible
    coll = bpy.data.collections.get("WGTS")
    if not coll:
        raise RuntimeError(f"Failed to load WGTS collection from {blend_path}")
    
    coll.name = "WGTS_" + collection_name  # Rename collection to match armature
    if coll.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(coll)

    for shape in coll.all_objects:
        new_shape_name = 'WGT_' + collection_name + '_'
        shape.name = shape.name.replace('WGT_Armature_', new_shape_name)

    coll.hide_viewport = True
