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
import sys

# PyQt5
from PyQt5.QtWidgets            import QApplication

# Plt
from appData                    import SiPoMin, __copyright__, __version__
from ui.uikits.Widget           import Widget
from ui.uikits.GridLayout       import GridLayout
from ui.uikits.UiPreset         import Label

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

        version         = Label({'txt': __version__, 'alg': 'right'})
        copyR           = Label({'txt': __copyright__, 'alg': 'right'})

        layout.addWidget(version, 0, 0, 1, 9)
        layout.addWidget(copyR, 1, 0, 1, 9)
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