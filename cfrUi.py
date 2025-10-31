try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import os, sys

module_path = os.path.dirname(__file__)
if module_path not in sys.path:
    sys.path.append(module_path)

from cfrUtil import create_head_ctrl, create_body_ctrl, create_arm_ctrl, create_leg_ctrl

ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'icons'))

# ------------------------------------------------------------------ #
# MAIN WINDOW
# ------------------------------------------------------------------ #
class CreateCurveRig(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Curve for Rigging")
        self.setMinimumSize(520, 450)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(20)  #เว้น
        main_layout.setContentsMargins(15, 15, 15, 15)

        # ------------------ CREATE CURVE ------------------ #
        create_curve_group = QtWidgets.QGroupBox("Create Curve")
        create_curve_layout = QtWidgets.QGridLayout()
        create_curve_layout.setHorizontalSpacing(25)
        create_curve_layout.setVerticalSpacing(15)
        create_curve_group.setLayout(create_curve_layout)

        self.icon_buttons = {}
        icon_data = {
            "Head": "head1.png",
            "Body": "body.png",
            "Arm": "arm.png",
            "Leg": "reg.png"
        }

        row, col = 0, 0
        for label, icon_file in icon_data.items():
            btn = QtWidgets.QPushButton()
            btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, icon_file)))
            btn.setIconSize(QtCore.QSize(64, 64))
            btn.setFixedSize(80, 80)
            btn.setToolTip(label)
            btn.setCheckable(True)

            #ชื่อบนปุ่มล่าง
            create_curve_layout.addWidget(QtWidgets.QLabel(label), row, col, alignment=QtCore.Qt.AlignCenter)
            create_curve_layout.addWidget(btn, row + 1, col, alignment=QtCore.Qt.AlignCenter)
            self.icon_buttons[label] = btn

            # Connect buttons
            if label == "Head":
                btn.clicked.connect(self.open_head_window)
            elif label == "Body":
                btn.clicked.connect(self.open_body_window)
            elif label == "Arm":
                btn.clicked.connect(self.open_arm_window)
            elif label == "Leg":
                btn.clicked.connect(self.open_reg_window)

            col += 1
            if col > 3:
                col = 0
                row += 2

        main_layout.addWidget(create_curve_group)

        # ------------------ RENAME ------------------ #

        rename_group = QtWidgets.QGroupBox("Rename")
        rename_group.setObjectName("Rename")
        rename_layout = QtWidgets.QFormLayout(rename_group)
        rename_layout.setVerticalSpacing(12)
        rename_layout.setContentsMargins(15, 25, 15, 15)

        self.name_line = QtWidgets.QLineEdit()
        self.prefix_line = QtWidgets.QLineEdit()
        self.suffix_line = QtWidgets.QLineEdit()

        rename_layout.addRow("Name:", self.name_line)
        rename_layout.addRow("Prefix:", self.prefix_line)
        rename_layout.addRow("Suffix:", self.suffix_line)

        main_layout.addWidget(rename_group)

        # ------------------ BUTTONS ------------------ #
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(10, 5, 10, 5)

        self.rename_button = QtWidgets.QPushButton("Rename")
        self.rename_button.clicked.connect(self.rename_selected)
        self.delete_button = QtWidgets.QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_selected)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        for btn, color in [
            (self.rename_button, "#619b8a"),
            (self.delete_button, "#ff4b2e"),
            (self.cancel_button, "#fe7f2d")
        ]:
            btn.setStyleSheet(f"""
                background-color: {color};
                color: #1D1D33;
                font-weight: bold;
                font-size: 11pt;
                padding: 8px 16px;
                border-radius: 6px;
            """)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)


        # ------------------ STYLE ------------------ #
        self.setStyleSheet('''
            QGroupBox {
                font-weight: bold;
                font-size: 14pt;
                font-family: Papyrus;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
            }
            QPushButton {
                background-color: #233d4d;
                border-radius: 10px;  
                color: white;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #fcca46;
            }
            QGroupBox#Rename QLineEdit {
                background-color: #fcca46;
                color: #1D1D33;
                font-size: 11pt;
                border: 1px solid #AAA;
                border-radius: 3px;
                padding: 3px;
            }
            QDialog {
                background-color: #233d4d;
            }
            QLabel {
                color: white;
                font-size: 11pt;
            }
        ''')
