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
import os
import subprocess
import sys

# PyQt5
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QTextEdit, QTextBrowser, QLabel

# Plt
from cores.Loggers import Loggers
from cores.base import DAMG
from cores.paths import SiPoMin, SiPoExp
from ui.uikits.Button import Button

# -------------------------------------------------------------------------------------------------------------
""" Sub class """

class CommandPrompt(QLineEdit):

    def __init__(self, parent=None):
        super(CommandPrompt, self).__init__(parent)

        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)

class Terminal(QTextBrowser):

    def __init__(self, parent=None):
        super(Terminal, self).__init__(parent)

        self.applySetting()

    def applySetting(self):
        self.setFrameStyle(QTextEdit.DrawWindowBackground)
        self.setSizePolicy(SiPoExp, SiPoExp)

# -------------------------------------------------------------------------------------------------------------
""" TopTab5 """

class TopTab5(QWidget):

    key = 'topTab5'
    executing = pyqtSignal(str)
    showLayout = pyqtSignal(str, str)
    addLayout = pyqtSignal(DAMG)

    def __init__(self, parent=None):
        super(TopTab5, self).__init__(parent)
        self.logger = Loggers(self)
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.addLayout.emit(self)

    def buildUI(self):
        self.basePth = os.getcwd() + ">"

        self.cmdBtn = Button({'txt': 'Run', 'stt': 'Execute command', 'cl': self.on_btn_clicked})
        # self.cmdBtn.clicked.connect(self.on_btn_clicked)
        # self.cmdBtn.setAutoDefault(True)

        self.terminal = Terminal()
        self.cmdConsole = CommandPrompt()
        self.cmdConsole.returnPressed.connect(self.cmdBtn.click)

        self.layout.addWidget(self.terminal, 0, 0, 4, 8)
        self.layout.addWidget(self.cmdConsole, 4, 0, 1, 6)
        self.layout.addWidget(self.cmdBtn, 4, 6, 1, 2)

        btn1 = Button({'txt': "Create New", 'stt': "Create django project"})
        btn2 = Button({'txt': "Create app", 'stt': "Create django app"})
        btn3 = Button({'txt': "Start Server", 'stt': "Operate running server"})
        btn4 = Button({'txt': "Save preset", 'stt': "Save app preset"})
        btn5 = Button({'txt': "Run Preset", 'stt': "Create data tables"})
        btn6 = Button({'txt': "Create SQL", 'stt': "Create database"})
        btn7 = Button({'txt': "Create Admin", 'stt': "Create Admin Account"})

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
        self.setSizePolicy(SiPoMin, SiPoMin)

def main():
    app = QApplication(sys.argv)
    layout = TopTab5()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 26/05/2018 - 1:41 AM