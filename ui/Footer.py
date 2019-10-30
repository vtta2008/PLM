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
from functools                              import partial

# PyQt5
from PyQt5.QtWidgets                        import QApplication

# Plt
from appData                                import BTNTAGSIZE
from ui.uikits.Widget                       import Widget
from ui.uikits.GridLayout                   import GridLayout
from ui.uikits.Button                       import Button
from ui.uikits.Label                        import Label



# -------------------------------------------------------------------------------------------------------------
""" Footer """

class Footer(Widget):

    key                 = 'Footer'

    tags = dict(python  = "https://docs.anaconda.com/anaconda/reference/release-notes/",
                licence = "https://github.com/vtta2008/damgteam/blob/master/LICENCE",
                version = "https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst")

    def __init__(self, parent=None):
        super(Footer, self).__init__(parent)

        self.parent     = parent
        self.buildUI()

    def buildUI(self):
        layout          = GridLayout()

        for i in range(7):
            layout.addWidget(Label({'txt': " "}), 0, i, 1, 1)
            i += 1

        for tag in ['python', 'licence', 'version']:
            layout.addWidget(self.createButton(tag), 0, i, 1, 1)
            i +=  1

        self.setLayout(layout)

    def createButton(self, tagName):

        if not tagName in self.tags.keys():
            print('KeyError: tag name is not existed: {0}'.format(tagName))
            button = Button()
        else:
            button = Button({'tag': tagName,
                             'fix': BTNTAGSIZE,
                             'ics': BTNTAGSIZE,
                             'cl' : partial(self.signals.openBrowser.emit, self.tags[tagName])})
        return button

def main():
    app = QApplication(sys.argv)
    layout = Footer()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/06/2018 - 4:24 AM