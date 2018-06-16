#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: TopTab5.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    Tab 5 layout
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, subprocess

# PyQt5
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QTextEdit, QTextBrowser, QLabel

# Plt
import appData as app

from ui import uirc as rc

from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Sub class """

class CommandPrompt(QLineEdit):

    def __init__(self, parent=None):
        super(CommandPrompt, self).__init__(parent)

        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(app.SiPoMin, app.SiPoMin)

class Terminal(QTextBrowser):

    def __init__(self, parent=None):
        super(Terminal, self).__init__(parent)

        self.applySetting()

    def applySetting(self):
        self.setFrameStyle(QTextEdit.DrawWindowBackground)
        self.setSizePolicy(app.SiPoExp, app.SiPoExp)

# -------------------------------------------------------------------------------------------------------------
""" TopTab5 """

class TopTab5(QWidget):

    def __init__(self, parent=None):
        super(TopTab5, self).__init__(parent)

        self.appSetting = app.APPSETTING

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.basePth = os.getcwd() + ">"

        self.cmdBtn = rc.Button(["Run", "Excute command"])
        self.cmdBtn.clicked.connect(self.on_btn_clicked)
        self.cmdBtn.setAutoDefault(True)

        self.terminal = Terminal()
        self.cmdConsole = CommandPrompt()
        self.cmdConsole.returnPressed.connect(self.cmdBtn.click)

        self.layout.addWidget(self.terminal, 0, 0, 4, 8)
        self.layout.addWidget(self.cmdConsole, 4, 0, 1, 6)
        self.layout.addWidget(self.cmdBtn, 4, 6, 1, 2)

        btn1 = rc.Button(["Create New", "Create django project"])
        btn2 = rc.Button(["Create app", "Create django app"])
        btn3 = rc.Button(["Start Server", "Operate running server"])
        btn4 = rc.Button(["Save preset", "Save app preset"])
        btn5 = rc.Button(["Run Preset", "Create data tables"])
        btn6 = rc.Button(["Create SQL", "Create database"])
        btn7 = rc.Button(["Create Admin", "Create Admin Account"])

        self.layout.addWidget(QLabel())

        self.layout.addWidget(btn1, 6, 0, 1, 2)
        self.layout.addWidget(btn2, 6, 2, 1, 2)
        self.layout.addWidget(btn3, 6, 4, 1, 2)
        self.layout.addWidget(btn4, 6, 6, 1, 2)
        self.layout.addWidget(btn5, 7, 0, 1, 2)
        self.layout.addWidget(btn6, 7, 2, 1, 2)
        self.layout.addWidget(btn7, 7, 4, 1, 2)

        self.applySetting()

    @pyqtSlot()
    def on_btn_clicked(self):
        self.release_command(self.cmdConsole.text())

    def release_command(self, cmd):
        text = os.getcwd() + ">" + cmd + "\n"
        self.terminal.insertPlainText(text)
        self.update_terminal(cmd)

    def update_terminal(self, cmd):
        self.terminal.insertPlainText(subprocess.getoutput(cmd=cmd) + "\n")

    def applySetting(self):
        self.layout.setSpacing(2)
        self.setSizePolicy(app.SiPoMin, app.SiPoMin)

def main():
    app = QApplication(sys.argv)
    layout = TopTab5()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 26/05/2018 - 1:41 AM