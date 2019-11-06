#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ToolBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import json, sys, os
from functools              import partial
from damg                   import DAMGLIST

# PyQt5
from PyQt5.QtCore           import pyqtSlot
from PyQt5.QtWidgets        import QApplication, QAction, QToolBar

# PLM
from appData                import CONFIG_TDS, CONFIG_VFX, CONFIG_ART, CONFIG_TEX, CONFIG_POST, mainConfig, SiPoMin, actionTypes
from ui.uikits.Action       import Action
from ui.uikits.MainWindow   import MainWindow
from ui.uikits.ToolBar      import ToolBar
from utils                  import str2bool, bool2str, is_string, is_action

# -------------------------------------------------------------------------------------------------------------
""" ToolBar """

# class PLMToolBar(ToolBar):
#     registerActions = DAMGLIST()
#
#     with open(mainConfig, 'r') as f:
#         mainInfo = json.load(f)
#
#     def __init__(self, configKey=None, actions=[], parent=None):
#         ToolBar.__init__(self)
#
#         self.parent = parent
#         self.configKey = configKey
#         self.actions = actions
#         self.setWindowTitle('TestToolBar')
#
#         if self.configKey is None or self.configKey == '':
#             if self.actions is None or self.actions == []:
#                 print('CREATEACTIONERROR: Empty key: {0}, {1}'.format(self.configKey, self.actions))
#             else:
#                 self.add_multiple_actions(self.actions)
#         else:
#             self.add_actions_by_key(self.configKey)
#
#         self.setAccessibleName(self.configKey)
#         self.setMinimumWidth((len(self.actions) + 1) * 32)
#
#     def add_multiple_actions(self, actions=[]):
#         for action in actions:
#             if is_string(action):
#                 self.add_action(self.create_action(action))
#             elif is_action(action):
#                 self.add_action(action)
#             else:
#                 print("DATATYPEERROR: Could not add action: {0}".format(action))
#
#     def add_action(self, action):
#         self.registerActions.append(action)
#         return self.addAction(action)
#
#     def create_action(self, key):
#         if key in self.mainInfo.keys():
#             action = Action({
#
#                 'icon': key,
#                 'stt': self.mainInfo[key][0],
#                 'txt': key,
#                 'trg': (partial(self.parent.signals.executing.emit, self.mainInfo[key][2]))
#
#             }, self.parent)
#             return action
#         else:
#             print("KEYACTIONERROR: Could not find key in main config: {0}".format(key))
#
#     def add_actions_by_key(self, key):
#         if key in self.actionData.keys():
#             apps = self.actionData[key]
#             for app in apps:
#                 self.add_action(self.create_action(app))
#         else:
#             print("CONFIGKEYERROR: This key is not configed yet: {0}".format(key))