#######snap joint
    def create_with_snap(self, util_function, ctrl_name):
        import maya.cmds as cmds
        sel = cmds.ls(selection=True)

        if not sel:
            cmds.warning("[CurveForRigging] ⚠️ Please select a joint to snap the control.")
            return

        joint = sel[0]
        if cmds.objectType(joint) != "joint":
            cmds.warning(f"[CurveForRigging] ⚠️ Selected object '{joint}' is not a joint.")
            return

        util_function(ctrl_name, snap_to=joint)
#######rename
    def rename_selected(self):
        import maya.cmds as cmds
        
        sel = cmds.ls(selection=True)
        if not sel:
            cmds.warning("[CurveForRigging] ⚠️ No object selected to rename.")
            return

        base_name = self.name_line.text().strip()
        prefix = self.prefix_line.text().strip()
        suffix = self.suffix_line.text().strip()

        if not base_name:
            cmds.warning("[CurveForRigging] ⚠️ Please enter a name.")
            return

        for i, obj in enumerate(sel):
            new_name = f"{prefix}{base_name}{suffix}"
            renamed = cmds.rename(obj, new_name)
            print(f"[CurveForRigging] ✅ Renamed: {obj} ➝ {renamed}")
#######delete
    def delete_selected(self):
        import maya.cmds as cmds
        sel = cmds.ls(selection=True)

        if not sel:
            cmds.warning("[CurveForRigging] ⚠️ No object selected to delete.")
            return

        for obj in sel:
            try:
                cmds.delete(obj)
                print(f"[CurveForRigging] 🗑️ Deleted: {obj}")
            except Exception as e:
                cmds.warning(f"[CurveForRigging] ❌ Could not delete {obj}: {e}")

    # ------------------------------------------------------------------ #
    # Sub-windows
    def connect_buttons(self, window, util_function):
        for child in window.findChildren(QtWidgets.QPushButton):
            label = child.toolTip()
            child.setCheckable(False)
            child.clicked.connect(lambda checked=False, n=label: self.create_with_snap(util_function, n))
#

    def open_head_window(self):
        self.head_window = HeadWindow(self)
        self.head_window.show()
#
    def open_body_window(self):
        self.body_window = BodyWindow(self)
        self.body_window.show()
#
    def open_arm_window(self):
        self.arm_window = ArmWindow(self)
        self.arm_window.show()
#
    def open_reg_window(self):
        self.reg_window = RegWindow(self)
        self.reg_window.show()

# ------------------------------------------------------------------ #
# HEAD WINDOW
# ------------------------------------------------------------------ #
class HeadWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Head Curve Options")
        self.setMinimumSize(500, 400)

        # ------------------ MAIN LAYOUT ------------------ #
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # ------------------ HEAD ICON ------------------ #
        head_group = QtWidgets.QGroupBox("Head")
        head_layout = QtWidgets.QGridLayout()
        head_layout.setHorizontalSpacing(25)
        head_layout.setVerticalSpacing(15)
        head_group.setLayout(head_layout)

        icon_data = {
            "Eyes": "eyes.png",
            "Mouth": "mouth.png",
            "Eyebrow": "eyebrow.png",
            "Jaw": "jaw.png",
            "Head": "head.png"
        }

        row, col = 0, 0
        for label, icon_file in icon_data.items():
            btn = QtWidgets.QPushButton()
            btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, icon_file)))
            btn.setIconSize(QtCore.QSize(64, 64))
            btn.setFixedSize(80, 80)
            btn.setToolTip(label)
            btn.setCheckable(True)

            head_layout.addWidget(QtWidgets.QLabel(label), row, col, alignment=QtCore.Qt.AlignCenter)
            head_layout.addWidget(btn, row + 1, col, alignment=QtCore.Qt.AlignCenter)

            col += 1
            if col > 2:
                col = 0
                row += 2

        main_layout.addWidget(head_group)
        self.parent().connect_buttons(self, create_head_ctrl)

        # ------------------ CONTROL BUTTONS ------------------ #
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(10, 5, 10, 5)

        self.delete_button = QtWidgets.QPushButton("Delete")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        for btn, color in [
            (self.delete_button, "#ff4b2e"),
            (self.cancel_button, "#fe7f2d")
        ]:
            btn.setStyleSheet(f"""
                background-color: {color};
                color: #1D1D33;
                font-weight: bold;
                font-size: 11pt;
                padding: 8px 16px;
                border-radius: 6px;
            """)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)

        # ------------------ STYLE ------------------ #
        self.setStyleSheet('''
            QGroupBox {
                font-weight: bold;
                font-size: 14pt;
                font-family: Papyrus;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
            }
            QPushButton {
                background-color: #233d4d;
                color: white;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #fcca46;
            }
            QDialog {
                background-color: #233d4d;
            }
            QLabel {
                color: white;
                font-size: 11pt;
            }
        ''')





class BodyWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Body Curve Options")
        self.setMinimumSize(500, 400)

        # ------------------ MAIN LAYOUT ------------------ #
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # ------------------ ICON ------------------ #
        body_group = QtWidgets.QGroupBox("Body")
        body_layout = QtWidgets.QGridLayout()
        body_layout.setHorizontalSpacing(25)
        body_layout.setVerticalSpacing(15)
        body_group.setLayout(body_layout)

        icon_data = {
            "Root": "root.png",
            "Pelvis": "pelvis.png",
            "Back1": "back1.png",
            "Back2": "back2.png",
            "Back3": "back3.png"
        }

        row, col = 0, 0
        for label, icon_file in icon_data.items():
            btn = QtWidgets.QPushButton()
            btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, icon_file)))
            btn.setIconSize(QtCore.QSize(64, 64))
            btn.setFixedSize(80, 80)
            btn.setToolTip(label)
            btn.setCheckable(True)

            body_layout.addWidget(QtWidgets.QLabel(label), row, col, alignment=QtCore.Qt.AlignCenter)
            body_layout.addWidget(btn, row + 1, col, alignment=QtCore.Qt.AlignCenter)
            col += 1
            if col > 2:
                col = 0
                row += 2

        main_layout.addWidget(body_group)

        # ------------------ CONTROL BUTTONS ------------------ #
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(10, 5, 10, 5)

        self.delete_button = QtWidgets.QPushButton("Delete")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        for btn, color in [
            (self.delete_button, "#ff4b2e"),
            (self.cancel_button, "#fe7f2d")
        ]:
            btn.setStyleSheet(f"""
                background-color: {color}; 
                color: #1D1D33;
                font-weight: bold;
                font-size: 11pt;
                padding: 8px 16px;
                border-radius: 6px;
            """)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)
        self.parent().connect_buttons(self, create_body_ctrl)

        # ------------------ STYLE ------------------ #
        self.setStyleSheet('''
            QGroupBox {
                font-weight: bold;
                font-size: 14pt;
                font-family: Papyrus;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
            }
            QPushButton {
                background-color: #233d4d;
                color: white;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #fcca46;
            }
            QDialog {
                background-color: #233d4d;
            }
            QLabel {
                color: white;
                font-size: 11pt;
            }
        ''')

# ------------------------------------------------------------------ #
# ARM WINDOW
# ------------------------------------------------------------------ #
class ArmWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Arm Curve Options")
        self.setMinimumSize(500, 400)

        # ------------------ MAIN LAYOUT ------------------ #
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # ------------------ ICON ------------------ #
        arm_group = QtWidgets.QGroupBox("Arm")
        arm_layout = QtWidgets.QGridLayout()
        arm_layout.setHorizontalSpacing(25)
        arm_layout.setVerticalSpacing(15)
        arm_group.setLayout(arm_layout)

        icon_data = {
            "Clavicle": "clavicle.png",
            "Elbow": "elbow.png",
            "Wrist": "wrist.png",
            "Finger": "finger.png"
        }

        row, col = 0, 0
        for label, icon_file in icon_data.items():
            btn = QtWidgets.QPushButton()
            btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, icon_file)))
            btn.setIconSize(QtCore.QSize(64, 64))
            btn.setFixedSize(80, 80)
            btn.setToolTip(label)
            btn.setCheckable(True)

            arm_layout.addWidget(QtWidgets.QLabel(label), row, col, alignment=QtCore.Qt.AlignCenter)
            arm_layout.addWidget(btn, row + 1, col, alignment=QtCore.Qt.AlignCenter)

            col += 1
            if col > 2:
                col = 0
                row += 2

        main_layout.addWidget(arm_group)

        # ------------------ CONTROL BUTTONS ------------------ #
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(10, 5, 10, 5)

        self.delete_button = QtWidgets.QPushButton("Delete")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        for btn, color in [
            (self.delete_button, "#ff4b2e"),
            (self.cancel_button, "#fe7f2d")
        ]:
            btn.setStyleSheet(f"""
                background-color: {color}; 
                color: #1D1D33;
                font-weight: bold;
                font-size: 11pt;
                padding: 8px 16px;
                border-radius: 6px;
            """)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)
        self.parent().connect_buttons(self, create_arm_ctrl)

        # ------------------ STYLE ------------------ #
        self.setStyleSheet('''
            QGroupBox {
                font-weight: bold;
                font-size: 14pt;
                font-family: Papyrus;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
            }
            QPushButton {
                background-color: #233d4d;
                color: white;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #fcca46;
            }
            QDialog {
                background-color: #233d4d;
            }
            QLabel {
                color: white;
                font-size: 11pt;
            }
        ''')


# ------------------------------------------------------------------ #
# REG WINDOW
# ------------------------------------------------------------------ #
class RegWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Leg Curve Options")
        self.setMinimumSize(500, 400)

        # ------------------ MAIN LAYOUT ------------------ #
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # ------------------ ICON ------------------ #
        reg_group = QtWidgets.QGroupBox("Leg")
        reg_layout = QtWidgets.QGridLayout()
        reg_layout.setHorizontalSpacing(25)
        reg_layout.setVerticalSpacing(15)
        reg_group.setLayout(reg_layout)

        icon_data = {
            "Hip": "hip.png",
            "Leg Upper": "leg_upper.png",
            "Knee": "knee.png",
            "Leg Lower": "leg_lower.png",
            "Foot": "foot.png"
        }

        row, col = 0, 0
        for label, icon_file in icon_data.items():
            btn = QtWidgets.QPushButton()
            btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, icon_file)))
            btn.setIconSize(QtCore.QSize(64, 64))
            btn.setFixedSize(80, 80)
            btn.setToolTip(label)
            btn.setCheckable(True)

            reg_layout.addWidget(QtWidgets.QLabel(label), row, col, alignment=QtCore.Qt.AlignCenter)
            reg_layout.addWidget(btn, row + 1, col, alignment=QtCore.Qt.AlignCenter)

            col += 1
            if col > 2: 
                col = 0
                row += 2

        main_layout.addWidget(reg_group)

        # ------------------ CONTROL BUTTONS ------------------ #
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(10, 5, 10, 5)

        self.delete_button = QtWidgets.QPushButton("Delete")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        for btn, color in [
            (self.delete_button, "#ff4b2e"),
            (self.cancel_button, "#fe7f2d")
        ]:
            btn.setStyleSheet(f"""
                background-color: {color}; 
                color: #1D1D33;
                font-weight: bold;
                font-size: 11pt;
                padding: 8px 16px;
                border-radius: 6px;
            """)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)
        self.parent().connect_buttons(self, create_leg_ctrl)

        # ------------------ STYLE ------------------ #
        self.setStyleSheet('''
            QGroupBox {
                font-weight: bold;
                font-size: 14pt;
                font-family: Papyrus;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
            }
            QPushButton {
                background-color: #233d4d;
                color: white;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #fcca46;
            }
            QDialog {
                background-color: #233d4d;
            }
            QLabel {
                color: white;
                font-size: 11pt;
            }
        ''')

# ------------------------------------------------------------------ #
# RUN FUNCTION FOR MAYA
# ------------------------------------------------------------------ #
def run():
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = CreateCurveRig(parent=ptr)
    ui.show()
