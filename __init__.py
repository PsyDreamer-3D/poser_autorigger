# START — workflow remove
_needs_reload = "bpy" in locals()
# END — workflow remove

import bpy
from .panels import RigPoserArmature_PT_Panel
from .operators import OT_GenerateBaseRig_Operator

# START — workflow remove
if _needs_reload:
    import sys, importlib
    from .panels import RigPoserArmature_PT_Panel
    from .operators import OT_GenerateBaseRig_Operator

    all_modules = sys.modules
    all_modules = dict(sorted(all_modules.items(), key=lambda x: x[0]))  # sort them
    # reload modules
    for k, v in all_modules.items():
        if k.startswith(__name__):
            importlib.reload(v)
# END — workflow remove


bl_info = {
    "name": "Poser Rigger",
    "author": "Jess Green",
    "version": (0, 1, 0),
    "blender": (4, 5, 3),
    "location": "View3D",
    "category": "Object",
}


classes = [RigPoserArmature_PT_Panel, OT_GenerateBaseRig_Operator]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
