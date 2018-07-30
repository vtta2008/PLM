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
from appData import SiPoExp
from ui.uikits.ToolBar import ToolBar

# -------------------------------------------------------------------------------------------------------------
""" Tool bar docking class """

class ToolBarDock(QDockWidget):

    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    addLayout = pyqtSignal(object)
    setSetting = pyqtSignal(str, str, str)
    key = 'Toolbar'

    def __init__(self, name="TEXTURE", parent=None):
        super(ToolBarDock, self).__init__(parent)
        # print(self.__class__.isWindowType())
        self.name = name
        self.setWindowTitle(self.name)
        self.layout = QGridLayout()
        self.toolbar = ToolBar(self.name, self)
        self.toolbar.executing.connect(self.executing)
        # self.toolbar.move(0, 30)
        self.layout.addWidget(self.toolbar, 0, 0, 1, 1)
        self.setLayout(self.layout)

        self.applySetting()

    def applySetting(self):
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setSizePolicy(SiPoExp, SiPoExp)

    def showEvent(self, event):
        pass

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 21/07/2018 - 6:43 AM
# © 2017 - 2018 DAMGteam. All rights reserved