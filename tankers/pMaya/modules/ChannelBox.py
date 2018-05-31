#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ChannelBox.py
Author: Do Trinh/Jimmy - TD artist

Description:
    This script makes a new Channel box UI with new menu. It easier for me to use channel box in this way.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import logging
import os
from functools import partial  # partial module can store variables to method

import maya.OpenMayaUI as omui  # the extent of the internal Maya_tk API
import maya.mel as mel
# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds

from appPackages.maya.plt_modules import MayaVariables as var

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
NAMES = var.MAINVAR
MESSAGE = var.MESSAGE
TITLE = var.TITLE
VERSION = NAMES['mayaVersion']

# Icon directory:
ICONS = var.ICONS

# -------------------------------------------------------------------------------------------------------------
# IMPORT QT MODULES
# -------------------------------------------------------------------------------------------------------------
from tankers.pMaya.QtPlugins import Qt  # plugin module go with DAMGtool to make UI
from tankers.pMaya.QtPlugins.Qt import QtWidgets

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
if Qt.__binding__ == 'PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance


# -------------------------------------------------------------------------------------------------------------
# SHOW UI - MAKE UI IS DOCKABLE INSIDE MAYA
# -------------------------------------------------------------------------------------------------------------

def getMayaMainWindow():
    """
    Since maya is Qt, we can parent our UIs to it.
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


def getDock(name='Channel Box', label='Channel Box', version=VERSION):
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
        ctrl = cmds.workspaceControl(name, label=label)
    else:
        ctrl = cmds.dockControl(name, label=label)
    # Use the OpenMayaUI API to get the actual Qt widget associated with the name
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    # Use wrapInstance to convert it to something Python can understand (QWidget)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr


def deleteDock(name='Channel Box', version=VERSION):
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


# get button functions data
def importBTS():
    from plt_maya.modules import MayaFuncs
    reload(MayaFuncs)
    return MayaFuncs


# ----------------------------------------------------------------------------------------------------------- #
"""                                        MAIN CLASS: CHANNELBOX UI                                        """


# ----------------------------------------------------------------------------------------------------------- #
class ChannelBox(QtWidgets.QWidget):
    icons = ICONS
    curPth = cmds.workspace(q=True, rd=True)
    curPthParts = curPth.split('/')
    curPthList = [f for f in os.listdir(curPth) if os.path.isdir(curPth + f)]
    bts = importBTS()

    def __init__(self, dock=True):
        if dock:
            parent = getDock(name='Channel Box', label='Channel Box')
        else:
            deleteDock()
            try:
                cmds.deleteUI('Channel Box')
            except:
                logger.debug('No previous UI exists')

            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('Channel Box')
            parent.setWindowTItle('Channel Box')
            dialogLayout = QtWidgets.QVBoxLayout(parent)

        super(ChannelBox, self).__init__(parent=parent)

        self.buildUI()

        if not dock:
            parent.show()

    def buildUI(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.cb1 = cmds.channelBox('Channel Box')

        self.menuChannelBoxWhenRightClick()

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
        cmds.channelBox('Channel Box', edit=True, pre=newPreNum, fieldWidth=newWidth)
        cmds.deleteUI('setPrecisionNumber')

    def hyperbolicSet(self, *args):
        hyperbolicCheck = cmds.menuItem('hyperCheckBox', query=True, checkBox=True)
        if hyperbolicCheck == True:
            cmds.channelBox('Channel Box', e=True, hyp=True)
        if hyperbolicCheck == False:
            cmds.channelBox('Channel Box', e=True, hyp=False)

    def speedSlowSet(self, *args):
        cmds.channelBox(self.cb1, e=True, spd=0.1)

    def speedNormalSet(self, *args):
        cmds.channelBox(self.cb1, e=True, spd=1)

    def speedFastSet(self, *args):
        cmds.channelBox(self.cb1, e=True, spd=10)

    def niceNameSet(self, *args):
        cmds.channelBox(self.cb1, e=True, nn=True, ln=False)

    def longNameSet(self, *args):
        cmds.channelBox(self.cb1, e=True, nn=False, ln=True)

    def shortNameSet(self, *args):
        cmds.channelBox(self.cb1, e=True, nn=False, ln=False)

    def channelBoxCommand(self, operation, *args):
        channelSel = cmds.channelBox(self.cb1, query=True, sma=True)
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
                    defaultValue = cmds.addAttr(obj + "." + channel, query=True, dv=True)
                    cmds.setAttr(obj + "." + channel, defaultValue)
        elif (operation == "-keySelected"):
            print 'Channel Box', channelSel, objSel
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

            # -------------------------------------------------------------------------------------------------------------
            # END OF CODE
            # -------------------------------------------------------------------------------------------------------------
