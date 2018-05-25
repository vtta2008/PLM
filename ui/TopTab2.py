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
import os, sys, logging

# PyQt5
from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QGroupBox

# Plt
import appData as app
from ui import uirc as rc
from utilities import utils as func
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
# Get apps info config
APPINFO = func.preset_load_appInfo()

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" TopTab2 """

class TopTab2(QWidget):
    TopTab2Sig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(TopTab2, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.appInfo = func.preset_load_appInfo()

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        btn1 = QPushButton('New Project')
        btn1.clicked.connect(self.on_newProjBtbn_clicked)
        btn2 = QPushButton('New Group')
        btn2.clicked.connect(self.on_newGrpBtn_clicked)
        btn3 = QPushButton('Your Projects')
        btn3.clicked.connect(self.on_prjLstBtn_clicked)

        btn4 = QPushButton('Find crew')
        btn4.clicked.connect(self.on_recruitBtn_clicked)
        btn5 = QPushButton('Get crew')
        btn5.clicked.connect(self.on_getCrewBtn_clicked)
        btn6 = QPushButton('Your crew')
        btn6.clicked.connect(self.on_crewLstBtn_clicked)

        btns1 = [btn1, btn2, btn3]
        btns2 = [btn4, btn5, btn6]
        sec1Grp = rc.AutoSectionBtnGrp("Project", btns1, "BtnGrid")
        sec2Grp = rc.AutoSectionBtnGrp("Crew", btns2, "BtnGrid")

        sec3Grp = QGroupBox('Info')
        sec3Grid = QGridLayout()
        sec3Grp.setLayout(sec3Grid)

        self.layout.addWidget(sec1Grp, 0, 0, 3, 3)
        self.layout.addWidget(sec2Grp, 3, 0, 3, 3)
        self.layout.addWidget(sec3Grp, 0, 3, 6, 6)

        self.applySetting()

    def applySetting(self):
        pass

    def on_newProjBtbn_clicked(self):
        from ui import NewProject
        app.reload(NewProject)
        layout = NewProject.NewProject()
        layout.show()
        layout.exec_()

    def on_newGrpBtn_clicked(self):
        pass

    def on_prjLstBtn_clicked(self):
        pass

    def on_recruitBtn_clicked(self):
        pass

    def on_getCrewBtn_clicked(self):
        pass

    def on_crewLstBtn_clicked(self):
        pass

def main():
    app = QApplication(sys.argv)
    layout = TopTab2()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018