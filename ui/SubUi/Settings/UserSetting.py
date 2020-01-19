#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ui_acc_setting.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    Setting your account.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Plt
from devkit.Widgets                 import Widget, GridLayout
from devkit.Gui                     import AppIcon
from ui.base                        import Profile, Location, Avatar, PassWord

# ----------------------------------------------------------------------------------------------------------- #
""" User setting layout """

class UserSetting(Widget):

    key                             = 'UserSetting'

    def __init__(self, parent=None):
        super(UserSetting, self).__init__(parent)

        self.setWindowIcon(AppIcon(32, "UserSetting"))
        self.layout                 = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.avatarGrp                 = Avatar(self)
        self.password               = PassWord(self)
        self.profile                = Profile(self)
        self.location               = Location(self)

        self.layout.addWidget(self.avatarGrp, 0, 0, 1, 1)
        self.layout.addWidget(self.password, 0, 1, 1, 1)
        self.layout.addWidget(self.profile, 1, 0, 1, 1)
        self.layout.addWidget(self.location, 1, 1, 1, 1)

    def resizeEvent(self, event):
        for gb in [self.avatarGrp, self.password, self.profile, self.location]:
            gb.setMaximumHeight(self.height()/2)
            gb.setMaximumWidth(self.width()/2)


