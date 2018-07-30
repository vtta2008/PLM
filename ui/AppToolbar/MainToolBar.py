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
from functools import partial

# PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSignal, pyqtSlot

# Plt
from appData import CONFIG_TDS, CONFIG_VFX, CONFIG_ART, APPINFO, SiPoMin
from ui.uikits.Action import Action
from utilities.utils import str2bool
from core.Specs import Specs
from core.Loggers import SetLogger


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

        self.specs = Specs(self.key, self)
        self.logger = SetLogger(self)
        self.appInfo = APPINFO

        self.tdToolBar = self.create_toolBar("TD", CONFIG_TDS)
        self.compToolBar = self.create_toolBar("VFX", CONFIG_VFX)
        self.artToolBar = self.create_toolBar("ART", CONFIG_ART)

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
            self.setSetting.emit(toolbar, 'hide', self.objectName())
        elif toolbar == 'vfx':
            self.compToolBar.setVisible(str2bool(mode))
            self.setSetting.emit(toolbar, 'hide', self.objectName())
        elif toolbar == 'art':
            self.artToolBar.setVisible(str2bool(mode))
            self.setSetting.emit(toolbar, 'hide', self.objectName())
        else:
            for tb in [self.tdToolBar, self.compToolBar, self.artToolBar]:
                tb.setVisible(True)

            self.setSetting.emit('td', 'hide', self.objectName())
            self.setSetting.emit('vfx', 'hide', self.objectName())
            self.setSetting.emit('art', 'hide', self.objectName())

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