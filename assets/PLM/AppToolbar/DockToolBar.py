# -*- coding: utf-8 -*-
"""

Script Name: ToolBarDock.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDockWidget, QGridLayout

# PLM
from assets.Storage import PObj
from core.paths import SiPoExp
from ui.uikits.ToolBar import ToolBar

# -------------------------------------------------------------------------------------------------------------
""" Tool bar docking class """

class DockToolBar(QDockWidget):

    key = 'docker toolbar'
    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    addLayout = pyqtSignal(object)
    setSetting = pyqtSignal(str, str, str)

    def __init__(self, name="TEXTURE", parent=None):
        super(DockToolBar, self).__init__(parent)

        self.name = name
        self.key = 'dockToolBar' + " {0}".format(self.name)
        self.setWindowTitle(self.name)
        self.layout = QGridLayout()
        self.toolbar = ToolBar(self.name, self)
        self.toolbar.executing.connect(self.executing)

        self.layout.addWidget(self.toolbar, 0, 0, 1, 1)
        self.setLayout(self.layout)
        self.applySetting()
        self.reg = PObj(self)

    def applySetting(self):
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setSizePolicy(SiPoExp, SiPoExp)

    def showEvent(self, event):
        pass

    def closeEvent(self, event):
        self.addLayout.emit(self)
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 21/07/2018 - 6:43 AM
# © 2017 - 2018 DAMGteam. All rights reserved