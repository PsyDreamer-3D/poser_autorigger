"""Operators for the Poser Auto-Rigger add-on."""

import bpy
from .generate_base_rig import setup_poser_figure


class OT_GenerateBaseRig_Operator(bpy.types.Operator):
    """Generate animation-ready control rig from imported Poser FBX armature."""

    bl_idname = "poser.generate_base_rig"
    bl_label = "Generate Base Rig"
    bl_description = "Generate animation-ready control rig with IK/FK chains, custom shapes, and constraints"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """Check if the operator can be executed."""
        return context.active_object is not None and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        """Execute the rig generation process."""
        try:
            setup_poser_figure(context.active_object)
            self.report({'INFO'}, "Base rig generated successfully")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to generate rig: {str(e)}")
            return {'CANCELLED'}
