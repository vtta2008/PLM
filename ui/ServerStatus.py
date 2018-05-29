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
from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication, QGridLayout

from PyQt5.QtNetwork import QHostAddress

# Plt
import appData as app
from ui import uirc as rc
from utilities import variables as var
from appData.__core.pServer__ import Server

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """
logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ServerStatus(QGridLayout):

    networkStatutSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ServerStatus, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.server = Server.Server()
        self.server.listen(QHostAddress(app.__server__), 9000)
        self.serverOpen = self.server.isListening()

        self.netGood = rc.ImageUI("NetworkGood")
        self.netBad = rc.ImageUI("NetworkError")

        self.networkStatutSig.connect(self.connection_status)
        self.networkStatutSig.emit(self.serverOpen)

        if not self.serverOpen:
            self.text = "Failed to connect"
        else:
            self.text = "IP: %s\nport: %d\n\n" % (self.server.serverAddress().toString(), self.server.serverPort())

        self.buildUI()

    def buildUI(self):

        self.addWidget(rc.Label(txt=self.text, alg=app.left), 0, 1, 1, 1)

        self.applySetting()

    def applySetting(self):
        self.setSpacing(1)

    def connection_status(self, param):
        if param:
            self.addWidget(self.netGood, 0, 0, 1, 1)
            self.removeWidget(self.netBad)
        else:
            self.addWidget(self.netBad, 0, 0, 1, 1)
            self.removeWidget(self.netGood)

def main():
    app = QApplication(sys.argv)
    layout = ServerStatus()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018