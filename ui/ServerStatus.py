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

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGridLayout, QLabel
from PyQt5.QtNetwork import QHostAddress

# Plt
from appData import right, __serverUrl__
from appData.ServerCfg import ServerCfg
from ui.uirc import Label
from utilities.utils import getAppIcon
from core.Specs import Specs
from core.Loggers import SetLogger

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ServerStatus(QGridLayout):

    key = 'serverStatus'
    onlineStage = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ServerStatus, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.logger = SetLogger(self)
        self.server = ServerCfg()
        self.server.listen(QHostAddress(__serverUrl__), 9000)

        self.serverOpen = self.server.isListening()

        self.connected = getAppIcon(16, 'Connected')
        self.disconnected = getAppIcon(16, 'Disconnected')
        self.networkStatus = QLabel()
        self.networkStatus.setPixmap(QPixmap(self.connected))

        self.addWidget(self.networkStatus, 0, 0, 1, 1)

        self.onlineStage.connect(self.connection_status)
        self.onlineStage.emit(self.serverOpen)
        if not self.serverOpen:
            self.text = "Failed to connect"
        else:
            self.text = "IP: %s\nport: %d\n\n" % (self.server.serverAddress().toString(), self.server.serverPort())
        self.buildUI()

    def buildUI(self):

        self.addWidget(Label(self.text, right), 0, 1, 1, 1)
        self.applySetting()

    def applySetting(self):
        pass

    def connection_status(self, param):
        if param:
            self.networkStatus.setPixmap(QPixmap(self.connected))
        else:
            self.networkStatus.setPixmap(QPixmap(self.disconnected))

        self.networkStatus.update()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018