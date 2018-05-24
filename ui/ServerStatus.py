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
import os, sys, logging, requests, socket

# PyQt5
from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication, QGridLayout, QPushButton

# Plt
import appData as app

from ui import uirc as rc

from utilities import utils as func
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
# Get apps info config
APPINFO = func.preset_load_appInfo()

# -------------------------------------------------------------------------------------------------------------
""" Variables """

from urllib.parse import urlparse
from urllib.request import urlopen, URLError

class ConnectionChecker(object):

    con_url = app.__server__

    def __init__(self):
        pass

    def test_connection(self):
        try:
            data = urlopen(self.con_url, timeout=5)
        except URLError:
            return False

        host = data.fp.raw._sock.getpeername()

        self.conn_url = 'http://' + (host[0] if len(host) == 2 else socket.gethostbyname(urlparse(data.geturl()).hostname))

        return True

# -------------------------------------------------------------------------------------------------------------
""" ServerStatus """

class ServerStatus(QGridLayout):

    serverStatusSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ServerStatus, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        checker = ConnectionChecker()
        check = checker.test_connection()
        print(checker, check, type(check))

        self.buildUI()

    def buildUI(self):

        self.networdErrorIcon = rc.ImageUI("NetworkError")
        self.networkGoodIcon = rc.ImageUI("NetworkGood")
        self.addWidget(self.networkGoodIcon, 0, 0, 1, 1)
        self.addWidget(self.networdErrorIcon, 0, 0, 1, 1)

        self.serverStatusSig.connect(self.network_status)

        self.applySetting()

    def network_status(self, param):
        self.networkGoodIcon.setVisible(param)
        self.networdErrorIcon.setVisible(not param)

    def applySetting(self):
        self.setSpacing(2)


def main():
    app = QApplication(sys.argv)
    layout = ServerStatus()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018