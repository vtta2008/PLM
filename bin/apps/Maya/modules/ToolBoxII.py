#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: toolBoxII
Author: Do Trinh/Jimmy - TD artist

Warning: This is the most complex code structure I have build, it is using more advanced maya features alongside
              more advanced python features than before.

Description:
    It makes an UI that you can quickly create nurbs controller for Maya, you can also save it for your own. All
    the data you save will be stored in 'userLibrary' folder inside DAMGpipelinetool folder.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import json  # to read and write info & data
import logging
from functools import partial  # partial module can store variables to method

import maya.OpenMayaUI as omui  # the extent of the internal Maya_tk API
import maya.app.renderSetup.views.renderSetupButton as marv  # very nice symbol button
import pymel.core as pm  # Pymel command for maya
# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds, mel  # Maya_tk Python command

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
from tankers.pMaya.plt_modules import MayaVariables as var
from tankers.pMaya.plt_modules import ToolBoxIIfuncs

NAMES = var.MAINVAR
VERSION = var.MAYAVERSION
DIRECTORY = os.path.join(os.getenv(__root__), 'maya', 'userLibrary')
CHANNELBOX_ID = 'ChannelBoxID'

# -------------------------------------------------------------------------------------------------------------
# IMPORT QT MODULES
# -------------------------------------------------------------------------------------------------------------
from tankers.pMaya.QtPlugins import Qt  # plugin module go with DAMGtool to make UI
from tankers.pMaya.QtPlugins.Qt import QtWidgets, QtCore, QtGui

# -------------------------------------------------------------------------------------------------------------
# MAKE MAYA UNDERSTAND QT UI AS MAYA WINDOW,  FIX PLM_VERSION CONVENTION
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
if Qt.__binding__ == 'PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
    from appPackages.maya.plugins.Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
    from appPackages.maya.plugins.Qt.QtCore import pyqtSignal as Signal
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance
    from appPackages.maya.plugins.Qt.QtCore import Signal


