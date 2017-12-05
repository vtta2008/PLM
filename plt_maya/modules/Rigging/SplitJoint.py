# -*-coding:utf-8 -*
"""

Script Name: SplitJoint.py
Author: Do Trinh/Jimmy - TD artist

Description:
    Splits the selected joint into the specified number of segments.

"""

import logging

import maya.OpenMayaUI as omui
# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds  # Maya_tk Python command

# -------------------------------------------------------------------------------------------------------------
# IMPORT QT MODULES
# -------------------------------------------------------------------------------------------------------------
from plt_maya.plugins import Qt  # plugin module go with DAMGtool to make UI
from plt_maya.plugins.Qt import QtWidgets, QtCore

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------
# MAKE MAYA UNDERSTAND QT UI AS MAYA WINDOW,  FIX VERSION CONVENTION
# -------------------------------------------------------------------------------------------------------------
# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
# -------------------------------------------------------------------------------------------------------------
# CHECK THE CORRECT BINDING THAT BE USING UNDER QT.PY
# -------------------------------------------------------------------------------------------------------------
# While Qt.py lets us abstract the actual Qt library, there are a few things it cannot do yet
# and a few support libraries we need that we have to import manually.
if Qt.__binding__=='PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance

VERSION = 2017

# -------------------------------------------------------------------------------------------------------------
# SHOW UI - MAKE UI IS DOCKABLE INSIDE MAYA
# -------------------------------------------------------------------------------------------------------------
def deleteDock(name='SplitJoint', version=VERSION):
    """
    A simple function to delete the given dock
    Args:
        name: the name of the dock
    """
    if version >= 2017:
        if cmds.workspaceControl(name, query=True, exists=True):
            cmds.deleteUI(name)
    else:
        if cmds.dockControl(name, query=True, exists=True):
            cmds.deleteUI(name)

def getMayaMainWindow():
    """
    Since plt_maya is Qt, we can parent our UIs to it.
    This means that we don't have to manage our UI and can leave it to plt_maya.
    Returns:
        QtWidgets.QMainWindow: The plt_maya MainWindow
    """
    # Use the OpenMayaUI API to get a reference to Maya_tk's MainWindow
    win = omui.MQtUtil_mainWindow()
    # Use the wrapInstance method to convert it to something python can understand (QMainWindow)
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    # Return this to whoever wants it
    return ptr

def getDock(name='DAMGtoolBoxIIDock', version = VERSION):
    """
    This function creates a dock with the given name.
    It's an example of how we can mix plt_maya's UI elements with Qt elements
    Args:
        name: The name of the dock to create
    Returns:
        QtWidget.QWidget: The dock's widget
    """
    # Delete any conflicting docks
    deleteDock( name )
    # Create a workspaceControl dock using Maya_tk's UI tools
    if version >= 2017:
        ctrl = cmds.workspaceControl(name, label='Split Joint')
    else:
        ctrl = cmds.dockControl(name, label='Split Joint')
    # Use the OpenMayaUI API to get the actual Qt widget associated with the name
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    # Use wrapInstance to convert it to something Python can understand (QWidget)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr


