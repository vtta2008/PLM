#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Footer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, webbrowser

# PyQt5
from PyQt5.QtWidgets            import QApplication

# Plt
from appData                    import BTNTAGSIZE, TAGBTNSIZE
from ui.uikits.Widget                     import Widget
from ui.uikits.GridLayout import GridLayout
from ui.uikits.Button import Button
from ui.uikits.Label import Label

pythonPth = "https://docs.anaconda.com/anaconda/reference/release-notes/"
licencePth = "https://github.com/vtta2008/damgteam/blob/master/LICENCE"
versionPth = "https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst"

# -------------------------------------------------------------------------------------------------------------
""" Footer """

class Footer(Widget):

    key = 'Footer'

    def __init__(self, parent=None):
        super(Footer, self).__init__(parent)

        self.parent     = parent
        self.buildUI()


    def buildUI(self):
        layout          = GridLayout()

        btn1 = Button({'tag': 'python', 'fix': BTNTAGSIZE, 'ics': BTNTAGSIZE, 'emit2': [webbrowser.open, pythonPth]})
        btn2 = Button({'tag': 'licence', 'fix': BTNTAGSIZE, 'ics': BTNTAGSIZE, 'emit2': [webbrowser.open, licencePth]})
        btn3 = Button({'tag': 'version', 'fix': BTNTAGSIZE, 'ics': BTNTAGSIZE, 'emit2': [webbrowser.open, versionPth]})

        layout.addWidget(Label({'txt': " "}), 0, 0, 1, 1)
        layout.addWidget(Label({'txt': " "}), 0, 1, 1, 1)
        layout.addWidget(Label({'txt': " "}), 0, 2, 1, 1)
        layout.addWidget(Label({'txt': " "}), 0, 3, 1, 1)
        layout.addWidget(Label({'txt': " "}), 0, 4, 1, 1)
        layout.addWidget(Label({'txt': " "}), 0, 5, 1, 1)
        layout.addWidget(Label({'txt': " "}), 0, 6, 1, 1)

        layout.addWidget(btn1, 0, 7, 1, 1)
        layout.addWidget(btn2, 0, 8, 1, 1)
        layout.addWidget(btn3, 0, 9, 1, 1)

        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    layout = Footer()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/06/2018 - 4:24 AM