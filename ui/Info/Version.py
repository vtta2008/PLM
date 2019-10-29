# -*- coding: utf-8 -*-
"""
Script Name: Credit.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Credit infomation.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from functools import partial

# PtQt5
from PyQt5.QtWidgets import QApplication, QScrollArea

# Plm
from appData import VERSION
from ui.uikits.Widget                         import Widget
from ui.uikits.Icon import AppIcon
from ui.uikits.Button import Button
from ui.uikits.Label import Label
from ui.uikits.GridLayout import GridLayout
# -------------------------------------------------------------------------------------------------------------
""" Contributing Layout """

class Version(Widget):

    key = 'version'

    def __init__(self, parent=None):

        super(Version, self).__init__(parent)
        self.setWindowIcon(AppIcon(32, 'Version'))

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.resize(450, 150)

    def buildUI(self):
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        TXT = """
            {0}
            
            Version will start from v13 and never change number 13.
            Current stage: Test Beta.
            Warning: Not stable, a lot of bugs.
            Status: Under developing
            
            """.format(VERSION)

        self.content = Label({'txt':TXT, 'alg':'left', 'link': True})

        self.content.setGeometry(0, 0, 450, 150)
        self.scrollArea.setWidget(self.content)

        closeBtn = Button({'txt': 'Close', 'tt': 'Close window', 'cl': partial(self.signals.showLayout.emit, self.key, 'hide')})

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(closeBtn, 8, 3, 1, 1)

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

def main():
    app = QApplication(sys.argv)
    about_layout = Version()
    about_layout.show()
    app.exec_()

if __name__=='__main__':
    main()