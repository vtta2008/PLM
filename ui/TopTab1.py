#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: topTab1.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import json, os, sys

# PyQt5
from PyQt5.QtWidgets                import QApplication

# Plt
from appData                        import (__envKey__, CONFIG_TOOLS, CONFIG_DEV, CONFIG_EXTRA, CONFIG_OFFICE, BTNICONSIZE,
                                            ICONBTNSIZE, FIX_KEYS)
from ui.uikits.Widget                         import Widget
from ui.uikits.GridLayout import GridLayout
from ui.uikits.Button import Button
from ui.uikits.GroupBox import GroupBox
from ui.uikits.LineEdit import LineEdit

# -------------------------------------------------------------------------------------------------------------
""" topTab1 """

class TopTab1(Widget):

    key = 'TopTab1'

    with open(os.path.join(os.getenv(__envKey__), 'appData/.config', 'main.cfg'), 'r') as f:
        appInfo = json.load(f)

    def __init__(self, parent=None):
        super(TopTab1, self).__init__(parent)

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

        self.signals.regisLayout.emit(self)

    def buildUI(self):

        officeBtns = []
        keys = ['TextEditor', 'NoteReminder']
        for key in keys:
            if key in self.appInfo:
                btn = Button({'icon':key, 'tt': self.appInfo[key][2], 'fix': BTNICONSIZE, 'ics': ICONBTNSIZE, 'emit2':[self.signals.showLayout.emit, [FIX_KEYS[key], 'show']]})
                officeBtns.append(btn)

        for key in CONFIG_OFFICE:
            if key in self.appInfo:
                btn = Button({'icon': key, 'tt': self.appInfo[key][2], 'fix': BTNICONSIZE, 'ics': ICONBTNSIZE, 'emit1': [self.signals.executing.emit, self.appInfo[key][2]]})
                officeBtns.append(btn)

        devBtns = []
        for key in CONFIG_DEV:
            if key in self.appInfo:
                btn = Button({'icon': key, 'tt': self.appInfo[key][2], 'fix': BTNICONSIZE, 'ics': ICONBTNSIZE, 'emit1': [self.signals.executing.emit, self.appInfo[key][2]]})
                devBtns.append(btn)

        pyuiBtn = []
        for key in CONFIG_TOOLS:
            if key in self.appInfo:
                btn = Button({'icon': key, 'tt': self.appInfo[key][2], 'fix': BTNICONSIZE, 'ics': ICONBTNSIZE, 'emit2': [self.signals.showLayout.emit, [FIX_KEYS[key], 'show']]})
                pyuiBtn.append(btn)

        extraBtns = []
        for key in CONFIG_EXTRA:
            if key in self.appInfo:
                btn = Button({'icon': key, 'tt': self.appInfo[key][2], 'fix': BTNICONSIZE, 'ics': ICONBTNSIZE, 'emit2': [self.signals.executing.emit, key]})
                extraBtns.append(btn)

        sec1Grp = GroupBox("Office", officeBtns, "IconGrid")
        sec2Grp = GroupBox("Dev", devBtns, "IconGrid")
        sec3Grp = GroupBox("Tools", pyuiBtn, "IconGrid")
        sec4Grp = GroupBox("Extra", extraBtns, "IconGrid")

        self.findEdit = LineEdit()
        findBtn = Button({'txt':"Find Tool"})

        sec5Grp = GroupBox("Find Tool")
        sec5Grid = GridLayout()
        sec5Grid.addWidget(self.findEdit, 0, 0, 1, 7)
        sec5Grid.addWidget(findBtn, 0, 7, 1, 2)
        sec5Grp.setLayout(sec5Grid)

        self.layout.addWidget(sec1Grp, 0, 0, 2, 3)
        self.layout.addWidget(sec2Grp, 2, 0, 2, 3)
        self.layout.addWidget(sec3Grp, 0, 3, 4, 3)
        self.layout.addWidget(sec4Grp, 0, 6, 4, 3)
        self.layout.addWidget(sec5Grp, 4, 0, 1, 9)

def main():
    app = QApplication(sys.argv)
    layout = TopTab1()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018