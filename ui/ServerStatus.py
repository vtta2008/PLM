#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ServerStatus.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, logging

# PyQt5
from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget

# Plt
import appData as app

from ui import uirc as rc

from utilities import utils as func
from utilities import variables as var
from utilities import Networking as net

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
# Get apps info config
APPINFO = func.preset_load_appInfo()

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ServerStatus(QGridLayout):

    serverStatusSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ServerStatus, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        checker = net.ConnectionChecker()
        check = checker.check_url()
        print(checker, check, type(check))

        self.buildUI()

    def buildUI(self):

        goodLayout = QHBoxLayout()
        goodLayout.addWidget(rc.ImageUI("NetworkGood"))
        goodLayout.addWidget(rc.Label("Connected"))
        self.goodWidget = QWidget()
        self.goodWidget.setLayout(goodLayout)

        badLayout = QHBoxLayout()
        badLayout.addWidget(rc.ImageUI("NetworkError"))
        badLayout.addWidget(rc.Label("Disconnected"))
        self.badWidget = QWidget()
        self.badWidget.setLayout(badLayout)

        self.addWidget(self.goodWidget, 0, 0, 1, 1)
        self.addWidget(self.badWidget, 0, 0, 1, 1)

        self.serverStatusSig.connect(self.network_status)

        self.applySetting()

    def network_status(self, param):
        self.goodWidget.setVisible(param)
        self.badWidget.setVisible(not param)

    def applySetting(self):
        self.setSpacing(2)


def main():
    app = QApplication(sys.argv)
    layout = ServerStatus()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018