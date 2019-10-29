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

# PtQt5
from PyQt5.QtWidgets import QApplication, QScrollArea

# Plm
from appData import LICENCE_MIT
from ui.uikits.Widget                         import Widget
from ui.uikits.Icon import AppIcon
from ui.uikits.Button import Button
from ui.uikits.Label import Label
from ui.uikits.GridLayout import GridLayout

# -------------------------------------------------------------------------------------------------------------
""" Contributing Layout """

class LicenceMIT(Widget):

    key = 'licenceMIT'

    def __init__(self, parent=None):

        super(LicenceMIT, self).__init__(parent)
        self.setWindowIcon(AppIcon(32, 'Licence'))
        self.setWindowTitle('LICENCE')

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.resize(500, 400)

    def buildUI(self):

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = Label({'txt':LICENCE_MIT, 'alg': 'left', 'link': True})

        self.content.setGeometry(0, 0, 500, 400)
        self.scrollArea.setWidget(self.content)

        closeBtn = Button({'txt': 'Close', 'tt': 'Close window', 'cl': self.close})

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(closeBtn, 8, 3, 1, 1)

def main():
    app = QApplication(sys.argv)
    about_layout = InfoWidget(LicenceMIT)
    about_layout.show()
    app.exec_()

if __name__=='__main__':
    main()