# class MainToolBar(MainWindow):
#
#     key = 'MainToolBar'
#
#     with open(mainConfig, 'r') as f:
#         mainInfo = json.load(f)
#
#     def __init__(self, actionManager, parent=None):
#         super(MainToolBar, self).__init__(parent)
#
#         self.parent = parent
#         self.actionManager = actionManager
#
#         self.tdToolBar      = self.create_toolBar("TD", CONFIG_TDS)
#         self.compToolBar    = self.create_toolBar("VFX", CONFIG_VFX)
#         self.artToolBar     = self.create_toolBar("ART", CONFIG_ART)
#         self.textureToolBar = self.create_toolBar('TEX', CONFIG_TEX)
#         self.postToolBar    = self.create_toolBar('POST', CONFIG_POST)
#         self.toolBars       = [self.tdToolBar, self.compToolBar, self.artToolBar, self.textureToolBar, self.postToolBar]
#
#     def create_toolBar(self, name="", apps=[]):
#
#         toolBar = self.addToolBar(name)
#
#         k = 0
#         for key in apps:
#             if key in self.mainInfo:
#                 toolBar.addAction(Action({'icon':key,
#                                           'stt':self.mainInfo[key][0],
#                                           'txt':key,
#                                           'trg':(partial(os.startfile, self.mainInfo[key][2]))}, self))
#                 k += 1
#
#         # mainToolBar.setMinimumWidth(k*32 + 1)
#         # mainToolBar.setMinimumHeight(32 + 1)
#         toolBar.setSizePolicy(SiPoMin, SiPoMin)
#         return toolBar
#
#     @pyqtSlot(str, bool)
#     def showToolBar(self, toolbar, mode):
#         if toolbar == 'TD':
#             self.tdToolBar.setVisible(str2bool(mode))
#             self.signals.setSetting.emit(toolbar, bool2str(mode), self.objectName())
#         elif toolbar == 'VFX':
#             self.compToolBar.setVisible(str2bool(mode))
#             self.signals.setSetting.emit(toolbar, bool2str(mode), self.objectName())
#         elif toolbar == 'ART':
#             self.artToolBar.setVisible(str2bool(mode))
#             self.signals.setSetting.emit(toolbar, bool2str(mode), self.objectName())
#         elif toolbar == 'TEX':
#             self.textureToolBar.setVisible(str2bool(mode))
#             self.signals.setSetting.emit(toolbar, bool2str(mode), self.objectName())
#         elif toolbar == 'POS':
#             self.postToolBar.setVisible(str2bool(mode))
#             self.signals.setSetting.emit(toolbar, bool2str(mode), self.objectName())
#         else:
#             for tb in self.toolBars:
#                 tb.setVisible(str2bool(mode))
#                 self.signals.setSetting.emit(tb, bool2str(mode), self.objectName())

class MainToolBar(MainWindow):

    key = 'MainToolBar'

    def __init__(self, actionManager, parent=None):
        super(MainToolBar, self).__init__(parent)

        self.parent         = parent
        self.actionManager  = actionManager

        self.tdToolBar      = self.build_toolBar("TD")
        self.compToolBar    = self.build_toolBar("VFX")
        self.artToolBar     = self.build_toolBar("ART")
        self.textureToolBar = self.build_toolBar('TEX')
        self.postToolBar    = self.build_toolBar('POST')

        self.toolBars       = [self.tdToolBar, self.compToolBar, self.artToolBar, self.textureToolBar, self.postToolBar]

    def build_toolBar(self, name=''):
        toolBar = self.addToolBar(name)
        actions = self.getActions(name)
        for action in actions:
            toolBar.addAction(action)

        toolBar.setSizePolicy(SiPoMin, SiPoMin)
        return toolBar

    def getActions(self, title):
        if title == 'TD':
            actions = self.actionManager.tdToolBarActions(self)
        elif title == 'VFX':
            actions = self.actionManager.vfxToolBarActions(self)
        elif title == 'ART':
            actions = self.actionManager.artToolBarActions(self)
        elif title == 'TEX':
            actions = self.actionManager.texToolBarActions(self)
        elif title == 'POST':
            actions = self.actionManager.postToolBarActions(self)
        else:
            print('WindowTitleError: There is no toolBar name: {0}'.format(title))
            actions = self.actionManager.extraToolActions(self)
        return actions

    @pyqtSlot(str, bool)
    def showToolBar(self, toolbar, mode):
        if toolbar == 'TD':
            self.tdToolBar.setVisible(str2bool(mode))
            self.settings.iniSetValue(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'VFX':
            self.compToolBar.setVisible(str2bool(mode))
            self.settings.iniSetValue(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'ART':
            self.artToolBar.setVisible(str2bool(mode))
            self.settings.iniSetValue(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'TEX':
            self.textureToolBar.setVisible(str2bool(mode))
            self.settings.iniSetValue(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'POS':
            self.postToolBar.setVisible(str2bool(mode))
            self.settings.initSetValue(toolbar, bool2str(mode), self.objectName())
        else:
            for tb in self.toolBars:
                tb.setVisible(str2bool(mode))
                self.settings.iniSetValue(tb, bool2str(mode), self.objectName())

def main():
    app = QApplication(sys.argv)
    toolBar = MainToolBar()
    toolBar.show()
    app.exec_()

if __name__=='__main__':
    main()