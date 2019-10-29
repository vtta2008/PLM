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
from ui.uikits.Button import Button
from ui.uikits.GroupBox import GroupBox
# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" TopTab2 """

class TopTab1(Widget):

    key = 'TopTab2'

    def __init__(self, parent=None):
        super(TopTab1, self).__init__(parent)

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.signals.regisLayout.emit(self)

    def buildUI(self):

        btn1 = Button({'txt':'New Project', 'tt':'New Project', 'cl':partial(self.signals.showLayout.emit, 'NewProject', 'show')})
        btn2 = Button({'txt':'Project List', 'tt':'Project List', 'cl':partial(self.signals.showLayout.emit, 'ProjectList', 'show')})
        btn3 = Button({'txt':'Config Project', 'tt':'Config Projects', 'cl':partial(self.signals.showLayout.emit, 'ConfigProject', 'show')})

        btn4 = Button({'txt':'New Task', 'tt':'New Task', 'cl':partial(self.signals.showLayout.emit, 'NewTask', 'show')})
        btn5 = Button({'txt':'Task List', 'tt':'Task List', 'cl':partial(self.signals.showLayout.emit, 'TaskList', 'show')})
        btn6 = Button({'txt':'Config Task', 'tt':'Config Task', 'cl':partial(self.signals.showLayout.emit, 'ConfigTask', 'show')})

        sec1Grp     = GroupBox("Project", [btn1, btn2, btn3], "BtnGrid")
        sec2Grp     = GroupBox("Task", [btn4, btn5, btn6], "BtnGrid")

        sec3Grp     = GroupBox('Info')
        sec3Grid    = GridLayout()

        sec3Grp.setLayout(sec3Grid)

        self.layout.addWidget(sec1Grp, 0, 0, 3, 3)
        self.layout.addWidget(sec2Grp, 3, 0, 3, 3)
        self.layout.addWidget(sec3Grp, 0, 3, 6, 6)

    def showEvent(self, event):
        self.signals.showLayout.emit(self.key, 'show')
        self.signals.showLayout.emit('TopTab3', 'hide')
        self.signals.showLayout.emit('TopTab5', 'hide')

def main():
    app = QApplication(sys.argv)
    layout = TopTab1()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018