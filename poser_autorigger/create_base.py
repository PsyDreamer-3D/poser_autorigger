"""Functions for creating base rig bones (root and properties)."""

import bpy
from bpy.types import EditBone
from .helpers import create_bone


def create_properties_bone() -> EditBone:
    """
    Create the PROPERTIES bone for storing custom rig properties.
    
    This bone holds FK/IK switches and other control properties.
    
    Returns:
        The created PROPERTIES EditBone
    """
    edit_bones = bpy.context.object.data.edit_bones
    collection = bpy.context.object.data.collections_all.get('Root')
    return create_bone(
        edit_bones=edit_bones,
        name='PROPERTIES',
        bbone_size=0.01,
        head=[0, 0, 0],
        tail=[0, 0.25, 0],
        use_deform=False,
        palette='THEME03',
        collection=collection,
        parent=edit_bones['root']
    )


def create_root() -> None:
    """
    Create the root bone by repurposing the Poser 'Body' bone.
    
    The Body bone from Poser FBX is renamed to 'root' and repositioned
    at the origin to serve as the main parent for the rig hierarchy.
    """
    collection = bpy.context.object.data.collections_all.get('Root')
    edit_bones = bpy.context.object.data.edit_bones
    
    # Rename Body to root, disconnect, and position at origin
    edit_bones['Hip'].use_connect = False
    edit_bones['Body'].use_deform = False
    edit_bones['Body'].head = [0, 0, 0]
    edit_bones['Body'].tail = [0, 0.5, 0]
    edit_bones['Body'].color.palette = 'THEME09'
    edit_bones['Body'].name = 'root'
    collection.assign(edit_bones['root'])