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
from toolkits.Widgets               import Widget, GridLayout, AppIcon
from .base                          import PassWord, Avatar, ProFile, Location

# ----------------------------------------------------------------------------------------------------------- #
""" User setting layout """

class UserSetting(Widget):

    key                             = 'UserSetting'

    def __init__(self, parent=None):
        super(UserSetting, self).__init__(parent)

        self.setWindowIcon(AppIcon(32, "UserSetting"))
        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.avatar = Avatar(self)
        self.password = PassWord(self)
        self.profile = ProFile(self)
        self.location = Location(self)

        self.layout.addWidget(self.avatar, 0, 0, 1, 1)
        self.layout.addWidget(self.password, 0, 1, 1, 1)
        self.layout.addWidget(self.profile, 1, 0, 1, 1)
        self.layout.addWidget(self.location, 1, 1, 1, 1)


