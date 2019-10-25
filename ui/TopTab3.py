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

from PyQt5.QtCore import pyqtSlot
# PyQt5
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QGroupBox, QLabel)

# Plt
from ui.UiSignals import UiSignals
from ui.uikits.Button import Button
from ui.uikits.GroupBox import GroupBox
from utils import localSQL as usql
from utils.utils import get_avatar_icon

# -------------------------------------------------------------------------------------------------------------
""" TopTab3 """

class TopTab3(QWidget):

    key = 'topTab3'

    def __init__(self, parent=None):
        super(TopTab3, self).__init__(parent)
        
        self.signals = UiSignals(self)
        
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

        self.applySetting()
        self.signals.regisLayout.emit(self)

    def buildUI(self):
        self.query = usql.QuerryDB()
        try:
            self.username, token, cookie, remember = self.query.query_table('curUser')
        except (ValueError, IndexError):
            self.username = 'DemoUser'

        self.avatar = QLabel()
        self.avatar.setPixmap(QPixmap.fromImage(QImage(get_avatar_icon(self.username))))
        self.avatar.setScaledContents(True)
        self.avatar.setFixedSize(100, 100)

        btn1 = Button({'txt':'Account Setting', 'cl': partial(self.signals.showLayout.emit, 'userSetting', 'show')})
        btn2 = Button({'txt':'Log Out', 'cl': partial(self.signals.showLayout.emit, 'login', 'show')})

        btns = [btn1, btn2]

        sec1Grp = GroupBox(self.username, [self.avatar], "ImageView")
        sec2Grp = GroupBox("Setting", btns, "BtnGrid")

        sec3Grp = QGroupBox("Messenger")
        sec3Grid = QGridLayout()
        sec3Grp.setLayout(sec3Grid)

        self.layout.addWidget(sec1Grp, 0, 0, 1, 1)
        self.layout.addWidget(sec2Grp, 1, 0, 1, 1)
        self.layout.addWidget(sec3Grp, 0, 1, 2, 2)

    @pyqtSlot(bool)
    def update_avatar(self, param):
        print("receive signal emit to update avatar: {0}".format(param))
        # if param:
        #     self.username, token, cookie, remember = self.query.query_table('curUser')
        #     self.avatar = QPixmap(func.getAvatar(self.username))
        #     self.avatarScene = QGraphicsScene()
        #     self.avatarScene.addPixmap(self.avatar)
        #     self.avatarScene.update()

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