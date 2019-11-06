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
from PyQt5.QtGui                import QPixmap
from PyQt5.QtWidgets            import (QApplication, QLabel, QGraphicsScene)

# Plt
from ui.uikits.Widget           import Widget
from ui.uikits.GridLayout       import GridLayout
from ui.uikits.Button           import Button
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

        buttons = self.buttonManager.userButtonGroupBox(self.parent)

        # btn1 = Button({'txt': 'Account Setting', 'cl': partial(self.signals.showLayout.emit, 'UserSetting', 'show')})
        # btn2 = Button({'txt': 'Messages', 'cl': partial(self.signals.showLayout.emit, 'Messages', 'show')})
        # btn3 = Button({'txt': 'Log Out', 'cl': partial(self.signals.showLayout.emit, 'SignIn', 'show')})
        # btns = [btn1, btn2, btn3]

        sec1Grp = GroupBox(self.username, [self.avatar], "ImageView")
        sec2Grp = GroupBox("Setting", buttons, "BtnGrid")
        sec1Grp.setMaximumWidth(120)
        sec2Grp.setMaximumWidth(120)

        sec3Grp, sec3Grid = GroupGrid("Messenger")

        self.layout.addWidget(sec1Grp, 0, 0, 3, 3)
        self.layout.addWidget(sec2Grp, 3, 0, 3, 3)
        self.layout.addWidget(sec3Grp, 0, 3, 6, 6)

    @pyqtSlot(bool)
    def update_avatar(self, param):
        print("receive signal_cpu emit to update avatar: {0}".format(param))
        if param:
            self.username, token, cookie, remember = self.query.query_table('curUser')
            self.avatar = QPixmap(get_avatar_image(self.username))
            self.avatarScene = QGraphicsScene()
            self.avatarScene.addPixmap(self.avatar)
            self.avatarScene.update()

    def showEvent(self, event):
        self.signals.showLayout.emit(self.key, 'show')
        self.signals.showLayout.emit('TopTab1', 'hide')
        self.signals.showLayout.emit('TopTab3', 'hide')

def main():
    app = QApplication(sys.argv)
    layout = TopTab2()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018