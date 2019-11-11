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
from PyQt5.QtCore               import pyqtSignal
from PyQt5.QtGui                import QPixmap


# Plt
from appData                    import __localServer__, SERVER_CONNECT_FAIL
from ui.uikits.MessageBox       import MessageBox
from ui.uikits.GridLayout       import GridLayout
from ui.uikits.Label            import Label
from utils                      import get_app_icon

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ConnectStatus(GridLayout):

    key = 'ConnectStatus'

    onlineStage = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ConnectStatus, self).__init__(parent)

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

        self.networkStatus = Label({'txt': ''})
        self.networkStatus.setMaximumWidth(20)

        if self.serverConnectable:
            self.networkStatus.setPixmap(QPixmap(self.connected))
        else:
            self.networkStatus.setPixmap(QPixmap(self.disconnected))

        self.addWidget(self.networkStatus, 0, 0, 1, 1)

        self.onlineStage.connect(self.connection_status)
        self.onlineStage.emit(self.serverConnectable)
        self.txt = Label({'txt': "Connecting"})

        self.addWidget(self.txt, 0, 1, 1, 1)

    def connection_status(self, param):

        if param:
            self.networkStatus.setPixmap(QPixmap(self.connected))
        else:
            self.networkStatus.setPixmap(QPixmap(self.disconnected))

        self.networkStatus.update()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018