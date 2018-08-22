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
import json
import os
import sys
from functools import partial

from PyQt5.QtCore import pyqtSignal, pyqtSlot
# PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication

# Plt
from core.Loggers import SetLogger
from core.Metadata import __envKey__
from core.keys import CONFIG_TDS, CONFIG_VFX, CONFIG_ART, CONFIG_TEX, CONFIG_POST
from core.paths import SiPoMin
from ui.uikits.Action import Action
from docker.utils import str2bool, bool2str

# -------------------------------------------------------------------------------------------------------------
""" ToolBar """

class MainToolBar(QMainWindow):

    key = 'mainToolBar'

    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    addLayout = pyqtSignal(object)
    openBrowser = pyqtSignal(str)
    setSetting = pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        super(MainToolBar, self).__init__(parent)
        self.logger = SetLogger(self)

        with open(os.path.join(os.getenv(__envKey__), 'cfg', 'main.cfg'), 'r') as f:
            self.appInfo = json.load(f)

        self.tdToolBar = self.create_toolBar("TD", CONFIG_TDS)
        self.compToolBar = self.create_toolBar("VFX", CONFIG_VFX)
        self.artToolBar = self.create_toolBar("ART", CONFIG_ART)
        self.textureToolBar = self.create_toolBar('TEX', CONFIG_TEX)
        self.postToolBar = self.create_toolBar('POST', CONFIG_POST)

        self.toolBars = [self.tdToolBar, self.compToolBar, self.artToolBar, self.textureToolBar, self.postToolBar]

        self.setSizePolicy(SiPoMin, SiPoMin)

    def create_toolBar(self, name="", apps=[]):
        toolBar = self.addToolBar(name)
        for key in apps:
            if key in self.appInfo:
                toolBar.addAction(Action({'icon':key,
                                          'stt':self.appInfo[key][0],
                                          'txt':key,
                                          'trg':(partial(self.executing.emit, self.appInfo[key][2]))}, self))
        return toolBar

    @pyqtSlot(str, bool)
    def showToolBar(self, toolbar, mode):
        if toolbar == 'td':
            self.tdToolBar.setVisible(str2bool(mode))
            self.setSetting.emit(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'vfx':
            self.compToolBar.setVisible(str2bool(mode))
            self.setSetting.emit(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'art':
            self.artToolBar.setVisible(str2bool(mode))
            self.setSetting.emit(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'tex':
            self.textureToolBar.setVisible(str2bool(mode))
            self.setSetting.emit(toolbar, bool2str(mode), self.objectName())
        elif toolbar == 'post':
            self.postToolBar.setVisible(str2bool(mode))
            self.setSetting.emit(toolbar, bool2str(mode), self.objectName())
        else:
            for tb in self.toolBars:
                tb.setVisible(str2bool(mode))
                self.setSetting.emit(tb, bool2str(mode), self.objectName())

    def hideEvent(self, event):
        self.setSetting.emit(self.key, 'hide', self.objectName())

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

def main():
    app = QApplication(sys.argv)
    toolBar = MainToolBar()
    toolBar.show()
    app.exec_()

if __name__=='__main__':
    main()