class SplitJoint(QtWidgets.QDialog):
    def __init__(self, dock=False):
        if dock:
            parent = getDock()
        else:
            deleteDock()
            try:
                cmds.deleteUI('SplitJoint')
            except:
                logger.debug('No previous UI exists')

            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('SplitJoint')
            parent.setWindowTitle('Split Joint')
            self.layout = QtWidgets.QVBoxLayout(parent)

        super(SplitJoint, self).__init__(parent=parent)

        self.buildUI()

        self.parent().layout().addWidget(self)
        if not dock:
            parent.show()

    def buildUI(self):
        self.fjButton = QtWidgets.QPushButton("Set")
        self.fjButton.setMaximumWidth(50)
        self.fjButton.setStyleSheet("QtWidgets.QPushButton {background-color: rgb (70,90,100)}")

        self.sjButton = QtWidgets.QPushButton("Set")
        self.sjButton.setMaximumWidth(50)
        self.sjButton.setStyleSheet("QtWidgets.QPushButton {background-color: rgb (70,90,100)}")

        self.splitButton = QtWidgets.QPushButton("Split")
        self.splitButton.setMaximumWidth(150)
        self.splitButton.setStyleSheet("QtWidgets.QPushButton {background-color: rgb (70,90,100)}")

        self.splitCountName = QtWidgets.QLineEdit()
        self.splitCountName.setMaximumWidth(50)

        self.fjName = QtWidgets.QLineEdit("select the first joint and click Set")
        self.fjName.setEnabled(False)
        self.fjName.setMaximumWidth(200)

        self.sjName = QtWidgets.QLineEdit("select the second joint and click Set")
        self.sjName.setEnabled(False)
        self.sjName.setMaximumWidth(200)

        # labels
        self.select_lbl = QtWidgets.QLabel('SELECT JOINTS TO SPLIT', self)
        self.select_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.count_lbl = QtWidgets.QLabel('NUMBER OF JOINTS TO INSERT', self)
        self.count_lbl.setAlignment(QtCore.Qt.AlignCenter)

        # layout
        select_lbl_layout = QtWidgets.QHBoxLayout()
        select_lbl_layout.addWidget(self.select_lbl)

        fjButton_layout = QtWidgets.QHBoxLayout()
        fjButton_layout.addWidget(self.fjName)
        fjButton_layout.addWidget(self.fjButton)

        sjButton_layout = QtWidgets.QHBoxLayout()
        sjButton_layout.addWidget(self.sjName)
        sjButton_layout.addWidget(self.sjButton)

        splitButton_layout = QtWidgets.QHBoxLayout()
        splitButton_layout.addWidget(self.splitButton)

        splitCount_layout = QtWidgets.QHBoxLayout()
        splitCount_layout.addWidget(self.count_lbl)
        splitCount_layout.addWidget(self.splitCountName)

        # mainLayout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(10, 4, 10, 8)
        mainLayout.addLayout(select_lbl_layout)
        mainLayout.addLayout(fjButton_layout)
        mainLayout.addLayout(sjButton_layout)
        mainLayout.addLayout(splitCount_layout)
        mainLayout.addLayout(splitButton_layout)

        # bindLayout
        self.setLayout(mainLayout)

        # connect buttons
        self.splitButton.clicked.connect(self.splitJoints)
        self.fjButton.clicked.connect(self.firstJoint)
        self.sjButton.clicked.connect(self.secondJoint)

    def firstJoint(self):
        firstJnt = cmds.ls(sl=True)
        self.fjName.setText(str(firstJnt[0]))

    def secondJoint(self):
        secondJnt = cmds.ls(sl=True)
        self.sjName.setText(str(secondJnt[0]))

    def splitJoints(self):
        firstJnt = self.fjName.text()
        wldPos1 = cmds.xform(firstJnt, q=1, ws=1, rp=1)

        secondJnt = self.sjName.text()
        wldPos2 = cmds.xform(secondJnt, q=1, ws=1, rp=1)

        splitCount = self.splitCountName.text()
        returnPosX = (wldPos2[0] - wldPos1[0]) / (int(splitCount) + 1)
        returnPosZ = (wldPos2[2] - wldPos1[2]) / (int(splitCount) + 1)
        returnPosY = (wldPos2[1] - wldPos1[1]) / (int(splitCount) + 1)

        offsetX = returnPosX + wldPos1[0]
        offsetY = returnPosY + wldPos1[1]
        offsetZ = returnPosZ + wldPos1[2]

        cmds.select(cl=True)

        for x in range(0, int(splitCount)):
            cmds.joint(n=firstJnt + '_split' + str(x + 1))
            cmds.setAttr(firstJnt + '_split' + str(x + 1) + '.translateX', returnPosX)
            cmds.setAttr(firstJnt + '_split' + str(x + 1) + '.translateY', returnPosY)
            cmds.setAttr(firstJnt + '_split' + str(x + 1) + '.translateZ', returnPosZ)

        captureLast = firstJnt + '_split' + str(splitCount)

        # reparent
        cmds.setAttr(firstJnt + '_split1.translateX', offsetX)
        cmds.setAttr(firstJnt + '_split1.translateY', offsetY)
        cmds.setAttr(firstJnt + '_split1.translateZ', offsetZ)
        cmds.parent(firstJnt + '_split1', firstJnt)
        cmds.parent(secondJnt, captureLast)
        cmds.warning("CHAIN SPLIT")


def initialize():
    SplitJoint()