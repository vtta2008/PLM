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
from PyQt5.QtGui                import QPixmap


# Plt
from appData                    import __localServer__, __globalServer__, __google__, SERVER_CONNECT_FAIL
from bin                        import DAMGTIMER, DAMGLIST
from ui.base                    import Conection
from toolkits.Widgets           import GridLayout, Label, MessageBox

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ConnectStatus(GridLayout):

    key = 'ConnectStatus'
    _allowLocalMode = True
    _updatting = False
    _mode = None
    _server = None
    labels = DAMGLIST()

    def __init__(self, parent=None):
        super(ConnectStatus, self).__init__(parent)

        self.parent             = parent
        self._server            = self.getServer()
        # self.serverStatus       = Label({'wmax': 20, 'sst': 'Server Connection Status', })
        # self.internetStatus     = Label({'wmax': 20, 'sst': 'Internet Connection Status', })
        self.modeStatus         = Label({'txt': self._mode, 'sst': 'Operating Mode Status'})
        self.updateTimer        = DAMGTIMER()

        self.updateTimer.setParent(self)
        self.updateTimer.timeout.connect(self.update_icon)

        self.server_status()
        self.internet_status()
        self.mode_status()

        self.addWidget(self.serverIcon, 0, 0, 1, 1)
        self.addWidget(self.internetIcon, 0, 1, 1, 1)
        self.addWidget(self.modeStatus, 0, 2, 1, 1)

        self.labels.appendList([self.serverIcon, self.internetIcon, self.modeStatus])

        if not self._updatting:
            self.updateTimer.stop()
        else:
            self.updateTimer.start(1000)

    def server_status(self):

        stt = 'Server Connection Status'

        try:
            r = requests.get(__localServer__)
        except Exception:
            if not self._allowLocalMode:
                MessageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
                sys.exit()
            else:
                self.parent.signals.emit('sysNotify', 'Offline', 'Can not connect to Server', 'crit', 500)
                self.serverIcon = Conection('Disconnected', stt, self)
        else:
            if r.status_code == 200:
                self.serverIcon = Conection('Connected', stt, self)
            else:
                self.serverIcon = Conection('Disconnected', stt, self)

        self.serverIcon.update()

    def internet_status(self):

        stt = 'Internet Connection Status'

        try:
            r = requests.get(__google__)
        except requests.ConnectionError:
            self.parent.signals.emit('sysNotify', 'Offline', 'Can not connect to Internet', 'crit', 500)
            self.internetIcon = Conection('Disconnected', stt, self)
        else:
            self.parent.signals.emit('sysNotify', 'Online', 'Internet connected', 'info', 500)
            self.internetIcon = Conection('Connected', stt, self)

        self.internetIcon.update()

    def mode_status(self):
        self.getServer()
        self.modeStatus.setText(self._mode)
        self.modeStatus.update()

    def update_icon(self):
        self.internet_status()
        self.server_status()
        self.mode_status()

    def setMode(self, mode):
        self._mode = mode

    def getServer(self):
        try:
            r = requests.get(__globalServer__)
        except Exception:
            try:
                r = requests.get(__localServer__)
            except Exception:
                if not self._allowLocalMode:
                    MessageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
                    sys.exit()
                else:
                    self.setMode('Off')
            else:
                if r.status_code == 200:
                    self._server = __localServer__
                    self.setMode('Local')
                else:
                    self.setMode('Off')
        else:
            if r.status_code == 200:
                self._server = __globalServer__
                self.setMode('G')
            else:
                self.setMode('O')

        return self._server

    @property
    def updatting(self):
        return self._updatting

    @property
    def allowOfflineMode(self):
        return self._allowLocalMode

    @property
    def mode(self):
        return self._mode

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, val):
        self._server = val

    @mode.setter
    def mode(self, val):
        self._mode = val

    @updatting.setter
    def updatting(self, val):
        self._updatting = val

    @allowOfflineMode.setter
    def allowOfflineMode(self, val):
        self._allowLocalMode = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018