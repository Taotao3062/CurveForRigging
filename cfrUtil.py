import maya.cmds as cmds
import os

module_path = os.path.dirname(__file__)
curve_folder = os.path.join(module_path, "curves")


# ------------------------------------------------------------
# UTIL: Import curve file
# ------------------------------------------------------------
def import_curve(file_name):
    import maya.cmds as cmds
    import os

    file_path = os.path.join(curve_folder, file_name)

    if not os.path.exists(file_path):
        cmds.warning(f"[CurveForRigging] Missing curve file: {file_path}")
        return None

    # เก็บรายชื่อ object
    before = set(cmds.ls(tr=True))


    namespace = os.path.splitext(file_name)[0]

    try:
        cmds.file(
            file_path,
            i=True,
            type="mayaAscii",
            ignoreVersion=True,
            ra=True,
            mergeNamespacesOnClash=True,
            namespace=namespace
        )
    except Exception as e:
        cmds.warning(f"[CurveForRigging] ❌ Could not import {file_name}: {e}")
        return None


    after = set(cmds.ls(tr=True))
    new_objs = list(after - before)

    if not new_objs:
        cmds.warning(f"[CurveForRigging] ⚠️ No objects imported{file_name}")
        return None

    print(f"[CurveForRigging] ✅ Imported: {new_objs}")
    return new_objs



def finalize_curve(imported, ctrl_name, color, snap_to=None):
    import maya.cmds as cmds

    if not imported:
        cmds.warning("[CurveForRigging] ❌ No imported curve to snap to joint.")
        return None

    for node in imported:
        if cmds.objectType(node) == "transform":
            new_name = cmds.rename(node, ctrl_name)
            cmds.setAttr(new_name + ".overrideEnabled", 1)
            cmds.setAttr(new_name + ".overrideColor", color)
                #snap loint
            if snap_to and cmds.objExists(snap_to):
                try:
                    snap_target = cmds.ls(snap_to, long=True)[0]  # ✅ ล็อกชื่อเต็มของ joint
                    print(f"[CurveForRigging] 🔄 Snapping {new_name} to {snap_target}")
                    cmds.delete(cmds.pointConstraint(snap_target, new_name))
                    cmds.makeIdentity(new_name, apply=True, t=1, r=0, s=1, n=0)
                except Exception as e:
                    cmds.warning(f"[CurveForRigging] ⚠️ Could not snap to {snap_to}: {e}")

            else:
                print("[CurveForRigging] ℹ️ No joint selected, control created at origin.")

            print(f"[CurveForRigging] ✅ Created {ctrl_name}")
            return new_name





# ------------------------------------------------------------
# HEAD
# ------------------------------------------------------------
HEAD_CURVE_MAP = {
    "Eyes":     ("eyes.ma",      "Eyes_CTRL",     18),
    "Mouth":    ("mouth.ma",     "Mouth_CTRL",    13),
    "Eyebrow":  ("eyebrow.ma",   "Brow_CTRL",      6),
    "Jaw":      ("jaw.ma",       "Jaw_CTRL",      17),
    "Head":     ("head.ma",      "Head_CTRL",     17),
}

def create_head_ctrl(name, snap_to=None):
    if name not in HEAD_CURVE_MAP:
        cmds.warning(f"[CurveForRigging] No head curve for: {name}")
        return

    file_name, ctrl_name, color = HEAD_CURVE_MAP[name]
    return finalize_curve(import_curve(file_name), ctrl_name, color, snap_to)


# ------------------------------------------------------------
# BODY
# ------------------------------------------------------------
BODY_CURVE_MAP = {
    "Root":   ("root.ma",   "Root_CTRL",   17),
    "Pelvis": ("pelvis.ma", "Pelvis_CTRL", 17),
    "Back1":  ("back1.ma",  "Back1_CTRL",  17),
    "Back2":  ("back2.ma",  "Back2_CTRL",  17),
    "Back3":  ("back3.ma",  "Back3_CTRL",  17),
}

def create_body_ctrl(name, snap_to=None):
    if name not in BODY_CURVE_MAP:
        cmds.warning(f"[CurveForRigging] No body curve for: {name}")
        return

    file_name, ctrl_name, color = BODY_CURVE_MAP[name]
    return finalize_curve(import_curve(file_name), ctrl_name, color, snap_to)


# ------------------------------------------------------------
# ARM
# ------------------------------------------------------------
ARM_CURVE_MAP = {
    "Clavicle": ("clavicle.ma", "Clavicle_CTRL", 18),
    "Elbow":    ("elbow.ma",    "Elbow_CTRL",    18),
    "Wrist":    ("wrist.ma",    "Wrist_CTRL",    18),
    "Finger":   ("finger.ma",   "Finger_CTRL",   18),
}

def create_arm_ctrl(name, snap_to=None):
    if name not in ARM_CURVE_MAP:
        cmds.warning(f"[CurveForRigging] No arm curve for: {name}")
        return

    file_name, ctrl_name, color = ARM_CURVE_MAP[name]
    return finalize_curve(import_curve(file_name), ctrl_name, color, snap_to)


# ------------------------------------------------------------
# LEG
# ------------------------------------------------------------
LEG_CURVE_MAP = {
    "Hip":        ("hip.ma",        "Hip_CTRL",        14),
    "Leg Upper":  ("leg_upper.ma",  "LegUpper_CTRL",   14),
    "Knee":       ("knee.ma",       "Knee_CTRL",       14),
    "Leg Lower":  ("leg_lower.ma",  "LegLower_CTRL",   14),
    "Foot":       ("foot.ma",       "Foot_CTRL",       14),
}

def create_leg_ctrl(name, snap_to=None):
    if name not in LEG_CURVE_MAP:
        cmds.warning(f"[CurveForRigging] No leg curve for: {name}")
        return

    file_name, ctrl_name, color = LEG_CURVE_MAP[name]
    return finalize_curve(import_curve(file_name), ctrl_name, color, snap_to)
