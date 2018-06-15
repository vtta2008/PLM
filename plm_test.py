
import sys, json, pprint

from PyQt5.QtNetwork import QNetworkReply, QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, QCoreApplication

import appData as app

class Request(QNetworkRequest):

    def __init__(self):
        super(Request, self).__init__()

        self.host = QUrl(app.__serverCheck__)
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

