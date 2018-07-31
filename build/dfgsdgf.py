# -*- coding: utf-8 -*-
"""

Script Name: dfgsdgf.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
import sys, json, pprint

from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, QCoreApplication

from appData import __serverCheck__

class Request(QNetworkRequest):

    def __init__(self):
        super(Request, self).__init__()

        self.host = QUrl(__serverCheck__)
        self.setUrl(self.host)
        self.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")

class NetworkManager(QNetworkAccessManager):

    def __init__(self, parent=None):
        super(NetworkManager, self).__init__(parent)

        self.request = Request()
        self.finished.connect(self.handleResponse)
        self.get(self.request)

    def handleResponse(self, reply):

        self.reply = reply
        er = self.reply.error()
        print(er)
        if er == self.reply.NoError:
            bytes_string = self.reply.readAll()
            raw = json.load(bytes_string, 'utf-8')

            pprint.pprint(raw)

        QCoreApplication.quit()


app2 = QCoreApplication([])
manager = NetworkManager()
sys.exit(app2.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/07/2018 - 1:21 PM
# © 2017 - 2018 DAMGteam. All rights reserved