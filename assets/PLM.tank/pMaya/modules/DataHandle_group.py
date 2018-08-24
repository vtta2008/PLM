#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import logging
from maya import cmds

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
# if Qt.__binding__=='PySide':
#     logger.debug('Using PySide with shiboken')
#     from shiboken import wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import Signal
# elif Qt.__binding__.startswith('PyQt'):
#     logger.debug('Using PyQt with sip')
#     from sip import wrapinstance as wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import pyqtSignal as Signal
# else:
#     logger.debug('Using PySide2 with shiboken2')
#     from shiboken2 import wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import Signal

def importBTS():
    from appPackages.maya.plt_modules import MayaFuncs
    reload(MayaFuncs)
    return MayaFuncs


class DataHandle(object):
    bts = importBTS()

    def __init__(self):
        self.curPth = cmds.workspace(q=True, rd=True)
        self.workPth = os.path.join(self.curPth, 'scenes')
        self.filePth = cmds.file(q=True, loc=True)

        if self.filePth == 'unknown':
            self.setStartPointUI()

    def setStartPointUI(self):
        mes1 = 'It seems to be like you have not done anything yet, please choose your start'

        mes2 = 'Or, you can create a new project'

        winID = 'Choose Start Point'
        winTitle = winID

        if cmds.window(winID, q=True, exists=True):
            cmds.deleteUI(winID)

        cmds.window(winID, t=winTitle)
        cmds.rowColumnLayout()

    def snapshotUI(self):
        print 'snapshotUI group fm'

    def publishUI(self):
        print 'publishUI group fm'

    def loaderUI(self):
        print 'loaderUI group fm'
