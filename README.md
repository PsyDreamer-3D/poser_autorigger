# Poser Autorigger for Blender

**Under development—Use at your own risk**

An autorigger for Poser characters imported as FBX files.

This auto-rigging tool is intended for figures that were exported from Poser as FBX files—which already have an existing base armature. This tool takes that existing armature and automates the setup of IK/FK chains, bone collections, and bone widgets.

This tool also adds a deformer bone to the spine chain called `LowerAbdomen` in order to complete the imported spine chain from Poser. However, it does not create a weight-group. This weight-group will need to be created manually and blended with the hip and abdomen weight-groups. This feature may be removed or moved behind an option flag.

## Motivation

The motivation for creating this tool was to automate a number of tasks I do to a figure that I've imported from Poser. It also standardizes my workflow so I'm not forgetting my naming conventions or collection sets between when working on different figures.

## **Workflow Summary**

1. User imports their FBX Poser character to Blender.
2. Runs auto-rigger script/addon.
3. Addon detects the armature, generates required IK/FK chains, creates controls, and assigns custom shapes.
4. Rig is ready for animation with standard Blender controls.

## TODOs

- [x] Move mesh correction code to [Poser Tools](https://github.com/jesgs/poser-tools)
- [ ] **FEATURE**: Add option for Rig UI panel but still provide support for [Bone Manager](https://fin.gumroad.com/l/STdb) and [Rig UI](https://superhivemarket.com/products/rig-ui)
- [ ] **FEATURE**: Add support for other Poser figures. At the moment, this add-on only supports the base Daz3D Millennium 3 figures.
- [ ] Test against other Poser figures (Daz3d Millennium 4 figures, La Femme and Le Homme, AnimeDoll, etc.)
  - [ ] **BUG**: Fails with La Femme and Le Homme due to extra different naming conventions for toe bone, plus extra toe bones and a facial rig that's already present.
- [ ] Bring code in line with [Blender guidelines](https://developer.blender.org/docs/features/extensions/moderation/guidelines/)
- [ ] Consider merging [Poser Tools](https://github.com/jesgs/poser-tools) with this add-on.
- [ ] **FEATURE**: Move process for creating lower abdomen bone to an option
- [ ] **FEATURE**: Add option for creating pelvis bones
- [ ] **FEATURE**: Add base face rig, which will need to be adjusted by the user to fit the character.
  - [ ] Automate creation of inner mouth rig.
    - [ ] Generate deformer, MCH and control bones for upper and lower teeth.
    - [ ] Generate deformer, MCH and control bones for jaw.
  - [ ] Automate creation of tongue rig
    - [ ] IK/FK switching
    - [ ] Spline IK chain

## Ideas
Below are some ideas that could be handled by user before the control rig is generated. Rig generation process would automatically detect these bones and add controls as needed. 
The process to create the `LowerAbdomen` bone and reposition the `Body` bone and rename it `root` could also be optionally left to the user.
- [ ] Add option to modify hip/buttock bones into a full pelvis setup. This process should run before bones are renamed, similar to how LowerAbdomen is created.
  - `Left_Buttock` and `Right_Buttock` are renamed to `Left_Hip` and `Right_Hip`. The tail of each bone should be aligned to their respective heads
  - Create `Left_Pelvis` and parent it to the main `Hip` bone. Position the head of each bone to align with the head of the `Hip` bone
    - Align x-axis of the tail of `Left_Pelvis` with the head of `Left_Hip` (`Left_Hip` head.x - ~0.0096)
    - Align y-axis of the tail of `Left_Pelvis` with the head of `Left_Hip` (`Left_Hip` head.y + ~-0.0474)
    - Align z-axis of the tail of `Left_Pelvis` with the head of `Left_Hip` (`Left_Hip` head.z + ~0.052)
  - Create `Left_Buttock` and parent it to `Left_Pelvis`. Head of `Left_Buttock` should be aligned with tail of `Left_Pelvis`. Position tail of `Left_Buttock`:
    - `Left_Buttock` tail.x = `Left_Pelvis` head.x - 0.035
    - `Left_Buttock` tail.y = `Left_Pelvis` head.y + -0.16
    - `Left_Buttock` tail.z = `Left_Pelvix` head.z - 0.0603
- [ ] Add option to create breast/pectoral deforming bones.

## Base Feature Set for Poser FBX Auto-Rigger in Blender

### 1. IK/FK Chain Creation
- **Limbs (Arms & Legs):**
  - [x] Detect existing limb bones (shoulder, upper arm, forearm, hand, thigh, shin, foot).
  - [x] Generate IK chains for arms and legs.
  - [x] Generate FK chains for arms and legs.
  
- **Fingers:**
  - [x] Detect finger bones.
  - [x] Create FK controls for each finger.
  - [x] Add IK controls for each finger, including thumb.

- **Spine:**
  - [x] Detect spine bones.
  - [x] Create FK controls along the spine.
  - [x] Create IK controls along the spine.
  - [ ] Change deformer bones to full bendy-bones.

### 2. Foot Roll Control
- **Foot Rig Features:**
  - [x] Add foot roll controller.
  - [ ] Setup constraints for toe bend, heel lift, ball roll, etc.
  - [ ] Automatic foot banking (side-to-side roll).

### 3. Constraints Setup
- **Rig Constraints:**
  - [x] Add necessary constraints for all IK and FK chains.
  - [x] Ensure pole targets are generated and positioned correctly for knees/elbows.
  - [x] Setup drivers or custom properties for easy switching and control.
  - [ ] Limit Rotation constraints for bones that need them

### 4. Control Custom-Shapes
- **Custom Bone Shapes:**
  - [x] Assign custom shapes to each main control (IK handles, FK controls, foot roll, pole targets).

### 5. User Interface (Optional, but recommended for usability)
- **Rig UI Panel:**
  - [ ] Add a custom sidebar panel in Blender for rig controls (IK/FK switch, foot roll parameters, etc.).
  - [ ] Buttons for common actions (zero pose, snap FK to IK, etc.).
  - [ ] Panel to control figure's "non-driven" shapekeys.

### 6. Error Checking and Reporting
- **Validation:**
  - [ ] Check for missing bones or naming conventions (warn if not standard).
  - [ ] Warn if FBX armature isn’t compatible (missing limbs, etc.).

## Development

### Code Quality

This project uses several tools to maintain code quality:

- **Ruff**: Fast Python linter and formatter
- **Type Hints**: Type annotations for better code clarity
- **Docstrings**: Comprehensive documentation for all functions

### Setting Up Development Environment

```bash
# Install development dependencies
pip install ruff

# Run linter
ruff check .

# Format code
ruff format .
```

### Code Style Guidelines

- Follow PEP 8 style guidelines with 120 character line limit
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Use constants from `constants.py` instead of magic numbers

### Bone Naming Conventions

The add-on uses consistent naming prefixes:
- `DEF-`: Deform bones (affect mesh)
- `IK-`: IK chain bones
- `FK-`: FK chain bones
- `CTRL-`: Control bones (visible to animators)
- `MCH-`: Mechanism bones (helper bones)

Suffixes indicate side:
- `.L`: Left side
- `.R`: Right side
- No suffix: Center/spine bones

### Required Bones

For proper rig generation, the imported FBX must contain these bones:
- `Body` (renamed to `root`)
- `Hip`
- `Chest`
- `Head`
- `Neck`

### Testing

Currently, this add-on requires manual testing in Blender. To test:

1. Open Blender
2. Install the add-on as a development extension
3. Import a Poser FBX character
4. Select the armature
5. Run the "Generate Base Rig" operator from the Rig Poser panel

### Contributing

Contributions are welcome! Please:

1. Follow the code style guidelines
2. Add docstrings to new functions
3. Update constants.py for any new magic values
4. Test changes with a Poser FBX import
5. Update documentation as needed

