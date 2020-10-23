#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ServerStatus.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

__globalServer__                        = "https://server.damgteam.com"
__globalServerCheck__                   = "https://server.damgteam.com/check"
__globalServerAutho__                   = "https://server.damgteam.com/auth"

__localPort__                           = "20987"
__localHost__                           = "http://localhost:"
__localServer__                         = "{0}{1}".format(__localHost__, __localPort__)
__localServerCheck__                    = "{0}/check".format(__localServer__)
__localServerAutho__                    = "{0}/auth".format(__localServer__)

# Python
import requests, sys

# PLM
from PLM                                import glbSettings
from PLM.configs                        import configPropText
p = configPropText()
from pyPLM.Widgets                      import GroupHBox, MessageBox, Widget, HBoxLayout
from pyPLM.damg                         import DAMGLIST
from PLM.cores.models                   import ConnectMonitor
from PLM.ui.base                        import Conection

# -------------------------------------------------------------------------------------------------------------
""" Server Status Layout """

class ConnectStatus(Widget):

    key                                 = 'ConnectStatus'
    _updating                           = False
    _server                             = None
    _connectServer                      = False
    _connectInternet                    = False
    labels                              = DAMGLIST()

    def __init__(self, parent=None):
        super(ConnectStatus, self).__init__(parent=parent)

        self.parent                     = parent

        self.layout                     = HBoxLayout(self)
        self._server                    = self.getServer()

        worker                          = ConnectMonitor(self)
        worker.updateServer.connect(self.server_status)
        worker.updateInternet.connect(self.internet_status)
        worker.start()

        self.server_status()
        self.internet_status()

        self.layout.addWidget(self.serverIcon)
        self.layout.addWidget(self.internetIcon)

        self.labels.appendList([self.serverIcon, self.internetIcon])
        self.setLayout(self.layout)

    def server_status(self):

        stt = 'Server Connection Status'

        try:
            r = requests.get(__localServer__)
        except requests.exceptions.ConnectionError:
            if not glbSettings.allowLocalMode:
                MessageBox(None, 'Connection Failed', 'critical', p['SERVER_CONNECT_FAIL'], 'close')
                sys.exit()
            else:
                self.parent.grabber.emit('sysNotify', ['Offline', 'Can not connect to Server', 'crit', 500])
                self.serverIcon         = Conection('Disconnected', stt, self)
        else:
            if r.status_code == 200:
                self.serverIcon         = Conection('Connected', stt, self)
            else:
                self.serverIcon         = Conection('Disconnected', stt, self)

        self.serverIcon.update()

    def internet_status(self):

        try:
            r = requests.get("http://www.google.com")
        except requests.ConnectionError:
            # self.parent.sysTray.notifier('Offline', 'Can not connect to Internet', 'crit', 500)
            self.internetIcon           = Conection('InternetOff', 'Internet Connection Status', self)
            self._connectInternet       = False
        else:
            # self.parent.sysTray.notifier('Online', 'Internet connected', 'info', 500)
            self.internetIcon           = Conection('InternetOn', 'Internet Connection Status', self)
            self._connectInternet       = True

        self.internetIcon.update()

    def getServer(self):
        """ Now only have local server """
        try:
            r                       = requests.get(__localServer__)
        except Exception:
            if not glbSettings.allowLocalMode:
                MessageBox(None, 'Connection Failed', 'critical', p['SERVER_CONNECT_FAIL'], 'close')
                sys.exit()
            else:
                self.setMode('Off')
                self._connectServer = False
        else:
            if r.status_code == 200:
                self._server        = __localServer__
                self._connectServer = True
            else:
                self.setMode('Off')
                self._connectServer = False

        return self._server

    @property
    def updating(self):
        return self._updating

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

    @updating.setter
    def updating(self, val):
        self._updating                  = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018