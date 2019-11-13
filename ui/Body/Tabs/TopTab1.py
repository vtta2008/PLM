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

# PyQt5
from PyQt5.QtWidgets        import QApplication
from PyQt5.QtGui import QResizeEvent

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

        prjButtons  = self.buttonManager.projectButtonsGroupBox(self.parent)
        taskButtons = self.buttonManager.taskButtonsGroupBox(self.parent)
        teamButtons = self.buttonManager.teamButtonsGroupBox(self.parent)

        self.infoGrp = GroupBox('Info')
        self.infoGrid = GridLayout()
        self.infoGrp.setLayout(self.infoGrid)
        self.infoGrp.setMinimumHeight(150)

        self.prjGrp      = GroupBox("Project", prjButtons, "BtnGrid")
        self.taskGrp     = GroupBox("Task", taskButtons, "BtnGrid")
        self.teamGrp     = GroupBox('Team', teamButtons, 'BtnGrid')

        self.layout.addWidget(self.infoGrp, 0, 0, 4, 6)
        self.layout.addWidget(self.prjGrp, 4, 0, 3, 2)
        self.layout.addWidget(self.taskGrp, 4, 2, 3, 2)
        self.layout.addWidget(self.teamGrp, 4, 4, 3, 2)

    # def resizeEvent(self, event):
    #     w = self.width()
    #     h = self.height()
    #
    #     self.infoGrp.resize(w-4, h/2-4)
    #
    #     for grp in [self.prjGrp, self.taskGrp, self.teamGrp]:
    #         grp.resize(w/3-4, h/2-4)


def main():
    app = QApplication(sys.argv)
    layout = TopTab1()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018