# -*- coding: utf-8 -*-
"""

Script Name: InfoWidget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import sys
from PyQt5.QtWidgets import QApplication

from ui.uikits.Icon import AppIcon
from appData import (SiPoMin, PLM_ABOUT, CODECONDUCT, CONTRIBUTING, CREDIT, LICENCE_MIT, REFERENCE, VERSION)

from ui.uikits.Widget import Widget
from ui.uikits.GridLayout import GridLayout
from ui.uikits.Label import Label
from ui.uikits.Button import Button

class InfoWidget(Widget):

    content = dict(
        About               = PLM_ABOUT,
        CodeOfConduct       = CODECONDUCT,
        Contributing        = CONTRIBUTING,
        Credit              = CREDIT,
        Licence             = LICENCE_MIT,
        Reference           = REFERENCE,
        Version             = VERSION
    )

    def __init__(self, key=None, parent=None):
        super(InfoWidget, self).__init__(parent)

        self.key = key
        self.parent = parent

        if self.key is None or self.key not in self.content.keys():
            print("KeyError: Key is None, or not in content data: {0}".format(self.key))
            return
        else:
            self.context = self.content[self.key]

        self.setWindowTitle(self.key)
        self.setWindowIcon(AppIcon(32, self.key))

        self.layout             = GridLayout(self)
        label                   = Label({'txt': self.content[self.key]})
        btn                     = Button({'txt': 'Ok', 'cl': self.close})

        self.layout.addWidget(label,    0, 0, 6, 6)
        self.layout.addWidget(btn,      6, 6, 1, 1)

        self.setLayout(self.layout)
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.setContentsMargins(1,1,1,1)

if __name__=='__main__':
    from appData import PLM_ABOUT
    app = QApplication(sys.argv)
    window = InfoWidget('About', PLM_ABOUT)
    window.show()
    app.exec_()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/10/2019 - 3:52 AM
# © 2017 - 2018 DAMGteam. All rights reserved