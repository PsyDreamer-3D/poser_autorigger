"""Constants and configuration for the Poser Auto-Rigger add-on."""

# Bone size constants
BONE_SIZE_DEF = 0.001
BONE_SIZE_IK = 0.004
BONE_SIZE_FK = 0.002
BONE_SIZE_CTRL = 0.01
BONE_SIZE_POLE = 0.002

# Bone naming prefixes
PREFIX_DEF = 'DEF-'
PREFIX_IK = 'IK-'
PREFIX_FK = 'FK-'
PREFIX_CTRL = 'CTRL-'
PREFIX_MCH = 'MCH-'

# Special bone names
BONE_ROOT = 'root'
BONE_PROPERTIES = 'PROPERTIES'
BONE_BODY = 'Body'
BONE_HIP = 'Hip'
BONE_LOWER_ABDOMEN = 'LowerAbdomen'

# Suffixes
SUFFIX_LEFT = '.L'
SUFFIX_RIGHT = '.R'

# Collection names
COLLECTION_ROOT = 'Root'
COLLECTION_FACE = 'Face'
COLLECTION_EYES_CTRL = 'Eyes CTRL'
COLLECTION_BODY = 'Body'
COLLECTION_SPINE = 'Spine'
COLLECTION_SPINE_IK = 'Spine IK'
COLLECTION_SPINE_FK = 'Spine FK'
COLLECTION_SPINE_CTRL = 'Spine CTRL'
COLLECTION_LEGS = 'Legs'
COLLECTION_LEGS_IK = 'Legs IK'
COLLECTION_LEGS_FK = 'Legs FK'
COLLECTION_LEGS_CTRL = 'Legs CTRL'
COLLECTION_ARMS = 'Arms'
COLLECTION_ARMS_IK = 'Arms IK'
COLLECTION_ARMS_FK = 'Arms FK'
COLLECTION_ARMS_CTRL = 'Arms CTRL'
COLLECTION_FINGERS = 'Fingers'
COLLECTION_FINGERS_IK = 'Fingers IK'
COLLECTION_FINGERS_FK = 'Fingers FK'
COLLECTION_FINGERS_IK_CTRL = 'Fingers IK CTRL'
COLLECTION_FINGERS_FK_CTRL = 'Fingers FK CTRL'
COLLECTION_RIGGING = 'Rigging'
COLLECTION_DEF = 'DEF'
COLLECTION_MCH = 'MCH'

# Finger bone chains
FINGER_THUMB_CHAIN = ['Thumb_1', 'Thumb_2', 'Thumb_3']
FINGER_INDEX_CHAIN = ['Index_1', 'Index_2', 'Index_3']
FINGER_MID_CHAIN = ['Mid_1', 'Mid_2', 'Mid_3']
FINGER_RING_CHAIN = ['Ring_1', 'Ring_2', 'Ring_3']
FINGER_PINKY_CHAIN = ['Pinky_1', 'Pinky_2', 'Pinky_3']
FINGER_NAMES = ['Thumb', 'Index', 'Mid', 'Ring', 'Pinky']

# Limb bone chains
LEG_CHAIN = ['Buttock', 'Thigh', 'Shin', 'Foot', 'Toe']
ARM_CHAIN = ['Collar', 'Shoulder', 'Forearm', 'Hand']
SPINE_CHAIN = ['Hip', 'LowerAbdomen', 'Abdomen', 'Chest', 'Neck', 'Head']

# Positioning constants
POLE_Y_OFFSET = 0.625
POLE_LENGTH = 0.125
FINGER_CTRL_LENGTH = 0.025
FINGER_CTRL_SIZE_MULTIPLIER = 3
EYE_TARGET_DISTANCE = 0.25
EYE_BONE_EXTENSION = 0.1  # Extension for eye bones forward for better control
TOE_BONE_EXTENSION = 0.1  # Extension for toe bones forward for foot roll

# Constraint influence defaults
DEFAULT_INFLUENCE = 1.0
ZERO_INFLUENCE = 0.0

# Property names for FK/IK switching
PROP_ARMS_FKIK = 'arms_fkik'
PROP_LEGS_FKIK = 'legs_fkik'
PROP_SPINE_FKIK = 'spine_fkik'
PROP_FINGERS_FKIK_LEFT = 'fingers_fkik_l'
PROP_FINGERS_FKIK_RIGHT = 'fingers_fkik_r'
PROP_HEAD_TRACKING = 'head_tracking'
PROP_COLLAR_TRACKING = 'collar_tracking_speed_multiplier'

# FK/IK switch defaults
FKIK_DEFAULT = 1.0
FKIK_MIN = 0.0
FKIK_MAX = 1.0

# Rotation mode
ROTATION_MODE_XYZ = 'XYZ'

# Transform orientation and pivot
ORIENTATION_NORMAL = 'NORMAL'
ORIENTATION_GLOBAL = 'GLOBAL'
PIVOT_INDIVIDUAL = 'INDIVIDUAL_ORIGINS'
PIVOT_MEDIAN = 'MEDIAN_POINT'
