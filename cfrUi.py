try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import os

ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'icons'))


# ------------------------------------------------------------------ #
# MAIN WINDOW
# ------------------------------------------------------------------ #
class CreateCurveRig(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle("Create Curve for Rigging")
		self.setMinimumSize(500, 400)

		main_layout = QtWidgets.QVBoxLayout(self)

		# ------------------ CREATE CURVE ------------------ #
		create_curve_group = QtWidgets.QGroupBox("Create Curve")
		create_curve_layout = QtWidgets.QGridLayout()
		create_curve_group.setLayout(create_curve_layout)

		self.icon_buttons = {}
		icon_data = {
			"Head": "head.png",
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

		# ------------------ RENAME SECTION ------------------ #
		rename_group = QtWidgets.QGroupBox("Rename")
		rename_group.setObjectName("Rename")
		rename_layout = QtWidgets.QFormLayout(rename_group)

		self.name_line = QtWidgets.QLineEdit()
		self.prefix_line = QtWidgets.QLineEdit()
		self.suffix_line = QtWidgets.QLineEdit()

		rename_layout.addRow("Name:", self.name_line)
		rename_layout.addRow("Prefix:", self.prefix_line)
		rename_layout.addRow("Suffix:", self.suffix_line)

		main_layout.addWidget(rename_group)

		# ------------------ BUTTONS (เหมือน HeadWindow) ------------------ #
		button_layout = QtWidgets.QHBoxLayout()
		self.create_button = QtWidgets.QPushButton("Create")
		self.rename_button = QtWidgets.QPushButton("Rename")
		self.delete_button = QtWidgets.QPushButton("Delete")
		self.cancel_button = QtWidgets.QPushButton("Cancel")
		self.cancel_button.clicked.connect(self.close)

		for btn, color in [
			(self.create_button, "#fe7f2d"),
			(self.rename_button, "#619b8a"),
			(self.delete_button, "#ff4b2e"),
			(self.cancel_button, "#617f92")
		]:
			btn.setStyleSheet(f"background-color: {color}; color: #1D1D33;")
			button_layout.addWidget(btn)

		main_layout.addLayout(button_layout)

		# ------------------ STYLE ------------------ #
		self.setStyleSheet('''
			QGroupBox {
				font-weight: bold;
				color: white;
				border: 1px solid #555;
				border-radius: 5px;
				margin-top: 10px;
			}
			QGroupBox::title {
				subcontrol-origin: margin;
				subcontrol-position: top left;
				padding: 0 5px;
			}
			QPushButton {
				background-color: #444;
				color: white;
				padding: 5px;
			}
			QPushButton:hover {
				background-color: #666;
			}
			QGroupBox#Rename QLineEdit {
				background-color: #fcca46;
				color: #1D1D33;
				border: 1px solid #AAA;
				border-radius: 3px;
			}
			QDialog {
				background-color: #233d4d;
			}
			QLabel {
				color: white;
			}
		''')

	# ------------------------------------------------------------------ #
	# Sub-windows
	def open_head_window(self):
		self.head_window = HeadWindow(self)
		self.head_window.show()

	def open_body_window(self):
		self.body_window = BodyWindow(self)
		self.body_window.show()

	def open_arm_window(self):
		self.arm_window = ArmWindow(self)
		self.arm_window.show()

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

		main_layout = QtWidgets.QVBoxLayout(self)

		# Head icon buttons
		head_group = QtWidgets.QGroupBox("Head")
		head_layout = QtWidgets.QGridLayout(head_group)

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

		# Buttons
		button_layout = QtWidgets.QHBoxLayout()
		self.create_button = QtWidgets.QPushButton("Create")
		self.delete_button = QtWidgets.QPushButton("Delete")
		self.cancel_button = QtWidgets.QPushButton("Cancel")
		self.cancel_button.clicked.connect(self.close)

		for btn, color in [
			(self.create_button, "#fe7f2d"),
			(self.delete_button, "#ff4b2e"),
			(self.cancel_button, "#617f92")
		]:
			btn.setStyleSheet(f"background-color: {color}; color: #1D1D33;")
			button_layout.addWidget(btn)

		main_layout.addLayout(button_layout)

		self.setStyleSheet('''
			QGroupBox {
				font-weight: bold;
				color: white;
				border: 1px solid #555;
				border-radius: 5px;
				margin-top: 10px;
			}
			QGroupBox::title {
				subcontrol-origin: margin;
				subcontrol-position: top left;
				padding: 0 5px;
			}
			QPushButton {
				background-color: #444;
				color: white;
				padding: 5px;
			}
			QPushButton:hover {
				background-color: #666;
			}
			QLabel {
				color: white;
			}
			QDialog {
				background-color: #233d4d;
			}
		''')


# ------------------------------------------------------------------ #
# BODY WINDOW
# ------------------------------------------------------------------ #
class BodyWindow(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("Body Curve Options")
		self.setMinimumSize(500, 400)

		main_layout = QtWidgets.QVBoxLayout(self)

		body_group = QtWidgets.QGroupBox("Body")
		body_layout = QtWidgets.QGridLayout(body_group)

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

		button_layout = QtWidgets.QHBoxLayout()
		self.create_button = QtWidgets.QPushButton("Create")
		self.delete_button = QtWidgets.QPushButton("Delete")
		self.cancel_button = QtWidgets.QPushButton("Cancel")
		self.cancel_button.clicked.connect(self.close)

		for btn, color in [
			(self.create_button, "#fe7f2d"),
			(self.delete_button, "#ff4b2e"),
			(self.cancel_button, "#617f92")
		]:
			btn.setStyleSheet(f"background-color: {color}; color: #1D1D33;")
			button_layout.addWidget(btn)

		main_layout.addLayout(button_layout)

		self.setStyleSheet('''
			QGroupBox {
				font-weight: bold;
				color: white;
				border: 1px solid #555;
				border-radius: 5px;
				margin-top: 10px;
			}
			QGroupBox::title {
				subcontrol-origin: margin;
				subcontrol-position: top left;
				padding: 0 5px;
			}
			QPushButton {
				background-color: #444;
				color: white;
				padding: 5px;
			}
			QPushButton:hover {
				background-color: #666;
			}
			QLabel {
				color: white;
			}
			QDialog {
				background-color: #233d4d;
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

		main_layout = QtWidgets.QVBoxLayout(self)

		# Arm icon buttons
		arm_group = QtWidgets.QGroupBox("Arm")
		arm_layout = QtWidgets.QGridLayout(arm_group)

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

		# Buttons (เหมือน HeadWindow)
		button_layout = QtWidgets.QHBoxLayout()
		self.create_button = QtWidgets.QPushButton("Create")
		self.rename_button = QtWidgets.QPushButton("Rename")
		self.delete_button = QtWidgets.QPushButton("Delete")
		self.cancel_button = QtWidgets.QPushButton("Cancel")
		self.cancel_button.clicked.connect(self.close)

		for btn, color in [
			(self.create_button, "#fe7f2d"),
			(self.rename_button, "#619b8a"),
			(self.delete_button, "#ff4b2e"),
			(self.cancel_button, "#617f92")
		]:
			btn.setStyleSheet(f"background-color: {color}; color: #1D1D33;")
			button_layout.addWidget(btn)

		main_layout.addLayout(button_layout)

		# Style
		self.setStyleSheet('''
			QGroupBox {
				font-weight: bold;
				color: white;
				border: 1px solid #555;
				border-radius: 5px;
				margin-top: 10px;
			}
			QGroupBox::title {
				subcontrol-origin: margin;
				subcontrol-position: top left;
				padding: 0 5px;
			}
			QPushButton {
				background-color: #444;
				color: white;
				padding: 5px;
			}
			QPushButton:hover {
				background-color: #666;
			}
			QLabel {
				color: white;
			}
			QDialog {
				background-color: #233d4d;
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

		main_layout = QtWidgets.QVBoxLayout(self)

		# ------------------ LEG ICON BUTTONS ------------------ #
		reg_group = QtWidgets.QGroupBox("Leg")
		reg_layout = QtWidgets.QGridLayout(reg_group)

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
			if col > 2:  # จัด layout เป็น 3 คอลัมน์
				col = 0
				row += 2

		main_layout.addWidget(reg_group)

		# ------------------ BUTTONS ------------------ #
		button_layout = QtWidgets.QHBoxLayout()
		self.create_button = QtWidgets.QPushButton("Create")
		self.delete_button = QtWidgets.QPushButton("Delete")
		self.cancel_button = QtWidgets.QPushButton("Cancel")
		self.cancel_button.clicked.connect(self.close)

		for btn, color in [
			(self.create_button, "#fe7f2d"),
			(self.delete_button, "#ff4b2e"),
			(self.cancel_button, "#617f92")
		]:
			btn.setStyleSheet(f"background-color: {color}; color: #1D1D33;")
			button_layout.addWidget(btn)

		main_layout.addLayout(button_layout)

		# ------------------ STYLE ------------------ #
		self.setStyleSheet('''
			QGroupBox {
				font-weight: bold;
				color: white;
				border: 1px solid #555;
				border-radius: 5px;
				margin-top: 10px;
			}
			QGroupBox::title {
				subcontrol-origin: margin;
				subcontrol-position: top left;
				padding: 0 5px;
			}
			QPushButton {
				background-color: #444;
				color: white;
				padding: 5px;
			}
			QPushButton:hover {
				background-color: #666;
			}
			QLabel {
				color: white;
			}
			QDialog {
				background-color: #233d4d;
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
