# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
import sys
from PyQt5 import QtCore, QtNetwork, QtWidgets


class CheckConnectivity(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)

        url = QtCore.QUrl("https://www.google.com/")
        req = QtNetwork.QNetworkRequest(url)
        net_manager = QtNetwork.QNetworkAccessManager()

        self.res = net_manager.get(req)
        self.res.finished.connect(self.processRes)
        self.res.error.connect(self.processErr)
        self.msg = QtWidgets.QMessageBox()

    @QtCore.pyqtSlot()
    def processRes(self):
        if self.res.bytesAvailable():
            self.msg.information(self, "Info", "You are connected to the Internet.")
        else:
            self.msg.critical(self, "Info", "You are not connected to the Internet.")
        self.msg.show()
        self.res.close()

    @QtCore.pyqtSlot(QtNetwork.QNetworkReply.NetworkError)
    def processErr(self, *args):
        print(*args)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ic = CheckConnectivity()
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:17 AM
# © 2017 - 2019 DAMGteam. All rights reserved