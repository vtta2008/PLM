#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ServerStatus.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from PLM.__main__ import globalSetting
""" Import """

# Python
import requests, sys

# PLM
from configs                            import __localServer__, __globalServer__, __google__, SERVER_CONNECT_FAIL
from bin                                import DAMGLIST
from PLM.ui.base import Conection
from PLM.commons.Widgets import GroupGrid, Label, MessageBox
from devkit.Core                        import Timer

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ConnectStatus(GroupGrid):

    key                                 = 'ConnectStatus'
    _updatting                          = False
    _mode                               = None
    _server                             = None
    _connectServer                      = False
    _connectInternet                    = False
    labels                              = DAMGLIST()

    def __init__(self, parent=None):
        super(ConnectStatus, self).__init__(parent=parent)

        self.parent                     = parent
        self._server                    = self.getServer()
        self.modeStatus                 = Label({'txt': self._mode, 'sst': 'Operating Mode Status'})
        self.updateTimer                = Timer()

        self.updateTimer.setParent(self)
        self.updateTimer.timeout.connect(self.update_icon)

        self.server_status()
        self.internet_status()
        self.mode_status()

        self.layout.addWidget(self.serverIcon, 0, 0, 1, 1)
        self.layout.addWidget(self.internetIcon, 0, 1, 1, 1)
        self.layout.addWidget(self.modeStatus, 0, 2, 1, 1)

        self.labels.appendList([self.serverIcon, self.internetIcon, self.modeStatus])

        if not self._updatting:
            self.updateTimer.stop()
        else:
            self.updateTimer.start(1000)

    def server_status(self):

        stt = 'Server Connection Status'

        try:
            r = requests.get(__localServer__)
        except requests.exceptions.ConnectionError:
            if not globalSetting.modes.allowLocalMode:
                MessageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
                sys.exit()
            else:
                self.parent.signals.emit('sysNotify', ['Offline', 'Can not connect to Server', 'crit', 500])
                self.serverIcon         = Conection('Disconnected', stt, self)
        else:
            if r.status_code == 200:
                self.serverIcon         = Conection('Connected', stt, self)
            else:
                self.serverIcon         = Conection('Disconnected', stt, self)

        self.serverIcon.update()

    def internet_status(self):

        stt = 'Internet Connection Status'

        try:
            r = requests.get(__google__)
        except requests.ConnectionError:
            self.parent.signals.emit('sysNotify', ['Offline', 'Can not connect to Internet', 'crit', 500])
            self.internetIcon           = Conection('Disconnected', stt, self)
            self._connectInternet       = False
        else:
            self.parent.signals.emit('sysNotify', ['Online', 'Internet connected', 'info', 500])
            self.internetIcon           = Conection('Connected', stt, self)
            self._connectInternet       = True

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
        self._mode                      = mode

    def getServer(self):
        try:
            r                           = requests.get(__globalServer__)
        except Exception:
            try:
                r                       = requests.get(__localServer__)
            except Exception:
                if not globalSetting.modes.allowLocalMode:
                    MessageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
                    sys.exit()
                else:
                    self.setMode('Off')
                    self._connectServer = False
            else:
                if r.status_code == 200:
                    self._server        = __localServer__
                    self.setMode('Local')
                    self._connectServer = True
                else:
                    self.setMode('Off')
                    self._connectServer = False
        else:
            if r.status_code == 200:
                self._server            = __globalServer__
                self.setMode('Global')
                self._connectServer     = True
            else:
                self.setMode('Off')
                self._connectServer     = True

        return self._server

    @property
    def updatting(self):
        return self._updatting

    @property
    def mode(self):
        return self._mode

    @property
    def server(self):
        return self._server

    @property
    def connectServer(self):
        return self._connectServer

    @property
    def connectInternet(self):
        return self._connectInternet

    @connectServer.setter
    def connectServer(self, val):
        self._connectServer             = val

    @connectInternet.setter
    def connectInternet(self, val):
        self._connectInternet           = val

    @server.setter
    def server(self, val):
        self._server                    = val

    @mode.setter
    def mode(self, val):
        self._mode                      = val

    @updatting.setter
    def updatting(self, val):
        self._updatting                 = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018