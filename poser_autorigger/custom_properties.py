"""Custom properties setup for rig controls."""

import bpy
from .constants import (
    PROP_HEAD_TRACKING, PROP_COLLAR_TRACKING, PROP_ARMS_FKIK, PROP_LEGS_FKIK,
    PROP_SPINE_FKIK, PROP_FINGERS_FKIK_LEFT, PROP_FINGERS_FKIK_RIGHT,
    FKIK_DEFAULT, FKIK_MIN, FKIK_MAX
)


def create_custom_properties() -> None:
    """
    Create custom properties on the PROPERTIES bone for rig controls.
    
    Sets up FK/IK switching properties and other control parameters.
    Properties are library-overridable for linking across files.
    """
    properties_bone = bpy.context.object.pose.bones['PROPERTIES']

    # Tracking properties
    properties_bone[PROP_HEAD_TRACKING] = False
    properties_bone[PROP_COLLAR_TRACKING] = 0.05

    # FK/IK switching properties (1.0 = FK, 0.0 = IK)
    properties_bone[PROP_ARMS_FKIK] = [FKIK_DEFAULT, FKIK_DEFAULT]
    properties_bone[PROP_LEGS_FKIK] = [FKIK_DEFAULT, FKIK_DEFAULT]
    properties_bone[PROP_SPINE_FKIK] = FKIK_DEFAULT
    properties_bone[PROP_FINGERS_FKIK_LEFT] = [FKIK_DEFAULT] * 5
    properties_bone[PROP_FINGERS_FKIK_RIGHT] = [FKIK_DEFAULT] * 5

    # Configure property UI settings
    _setup_property_ui(properties_bone, PROP_HEAD_TRACKING)
    _setup_property_ui(properties_bone, PROP_COLLAR_TRACKING, min_val=FKIK_MIN, max_val=FKIK_MAX)
    _setup_property_ui(properties_bone, PROP_ARMS_FKIK, min_val=FKIK_MIN, max_val=FKIK_MAX)
    _setup_property_ui(properties_bone, PROP_LEGS_FKIK, min_val=FKIK_MIN, max_val=FKIK_MAX)
    _setup_property_ui(properties_bone, PROP_SPINE_FKIK, min_val=FKIK_MIN, max_val=FKIK_MAX)
    _setup_property_ui(properties_bone, PROP_FINGERS_FKIK_LEFT, min_val=FKIK_MIN, max_val=FKIK_MAX)
    _setup_property_ui(properties_bone, PROP_FINGERS_FKIK_RIGHT, min_val=FKIK_MIN, max_val=FKIK_MAX)


def _setup_property_ui(properties_bone, prop_name: str, min_val: float = None, max_val: float = None) -> None:
    """
    Configure UI settings for a custom property.
    
    Args:
        properties_bone: Bone containing the property
        prop_name: Name of the property
        min_val: Minimum value (optional)
        max_val: Maximum value (optional)
    """
    properties_bone.property_overridable_library_set(f'["{prop_name}"]', True)
    ui = properties_bone.id_properties_ui(prop_name)
    
    if min_val is not None and max_val is not None:
        ui.update(min=min_val, max=max_val)
