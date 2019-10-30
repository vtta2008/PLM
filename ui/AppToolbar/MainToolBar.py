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

# PyQt5
from PyQt5.QtCore           import pyqtSlot
from PyQt5.QtWidgets        import QApplication

# PLM
from appData                import CONFIG_TDS, CONFIG_VFX, CONFIG_ART, CONFIG_TEX, CONFIG_POST, mainConfig, SiPoMin
from ui.uikits.Action       import Action
from ui.uikits.MainWindow   import MainWindow
from utils                  import str2bool, bool2str

# -------------------------------------------------------------------------------------------------------------
""" ToolBar """

print(CONFIG_POST, CONFIG_TDS, CONFIG_ART, CONFIG_TEX, CONFIG_VFX)

class MainToolBar(MainWindow):

    key = 'MainToolBar'

    with open(mainConfig, 'r') as f:
        appInfo = json.load(f)

    def __init__(self, parent=None):
        super(MainToolBar, self).__init__(parent)

        self.tdToolBar      = self.create_toolBar("TD", CONFIG_TDS)
        self.compToolBar    = self.create_toolBar("VFX", CONFIG_VFX)
        self.artToolBar     = self.create_toolBar("ART", CONFIG_ART)
        self.textureToolBar = self.create_toolBar('TEX', CONFIG_TEX)
        self.postToolBar    = self.create_toolBar('POST', CONFIG_POST)

        self.toolBars       = [self.tdToolBar, self.compToolBar, self.artToolBar, self.textureToolBar, self.postToolBar]

    def create_toolBar(self, name="", apps=[]):

        toolBar = self.addToolBar(name)

        k = 0
        for key in apps:
            if key in self.appInfo:
                print(key, k)
                toolBar.addAction(Action({'icon':key,
                                          'stt':self.appInfo[key][0],
                                          'txt':key,
                                          'trg':(partial(os.startfile, self.appInfo[key][2]))}, self))
                k += 1

        # mainToolBar.setMinimumWidth(k*32 + 1)
        # mainToolBar.setMinimumHeight(32 + 1)
        toolBar.setSizePolicy(SiPoMin, SiPoMin)
        return toolBar

    @pyqtSlot(str, bool)
    def showToolBar(self, toolbar, mode):
        if toolbar == 'TD':
            self.tdToolBar.setVisible(str2bool(mode))
            self.signals.setSetting.emit(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'VFX':
            self.compToolBar.setVisible(str2bool(mode))
            self.signals.setSetting.emit(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'ART':
            self.artToolBar.setVisible(str2bool(mode))
            self.signals.setSetting.emit(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'TEX':
            self.textureToolBar.setVisible(str2bool(mode))
            self.signals.setSetting.emit(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'POS':
            self.postToolBar.setVisible(str2bool(mode))
            self.signals.setSetting.emit(toolbar, bool2str(mode), self.objectName())
        else:
            for tb in self.toolBars:
                tb.setVisible(str2bool(mode))
                self.signals.setSetting.emit(tb, bool2str(mode), self.objectName())

def main():
    app = QApplication(sys.argv)
    toolBar = MainToolBar()
    toolBar.show()
    app.exec_()

if __name__=='__main__':
    main()