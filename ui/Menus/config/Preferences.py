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

# Python
import sys

# PyQt5
from PyQt5.QtWidgets        import QApplication

# Plt
from utils.utils            import str2bool, bool2str
from ui.uikits.Widget                         import Widget
from ui.uikits.Icon import AppIcon
from ui.uikits.CheckBox import CheckBox
from ui.uikits.Button import Button
from ui.uikits.MessageBox import MessageBox
from ui.uikits.Label import Label, usernameLabel, passwordLabel
from ui.uikits.GridLayout import GridLayout
from ui.uikits.LineEdit import LineEdit
from ui.uikits.GroupBox import GroupGrid

# -------------------------------------------------------------------------------------------------------------
""" Preferences window """

class GeneralSetting(GridLayout):

    key = 'GeneralSetting'

    def __init__(self, parent=None):

        super(GeneralSetting, self).__init__(parent)

        self.buildUI()

    def buildUI(self):

        self.tbTDCB         = CheckBox(txt="TD toolbar")
        self.tbCompCB       = CheckBox(txt="Comp toolbar")
        self.tbArtCB        = CheckBox(txt="Art toolbar")

        self.tbTexCB        = CheckBox(txt="Tex toolbar")
        self.tbPostCB       = CheckBox(txt='Post toolbar')
        self.mainToolBarCB  = CheckBox(txt="Main Toolbar")

        self.statusBarCB    = CheckBox(txt="Status Bar")
        self.connectStatuCB = CheckBox(txt="Connect Status")
        self.notifiCB       = CheckBox(txt="Notification")

        self.addWidget(self.tbTDCB, 0, 0, 1, 2)
        self.addWidget(self.tbCompCB, 1, 0, 1, 2)
        self.addWidget(self.tbArtCB, 2, 0, 1, 2)

        self.addWidget(self.tbTexCB, 0, 2, 1, 2)
        self.addWidget(self.tbPostCB, 1, 2, 1, 2)
        self.addWidget(self.mainToolBarCB, 2, 2, 1, 2)

        self.addWidget(self.statusBarCB, 0, 4, 1, 2)
        self.addWidget(self.connectStatuCB, 1, 4, 1, 2)
        self.addWidget(self.notifiCB, 2, 4, 1, 2)

        self.addWidget(Button({'txt': 'Close', 'cl': self.parent.close}), 3, 4, 1, 1)

        self.checkBoxes = [self.tbTDCB, self.tbCompCB, self.tbArtCB, self.tbTexCB, self.tbPostCB,
                           self.mainToolBarCB, self.statusBarCB, self.connectStatuCB, self.notifiCB]

        self.keys = ['toolbarTD', 'toolbarComp', 'toolbarArt', 'toolbarTex', 'toolbarPost', 'subToolbar',
                     'toolbarMain', 'toolbarStatus', 'toolbarSubMenu', 'toolbarConnect', 'toolbarNotifi']


class Preferences(Widget):

    key = 'Preferences'

    _msg_user_not_set = "Not configured yet, will be set with the first message received"

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        # self.resize(200, 100)
        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)
        self.layout = GeneralSetting(self)
        self.setLayout(self.layout)




def main():
    app = QApplication(sys.argv)
    pref_layout = Preferences()
    pref_layout.show()
    app.exec_()

if __name__=='__main__':
    main()

