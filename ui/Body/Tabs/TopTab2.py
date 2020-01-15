#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: TopTab3.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtGui                import QPixmap

# Plt
from devkit.Widgets             import Widget, GridLayout, GroupBox, GroupGrid
from ui.base                    import Avatar
from utils                      import get_avatar_image, LocalDatabase

# -------------------------------------------------------------------------------------------------------------
""" TopTab3 """

class TopTab2(Widget):

    key = 'TopTab2'

    def __init__(self, buttonManager, parent=None):
        super(TopTab2, self).__init__(parent)

        self.buttonManager      = buttonManager
        self.parent             = parent
        self.layout             = GridLayout()
        self.query              = LocalDatabase()

        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        try:
            self.username, token, cookie, remember = self.query.query_table('curUser')
        except (ValueError, IndexError):
            self.username = 'DemoUser'

        self.avatarGrp           = Avatar(self)

        self.avatarBtn          = self.buttonManager.userButtonGroupBox(self.parent)
        self.settingGrp         = GroupBox("Setting", self.avatarBtn, "BtnGrid")
        self.messGrp            = GroupGrid("Messenger")

        self.settingGrp.setMaximumWidth(120)
        self.avatarGrp.setMaximumSize(120, 180)
        self.messGrp.setMinimumWidth(380)

        self.layout.addWidget(self.avatarGrp, 0, 0, 1, 1)
        self.layout.addWidget(self.settingGrp, 1, 0, 1, 1)
        self.layout.addWidget(self.messGrp, 0, 1, 2, 2)

    def update_avatar(self, param):
        if param:
            self.username, token, cookie, remember = self.query.query_table('curUser')
            self.avatar.setPixmap(QPixmap(get_avatar_image(self.username)))
            self.avatar.update()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018