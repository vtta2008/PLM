# -*- coding: utf-8 -*-
"""

Script Name: ToolBarDock.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore       import Qt
from PyQt5.QtWidgets    import QDockWidget, QGridLayout

# PLM
from appData            import SiPoExp
from ui.uikits.ToolBar  import ToolBar
from ui.UiSignals       import UiSignals

# -------------------------------------------------------------------------------------------------------------
""" Tool bar docking class """

class DockToolBar(QDockWidget):

    key = 'dockToolBar'

    def __init__(self, name="TEXTURE", parent=None):
        super(DockToolBar, self).__init__(parent)

        self.name = name
        self.key = 'dockToolBar' + " {0}".format(self.name)
        self.setWindowTitle(self.name)
        self.signals = UiSignals(self)

        self.layout = QGridLayout()
        self.toolbar = ToolBar(self.name, self)
        self.toolbar.signals.executing.connect(self.signals.executing)

        self.layout.addWidget(self.toolbar, 0, 0, 1, 1)
        self.setLayout(self.layout)
        self.applySetting()

    def applySetting(self):
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setSizePolicy(SiPoExp, SiPoExp)

    def showEvent(self, event):
        pass

    def closeEvent(self, event):
        self.signals.regisLayout.emit(self)
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 21/07/2018 - 6:43 AM
# © 2017 - 2018 DAMGteam. All rights reserved