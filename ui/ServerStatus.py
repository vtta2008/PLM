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
import os, sys

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QLabel

from PyQt5.QtNetwork import QHostAddress

# Plt
import appData as app
from appData import ServerCfg
from ui import uirc as rc
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """
logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ServerStatus(QGridLayout):

    networkStatutSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ServerStatus, self).__init__(parent)

        self.settings = app.appSetting

        self.server = ServerCfg.ServerCfg()
        self.server.listen(QHostAddress(app.__serverUrl__), 9000)
        self.serverOpen = self.server.isListening()

        self.connected = func.getAppIcon(16, 'Connected')
        print(self.connected)
        self.disconnected = func.getAppIcon(16, 'Disconnected')

        self.networkStatus = QLabel()
        self.networkStatus.setPixmap(QPixmap(self.connected))

        self.addWidget(self.networkStatus, 0, 0, 1, 1)

        self.networkStatutSig.connect(self.connection_status)
        self.networkStatutSig.emit(self.serverOpen)

        if not self.serverOpen:
            self.text = "Failed to connect"
        else:
            self.text = "IP: %s\nport: %d\n\n" % (self.server.serverAddress().toString(), self.server.serverPort())

        self.buildUI()

    def buildUI(self):

        self.addWidget(rc.Label(txt=self.text, alg=app.right), 0, 1, 1, 1)

        self.applySetting()

    def applySetting(self):
        pass

    def connection_status(self, param):
        if param:
            self.networkStatus.setPixmap(QPixmap(self.connected))
        else:
            self.networkStatus.setPixmap(QPixmap(self.disconnected))

        self.networkStatus.update()


def main():
    app = QApplication(sys.argv)
    layout = ServerStatus()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018