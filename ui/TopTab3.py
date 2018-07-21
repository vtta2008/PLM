#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: TopTab3.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from functools import partial

# PyQt5
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QGraphicsView, QGraphicsScene, QSizePolicy,
                             QPushButton, QGroupBox)

# Plt

from core.Specs import Specs
from ui.Libs.GroupBox import GroupBox
from ui.Libs.Button import Button
from utilities import localSQL as usql
from utilities.utils import get_avatar_icon

# -------------------------------------------------------------------------------------------------------------
""" TopTab3 """

class TopTab3(QWidget):

    key = 'topTab3'
    executing = pyqtSignal(str)
    showLayout = pyqtSignal(str, str)
    addLayout = pyqtSignal(object)

    def __init__(self, parent=None):
        super(TopTab3, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.addLayout.emit(self)

    def buildUI(self):
        self.query = usql.QuerryDB()
        try:
            self.username, token, cookie, remember = self.query.query_table('curUser')
        except IndexError:
            self.username = 'DemoUser'

        self.avatar = QPixmap(get_avatar_icon(self.username))
        self.avatarScene = QGraphicsScene()
        self.avatarScene.addPixmap(self.avatar)

        self.avatarView = QGraphicsView()
        self.avatarView.setScene(self.avatarScene)
        self.avatarView.aspectRatioMode = Qt.KeepAspectRatio
        self.avatarView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.avatarView.scale(100 / self.avatar.width(), 100 / self.avatar.height())
        self.avatarView.setFixedSize(100, 100)

        btn1 = Button({'txt':'Account Setting', 'cl': partial(self.showLayout.emit, 'userSetting', 'show')})
        btn2 = Button({'txt':'Log Out', 'cl': partial(self.showLayout.emit, 'login', 'show')})

        btns = [btn1, btn2]

        sec1Grp = GroupBox(self.username, [self.avatarView], "ImageView")
        sec2Grp = GroupBox("Setting", btns, "BtnGrid")

        sec3Grp = QGroupBox("Messenger")
        sec3Grid = QGridLayout()
        sec3Grp.setLayout(sec3Grid)

        self.layout.addWidget(sec1Grp, 0, 0, 1, 1)
        self.layout.addWidget(sec2Grp, 1, 0, 1, 1)
        self.layout.addWidget(sec3Grp, 0, 1, 2, 2)

        self.applySetting()

    @pyqtSlot(bool)
    def update_avatar(self, param):
        print("receive signal emit to update avatar: {0}".format(param))
        # if param:
        #     self.username, token, cookie, remember = self.query.query_table('curUser')
        #     self.avatar = QPixmap(func.getAvatar(self.username))
        #     self.avatarScene = QGraphicsScene()
        #     self.avatarScene.addPixmap(self.avatar)
        #     self.avatarScene.update()

    def on_signOutBtn_clicked(self):
        self.settings.app.setValue("showMain", False)
        self.settings.app.setValue("showLogin", True)
        self.showPlt.emit(False)
        self.showLogin.emit(True)

    def applySetting(self):
        pass


def main():
    app = QApplication(sys.argv)
    layout = TopTab3()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018