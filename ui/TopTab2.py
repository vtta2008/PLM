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
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QGroupBox

# Plt
# from ui.uirc import AutoSectionBtnGrp
from ui.lib.LayoutPreset import Button, GroupBox
from core.Specs import Specs

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" TopTab2 """

class TopTab2(QWidget):
    addLayout = pyqtSignal(object)
    executing = pyqtSignal(str)
    showLayout = pyqtSignal(str, str)

    key = 'topTab2'

    def __init__(self, parent=None):
        super(TopTab2, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.addLayout.emit(self)

    def buildUI(self):

        btn1 = Button({'txt':'New Project', 'tt':'Create New Project', 'cl':partial(self.showLayout.emit, 'newProj', 'show')})
        btn2 = Button({'txt':'New Group', 'tt':'Create New Group', 'cl':partial(self.showLayout.emit, 'newGrp', 'show')})
        btn3 = Button({'txt':'Your Projects', 'tt':'Your Projects', 'cl':partial(self.showLayout.emit, 'yourPrj', 'show')})
        btn4 = Button({'txt':'Find crew', 'tt':'Find crew', 'cl':partial(self.showLayout.emit, 'findCrew', 'show')})
        btn5 = Button({'txt':'Get crew', 'tt':'Check applicant', 'cl':partial(self.showLayout.emit, 'getCrew', 'show')})
        btn6 = Button({'txt':'Your crew', 'tt':'Your crew', 'cl':partial(self.showLayout.emit, 'yourCrew', 'show')})

        sec1Grp = GroupBox("Project", [btn1, btn2, btn3], "BtnGrid")
        sec2Grp = GroupBox("Crew", [btn4, btn5, btn6], "BtnGrid")

        sec3Grp = QGroupBox('Info')
        sec3Grid = QGridLayout()
        sec3Grp.setLayout(sec3Grid)

        self.layout.addWidget(sec1Grp, 0, 0, 3, 3)
        self.layout.addWidget(sec2Grp, 3, 0, 3, 3)
        self.layout.addWidget(sec3Grp, 0, 3, 6, 6)


def main():
    app = QApplication(sys.argv)
    layout = TopTab2()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018