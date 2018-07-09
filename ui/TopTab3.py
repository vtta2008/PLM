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
from ui import uirc as rc
from ui import UserSetting
from utilities import localSQL as usql
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" TopTab3 """

class TopTab3(QWidget):

    key = 'topTab3'
    executing = pyqtSignal(str)
    showLayout = pyqtSignal(str, str)
    regLayout = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(TopTab3, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.query = usql.QuerryDB()
        try:
            self.username, token, cookie, remember = self.query.query_table('curUser')
        except IndexError:
            self.username = 'DemoUser'

        self.avatar = QPixmap(func.getAvatar(self.username))
        self.avatarScene = QGraphicsScene()
        self.avatarScene.addPixmap(self.avatar)

        self.avatarView = QGraphicsView()
        self.avatarView.setScene(self.avatarScene)
        self.avatarView.aspectRatioMode = Qt.KeepAspectRatio
        self.avatarView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.avatarView.scale(100 / self.avatar.width(), 100 / self.avatar.height())
        self.avatarView.setFixedSize(100, 100)

        btn1 = QPushButton('Account Setting')
        btn1.clicked.connect(self.on_userSettingBtn_clicked)

        btn2 = QPushButton('Log Out')
        btn2.clicked.connect(partial(self.showLayout.emit, 'login', 'show'))

        btns = [btn1, btn2]

        sec1Grp = rc.AutoSectionBtnGrp(self.username, [self.avatarView], "ImageView")
        sec2Grp = rc.AutoSectionBtnGrp("Setting", btns, "BtnGrid")

        sec3Grp = QGroupBox("Messenger")
        sec3Grid = QGridLayout()
        sec3Grp.setLayout(sec3Grid)

        self.layout.addWidget(sec1Grp, 0, 0, 1, 1)
        self.layout.addWidget(sec2Grp, 1, 0, 1, 1)
        self.layout.addWidget(sec3Grp, 0, 1, 2, 2)

        self.applySetting()

    @pyqtSlot(str)
    def update_avatar(self, param):
        print("receive signal emit to update avatar: {0}".format(param))
        # if param:
        #     self.username, token, cookie, remember = self.query.query_table('curUser')
        #     self.avatar = QPixmap(func.getAvatar(self.username))
        #     self.avatarScene = QGraphicsScene()
        #     self.avatarScene.addPixmap(self.avatar)
        #     self.avatarScene.update()

    def on_userSettingBtn_clicked(self):
        layout = UserSetting.UserSetting()
        layout.show()
        layout.updateAvatar.connect(self.update_avatar)
        layout.exec_()

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