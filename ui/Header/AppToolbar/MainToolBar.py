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
import sys

# PyQt5
from PyQt5.QtCore           import pyqtSlot
from PyQt5.QtWidgets        import QApplication

# PLM
from appData                import SiPoMin
from ui.uikits.MainWindow   import MainWindow
from ui.uikits.ToolBar      import ToolBar
from utils                  import str2bool, bool2str

# -------------------------------------------------------------------------------------------------------------
""" ToolBar """

class MainToolBar(MainWindow):

    key = 'MainToolBar'
    toolBars = dict()
    _count = 0

    def __init__(self, actionManager, parent=None):
        super(MainToolBar, self).__init__(parent)

        self.parent         = parent

        try:
            self.parent.children()
        except AttributeError:
            pass
        else:
            self.setParent(self.parent)

        self.actionManager  = actionManager

        if not self.settings._settingEnable:
            print('setting enable value: {0}'.format(self.settings._settingEnable))
            self.settings       = self.parent.settings

        self.tdToolBar      = self.build_toolBar("TD")
        self.compToolBar    = self.build_toolBar("VFX")
        self.artToolBar     = self.build_toolBar("ART")
        self.textureToolBar = self.build_toolBar('TEX')
        self.postToolBar    = self.build_toolBar('POST')

        self.updateWidth(True)

    def updateWidth(self, bool):
        i = 13
        if not self.tdToolBar.isVisible():
            i = i - 4

        if not self.compToolBar.isVisible():
            i = i - 2

        if not self.artToolBar.isVisible():
            i = i - 4

        if not self.textureToolBar.isVisible():
            i = i - 2

        if not self.postToolBar.isVisible():
            i = i - 1

        w = i*32 + i*2
        # print(w)
        self.setFixedWidth(w)
        # self.parent.setFixedWidth(w + 20)

    def build_toolBar(self, name=''):
        toolBar = ToolBar(self)
        toolBar.key = '{0}_{1}'.format(self.key, name)
        toolBar._name = toolBar.key
        toolBar.setWindowTitle(name)

        actions = self.getActions(name)

        for action in actions:
            toolBar.add_action(action)

        toolBar.setSizePolicy(SiPoMin, SiPoMin)
        toolBar.visibilityChanged.connect(self.updateWidth)
        self.toolBars[name] = toolBar
        self.addToolBar(toolBar)
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

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val):
        self._count = val

    @pyqtSlot(str, bool)
    def showToolBar(self, toolbar, mode):
        if toolbar in self.toolBars.keys():
            tb = self.toolBars[toolbar]
            tb.setVisible(str2bool(mode))
            self.settings.initSetValue('visible', bool2str(mode), tb.key)
        else:
            for tb in self.toolBars.values():
                tb.setVisible(str2bool(mode))
                self.settings.iniSetValue('visible', bool2str(mode), tb.key)

def main():
    app = QApplication(sys.argv)
    toolBar = MainToolBar()
    toolBar.show()
    app.exec_()

if __name__=='__main__':
    main()