#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: TopTab5.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, subprocess

# PyQt5
from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QComboBox

# Plt
import appData as app

from ui import uirc as rc

from utilities import utils as func
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" TopTab5 """

class TopTab5(QWidget):

    def __init__(self, parent=None):
        super(TopTab5, self).__init__(parent)
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.basePth = os.path.join(os.getenv(app.__envKey__), 'appData', '__core')

        step1 = ["Create New", "Create django project"]
        step2 = ["Create app", "Create django app"]
        step3 = ["Start Server", "Operate running server"]
        step4 = ["Save preset", "Save app preset"]
        step5 = ["Run Preset", "Create data tables"]
        step6 = ["Create SQL", "Create database"]
        step7 = ["Create Admin", "Create Admin Account"]

        self.dataField = QLineEdit("pSite__")
        self.appNameLst = QComboBox()
        self.appNumberLst = QComboBox()

        self.update_migrations()

        btn1 = rc.Button(step1)
        btn2 = rc.Button(step2)
        btn3 = rc.Button(step3)
        btn4 = rc.Button(step4)
        btn5 = rc.Button(step5)
        btn6 = rc.Button(step6)
        btn7 = rc.Button(step7)

        btn1.clicked.connect(self.step1)
        btn2.clicked.connect(self.step2)
        btn3.clicked.connect(self.step3)
        btn4.clicked.connect(self.step4)
        btn5.clicked.connect(self.step5)
        btn6.clicked.connect(self.step6)
        btn7.clicked.connect(self.step7)

        self.btns = [btn1, btn2, btn3, btn4, btn5, btn6]

        self.layout.addWidget(self.dataField, 0, 0, 1, 1)
        self.layout.addWidget(self.appNameLst, 0, 1, 1, 1)
        self.layout.addWidget(self.appNumberLst, 0, 2, 1, 1)

        self.layout.addWidget(btn1, 1, 0, 1, 1)
        self.layout.addWidget(btn2, 1, 1, 1, 1)
        self.layout.addWidget(btn3, 1, 2, 1, 1)
        self.layout.addWidget(btn4, 2, 0, 1, 1)
        self.layout.addWidget(btn5, 2, 1, 1, 1)
        self.layout.addWidget(btn6, 2, 2, 1, 1)
        self.layout.addWidget(btn7, 3, 0, 1, 1)

        self.applySetting()

    def step1(self):
        subprocess.Popen("start /wait django-admin startproject {0}".format(self.dataField.text()), cwd=self.basePth)

    def step2(self):
        subprocess.Popen("start /wait python manage.py startapp {0}".format(self.dataField.text()), cwd=self.basePth)
        self.update_migrations()

    def step3(self):
        subprocess.Popen("start /wait python manage.py runserver", cwd=self.basePth)

    def step4(self):
        subprocess.Popen("start /wait python manage.py makemigrations", cwd=os.path.join(self.base, self.appNameLst.currentText()))
        self.update_migrations()

    def step5(self):
        subprocess.Popen("start /wait python manage.py sqlmigrate {0}".format(self.appNumberLst.currentText()), cwd=os.path.join(self.basePth, self.appNumberLst.currentText()))
        self.update_migrations()

    def step6(self):
        subprocess.Popen("start /wait python manage.py migrate")

    def step7(self):
        subprocess.Popen("start /wait python manage.py createsuperuser")

    def update_migrations(self):

        dirs = [p for p in func.get_folder_path(self.basePth) if 'migrations' in p] or []

        fileLst = []
        if not len(dirs) == 0:
            for dir in dirs:
                files = [f for f in func.get_file_path(dir) if not '__init__' in f] or []
                fileLst = fileLst + files

        print(dirs)
        print(fileLst)
        appLst = [os.path.basename(d.split("migrations")[0]) for d in dirs] or []
        numberLst = [os.path.basename(f) for f in fileLst] or []

        self.appNameLst.addItems(appLst)
        self.appNumberLst.addItems(numberLst)


    def applySetting(self):
        self.layout.setSpacing(2)
        self.setSizePolicy(app.SiPoMin, app.SiPoMin)

        for widget in [self.dataField, self.appNameLst, self.appNumberLst] + self.btns:
            # widget.setFixedWidth((self.width()-30)/3)
            widget.setSizePolicy(app.SiPoMin, app.SiPoMin)
            widget.setFixedHeight(25)

def main():
    app = QApplication(sys.argv)
    layout = TopTab5()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 26/05/2018 - 1:41 AM