# -------------------------------------------------------------------------------------------------------------
# SHOW UI - MAKE UI IS DOCKABLE INSIDE MAYA
# -------------------------------------------------------------------------------------------------------------
def deleteDock(name=NAMES['id'][9], version=VERSION):
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
    Since maya is Qt, we can _parent our UIs to it.
    This means that we don't have to manage our UI and can leave it to maya.
    Returns:
        QtWidgets.QMainWindow: The maya MainWindow
    """
    # Use the OpenMayaUI API to get a reference to Maya_tk's MainWindow
    win = omui.MQtUtil_mainWindow()
    # Use the wrapInstance method to convert it to something python can understand (QMainWindow)
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    # Return this to whoever wants it
    return ptr


def getDock(name='DAMGtoolBoxIIDock', version=VERSION):
    """
    This function creates a dock with the given name.
    It's an example of how we can mix maya's UI elements with Qt elements
    Args:
        name: The name of the dock to create
    Returns:
        QtWidget.QWidget: The dock's widget
    """
    # Delete any conflicting docks
    deleteDock(name)
    # Create a workspaceControl dock using Maya_tk's UI tools
    if version >= 2017:
        ctrl = cmds.workspaceControl(name, label=NAMES['mayaLabel'][9])
    else:
        ctrl = cmds.dockControl(name, label=NAMES['mayaLabel'][9])
    # Use the OpenMayaUI API to get the actual Qt widget associated with the name
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    # Use wrapInstance to convert it to something Python can understand (QWidget)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr


# ------------------------------------- #
# SUB CLASSES FUNCTIONS AND UI ELEMENTS #
# ------------------------------------- #
# Controller Manager UI when create something
# ------------------------------------------------------

def geticon(icon):
    return os.path.join(os.getenv(__root__), 'imgs', 'maya.icon', icon)

class ControllerManager(QtWidgets.QWidget):
    onSolo = Signal(bool)
    tfW = 200

    def __init__(self, nurbs):
        super(ControllerManager, self).__init__()
        if isinstance(nurbs, basestring):
            nurbs = pm.PyNode(nurbs)

        self.nurbs = nurbs

        self.buildUI()

    def buildUI(self):

        btnW = 75

        layout = QtWidgets.QGridLayout(self)

        self.name = QtWidgets.QCheckBox()
        self.name.setChecked(self.nurbs.visibility.get())
        self.name.toggled.connect(lambda val: self.nurbs.getTransform().visibility.set(val))
        layout.addWidget(self.name, 0, 0)

        name = str(self.nurbs.getTransform())
        self.textFldName = QtWidgets.QLineEdit(name)
        self.textFldName.setMinimumWidth(self.tfW)
        self.textFldName.returnPressed.connect(self.renameController)
        layout.addWidget(self.textFldName, 0, 1)

        self.colorPlate = QtWidgets.QLabel()
        self.colorPlate.setMinimumWidth(30)
        self.nurbs.overrideRGBColors.set(0)
        self.nurbs.overrideEnabled.set(1)
        self.setColorPlate()
        layout.addWidget(self.colorPlate, 0, 2)

        soloBtn = QtWidgets.QPushButton('Isolate')
        soloBtn.setMinimumWidth(75)
        soloBtn.setCheckable(True)
        soloBtn.toggled.connect(lambda val: self.onSolo.emit(val))
        layout.addWidget(soloBtn, 0, 3)

        self.color_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.color_slider.setMinimumWidth(2.5 * btnW)
        self.color_slider.setMinimum(1)
        self.color_slider.setMaximum(31)
        self.color_slider.setValue(self.nurbs.overrideColor.get())
        self.color_slider.valueChanged.connect(self.sliderSetColor)
        layout.addWidget(self.color_slider, 0, 4)

        deleteBtn = QtWidgets.QPushButton('Delete')
        deleteBtn.setMinimumWidth(btnW)
        deleteBtn.clicked.connect(self.deleteController)
        layout.addWidget(deleteBtn, 0, 5)

    def renameController(self):
        oldName = str(self.nurbs.getTransform())
        newName = self.textFldName.text()
        cmds.rename(oldName, newName)

    def sliderSetColor(self):
        index = self.color_slider.value()
        self.nurbs.overrideColor.set(index)
        color = cmds.colorIndex(index, q=True)
        self.setColorPlate(color)

    def setColorPlate(self, color=None):
        if not color:
            indexColor = self.nurbs.overrideColor.get()
            if indexColor == 0:
                color = (.4, .4, .4)
            else:
                color = cmds.colorIndex(indexColor, query=True)

        assert len(color) == 3, "You must provide a list of 3 colors"
        r, g, b = [c * 255 for c in color]
        self.colorPlate.setStyleSheet('background-color: rgba(%s,%s,%s,1.0)' % (r, g, b))

    def setColor(self):
        nurbsIndexColor = self.nurbs.overrideColor.get()
        if nurbsIndexColor == 0:
            nurbsColor = (.4, .4, .4)
        else:
            nurbsColor = cmds.colorIndex(nurbsIndexColor, q=True)

        color = pm.colorEditor(rgbValue=nurbsColor)

        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)

        self.nurbs.overrideColorRGB.set(color)
        self.setColorPlate(color)

    def disableNurbs(self, value):
        self.name.setChecked(not value)

    def deleteController(self):
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()

        pm.delete(self.nurbs.getTransform())


# User Library Functions
# ------------------------------------------------------
class ControllerLibrary(dict):
    def createDirectory(self, directory=DIRECTORY):
        """
        Creates the given directory if it doesn't exists.
        :param directory (str): the directory to create 
        :return: 
        """
        if not os.path.exists(directory):
            os.mkdir(directory)

    def save(self, name, screenshot=True, directory=DIRECTORY, **info):

        self.createDirectory(directory)

        path = os.path.join(directory, '%s.ma' % name)
        infoFile = os.path.join(directory, '%s.json' % name)

        info['name'] = name
        info['path'] = path

        cmds.file(rename=path)

        if cmds.ls(sl=True):
            cmds.file(force=True, type='mayaAscii', exportSelected=True)
        else:
            cmds.file(save=True, type='mayaAscii', force=True)

        if screenshot:
            info['screenshot'] = self.saveScreenshot(name, directory=directory)

        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

        self[name] = info

    def remove(self, name, directory=DIRECTORY):
        mayapath = os.path.join(directory, '%s.ma' % name)
        jsonpath = os.path.join(directory, '%s.json' % name)
        imagepath = os.path.join(directory, '%s.jpg' % name)

        items = [mayapath, jsonpath, imagepath]

        for item in items:
            cmds.sysFile(item, delete=True)

    def reference(self, name, directory=DIRECTORY):
        mayapath = os.path.join(directory, '%s.ma' % name)
        cmds.file(mayapath, reference=True, usingNamespaces=False)

    def find(self, directory=DIRECTORY):
        self.clear()

        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        mayafiles = [f for f in files if f.endswith('.ma')]

        for ma in mayafiles:
            name, ext = os.path.splitext(ma)
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

    def load(self, name):
        path = self[name]['path']
        cmds.file(path, i=True, usingNamespaces=False)

    def saveScreenshot(self, name, directory=DIRECTORY):
        cmds.viewFit()
        path = os.path.join(directory, '%s.jpg' % name)
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
        cf = cmds.currentTime(q=True)
        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=cf, endTime=cf, viewer=False)
        return path


# A Maya_tk channel box UI with a few modify
# ------------------------------------------------------
class ChanelBox(QtWidgets.QWidget):
    channelBoxID = CHANNELBOX_ID

    def __init__(self):
        # _parent = QtWidgets.QWidget(_parent=getMayaMainWindow())
        # super(ChanelBox, self).__init__(_parent)

        super(ChanelBox, self).__init__()
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        self.cb1 = cmds.channelBox(CHANNELBOX_ID)

        self.menuChannelBoxWhenRightClick()

        ctrl = omui.MQtUtil.findControl(CHANNELBOX_ID)

        channelBoxWidget = wrapInstance(long(ctrl), QtWidgets.QWidget)

        layout.addWidget(channelBoxWidget)

    # Menu popup when right click in channel box:
    def menuChannelBoxWhenRightClick(self):
        cb1_popup = cmds.popupMenu(p=self.cb1, ctl=False, button=3)
        cmds.menuItem(l="Channels", c=partial(self.channelBoxCommand, "-channelEditor"))
        cmds.menuItem(d=True)
        cmds.menuItem(d=True)

        cmds.menuItem(parent=cb1_popup, l="Reset All Channels", c=partial(self.channelBoxCommand, "-setAllToZero"))
        cb1_menu_03 = cmds.menuItem(parent=cb1_popup, l="Channel Name", subMenu=True)
        cmds.setParent(cb1_menu_03, m=True)

        cmds.radioMenuItemCollection()
        cmds.menuItem('niceNameItem', l="Nice", rb=True, c=self.niceNameSet)
        cmds.menuItem('longNameItem', l="Long", rb=True, c=self.longNameSet)
        cmds.menuItem('shortNameItem', l="Short", rb=True, c=self.shortNameSet)
        cmds.setParent('..', m=True)
        cmds.menuItem(d=True)

        cmds.menuItem(l="Key Selected", c=partial(self.channelBoxCommand, "-keySelected"))
        cmds.menuItem(l="Key All", c=partial(self.channelBoxCommand, "-keyAll"))
        cmds.menuItem(l="Breakdown Selected", c=partial(self.channelBoxCommand, "-breakDownSelected"))
        cmds.menuItem(l="Breakdown All", c=partial(self.channelBoxCommand, "-breakDownAll"))
        cmds.menuItem(d=True)

        cmds.menuItem(l="Cut Selected", c=partial(self.channelBoxCommand, "-cutSelected"))
        cmds.menuItem(l="Copy Selected", c=partial(self.channelBoxCommand, "-copySelected"))
        cmds.menuItem(l="Paste Selected", c=partial(self.channelBoxCommand, "-pasteSelected"))
        cmds.menuItem(l="Delete Selected", c=partial(self.channelBoxCommand, "-deleteSelected"))
        cmds.menuItem(d=True)

        cmds.menuItem(l="Break Connections", c=partial(self.channelBoxCommand, "-breakConnection"))
        cmds.menuItem(d=True)

        cmds.menuItem(l="Lock Selected", c=partial(self.channelBoxCommand, "-lockSelected"))
        cmds.menuItem(l="Unlock Selected", c=partial(self.channelBoxCommand, "-unlockSelected"))
        cmds.menuItem(l="Hide Selected", c=partial(self.channelBoxCommand, "-hideSelected"))
        cmds.menuItem(l="Lock and Hide Selected", c=partial(self.channelBoxCommand, "-lockAndHideSelected"))
        cmds.menuItem(l="Show Hidden Channels", c=partial(self.channelBoxCommand, "-unhideHided"))
        cmds.menuItem(d=True)

        cmds.menuItem(l="Expressions...", c=partial(self.channelBoxCommand, "-expression"))
        cmds.menuItem(l="Set Driven Key", c=partial(self.channelBoxCommand, "-setDrivenKey"))
        cmds.menuItem(d=True)

        cmds.menuItem(l="Delete Attribute", c=partial(self.channelBoxCommand, "-deleteAttribute"))
        cmds.menuItem(d=True)

        cmds.menuItem(l="Setting", subMenu=True)
        cmds.setParent(m=True)

        cmds.menuItem(l="Slow", rb=True, c=self.speedSlowSet)
        cmds.menuItem(l="Normal", rb=True, c=self.speedNormalSet)
        cmds.menuItem(l="Fast", rb=True, c=self.speedFastSet)
        cmds.menuItem(d=True)

        cmds.menuItem('hyperCheckBox', l="Hyperbolic", checkBox=True, c=self.hyperbolicSet)
        cmds.menuItem(d=True)

        cmds.menuItem(l="Precision", c=self.precisionNumberUI)
        cmds.menuItem(d=True)

        cmds.menuItem(l="No Manips", rb=True, c="cmds.channelBox(self.myChannelBox, query=True, mnp=0)")
        cmds.menuItem(l="Invisible Manips", rb=True, c="cmds.channelBox(self.myChannelBox, query=True, mnp=1)")
        cmds.menuItem(l="Standard Manips", rb=True, c="cmds.channelBox(self.myChannelBox, query=True, mnp=2)")

    def warningPopup(self, message):
        cmds.confirmDialog(t='Warning', m=message, b='OK')
        cmds.warning(message)

    # Menu popup functions
    def precisionNumberUI(self, *args):
        if cmds.window('setPrecisionNumber', exists=True):
            cmds.deleteUI('setPrecisionNumber')
        cmds.window('setPrecisionNumber')
        cmds.columnLayout()
        cmds.intField('precisionNumber', w=195)
        cmds.text(l="", h=10)
        cmds.rowColumnLayout(nc=2, cw=[(1, 90), (2, 100)])
        cmds.button(l="Ok", w=90, c=self.setPreNum)
        cmds.button(l="Close", w=90, c="cmds.deleteUI('setPrecisionNumber')")
        cmds.showWindow('setPrecisionNumber')

    def setPreNum(self, *args):
        newPreNum = cmds.intField('precisionNumber', query=True, value=True)
        if newPreNum <= 3:
            newWidth = 65
        elif newPreNum <= 6:
            newWidth = 95
        elif newPreNum <= 9:
            newWidth = 115
        elif newPreNum <= 12:
            newWidth = 130
        else:
            newWidth = 155
        cmds.channelBox(self.channelBoxID, edit=True, pre=newPreNum, fieldWidth=newWidth)
        cmds.deleteUI('setPrecisionNumber')

    def hyperbolicSet(self, *args):
        hyperbolicCheck = cmds.menuItem('hyperCheckBox', query=True, checkBox=True)
        if hyperbolicCheck == True:
            cmds.channelBox(self.channelBoxID, e=True, hyp=True)
        if hyperbolicCheck == False:
            cmds.channelBox(self.channelBoxID, e=True, hyp=False)

    def speedSlowSet(self, *args):
        cmds.channelBox(self.channelBoxID, e=True, spd=0.1)

    def speedNormalSet(self, *args):
        cmds.channelBox(self.channelBoxID, e=True, spd=1)

    def speedFastSet(self, *args):
        cmds.channelBox(self.channelBoxID, e=True, spd=10)

    def niceNameSet(self, *args):
        cmds.channelBox(self.channelBoxID, e=True, nn=True, ln=False)

    def longNameSet(self, *args):
        cmds.channelBox(self.channelBoxID, e=True, nn=False, ln=True)

    def shortNameSet(self, *args):
        cmds.channelBox(self.channelBoxID, e=True, nn=False, ln=False)

    def channelBoxCommand(self, operation, *args):
        channelSel = cmds.channelBox(self.channelBoxID, query=True, sma=True)
        objSel = cmds.ls(sl=True)

        # reset default channels
        transformChannels = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]
        scaleChannels = ["scaleX", "scaleY", "scaleZ", "visibility"]

        if (operation == "-channelEditor"):
            mel.eval("lockingKeyableWnd;")
        elif (operation == "-setAllToZero"):
            for obj in objSel:
                for channel in transformChannels:
                    cmds.setAttr(obj + "." + channel, 0)
                for channel in scaleChannels:
                    cmds.setAttr(obj + "." + channel, 1)
                    # reset created channels
            for obj in objSel:
                createdChannels = []
                allChannels = cmds.listAnimatable(obj)
                for channel in allChannels:
                    attrName = channel.split(".")[-1]
                    createdChannels.append(attrName)
                channels = list(set(createdChannels) - set(transformChannels) - set(scaleChannels))
                for channel in channels:
                    defaultValue = cmds.addItem(obj + "." + channel, query=True, dv=True)
                    cmds.setAttr(obj + "." + channel, defaultValue)
        elif (operation == "-keySelected"):
            for obj in objSel:
                for channel in channelSel:
                    cmds.setKeyframe(obj + "." + channel)
        elif (operation == "-keyAll"):
            for obj in objSel:
                allChannels = cmds.listAnimatable(obj)
                cmds.select(obj)
                for channel in allChannels:
                    cmds.setKeyframe(channel)
        elif (operation == "-breakDownSelected"):
            for obj in objSel:
                for channel in channelSel:
                    cmds.setKeyframe(obj + "." + channel, breakdown=True)
        elif (operation == "-breakDownAll"):
            for obj in objSel:
                allChannels = cmds.listAnimatable(obj)
                cmds.select(obj)
                for channel in allChannels:
                    cmds.setKeyframe(channel, breakdown=True)
        elif (operation == "-cutSelected") or (operation == "-deleteSelected"):
            for obj in objSel:
                for channel in channelSel:
                    cmds.cutKey(obj, at=channel)
        elif (operation == "-copySelected"):
            for obj in objSel:
                for channel in channelSel:
                    cmds.copyKey(obj, at=channel)
        elif (operation == "-pasteSelected"):
            for obj in objSel:
                for channel in channelSel:
                    cmds.pasteKey(obj, connect=True, at=channel)
        elif (operation == "-breakConnection"):
            for obj in objSel:
                for channel in channelSel:
                    attr = obj + "." + channel
                    mel.eval("source channelBoxCommand; CBdeleteConnection \"%s\"" % attr)
        elif (operation == "-lockSelected"):
            for obj in objSel:
                for channel in channelSel:
                    cmds.setAttr(obj + "." + channel, lock=True)
        elif (operation == "-unlockSelected"):
            for obj in objSel:
                for channel in channelSel:
                    cmds.setAttr(obj + "." + channel, lock=False)
        elif (operation == "-hideSelected"):
            for obj in objSel:
                for channel in channelSel:
                    cmds.setAttr(obj + "." + channel, keyable=False, channelBox=False)
        elif (operation == "-lockAndHideSelected"):
            for obj in objSel:
                for channel in channelSel:
                    cmds.setAttr(obj + "." + channel, lock=True)
                    cmds.setAttr(obj + "." + channel, keyable=False, channelBox=False)
        elif (operation == "-unhideHided"):
            # channelBoxChannels = transformChannels + scaleChannels
            for obj in objSel:
                # for channel in channelBoxChannels:
                #     cmds.setAttr( obj + "." + channel, l=False, k=True )
                # get locked channel
                lockChannels = cmds.listAttr(obj, locked=True)
                if lockChannels == None:
                    message = "nothing is locked"
                    self.warningPopup(message)
                    break
                else:
                    for channel in lockChannels:
                        cmds.setAttr(obj + "." + channel, keyable=True, channelBox=True)
        elif (operation == "-showDefault"):
            for obj in objSel:
                defaultChannel = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
                for channel in defaultChannel:
                    cmds.setAttr(obj + "." + channel, k=True, cb=True)
        elif (operation == "-expression"):
            mel.eval('expressionEditor EE "" "";')
        elif (operation == "-unhideHided"):
            mel.eval('SetDrivenKeyOptions;')
        elif (operation == "-deleteAttribute"):
            for obj in objSel:
                for channel in channelSel:
                    cmds.deleteAttr(obj, at=channel)
        elif (operation == "-about"):
            cmds.confirmDialog(t="About DAMG Controller Maker",
                               m=("Thank you for using my script :D\n"
                                  "Made by Do Trinh - JimJim\n"
                                  "Please feel free to give your feedback\n"
                                  "Email me: dot@damgteam.com\n"),
                               b="Close")


# ----------------------------------------------------------------------------------------------------------- #
"""                        MAIN CLASS: DAMG TOOL BOX II - ALL ABOUT CONTROLLER UI                           """
# ----------------------------------------------------------------------------------------------------------- #

"""

                                          A DRAFT PREVIS FOR UI 
         
         WARNING: Change preVis here before changing code, or at least update it after changed the UI.
         
         It helps me easier in calculating or considering all the measurement, variables, 
         as well as how I handle innovating UI quickly and accurately. Actually, it's saving my time.
        
          (w)         4                    3                       4                           1
                      |                    |                       |                           |
        W  |---------------------||-----------------||----------------------------||---------------------|  
      H   Y
        X     1    2   |  3   4  ||   5    6    7   ||   8     9     10      11   ||          12
