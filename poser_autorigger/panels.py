"""UI panels for the Poser Auto-Rigger add-on."""

import bpy


class RigPoserArmature_PT_Panel(bpy.types.Panel):
    """Main panel for Poser auto-rigging tools."""

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Rig Poser"
    bl_category = "Rig Poser"
    bl_idname = "VIEW3D_PT_RigPoserArmature_PT_Panel"

    def draw(self, context):
        """Draw the panel UI."""
        layout = self.layout
        op_row = layout.row(align=True)
        op_row.scale_y = 1.5

        op_row.operator("poser.generate_base_rig", icon="POSE_HLT")
        
        # Display active object info
        if context.active_object and context.active_object.type == 'ARMATURE':
            layout.label(text=f"Active: {context.active_object.name}")
        else:
            layout.label(text="Select an armature", icon='ERROR')
