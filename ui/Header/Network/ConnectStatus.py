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
from appData                    import __localServer__, __google__, SERVER_CONNECT_FAIL
from ui.uikits.MessageBox       import MessageBox
from ui.uikits.GridLayout       import GridLayout
from ui.uikits.Label            import Label
from utils                      import get_app_icon

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ConnectStatus(GridLayout):

    key = 'ConnectStatus'

    def __init__(self, parent=None):
        super(ConnectStatus, self).__init__(parent)

        self.serverStatus = Label({'wmax': 20, 'stt': 'Server Connection Status', })
        self.internetStatus = Label({'wmax': 20, 'stt': 'Internet Connection Status', })

        self.server_status()
        self.addWidget(self.serverStatus, 0, 0, 1, 1)

    def server_status(self):

        try:
            r = requests.get(__localServer__)
        except Exception:
            MessageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
            sys.exit()
        else:
            if r.status_code == 200:
                self.serverIcon = get_app_icon(16, 'Connected')
            else:
                self.serverIcon = get_app_icon(16, 'Disconnected')

        self.serverStatus.setPixmap(QPixmap(self.serverIcon))
        self.serverStatus.update()

    def internet_status(self):
        try:
            r = requests.get(__google__)
        except Exception:
            self.parent.signals.emit('sysNotify', )

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018