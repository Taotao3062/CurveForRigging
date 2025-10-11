try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import os

ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'icons'))



class CreateCurveRigHead(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle("Create Curve Head")
		self.setMinimumSize(500, 400)

		self.main_layout = QtWidgets.QVBoxLayout(self)

		head_group = QtWidgets.QGroupBox("Head Curve")
		head_layout = QtWidgets.QFormLayout()
		head_group.setLayout(head_layout)

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
			col += 1

		self.main_layout.addWidget(head_layout)





def run():
	global ui
	try:
		ui.close()
	except:
		pass

	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = CreateCurveRig(parent=ptr)
	ui.show()