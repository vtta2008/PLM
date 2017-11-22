# -*-coding:utf-8 -*

"""

Script Name: UserLibrary.py
Author: Do Trinh/Jimmy - TD artist

Description:
    This script is make a user library UI and also update all the library data from user for later use.

"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds
import maya.OpenMayaUI as omui # the extent of the internal Maya_tk API
from functools import partial
import os, json, pprint, logging

# -------------------------------------------------------------------------------------------------------------
# IMPORT QT MODULES
# -------------------------------------------------------------------------------------------------------------
from Maya_tk.plugins import Qt # plugin module go with DAMGtool to make UI
from Maya_tk.plugins.Qt import QtWidgets, QtCore, QtGui

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
    from Maya_tk.plugins.Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
    from Maya_tk.plugins.Qt.QtCore import pyqtSignal as Signal
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance
    from Maya_tk.plugins.Qt.QtCore import Signal

# -------------------------------------------------------------------------------------------------------------
# SHOW UI - MAKE UI IS DOCKABLE INSIDE MAYA
# -------------------------------------------------------------------------------------------------------------
def deleteDock(name='UserLibrary', version=2017):
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
    Since Maya_tk is Qt, we can parent our UIs to it.
    This means that we don't have to manage our UI and can leave it to Maya_tk.
    Returns:
        QtWidgets.QMainWindow: The Maya_tk MainWindow
    """
    # Use the OpenMayaUI API to get a reference to Maya_tk's MainWindow
    win = omui.MQtUtil_mainWindow()
    # Use the wrapInstance method to convert it to something python can understand (QMainWindow)
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    # Return this to whoever wants it
    return ptr

def getDock(name='UserLibrary', version = 2017):
    """
    This function creates a dock with the given name.
    It's an example of how we can mix Maya_tk's UI elements with Qt elements
    Args:
        name: The name of the dock to create
    Returns:
        QtWidget.QWidget: The dock's widget
    """
    # Delete any conflicting docks
    deleteDock( name )
    # Create a workspaceControl dock using Maya_tk's UI tools
    if version >= 2017:
        ctrl = cmds.workspaceControl(name, label=name)
    else:
        ctrl = cmds.dockControl(name, label=name)
    # Use the OpenMayaUI API to get the actual Qt widget associated with the name
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    # Use wrapInstance to convert it to something Python can understand (QWidget)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr

USERLIBPTH = os.path.join(os.getenv('PIPELINE_TOOL'), 'Maya_tk/userLibrary')

def createDirectory(directory=USERLIBPTH):
    """
    Creates the given directory if it is not exists

    :param dir (str): The directory to create

    """
    if not os.path.exists(directory):
        os.mkdir(directory)

class UserLibrary(dict):

    def save(self, name, directory=USERLIBPTH, screenshot=True, **info):

        createDirectory(directory)

        path = os.path.join(directory, '%s.ma' % name)
        infoFile = os.path.join(directory, '%s.json' % name)

        info['name'] = name
        info['path'] = path

        cmds.file(rename=path)

        if cmds.ls(sl=True):
            cmds.file(force=True, type='mayaAscii', exportSelect=True)
        else:
            cmds.file(save=True, type='mayaAscii', force=True)

        if screenshot:
            info['screenshot'] = self.saveScreenshot(name, directory=directory)

        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

        self[name] = info

    def find(self, directory=USERLIBPTH):

        if not os.path.exists(directory):
            return

        files = os.listdir(directory)

        mayaFiles = [f for f in files if f.endswith('.ma')]

        for ma in mayaFiles:
            name, ext = os.path.split(ma)
            path = os.path.join(directory, ma)

            infoFile = '%s.json' % name
            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile, 'r') as f:
                    info = json.load(f)
            else:
                info = {}

            screenshot = '%s.jpg' % name
            if screenshot in files:
                info['screenshot'] = os.path.join(directory, name)

            info['name'] = name
            info['path'] = path

            self[name] = info

        pprint.pprint(self)

    def load(self, name):

        path = self[name]['path']

        cmds.file(path, i=True, usingNamespaces=False)

    def saveCreenshot(self, name, directory=USERLIBPTH):
        path = os.path.join(directory, '%s.jpg' % name)

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', w=200, h=200,
                       showOrnaments=False, startTime=1, viewer=False)


class UserLibraryUI(QtWidgets.QWidget):

    def __init__(self, dock=True):
        if dock:
            parent = getDock()
        else:
            deleteDock()
            try:
                cmds.deleteUI('UserLibrary')
            except:
                logger.debug('No previous UI exists')

            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('UserLibrary')
            parent.setWindowTitle('User Library')
            self.layout = QtWidgets.QVBoxLayout(parent)

        super(UserLibraryUI, self).__init__(parent=parent)

        self.library = UserLibrary()
        self.buildUI()
        self.populate()

    def buildUI(self):

        self.layout = QtWidgets.QVBoxLayout(self)

        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        self.layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton('Save')
        saveLayout.addWidget(saveBtn)
        #
        # self.layout.addWidget(saveWidget, 0, 0, 1, 3)
        #
        # self.listWidget = QtWidgets.QListWidget()
        # self.layout.addWidget(self.listWidget, 1, 0, 1, 3)
        #
        # btnWidget = QtWidgets.QWidget()
        # btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        #
        # importBtn = QtWidgets.QPushButton('Import')
        # btnLayout.addWidget(importBtn)
        #
        # refreshBtn = QtWidgets.QPushButton('Refresh')
        # btnLayout.addWidget(refreshBtn)
        #
        # closeBtn = QtWidgets.QPushButton('Close')
        # btnLayout.addWidget(closeBtn)
        #
        # self.layout.addWidget(btnLayout, 2,0,1,3)

    def populate(self):
        pass

def initialize():
    UserLibraryUI()
