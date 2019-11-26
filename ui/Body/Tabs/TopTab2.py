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
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui                import QPixmap
from PyQt5.QtWidgets            import ( QLabel, QGraphicsScene)

# Plt
from ui.uikits.Widget           import Widget
from ui.uikits.GridLayout       import GridLayout
from ui.uikits.GroupBox         import GroupBox, GroupGrid
from utils                      import localSQL as usql
from utils                      import get_avatar_image

# -------------------------------------------------------------------------------------------------------------
""" TopTab3 """

class TopTab2(Widget):

    key = 'TopTab2'

    def __init__(self, buttonManager, parent=None):
        super(TopTab2, self).__init__(parent)

        self.buttonManager = buttonManager
        self.parent = parent
        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

        self.signals.regisLayout.emit(self)

    def buildUI(self):
        self.query = usql.QuerryDB()
        try:
            self.username, token, cookie, remember = self.query.query_table('curUser')
        except (ValueError, IndexError):
            self.username = 'DemoUser'

        self.avatar = QLabel()
        self.avatar.setPixmap(QPixmap(get_avatar_image(self.username)))
        self.avatar.setScaledContents(True)
        self.avatar.setFixedSize(100, 100)
        self.avatarGrp = GroupBox(self.username, [self.avatar], "ImageView")

        self.avatarBtn = self.buttonManager.userButtonGroupBox(self.parent)
        self.settingGrp = GroupBox("Setting", self.avatarBtn, "BtnGrid")


        self.messGrp, sec3Grid = GroupGrid("Messenger")

        self.layout.addWidget(self.avatarGrp, 0, 0, 3, 3)
        self.layout.addWidget(self.settingGrp, 3, 0, 3, 3)
        self.layout.addWidget(self.messGrp, 0, 3, 6, 6)

    @pyqtSlot(bool)
    def update_avatar(self, param):
        # print("receive signal to update avatar: {0}".format(param))
        if param:
            self.username, token, cookie, remember = self.query.query_table('curUser')
            self.avatar = QPixmap(get_avatar_image(self.username))
            self.avatarScene = QGraphicsScene()
            self.avatarScene.addPixmap(self.avatar)
            self.avatarScene.update()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018