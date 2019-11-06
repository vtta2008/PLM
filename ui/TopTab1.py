#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: TopTab2.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from functools              import partial

# PyQt5
from PyQt5.QtWidgets        import QApplication

# Plt
from ui.uikits.Widget                         import Widget
from ui.uikits.GridLayout import GridLayout
from ui.uikits.GroupBox import GroupBox
# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" TopTab2 """

class TopTab1(Widget):

    key = 'TopTab1'

    def __init__(self, buttonManager, parent=None):
        super(TopTab1, self).__init__(parent)

        self.buttonManager = buttonManager
        self.parent = parent

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.signals.regisLayout.emit(self)

    def buildUI(self):

        prjButtons = self.buttonManager.projectButtonsGroupBox(self.parent)
        teamButtons = self.buttonManager.teamButtonsGroupBox(self.parent)

        sec1Grp     = GroupBox("Project", prjButtons, "BtnGrid")
        sec2Grp     = GroupBox("Task", teamButtons, "BtnGrid")
        sec1Grp.setMaximumWidth(120)
        sec2Grp.setMaximumWidth(120)

        sec3Grp     = GroupBox('Info')
        sec3Grid    = GridLayout()
        sec3Grp.setLayout(sec3Grid)

        self.layout.addWidget(sec1Grp, 0, 0, 4, 3)
        self.layout.addWidget(sec2Grp, 4, 0, 4, 3)
        self.layout.addWidget(sec3Grp, 0, 3, 8, 6)

def main():
    app = QApplication(sys.argv)
    layout = TopTab1()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018