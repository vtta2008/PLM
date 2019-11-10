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
from utils                  import str2bool, bool2str

# -------------------------------------------------------------------------------------------------------------
""" ToolBar """

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