# -*- coding: utf-8 -*-
"""

Script Name: test2.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import requests

from PyQt5.QtCore import QRunnable, QThread, QMetaObject, QThreadPool, pyqtSlot, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from core import PLMservice

class RequestRunnable(QRunnable):
    def __init__(self, dialog):
        QRunnable.__init__(self)
        self.w = dialog

    def run(self):
        QThread.msleep(10000)
        QMetaObject.invokeMethod(self.w, "setData", Qt.QueuedConnection, Q_ARG(str, "finish"))


class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        btn = QPushButton("Submit", self)
        btn.clicked.connect(self.submit)
        self.spinner = PLMservice.PLMservice(self)

        self.layout().addWidget(btn)
        self.layout().addWidget(self.spinner)

    def submit(self):
        self.spinner.start()
        runnable = RequestRunnable(self)
        QThreadPool.globalInstance().start(runnable)

    @pyqtSlot(str)
    def setData(self, data):
        print(data)
        self.spinner.stop()
        self.adjustSize()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dial = Dialog()
    dial.show()
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 10:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved