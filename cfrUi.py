try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import os

ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'icons'))


class CreateCurveRig(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle("Create Curve for Rigging")
		self.setMinimumSize(500, 400)

		self.main_layout = QtWidgets.QVBoxLayout(self)

		# ------------------------------------------------------------------ #
		# Create Curve
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
			create_curve_layout.addWidget(btn, row + 1, col)
			self.icon_buttons[label] = btn

			# เชื่อมปุ่ม
			if label == "Head":
				btn.clicked.connect(self.open_head_window)
			if label == "Body":
				btn.clicked.connect(self.open_body_window)

			col += 1

		self.main_layout.addWidget(create_curve_group)

		# ------------------------------------------------------------------ #
		# Rename
		rename_group = QtWidgets.QGroupBox("Rename")
		rename_group.setObjectName("Rename")
		rename_layout = QtWidgets.QFormLayout()
		rename_group.setLayout(rename_layout)

		self.name_line = QtWidgets.QLineEdit()
		self.prefix_line = QtWidgets.QLineEdit()
		self.suffix_line = QtWidgets.QLineEdit()

		rename_layout.addRow("Name:", self.name_line)
		rename_layout.addRow("Prefix:", self.prefix_line)
		rename_layout.addRow("Suffix:", self.suffix_line)

		self.main_layout.addWidget(rename_group)

		# ------------------------------------------------------------------ #
		# Buttons
		button_layout = QtWidgets.QHBoxLayout()
		self.create_button = QtWidgets.QPushButton("Create")
		self.rename_button = QtWidgets.QPushButton("Rename")
		self.delete_button = QtWidgets.QPushButton("Delete")
		self.cancel_button = QtWidgets.QPushButton("Cancel")

		self.cancel_button.clicked.connect(self.close)

		button_layout.addStretch()
		button_layout.addWidget(self.create_button)
		self.create_button.setStyleSheet('''
			QPushButton {
				background-color: #fe7f2d;
				color: #1D1D33;
			}
		''')
		button_layout.addWidget(self.rename_button)
		self.rename_button.setStyleSheet('''
			QPushButton {
				background-color: #619b8a;
				color: #1D1D33;
			}
		''')
		button_layout.addWidget(self.delete_button)
		self.delete_button.setStyleSheet('''
			QPushButton {
				background-color: #ff4b2e;
				color: #1D1D33;
			}
		''')
		button_layout.addWidget(self.cancel_button)
		self.cancel_button.setStyleSheet('''
			QPushButton {
				background-color: #617f92;
				color: #1D1D33;
			}
		''')

		self.main_layout.addLayout(button_layout)

		# ------------------------------------------------------------------ #
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
			/* เปลี่ยนสี QLineEdit ใน Rename group เท่านั้น */
			QGroupBox#Rename QLineEdit {
				background-color: #fcca46;
				color: #FFFFFF;
				border: 1px solid #AAA;
				border-radius: 3px;
			}
			QDialog {
				background-color: #233d4d;
			}
		''')

	# ------------------------------------------------------------------ #
	# เปิดหน้าต่างใหม่
	def open_head_window(self):
		self.head_window = HeadWindow(self)
		self.head_window.show()

	def open_body_window(self):
		self.body_window = BodyWindow(self)
		self.body_window.show()


class HeadWindow(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("Head Options")
		self.setMinimumSize(500, 400)
		layout = QtWidgets.QVBoxLayout(self)

# ------------------------------------------------------------------ #
		# Create Curve
		head_curve_group = QtWidgets.QGroupBox("Head Curve")
		head_curve_layout = QtWidgets.QGridLayout()
		head_curve_group.setLayout(head_curve_layout)

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

			head_curve_layout.addWidget(QtWidgets.QLabel(label), row, col, alignment=QtCore.Qt.AlignCenter)
			head_curve_layout.addWidget(btn, row + 1, col)
			self.icon_buttons[label] = btn


		close_btn = QtWidgets.QPushButton("Close")
		close_btn.clicked.connect(self.close)
		layout.addWidget(close_btn)


class BodyWindow(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("Body Options")
		self.setMinimumSize(500, 400)


		layout = QtWidgets.QVBoxLayout(self)
		label = QtWidgets.QLabel("Body", self)
		layout.addWidget(label)

		close_btn = QtWidgets.QPushButton("Close")
		close_btn.clicked.connect(self.close)
		layout.addWidget(close_btn)


def run():
	global ui
	try:
		ui.close()
	except:
		pass

	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = CreateCurveRig(parent=ptr)
	ui.show()