(h)   -      --------------------------------------------------------------------------------------------- 
 1----|  1 ||     USER ASSETS                CONTROLLER MANAGER                           CHANNEL BOX     ||
      -    | ---------------------  -----------------------------------------------  --------------------- |
 1----|  2 ||  txtFld  |   btn1   || txt | mnOp | btn2 | txt | mnOp | btn3 | btn4  ||                     ||
      _    ||---------------------||-----------------------------------------------||                     ||
      |    ||                     ||                                               ||                     ||
      |    ||                     ||                                               ||                     ||
 1----|  3 ||     QListWiget      ||                                               ||                     ||
      |    ||                     ||                   QGidWidget                  ||                     ||
      |    ||                     ||                                               ||                     ||
      -    ||-------------------- ||                                               ||                     ||
 1----|  4 || btn5   btn6   btn7  ||                                               ||                     ||                        
      -    | --------------------  ------------------------------------------------ |                     ||
 1----|  5 ||   txt        txt    ||       txt       ||           txt              ||                     ||
      -    | --------------------  ------------------  -------- ------------------- |                     ||
      |    || iconbtn  | iconbtn  || btn             || btn8 optionMenu textField  ||                     ||
      |    ||          |          ||                 ||----------------------------||                     ||
      |    ||          |          ||                 ||  cb   btn9   btn10   btn11 ||                     ||
      |    ||          |          ||                 ||----------------------------||                     ||
      |    ||          |          ||                 ||   txt        txtFld        ||                     ||
 1----|  6 ||          |          ||                 ||   txt        txtFld        ||                     ||
      |    ||          |          ||                 ||----------------------------||                     ||
      |    ||          |          ||                 ||  txt   txt    txt    txt   ||                     ||
      |    ||          |          ||                 || txtFld txtFld txtFld  mnOp ||                     ||
      |    ||          |          ||                 ||           btn13            ||                     ||
      |    ||          |          ||      btn12      || btn14  btn15  btn16  btn17 ||                     ||
      -    | ---------------------  -----------------  ----------------------------  --------------------- |
 1----|  7 |  btn18  btn19  btn20 ||                                                                       |
      -     -----------------------------------------------------------------------------------------------
            
            ||          |          ||                 ||                           ||                     ||
        
         btn|  1      2      3      4       5      6      7       8      9     10    11     12      13      14
            | Save |Create|Create|Refresh|Import|Refresh|Remove|Create|  X  |  Y  |  Z  |autoColor|AddA|leftHand|
            |   15       16        17      18     19      20
            |leftFoot|RightHand|RightFoot|Group|Cen.Piv|Frez.T|
         
         [x, y, height, width] = [X, Y, H, W]

