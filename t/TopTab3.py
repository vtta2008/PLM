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
import os, subprocess, sys

# PyQt5
from PyQt5.QtCore                               import pyqtSlot, QProcess, QStandardPaths
from PyQt5.QtWidgets                            import QApplication, QTextEdit, QTextBrowser

# Plt
from appData                                    import SiPoMin, SiPoExp
from ui.uikits.Widget                           import Widget
from ui.uikits.GridLayout                       import GridLayout
from ui.uikits.Button                           import Button
from ui.uikits.LineEdit                         import LineEdit
from ui.uikits.Label                            import Label

# -------------------------------------------------------------------------------------------------------------
""" Sub class """

class CommandPrompt(LineEdit):

    def __init__(self, parent=None):
        super(CommandPrompt, self).__init__(parent)

        self.setSizePolicy(SiPoMin, SiPoMin)
        self.setMaximumHeight(25)

class Terminal(QTextBrowser):

    def __init__(self, parent=None):
        super(Terminal, self).__init__(parent)

        self.setFrameStyle(QTextEdit.DrawWindowBackground)
        self.setSizePolicy(SiPoExp, SiPoExp)

# -------------------------------------------------------------------------------------------------------------
""" TopTab5 """

class TopTab3(Widget):

    key = 'TopTab3'

    def __init__(self, buttonManager, parent=None):
        super(TopTab3, self).__init__(parent)

        self.buttonManager = buttonManager
        self.parent = parent
        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.signals.regisLayout.emit(self)

    def buildUI(self):
        self.basePth = os.getcwd() + ">"

        # self.cmdBtn = Button({'txt': 'Run', 'stt': 'Execute command', 'cl': self.on_btn_clicked})
        # self.cmdBtn.clicked.connect(self.on_btn_clicked)
        # self.cmdBtn.setAutoDefault(True)

        self.terminal = Terminal()
        self.cmdConsole = CommandPrompt()
        self.cmdConsole.returnPressed.connect(self.release_command)

        self.layout.addWidget(self.terminal, 0, 0, 7, 6)
        self.layout.addWidget(self.cmdConsole, 7, 0, 1, 6)

    def release_command(self):
        txt = self.cmdConsole.text()
        text = os.getcwd() + ">" + txt + "\n"
        self.terminal.insertPlainText(text)
        self.update_terminal(txt)

    def update_terminal(self, cmd):
        self.terminal.insertPlainText(subprocess.getoutput(cmd=cmd) + "\n")

def main():
    app = QApplication(sys.argv)
    layout = TopTab3()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 26/05/2018 - 1:41 AM