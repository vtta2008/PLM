#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""

# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from bin.Widgets import Widget, VBoxLayout
from bin.Gui import AppIcon
from PLM.ui.components import HeaderCheckBoxes, FooterCheckBoxes, BodyCheckBoxes

# -------------------------------------------------------------------------------------------------------------
""" Preferences window """

class Preferences(Widget):

    key = 'Preferences'

    _msg_user_not_set                   = "Not configured yet, will be set with the first message received"

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)
        self.layout                     = VBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.header                     = HeaderCheckBoxes('Header', self)
        self.body                       = BodyCheckBoxes('Body', self)
        self.footer                     = FooterCheckBoxes('Footer', self)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.body)
        self.layout.addWidget(self.footer)

    def showEvent(self, event):
        self.resize(574, 252)
        self.resize(575, 252)

    def resizeEvent(self, event):
        for gp in [self.header, self.body, self.footer]:
            gp.setMaximumWidth(self.width())
            gp.setMaximumHeight(self.height()/3)


# from PyQt5.QtWidgets import QApplication
# import sys
#
# app = QApplication(sys.argv)
# win = Preferences()
# win.show()
# sys.exit(app.exec_())