"""


class ToolBoxII(QtWidgets.QWidget):
    """
    The DAMGtoolBoxII is a dialog that lets us save and import controllers, 
    also have functions to help user getting easier to modify or plt_model nurbs.
    """
    # --------------------------------------------------------------------------------------------------------
    # DICTIONARY TO STORE BINDATA TO MAKE CONTROLLERS SHOW IN DAMG CONTROLLER LIBRARY SECTION
    # --------------------------------------------------------------------------------------------------------
    # 2D nurbs types
    nurbsType2D = {
        'Arrow Curve': 'arrowCurve.icon.png', 'Plus Nurbs 2': 'boldPlusNurbs.icon.png',
        'Clock Arrow Up': 'clockArrowUp.icon.png', 'Clock Arrow Down': 'clockArrowDown.icon.png',
        'Female Symbol': 'femaleSymbol.icon.png', 'Male Symbol': 'maleSymbol.icon.png',
        'Two directions': 'twoDirections.icon.png', 'Style Arrow 2D': 'twoDstyleArrow.icon.png',
        'Lip Control': 'lipControl.icon.png', 'Upper Lip Control': 'upperLipControl.icon.png',
        'Eyes Control': 'eyeControl.icon.png', 'Circle Plus': 'circlePlus.icon.png',
        'Bold Circle 2D': 'twoDboldCircle.icon.png', 'Bear Foot Control': 'bearFootControl.icon.png',
        'Fist Curve': "fistCurve.icon.png", 'Hand Nurbs': 'handNurbs.icon.png',
        'Foot Control 1': "footControl1.icon.png", 'Foot Control 2': 'footControl2.icon.png',
        'Circle Arrow 2D': 'twoDcircleArrow.icon.png', 'Slider Control': "sliderControl.icon.png",
        'Master Control': 'masterControl.icon.png', 'Fan 5 Wings': 'fiveWingsFan.icon.png',
        'Move Control 2': "moveControl1.icon.png", 'Cross Control': "crossControl.icon.png",
        'Move Control 1': 'moveControl2.icon.png', 'Plus Nurbs 1': 'plusNurbs.icon.png'
    }

    # 3D nurbs types
    nurbsType3D = {
        'Crown Curve': 'crownCurve.icon.png', 'Cube Nurbs': 'cubeCurve.icon.png',
        'Cube Nurbs on base': "cubeOnBase.icon.png", 'Nail Arrow Up': 'nailArrowUp.icon.png',
        'Rotation Control 1': "rotationControl.icon.png", 'Nail Arrow Down': 'nailArrowDown.icon.png',
        'Diamond Control': "diamond.icon.png", 'Single Rotation': "singleRotateControl.icon.png",
        'Shere Control': "sphereControl.icon.png", 'Spike Cross Control': "spikeCrossControl.icon.png",
        'Pyramid': 'pyramid.icon.png', 'Four Sides Arrow': 'fourSidesArrow.icon.png',
        'Origin Control': 'orginControl.icon.png', 'Circle Arrow 3D': 'threeDcircleArrow.icon.png',
        'Arrow Both Sides': 'arrowBothSide.icon.png', 'Style Arrow 3D': 'threeDstyleArrow.icon.png',
        'Jaw Control': 'headJawControl.icon.png', 'Two Way Arrow': 'twoWayArrow.icon.png',
        'Locator Control': 'locatorControl.icon.png', 'Sphere Square': 'sphereSquare.icon.png',
        'Ear Control': 'earControl.icon.png', 'Half Sphere': 'halfSphere.icon.png',
        'Rotation Control 2': 'twoAxisRotation.icon.png', 'Fish Nail': 'fishNail.icon.png',
        'Cylinder Nurbs': 'cylinderCurve.icon.png', 'Point Mark': 'pointNote.icon.png',
        'Tongue Control': 'tongueControl.icon.png', 'Zig Zag Circle': 'zigZagCircle.icon.png'
    }

    # get the paths of plt.maya.icon folder
    scrIcons = os.path.join(os.getenv(__root__), 'imgs', 'maya.icon')

    def __init__(self, dock=True):
        if dock:
            parent = getDock()
        else:
            deleteDock()
            try:
                cmds.deleteUI('DAMGtoolBoxII')
            except:
                logger.debug('No previous UI exists')

            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('DAMGtoolBoxII')
            parent.setWindowTitle('DAMG Tool Box II - Nurbs/Curver/Controller AIO')
            self.layout = QtWidgets.QVBoxLayout(parent)

        super(ToolBoxII, self).__init__(parent=parent)
        # the library variable points to an instance of our controller library
        self.library = ControllerLibrary()

        # every time we create a showLayout_new instance, we will automatically build our UI and populate it
        self.buildUI()
        self.populateLibrarySection()
        self.populateManagerSection()

        self.parent().layout().addWidget(self)
        if not dock:
            parent.show()

    # -------------------------------------------
    # BUILD UI
    # -------------------------------------------
    def buildUI(self):
        """
        This is the main method to excute script of every UI elements to show up UI 
        :return: DAMG tool box II - All about controller
        """
        # ---------------------------------------------------------------------------------------------------------
        # Varialbes to manage UI elements

        btnW = [0, 60, 50]
        txtW = [0, 20, 75]
        txfW = [0, 150]
        cbbW = [0, 100, 150]
        size = [0, 50, 37.5, 50, 25]

        t1W = 4
        top1X = [0, 0, 1, 2, 3]
        top1Y = [0, 0, 0, 0, 0]
        top1H = [0, 1, 1, 1, 1]
        top1W = [0, t1W, t1W, t1W, t1W]
        top1L = ['', '2D Style ', '3D Style']
        top1B = ['', 'Save', 'Import', 'Remove', 'Refresh']

        t2Y = top1W[4]
        t2W = 7
        top2X = top1X
        top2Y = [0, t2Y, t2Y, t2Y, t2Y]
        top2H = [0, 1, 1, 2, 1]
        top2W = [0, t2W, t2W, t2W, t2W]
        top2L = ['', ' 2D: ', ' 3D: ']
        top2B = ['', 'Create', 'Create', 'Refresh']

        m1W = 4
        mid1X = [0, 4, 5, 6, 7]
        mid1Y = [0, 0, 0, 0, 0]
        mid1H = [0, 1, 1, 1, 1]
        mid1W = [0, m1W, m1W / 2, m1W, m1W]
        mid1L = ['', 'Preset 2D name Controller', 'Preset 3D name Controller']
        mid1B = ['', 'Group', 'Center Pivot', 'Freezee Transform']

        m2Y = mid1W[4]
        m2W = 3
        mid2X = mid1X
        mid2Y = [0, m2Y, m2Y, m2Y, m2Y]
        mid2H = [0, 1, 1, 1, 1]
        mid2W = [0, m2W, m2W, m2W, m2W]
        mid2L = ['', 'Change color selected controller']
        mid2B = ['', 'Left->Red & Right->Blue']

        m3Y = mid2W[4] + mid1W[4]
        m3W = 4
        mid3X = mid2X
        mid3Y = [0, m3Y, m3Y, m3Y, m3Y, m3Y]
        mid3H = [0, 1, 1, 1, 1]
        mid3W = [0, m3W, m3W, m3W, m3W, m3W]
        mid3L = [0, 'Text', 'Fonts', 'CurveText', 'MIRROR', 'ADD ATTRIBUTE', 'Long Name', 'Shot Name',
                 'Extra Functions',
                 'TEXT CURVE', 'MIRROR']
        mid3B = [0, 'Create', 'X', 'Y', 'Z', 'Add Attribute', 'Left Hand', 'Left Foot', 'Right Hand', 'Right Foot']

        top1 = {'title': 'USER ASSETS', 'X': top1X, 'Y': top1Y, 'H': top1H, 'W': top1W,
                'btnW': btnW, 'btn': top1B, 'txtW': txtW, 'tfW': txfW, 'ccbW': cbbW, 'label': top1L, 'size': size}

        top2 = {'title': 'CONTROLLER MANAGER', 'X': top2X, 'Y': top2Y, 'H': top2H, 'W': top2W,
                'btnW': btnW, 'btn': top2B, 'txtW': txtW, 'tfW': txfW, 'ccbW': cbbW, 'label': top2L, 'size': size}

        mid1 = {'title': 'CONTROLLER ASSETS', 'X': mid1X, 'Y': mid1Y, 'H': mid1H, 'W': mid1W,
                'btnW': btnW, 'btn': mid1B, 'txtW': txtW, 'tfW': txfW, 'ccbW': cbbW, 'label': mid1L, 'size': size}

        mid2 = {'title': 'COLOR', 'X': mid2X, 'Y': mid2Y, 'H': mid2H, 'W': mid2W,
                'btnW': btnW, 'btn': mid2B, 'txtW': txtW, 'tfW': txfW, 'ccbW': cbbW, 'label': mid2L, 'size': size}

        mid3 = {'title': 'FUNCTIONS', 'X': mid3X, 'Y': mid3Y, 'H': mid3H, 'W': mid3W,
                'btnW': btnW, 'btn': mid3B, 'txtW': txtW, 'tfW': txfW, 'ccbW': cbbW, 'label': mid3L, 'size': size}

        # --------------------------------------------------------------------------------------------------------
        # MAIN LAYOUT STRUCTURE
        # --------------------------------------------------------------------------------------------------------
        # Main Layout
        self.layout = QtWidgets.QGridLayout(self)
        # self.layout.setContentsMargins(QtCore.QMargins(5,5,5,5))

        # --------------------------------------------------------------------------------------------------------
        # TOP SECTION
        # Controller Library section (TOP1)
        self.controllerLibraryUI(top1)

        # Controller Manager section (TOP2)
        self.controllerManagerUI(top2)

        # Channel Box section (TOP3)
        # self.channelbox()

        # --------------------------------------------------------------------------------------------------------
        # MID SECTION
        # Quick Access section (MID1)
        self.controllerQuickAssetUI(mid1)

        # Color Pallet section (MID2)
        self.colorPalletUI(mid2)

        # Extra Function section (MID3)
        self.extraFunctions(mid3)

        # --------------------------------------------------------------------------------------------------------
        # BOT SECTION

    # UI ELEMENTS
    # -------------------------------------------
    # TOP
    # Top1 Layout
    def controllerLibraryUI(self, top1):
        """
        This will define a layout in first bottom column (left)

        return:
            A Library UI that you can load/save any controller from your own.
        """
        # ---------------------------------------------------------------------------------------------------------
        # LIBRARY SECTION
        # ---------------------------------------------------------------------------------------------------------
        # Title
        # ---------------------------------------------------------------------------------------------------------
        # Create QLabel (text)
        libraryLabel = QtWidgets.QLabel(top1['title'])
        libraryLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(libraryLabel, top1['X'][1], top1['Y'][1], top1['H'][1], top1['W'][1])

        # Header
        # ---------------------------------------------------------------------------------------------------------
        # Create QHBoxLayout Widget (text)
        libHeaderWidget = QtWidgets.QWidget()
        # libHeaderWidget.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        libHeaderLayout = QtWidgets.QHBoxLayout(libHeaderWidget)
        # libHeaderLayout.setContentsMargins(QtCore.QMargins(2,2,2,2))

        libHeaderScrollArea = QtWidgets.QScrollArea()
        libHeaderScrollArea.setWidget(libHeaderWidget)
        libHeaderScrollArea.setWidgetResizable(True)
        libHeaderScrollArea.setMaximumHeight(45)

        # Create QLineEdit
        self.layout.addWidget(libHeaderScrollArea, top1['X'][2], top1['Y'][2], top1['H'][2], top1['W'][2])
        self.saveNameField = QtWidgets.QLineEdit()
        self.saveNameField.setMinimumWidth(top1['btnW'][1])
        libHeaderLayout.addWidget(self.saveNameField)

        # Create QPlushButton
        saveBtn = QtWidgets.QPushButton(top1['btn'][1])
        saveBtn.setMinimumWidth(top1['btnW'][1])
        saveBtn.clicked.connect(self.saveItem)
        libHeaderLayout.addWidget(saveBtn)

        # Body - listWidget, load library from local computer
        # ---------------------------------------------------------------------------------------------------------
        # Create QListWidget
        buf = 12
        self.listLibWidget = QtWidgets.QListWidget()
        self.listLibWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listLibWidget.setIconSize(QtCore.QSize(top1['size'][1], top1['size'][1]))
        self.listLibWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listLibWidget.setGridSize(QtCore.QSize(top1['size'][1] + buf, top1['size'][1] + buf))
        self.layout.addWidget(self.listLibWidget, top1['X'][3], top1['Y'][3], top1['H'][3], top1['W'][3])

        # Library footer - 3 buttons: import, refresh, close
        # ---------------------------------------------------------------------------------------------------------
        # Create QGridLayout Widget
        libFooterWidget = QtWidgets.QWidget()
        # libFooterWidget.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        self.libFooterLayout = QtWidgets.QGridLayout(libFooterWidget)
        self.libFooterLayout.setContentsMargins(QtCore.QMargins(2, 2, 2, 2))

        # Create QScrollArea
        scrollLibArea = QtWidgets.QScrollArea()
        scrollLibArea.setWidget(libFooterWidget)
        scrollLibArea.setWidgetResizable(True)
        scrollLibArea.setMaximumHeight(45)
        self.layout.addWidget(scrollLibArea, top1['X'][4], top1['Y'][4], top1['H'][4], top1['W'][4])

        # Create QPlushButton
        importLibBtn = QtWidgets.QPushButton(top1['btn'][2])
        importLibBtn.setMinimumWidth(top1['btnW'][1])
        importLibBtn.clicked.connect(self.loadItem)
        self.libFooterLayout.addWidget(importLibBtn, 0, 0)

        # # Create QPlushButton
        referenceBtn = QtWidgets.QPushButton(top1['btn'][4])
        referenceBtn.setMinimumWidth(top1['btnW'][1])
        referenceBtn.clicked.connect(self.referenceItem)
        self.libFooterLayout.addWidget(referenceBtn, 0, 1)
        #
        # Create QPlushButton
        removeBtn = QtWidgets.QPushButton(top1['btn'][3])
        removeBtn.setMinimumWidth(top1['btnW'][1])
        removeBtn.clicked.connect(self.removeItem)
        self.libFooterLayout.addWidget(removeBtn, 0, 2)

    # Top2 Layout
    def controllerManagerUI(self, top2):
        # ---------------------------------------------------------------------------------------------------------
        # CONTROLLER MANAGER SECTION
        # ---------------------------------------------------------------------------------------------------------

        # Manager section title
        # ---------------------------------------------------------------------------------------------------------
        # Create QLabel
        managerLabel = QtWidgets.QLabel(top2['title'])
        managerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(managerLabel, top2['X'][1], top2['Y'][1], top2['H'][1], top2['W'][1])

        # Header
        # ---------------------------------------------------------------------------------------------------------
        # Create QHBoxLayout Widget
        controllerManagerHeaderWidget = QtWidgets.QWidget()
        controllerManagerHeaderWidget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        controllerManagerHeaderLayout = QtWidgets.QHBoxLayout(controllerManagerHeaderWidget)
        # controllerManagerHeaderLayout.setContentsMargins(QtCore.QMargins(2,2,2,2))

        controlManagerHeaderScrollArea = QtWidgets.QScrollArea()
        controlManagerHeaderScrollArea.setWidget(controllerManagerHeaderWidget)
        controlManagerHeaderScrollArea.setWidgetResizable(True)
        controlManagerHeaderScrollArea.setMaximumHeight(45)

        self.layout.addWidget(controlManagerHeaderScrollArea, top2['X'][2], top2['Y'][2], top2['H'][2], top2['W'][2])

        # Create QLabel
        text2D = QtWidgets.QLabel(top2['label'][1])
        text2D.setMinimumWidth(top2['txtW'][1])
        text2D.setMaximumWidth(top2['txtW'][1])
        controllerManagerHeaderLayout.addWidget(text2D)

        # Create QComboBox
        self.nurbsType2DCB = QtWidgets.QComboBox()
        for nurbsType in sorted(self.nurbsType2D):
            self.nurbsType2DCB.addItem(nurbsType)
        controllerManagerHeaderLayout.addWidget(self.nurbsType2DCB)

        # Create QPushButton
        create2DBtn = QtWidgets.QPushButton(top2['btn'][1])
        create2DBtn.setMinimumWidth(top2['btnW'][1])
        create2DBtn.clicked.connect(self.create2DController)
        controllerManagerHeaderLayout.addWidget(create2DBtn)

        # Create QLabel
        text3D = QtWidgets.QLabel(top2['label'][1])
        text3D.setMinimumWidth(top2['txtW'][1])
        text3D.setMaximumWidth(top2['txtW'][1])
        controllerManagerHeaderLayout.addWidget(text3D)

        # Create QComboBox
        self.nurbsType3DCB = QtWidgets.QComboBox()
        for nurbsType in sorted(self.nurbsType3D):
            self.nurbsType3DCB.addItem(nurbsType)
        controllerManagerHeaderLayout.addWidget(self.nurbsType3DCB)

        # Create QPushButton
        create3DBtn = QtWidgets.QPushButton(top2['btn'][2])
        create3DBtn.setMinimumWidth(top2['btnW'][1])
        create3DBtn.clicked.connect(self.create3DController)
        controllerManagerHeaderLayout.addWidget(create3DBtn)

        refreshBtn = QtWidgets.QPushButton(top2['btn'][3])
        refreshBtn.setMinimumWidth(top2['btnW'][1])
        refreshBtn.clicked.connect(self.populateAll)
        controllerManagerHeaderLayout.addWidget(refreshBtn)

        # Manager Body - scrollWidget
        # ---------------------------------------------------------------------------------------------------------
        # Create QWidget
        scrollManagerWidget = QtWidgets.QWidget()
        scrollManagerWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollManagerWidget)
        # self.scrollLayout.setContentsMargins(QtCore.QMargins(2,2,2,2))

        # Create QScrollArea
        scrollManagerArea = QtWidgets.QScrollArea()
        scrollManagerArea.setWidgetResizable(True)
        scrollManagerArea.setWidget(scrollManagerWidget)
        self.layout.addWidget(scrollManagerArea, top2['X'][3], top2['Y'][3], top2['H'][3], top2['W'][3])

    # Top 3 Layout
    def channelbox(self):
        title = QtWidgets.QLabel('CHANNEL BOX')
        title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(title, 0, 11)

        cbHeaderWidget = QtWidgets.QWidget()
        cbHeaderWidget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        cbHeaderLayout = QtWidgets.QVBoxLayout(cbHeaderWidget)

        cbHeaderScrollArea = QtWidgets.QScrollArea()
        cbHeaderScrollArea.setWidget(cbHeaderWidget)
        cbHeaderScrollArea.setWidgetResizable(True)
        self.layout.addWidget(cbHeaderScrollArea, 1, 11, 5, 1)

        channelBoxWidget = ChanelBox()
        cbHeaderLayout.addWidget(channelBoxWidget)

    # -------------------------------------------
    # MID
    # Mid1 Layout
    def controllerQuickAssetUI(self, mid1):
        """
        This will define a layout in first top column

        return:
            A DAMG CONTROLLER LIBRARY UI that you can create controllers
        """
        # ---------------------------------------------------------------------------------------------------------
        # DAMG CONTROLLER LIBRARY SECTION
        # ---------------------------------------------------------------------------------------------------------

        # Title
        # ---------------------------------------------------------------------------------------------------------
        # quickAccessLabel = QtWidgets.QLabel( mid1['title'] )
        # quickAccessLabel.setAlignment( QtCore.Qt.AlignCenter )
        # self.layout.addWidget( quickAccessLabel, mid1['X'][1], mid1['Y'][1], mid1['H'][1], mid1['W'][1])

        # Header
        # ---------------------------------------------------------------------------------------------------------
        # Create QHBoxLayout Widget
        quickAccessHeaderWidget = QtWidgets.QWidget()
        quickAccessLayout = QtWidgets.QGridLayout(quickAccessHeaderWidget)
        self.layout.addWidget(quickAccessHeaderWidget, mid1['X'][1], mid1['Y'][1], mid1['H'][1], mid1['W'][1])

        # Create QLabel (text)

        label2D = QtWidgets.QLabel(mid1['label'][1])
        label2D.setAlignment(QtCore.Qt.AlignCenter)
        quickAccessLayout.addWidget(label2D, 0, 0, 1, 4)

        # Create QLabel (text)
        label3D = QtWidgets.QLabel(mid1['label'][2])
        label3D.setAlignment(QtCore.Qt.AlignCenter)
        quickAccessLayout.addWidget(label3D, 0, 4, 1, 4)

        # Body
        # ---------------------------------------------------------------------------------------------------------

        # Create QWidget (2D nurbs)
        scrollNurbs2DWidget = QtWidgets.QWidget()
        # scrollNurbs2DWidget.setSizePolicy( QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum )
        self.quickAccess3DLayout = QtWidgets.QGridLayout(scrollNurbs2DWidget)

        # Create QScrollArea
        scrollNurbs2DArea = QtWidgets.QScrollArea()
        scrollNurbs2DArea.setWidgetResizable(True)
        # scrollNurbs2DArea.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        scrollNurbs2DArea.setWidget(scrollNurbs2DWidget)
        self.layout.addWidget(scrollNurbs2DArea, mid1['X'][2], mid1['Y'][2], mid1['H'][2], mid1['W'][2])

        # Create icon button
        nurbs2Dnames = [key for key in self.nurbsType2D]
        count2D = []
        z = mid1['W'][2] + 2
        for x in range((len(nurbs2Dnames) / z) + 1):
            for y in range(z):
                if len(count2D) >= len(nurbs2Dnames):
                    break
                else:
                    index = len(count2D)
                    count2D.append('%s,%s' % (x, y))
                    nurbsType = nurbs2Dnames[index]
                    iconPth = os.path.join(self.scrIcons, self.nurbsType2D[nurbsType])
                    # print iconPth
                    # print os.path.exists(iconPth)
                    icon = QtGui.QIcon(iconPth)
                    toolTip = "Create a showLayout_new " + nurbsType
                    button = marv.RenderSetupButton(self, icon, mid1['size'][2])
                    button.setMinimumSize(mid1['size'][2], mid1['size'][2])
                    button.setMaximumSize(mid1['size'][2], mid1['size'][2])
                    button.setToolTip(toolTip)
                    button.clicked.connect(partial(self.create2DController, nurbsType))
                    self.quickAccess3DLayout.addWidget(button, x, y)
                y += 1
            x += 1

        # Create QWidget (3D nurbs)
        scrollNurbs3DWidget = QtWidgets.QWidget()
        # scrollNurbs3DWidget.setSizePolicy( QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum )
        self.quickAccess3DLayout = QtWidgets.QGridLayout(scrollNurbs3DWidget)

        # Create QScrollArea
        scrollNurbs3DArea = QtWidgets.QScrollArea()
        scrollNurbs3DArea.setWidgetResizable(True)
        # scrollNurbs3DWidget.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        scrollNurbs3DArea.setWidget(scrollNurbs3DWidget)
        self.layout.addWidget(scrollNurbs3DArea, mid1['X'][2], mid1['Y'][2] + mid1['W'][2], mid1['H'][2], mid1['W'][2])

        # Create icon button
        nurbs3Dnames = [key for key in self.nurbsType3D]
        count3D = []
        for x in range((len(nurbs3Dnames) / z) + 1):
            for y in range(z):
                if len(count3D) >= len(nurbs3Dnames):
                    break
                else:
                    index = len(count3D)
                    count3D.append('%s,%s' % (x, y))
                    nurbsType = nurbs3Dnames[index]
                    iconPth = os.path.join(self.scrIcons, self.nurbsType3D[nurbsType])
                    # print iconPth
                    # print os.path.exists(iconPth)
                    icon = QtGui.QIcon(iconPth)
                    toolTip = "Create a showLayout_new " + nurbsType
                    button = marv.RenderSetupButton(self, icon, mid1['size'][2])
                    button.setMinimumSize(mid1['size'][2], mid1['size'][2])
                    button.setMaximumSize(mid1['size'][2], mid1['size'][2])
                    button.setToolTip(toolTip)
                    button.clicked.connect(partial(self.create3DController, nurbsType))
                    self.quickAccess3DLayout.addWidget(button, x, y)
                y += 1
            x += 1

        # Footer
        # ---------------------------------------------------------------------------------------------------------
        # Create QHBoxLayout Widget
        quickAccessFooterWidget = QtWidgets.QWidget()
        quickAccessFooterLayout = QtWidgets.QHBoxLayout(quickAccessFooterWidget)
        self.layout.addWidget(quickAccessFooterWidget, mid1['X'][3], mid1['Y'][3], mid1['H'][3], mid1['W'][3])

        # Create QPushButton
        quickAccessBtn1 = QtWidgets.QPushButton(mid1['btn'][1])
        quickAccessBtn1.clicked.connect(self.groupCenter)
        quickAccessBtn1.setMinimumWidth(mid1['btnW'][1])
        quickAccessFooterLayout.addWidget(quickAccessBtn1)

        # Create QPushButton
        quickAccessBtn2 = QtWidgets.QPushButton(mid1['btn'][2])
        quickAccessBtn2.clicked.connect(self.centerPivot)
        quickAccessBtn2.setMinimumWidth(mid1['btnW'][1])
        quickAccessFooterLayout.addWidget(quickAccessBtn2)

        # Create QPushButton
        quickAccessBtn3 = QtWidgets.QPushButton(mid1['btn'][3])
        quickAccessBtn3.clicked.connect(self.freezeTransformation)
        quickAccessBtn3.setMinimumWidth(mid1['btnW'][1])
        quickAccessFooterLayout.addWidget(quickAccessBtn3)

    # Mid2 Layout
    def colorPalletUI(self, mid2):
        # ---------------------------------------------------------------------------------------------------------
        # DAMG COLOR PALLET SECTION
        # ---------------------------------------------------------------------------------------------------------
        # Title
        # ---------------------------------------------------------------------------------------------------------
        # # Create QLabel
        # colorPalletTitle = QtWidgets.QLabel( mid2['title'] )
        # colorPalletTitle.setAlignment( QtCore.Qt.AlignCenter )
        # self.layout.addWidget( colorPalletTitle, mid2['X'][1], mid2['Y'][1], mid2['H'][1], mid2['W'][1])

        # Header
        # ---------------------------------------------------------------------------------------------------------
        # Create QHBoxlayout Widget
        colorPalletHeaderWidget = QtWidgets.QWidget()
        colorPalletHeaderLayout = QtWidgets.QHBoxLayout(colorPalletHeaderWidget)
        self.layout.addWidget(colorPalletHeaderWidget, mid2['X'][1], mid2['Y'][1], mid2['H'][1], mid2['W'][1])

        # Create QLabel
        colorPalletLabel = QtWidgets.QLabel(mid2['label'][1])
        colorPalletLabel.setAlignment(QtCore.Qt.AlignCenter)
        colorPalletHeaderLayout.addWidget(colorPalletLabel)

        # Body
        # ---------------------------------------------------------------------------------------------------------
        # Create QWidget

        # color index to RGB for button color
        rgb = {0: (.4, .4, .4), 16: (1, 1, 1), 3: (.75, .75, .75), 2: (.5, .5, .5), 1: (0, 0, 0), 18: (0, .7, 1),
               28: (0, .5, .5),
               29: (0, .2, .5), 15: (0, .2, .7), 6: (0, 0, 1), 5: (0, 0, 0.4), 19: (0, 1, .4), 14: (0, 1, 0),
               23: (0, .7, .1),
               26: (.4, .6, 0), 27: (0, .5, .2), 7: (0, 0.2, 0), 13: (1, 0, 0), 24: (.7, .4, .1), 10: (.7, 0.2, 0),
               4: (.5, 0, 0.02), 11: (.3, 0.1, 0.1), 12: (.3, 0, 0), 20: (1, .6, .6), 21: (1, .6, .4), 9: (.7, 0, .7),
               30: (.4, .2, .6), 31: (.5, .1, .3), 8: (.15, 0, .15), 22: (1, 1, .4), 17: (1, 1, 0), 25: (.6, .6, .2), }

        # Create QWidget
        scrollColorWidget = QtWidgets.QWidget()
        # scrollColorWidget.setSizePolicy( QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum )
        self.scrollColorLayout = QtWidgets.QGridLayout(scrollColorWidget)

        # Create QScrollArea
        scrollColorArea = QtWidgets.QScrollArea()
        scrollColorArea.setWidgetResizable(True)
        # scrollColorArea.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        scrollColorArea.setWidget(scrollColorWidget)
        self.layout.addWidget(scrollColorArea, mid2['X'][2], mid2['Y'][2], mid2['H'][2], mid2['W'][2])

        # Create icon button
        rgbKeys = [key for key in rgb]
        rgbKeys = sorted(rgbKeys)
        countColor = []
        z = mid2['W'][2] + 1
        for x in range((len(rgbKeys) / z) + 1):
            for y in range(z):
                key = len(countColor)
                countColor.append('%s,%s' % (x, y))
                if key >= len(rgbKeys):
                    break
                else:
                    index = rgbKeys[key]
                    r, g, b = [c * 255 for c in rgb[index]]
                    button = QtWidgets.QPushButton()
                    button.setMinimumSize(mid2['size'][3], mid2['size'][4])
                    button.setMaximumSize(mid2['size'][3], mid2['size'][4])
                    button.setStyleSheet('background-color: rgba(%s,%s,%s,1.0)' % (r, g, b))
                    button.clicked.connect(partial(self.setColor, index))
                    self.scrollColorLayout.addWidget(button, x, y)
                y += 1
            x += 1

        autoSideColorBtn = QtWidgets.QPushButton(mid2['btn'][1])
        # autoSideColorBtn.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        autoSideColorBtn.clicked.connect(self.changeColorBySides)
        self.scrollColorLayout.addWidget(autoSideColorBtn, x + 1, 0, mid2['H'][2], mid2['W'][2] + 1)

    # Mid3 Layout
    def extraFunctions(self, mid3):

        fontFull = cmds.fontDialog(fl=True)
        fontMain = []
        for i in range(len(fontFull)):
            fontMain.append(fontFull[i].split(" - ")[0])
        fontList = sorted(list(set(fontMain)))

        # title
        extraFunctionsLabel = QtWidgets.QLabel(mid3['label'][8])
        extraFunctionsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(extraFunctionsLabel, mid3['X'][1], mid3["Y"][1], mid3['H'][1],
                              mid3['W'][1])

        # Body
        bodyWidget = QtWidgets.QWidget()
        # bodyWidget.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        bodyWidget.setContentsMargins(2, 2, 2, 2)
        bodyLayout = QtWidgets.QVBoxLayout(bodyWidget)
        self.layout.addWidget(bodyWidget, mid3['X'][2], mid3["Y"][2], mid3['H'][2],
                              mid3['W'][2])

        curveTextWidget = QtWidgets.QWidget()
        # curveTextWidget.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        curveTextLayout = QtWidgets.QHBoxLayout(curveTextWidget)
        # curveTextLayout.setContentsMargins( QtCore.QMargins( 2, 2, 2, 2 ) )

        curveTextScrollArea = QtWidgets.QScrollArea()
        curveTextScrollArea.setWidget(curveTextWidget)
        curveTextScrollArea.setWidgetResizable(True)
        # curveTextScrollArea.setContentsMargins( QtCore.QMargins( 2, 2, 2, 2 ) )
        curveTextScrollArea.setMaximumHeight(45)
        bodyLayout.addWidget(curveTextScrollArea)

        # textCurveLabel = QtWidgets.QLabel(mid3['label'][9])
        # textCurveLabel.setAlignment( QtCore.Qt.AlignCenter )
        # curveTextLayout.addWidget(textCurveLabel, 0,0,1,4)

        createBtn = QtWidgets.QPushButton(mid3['btn'][1])
        createBtn.clicked.connect(self.createTextCurve)
        createBtn.setMinimumWidth(mid3['btnW'][1])
        curveTextLayout.addWidget(createBtn)

        self.fontList = QtWidgets.QComboBox()
        self.fontList.setMaximumWidth(mid3['ccbW'][2])
        for font in fontList:
            self.fontList.addItem(font)
        curveTextLayout.addWidget(self.fontList)

        self.functionsNameField = QtWidgets.QLineEdit()
        self.functionsNameField.setMinimumWidth(mid3['tfW'][1])
        curveTextLayout.addWidget(self.functionsNameField)

        mirrorWidget = QtWidgets.QWidget()
        # mirrorWidget.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        mirrorLayout = QtWidgets.QHBoxLayout(mirrorWidget)
        # mirrorLayout.setContentsMargins( QtCore.QMargins( 5, 5, 5, 5 ) )

        mirrorScrollArea = QtWidgets.QScrollArea()
        mirrorScrollArea.setWidget(mirrorWidget)
        mirrorScrollArea.setWidgetResizable(True)
        # mirrorScrollArea.setContentsMargins( QtCore.QMargins( 5, 5, 5, 5 ) )
        mirrorScrollArea.setMaximumHeight(45)
        bodyLayout.addWidget(mirrorScrollArea)

        # mirrorLabel = QtWidgets.QLabel(mid3['label'][10])
        # mirrorLabel.setAlignment(QtCore.Qt.AlignCenter)
        # mirrorLayout.addWidget(mirrorLabel, 0,0,1,4)

        self.copyCheck = QtWidgets.QCheckBox('Copy')
        mirrorLayout.addWidget(self.copyCheck)

        xbtn = QtWidgets.QPushButton(mid3['btn'][2])
        xbtn.clicked.connect(self.mirrorX)
        xbtn.setMinimumWidth(mid3['btnW'][1])
        mirrorLayout.addWidget(xbtn)

        ybtn = QtWidgets.QPushButton(mid3['btn'][3])
        ybtn.clicked.connect(self.mirrorY)
        ybtn.setMinimumWidth(mid3['btnW'][1])
        mirrorLayout.addWidget(ybtn)

        zbtn = QtWidgets.QPushButton(mid3['btn'][4])
        zbtn.clicked.connect(self.mirrorZ)
        zbtn.setMinimumWidth(mid3['btnW'][1])
        mirrorLayout.addWidget(zbtn)

        addAttrWidget = QtWidgets.QWidget()
        # addAttrWidget.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum )
        addAttrLayout = QtWidgets.QGridLayout(addAttrWidget)

        addAttrScrollArea = QtWidgets.QScrollArea()
        addAttrScrollArea.setWidget(addAttrWidget)
        addAttrScrollArea.setWidgetResizable(True)
        # addAttrScrollArea.setContentsMargins( QtCore.QMargins( 2, 2, 2, 2 ) )
        addAttrScrollArea.setMaximumHeight(180)
        bodyLayout.addWidget(addAttrScrollArea)

        titleLongName = QtWidgets.QLabel(mid3['label'][6])
        titleLongName.setAlignment(QtCore.Qt.AlignCenter)
        addAttrLayout.addWidget(titleLongName, 0, 0)

        self.longNameField = QtWidgets.QLineEdit()
        self.longNameField.setMinimumWidth(mid3['tfW'][1])
        addAttrLayout.addWidget(self.longNameField, 0, 1, 1, 3)

        titleShortName = QtWidgets.QLabel(mid3['label'][7])
        titleShortName.setAlignment(QtCore.Qt.AlignCenter)
        addAttrLayout.addWidget(titleShortName, 1, 0)

        self.shortNameField = QtWidgets.QLineEdit()
        self.shortNameField.setMinimumWidth(mid3['tfW'][1])
        addAttrLayout.addWidget(self.shortNameField, 1, 1, 1, 3)

        minLabel = QtWidgets.QLabel('Min')
        minLabel.setAlignment(QtCore.Qt.AlignCenter)
        addAttrLayout.addWidget(minLabel, 2, 0)

        defaultLabel = QtWidgets.QLabel('Default')
        defaultLabel.setAlignment(QtCore.Qt.AlignCenter)
        addAttrLayout.addWidget(defaultLabel, 2, 1)

        maxLabel = QtWidgets.QLabel('Max')
        maxLabel.setAlignment(QtCore.Qt.AlignCenter)
        addAttrLayout.addWidget(maxLabel, 2, 2)

        fbLabel = QtWidgets.QLabel('F/B')
        fbLabel.setAlignment(QtCore.Qt.AlignCenter)
        addAttrLayout.addWidget(fbLabel, 2, 3)

        self.minField = QtWidgets.QLineEdit()
        addAttrLayout.addWidget(self.minField, 3, 0)

        self.defaultField = QtWidgets.QLineEdit()
        addAttrLayout.addWidget(self.defaultField, 3, 1)

        self.maxField = QtWidgets.QLineEdit()
        addAttrLayout.addWidget(self.maxField, 3, 2)

        self.fbComboBox = QtWidgets.QComboBox()
        self.fbComboBox.addItem('Float')
        self.fbComboBox.addItem('Boolean')
        addAttrLayout.addWidget(self.fbComboBox, 3, 3)

        addAttrBtn = QtWidgets.QPushButton(mid3['btn'][5])
        addAttrBtn.clicked.connect(self.addAttr)
        addAttrLayout.addWidget(addAttrBtn, 4, 0, 1, 4)

        leftHandBtn = QtWidgets.QPushButton(mid3['btn'][6])
        leftHandBtn.setMinimumWidth(mid3['btnW'][1])
        leftHandBtn.clicked.connect(self.leftHandPreset)
        addAttrLayout.addWidget(leftHandBtn, 5, 0)

        leftFootBtn = QtWidgets.QPushButton(mid3['btn'][7])
        leftFootBtn.setMinimumWidth(mid3['btnW'][1])
        leftFootBtn.clicked.connect(self.leftFootPreset)
        addAttrLayout.addWidget(leftFootBtn, 5, 1)

        rightHandBtn = QtWidgets.QPushButton(mid3['btn'][8])
        rightHandBtn.setMinimumWidth(mid3['btnW'][1])
        rightHandBtn.clicked.connect(self.rightHandPreset)
        addAttrLayout.addWidget(rightHandBtn, 5, 2)

        rightFootBtn = QtWidgets.QPushButton(mid3['btn'][9])
        rightFootBtn.setMinimumWidth(mid3['btnW'][1])
        rightFootBtn.clicked.connect(self.rightFootPreset)
        addAttrLayout.addWidget(rightFootBtn, 5, 3)

    # -------------------------------------------
    # BOT
    def thisSectionWillUpdateLater(self):
        pass

    # ****************************************** #
    # -------------------------------------------
    # Main Class Functions
    # -------------------------------------------
    # ****************************************** #

    # -------------------------------------------
    # Functions required in common
    def warningFunction(self, message):
        cmds.confirmDialog(t='Warning', m=message, b='OK')
        cmds.warning(message)

    def DAMGtoolBoxIIHelp(self, *args):
        if cmds.window('helpDAMGToolBoxII', exists=True):
            cmds.deleteUI('helpDAMGToolBoxII')

        cmds.window('helpDAMGToolBoxII', t="Help")
        cmds.rowColumnLayout(nc=3, cw=[(1, 10), (2, 400), (3, 10)])
        cmds.columnLayout()
        cmds.text(l="")
        cmds.setParent('..')
        cmds.columnLayout()
        cmds.text(l="")
        cmds.text(l='This tool have nurbs controller that you can use in rigging')
        cmds.text(l='You can create any nurbs in the QUICK ASSETS sections, and color them as you want')
        cmds.text(l='You can make text nurbs with what ever fonts installed in your computer')
        cmds.text(l='You can add attributes in CREATE NEW ATTRIBUTE or delete attribut in CHANNEL BOX')
        cmds.text(l='You can join all the shapes of nurbs into one in ADJUSTMENT')
        cmds.text(l='The group button is to do group but center pivot object itself, not center of grid')
        cmds.text(l="")
        cmds.text('Have fun.')
        cmds.text(l="")
        cmds.setParent('..')
        cmds.text(l="")
        cmds.showWindow('helpDAMGToolBoxII')

    def populateAll(self):
        self.populateLibrarySection()
        self.populateManagerSection()

    # -------------------------------------------
    # Top1 - Functions for user library sections
    def loadItem(self):
        """load the currently selected controller"""
        currentItem = self.listLibWidget.currentItem()
        if not currentItem:
            self.warningFunction('You must select an item')

        name = currentItem.text()
        self.library.load(name)
        self.populateAll()

    def saveItem(self):
        """This saves the controller with the given file name"""
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("You must give a name")
            cmds.confirmDialog(t='Warning', m='You must give a name', b='OK')
            return

        files = [f for f in os.listdir(DIRECTORY)]

        for file in files:
            if name in file:
                cmds.confirmDialog(t='Confirm', m='File %s already exists, override?' % name,
                                   b=['Yes', 'No'], db='Yes', cb='No', dismissString='No')

        self.library.save(name)
        self.saveNameField.setText('')
        self.populateAll()

    def removeItem(self):
        currentItem = self.listLibWidget.currentItem()
        if not currentItem:
            self.warningFunction('You must select something')
            return
        self.library.remove(currentItem)
        self.populateAll()

    def referenceItem(self):
        name = self.listLibWidget.currentItem().text() or ""
        if name == "":
            self.warningFunction('You must select something')
            return

        self.library.reference(name)
        self.populateAll()

    def populateLibrarySection(self):
        self.listLibWidget.clear()
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listLibWidget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

    # -------------------------------------------
    # Top2 - Functions in controller manager
    def addNurbs(self, nurbs):
        widget = ControllerManager(nurbs)
        self.scrollLayout.addWidget(widget)
        widget.onSolo.connect(self.onSolo)

    def onSolo(self, value):
        nurbsWidgets = self.findChildren(ControllerManager)
        for widget in nurbsWidgets:
            if widget != self.sender():
                widget.disableNurbs(value)

    def populateManagerSection(self):
        while self.scrollLayout.count():
            widget = self.scrollLayout.takeAt(0).widget()
            if widget:
                widget.setVisible(False)
                widget.deleteLater()

        for nurbs in pm.ls(type=['nurbsCurve', 'nurbsSurface']):
            self.addNurbs(nurbs)

    # -------------------------------------------
    # Mid1 - Functions in quick _assets
    def create2DController(self, nurbsType=None):
        if not nurbsType:
            nurbsType = self.nurbsType2DCB.currentText()

        func = ToolBoxIIfuncs.ToolBoxIIfuncs
        func(nurbsType)
        nurbs = cmds.ls(sl=True)[0]
        cmds.rename(nurbs, nurbsType)
        self.populateAll()

    def create3DController(self, nurbsType=None, add=True):
        if not nurbsType:
            nurbsType = self.nurbsType3DCB.currentText()

        func = ToolBoxIIfuncs.ToolBoxIIfuncs
        func(nurbsType)
        nurbs = cmds.ls(sl=True)[0]
        cmds.rename(nurbs, nurbsType)
        self.populateAll()

    # -------------------------------------------
    # Mid2 - Functions in color pallet
    def setColor(self, index, *args):
        selection = cmds.ls(sl=True)
        for select in selection:
            shapes = cmds.listRelatives(select, ad=True, s=True, f=True)
            for node in shapes:
                cmds.setAttr(node + ".overrideRGBColors", 0)
                cmds.setAttr(node + ".overrideEnabled", 1)
                cmds.setAttr(node + ".overrideColor", index)
        self.populateAll()

    def changeColorBySides(self, *args):
        a = cmds.ls(sl=True) or []
        if len(a) == 0:
            a = cmds.ls(type='nurbsCurve')

        LNurbs = []
        RNurbs = []
        letterL = ["_L", "left", "Left"]
        letterR = ["_R", "right", "Right"]

        for nurbs in a:
            for left in letterL:
                if left in nurbs:
                    LNurbs.append(nurbs)
            for right in letterR:
                if right in nurbs:
                    RNurbs.append(nurbs)

        for nurbs in LNurbs:
            cmds.setAttr(nurbs + '.overrideEnabled', 1)
            cmds.setAttr(nurbs + '.overrideColor', 13)

        for nurbs in RNurbs:
            cmds.setAttr(nurbs + '.overrideEnabled', 1)
            cmds.setAttr(nurbs + '.overrideColor', 6)

        self.populateAll()

    # -------------------------------------------
    # Mid3 - Functions in extra functions
    def createTextCurve(self, *args):
        list = []
        getText = self.functionsNameField.text()
        font = self.fontList.currentText()

        if (len(getText) == 0):
            message = "Text field is empty, can not create text curve"
            self.warningFunction(message)
            return
        if (len(getText) > 0):
            list.append(cmds.textCurves(f=font, t=getText))
        for x in range(len(list) - 1):
            cmds.makeIdentity(list[x + 1], apply=True, t=1, r=1, s=1, n=0)
            shapeNode = cmds.listRelatives(list[x + 1], shapes=True)
            cmds.parent
            cmds.delete(list[x + 1])
        select = cmds.select(list[0])
        cmds.rename(select, getText)
        self.populateAll()

    def groupCenter(self, *args):
        a = cmds.ls(sl=True)
        cmds.group(n=a[0] + "_group")
        self.populateAll()

    def centerPivot(self, *args):
        a = cmds.ls(sl=True)
        if (len(a) > 0):
            cmds.xform(cp=True)
        self.populateAll()

    def freezeTransformation(self, *args):
        a = cmds.ls(sl=True)
        if (len(a) > 0):
            cmds.makeIdentity(apply=True)
        self.populateAll()

    def mirrorY(self, *args):
        copyValue = self.copyCheck.checkState()
        curSel = cmds.ls(sl=True)
        if len(curSel) > 0:
            if copyValue:
                cmds.duplicate()
            cmds.group(n="controllers_mirror_group")
            cmds.xform(os=True, piv=[0, 0, 0])
            cmds.scale(1, -1, 1)
            cmds.ungroup('controllers_mirror_group')
        else:
            cmds.warning("nothing selected")
        self.populateAll()

    def mirrorZ(self, *args):
        copyValue = self.copyCheck.checkState()
        curSel = cmds.ls(sl=True)
        if len(curSel) > 0:
            if copyValue:
                cmds.duplicate()
            cmds.group(n="controllers_mirror_group")
            cmds.xform(os=True, piv=[0, 0, 0])
            cmds.scale(1, 1, -1)
            cmds.ungroup('controllers_mirror_group')
        else:
            cmds.warning("nothing selected")
        self.populateAll()

    def mirrorX(self, *args):
        copyValue = self.copyCheck.checkState()
        curSel = cmds.ls(sl=True)
        if len(curSel) > 0:
            if copyValue:
                cmds.duplicate()
            cmds.group(n="controllers_mirror_group")
            cmds.xform(os=True, piv=[0, 0, 0])
            cmds.scale(-1, 1, 1)
            cmds.ungroup('controllers_mirror_group')
        else:
            cmds.warning("nothing selected")

        self.populateAll()

    def addAttr(self, *args):
        objSel = cmds.ls(sl=True) or []
        longName = self.longNameField.text()
        shortName = self.shortNameField.text()
        minNum = self.minField.text()
        defNum = self.defaultField.text()
        maxNum = self.maxField.text()
        ForB = self.fbComboBox.currentText()

        if objSel == []:
            message = 'You must select something'
            self.warningFunction(message)
            return
        if (len(longName) == 0):
            message = "Long name can not be blank"
            self.warningFunction(message)
            return
        if (len(longName.split(" ")) > 1):
            message = "Long name contains unavailable character"
            self.warningFunction(message)
            return
        if (len(shortName) == 0):
            shortName = longName
            if (ForB == 'Boolean'):
                for i in range(len(objSel)):
                    cmds.select(objSel[i])
                    cmds.addItem(ln=longName, nn=shortName, at='bool', dv=1, k=True)
                    i += 1
            if (ForB == 'Float'):
                for i in range(len(objSel)):
                    cmds.select(objSel[i])
                    cmds.addItem(ln=longName, nn=shortName, at='float', min=minNum,
                                 max=maxNum, dv=defNum, k=True)
                    i += 1
            return
        if (len(shortName) > 0):
            if (ForB == 'Boolean'):
                for i in range(len(objSel)):
                    cmds.select(objSel[i])
                    cmds.addItem(ln=longName, nn=shortName, at='bool', dv=1, k=True)
                    i += 1
            if (ForB == 'Float'):
                for i in range(len(objSel)):
                    cmds.select(objSel[i])
                    cmds.addItem(ln=longName, nn=shortName, at='float', min=minNum,
                                 max=maxNum, dv=defNum, k=True)
                    i += 1

    def leftHandPreset(self, *args):
        objSel = cmds.ls(sl=True)
        hand = ["thumb", "index", "middle", "ring", "little"]
        for i in objSel:
            cmds.select(i, r=True)
            for item in hand:
                longName = "L_" + item + "Finger_Curl"
                niceName = "L_" + item + "F_Curl"
                cmds.addItem(ln=longName, nn=niceName, at='float', min=-5, dv=0, max=15, k=True)

    def rightHandPreset(self, *args):
        objSel = cmds.ls(sl=True)
        hand = ["thumb", "index", "middle", "ring", "little"]
        for i in objSel:
            cmds.select(i, r=True)
            for item in hand:
                longName = "R_" + item + "Finger_Curl"
                niceName = "R_" + item + "F_Curl"
                cmds.addItem(ln=longName, nn=niceName, at='float', min=-5, dv=0, max=15, k=True)

    def leftFootPreset(self, *args):
        objSel = cmds.ls(sl=True)
        foot = ["big", "long", "middle", "ring", "pinky"]
        for i in objSel:
            cmds.select(i, r=True)
            for item in foot:
                longName = "L_" + item + "Toe_Curl"
                niceName = "L_" + item + "T_Curl"
                cmds.addItem(ln=longName, nn=niceName, at='float', min=-5, dv=0, max=15, k=True)

    def rightFootPreset(self, *args):
        objSel = cmds.ls(sl=True)
        foot = ["big", "long", "middle", "ring", "pinky"]
        for i in objSel:
            cmds.select(i, r=True)
            for item in foot:
                longName = "R_" + item + "Toe_Curl"
                niceName = "R_" + item + "T_Curl"
                cmds.addItem(ln=longName, nn=niceName, at='float', min=-5, dv=0, max=15, k=True)

                # --------------------------------------------------------------------------------------------------------
                # END OF CODE
                # --------------------------------------------------------------------------------------------------------
