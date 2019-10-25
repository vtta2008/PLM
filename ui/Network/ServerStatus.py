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
import requests, sys

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGridLayout, QLabel

# Plt
from appData import __globalServer__, __localServer__, SERVER_CONNECT_FAIL
from cores.Loggers import Loggers
from ui.UiSignals import UiSignals
from ui.MessageBox import MessageBox
from ui.uikits.UiPreset import Label
from utils.utils import get_app_icon

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ServerStatus(QGridLayout):

    key = 'serverStatus'
    onlineStage = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ServerStatus, self).__init__(parent)
        self.logger = Loggers(__file__)
        self.signals = UiSignals(self)

        self.serverConnectable = False

        try:
            r = requests.get(__localServer__)
        except Exception:
            MessageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
            sys.exit()
        else:
            if r.status_code == 200:
                self.serverConnectable = True
            else:
                self.serverConnectable = False

        self.connected = get_app_icon(16, 'Connected')
        self.disconnected = get_app_icon(16, 'Disconnected')

        self.networkStatus = QLabel()
        self.networkStatus.setMaximumWidth(20)

        if self.serverConnectable:
            self.networkStatus.setPixmap(QPixmap(self.connected))
        else:
            self.networkStatus.setPixmap(QPixmap(self.disconnected))

        self.addWidget(self.networkStatus, 0, 0, 1, 1)

        self.onlineStage.connect(self.connection_status)
        self.onlineStage.emit(self.serverConnectable)
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