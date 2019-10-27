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
from appData import REFERENCE
from ui import Button, Label, Widget, AppIcon, Widget, GridLayout

# -------------------------------------------------------------------------------------------------------------
""" Contributing Layout """

class Reference(Widget):

    key = 'reference'

    def __init__(self, parent=None):

        super(Reference, self).__init__(parent)
        self.setWindowIcon(AppIcon(32, 'Reference'))
        self.setWindowTitle('REFERENCE')

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.resize(450, 400)

    def buildUI(self):
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = Label({'txt':REFERENCE, 'alg':'left', 'link': True})

        self.content.setGeometry(0, 0, 450, 400)
        self.scrollArea.setWidget(self.content)

        closeBtn = Button({'txt': 'Close', 'tt': 'Close window', 'cl': partial(self.signals.showLayout.emit, self.key, 'hide')})

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(closeBtn, 8, 3, 1, 1)

def main():
    app = QApplication(sys.argv)
    about_layout = Reference()
    about_layout.show()
    app.exec_()

if __name__=='__main__':
    main()