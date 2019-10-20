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
from PyQt5.QtNetwork import QHostAddress
from PyQt5.QtWidgets import QGridLayout, QLabel

from appData.ServerCfg import ServerCfg
# Plt
from cores.Loggers import Loggers
from cores.Metadata import __serverGlobal__
from ui.uikits.UiPreset import Label
from utilities.utils import get_app_icon

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ServerStatus(QGridLayout):

    key = 'serverStatus'
    onlineStage = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ServerStatus, self).__init__(parent)
        self.logger = Loggers(self)
        self.server = ServerCfg()
        self.server.listen(QHostAddress(__serverGlobal__), 9000)

        self.serverOpen = self.server.isListening()

        self.connected = get_app_icon(16, 'Connected')
        self.disconnected = get_app_icon(16, 'Disconnected')

        self.networkStatus = QLabel()
        self.networkStatus.setMaximumWidth(20)
        self.networkStatus.setPixmap(QPixmap(self.connected))

        self.addWidget(self.networkStatus, 0, 0, 1, 1)

        self.onlineStage.connect(self.connection_status)
        self.onlineStage.emit(self.serverOpen)
        self.txt = Label({'txt': "Connecting"})
        self.buildUI()

    def buildUI(self):

        self.addWidget(self.txt, 0, 1, 1, 1)
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