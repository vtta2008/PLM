# -*- coding: utf-8 -*-
"""

Script Name: Runnable.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# PyQt5
from PyQt5.QtCore import pyqtSignal, QRunnable, QMetaObject
from PyQt5.QtWidgets import QApplication

# Plt
from core import (Indicator, PLMservice, Loading)


# -------------------------------------------------------------------------------------------------------------

""" Runnable """

class Runnable(QRunnable):

    RunnableSig = pyqtSignal(bool)

    def __init__(self):
        super(Runnable, self).__init__()

    def run(self):
        QThread.msleep(10000)
        QMetaObject.invokeMethod(self.w, "setData", Qt.QueuedConnection, Q_ARG(str, "finish"))


# -------------------------------------------------------------------------------------------------------------

""" Runnable """

class ThreadUI(QWidget):

    startThread = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ThreadUI, self).__init__(parent)

        self.startThread.connect(self.start_threading)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.service = PLMservice.PLMservice()
        self.indicator = Indicator.Indicator()
        self.loading = Loading.Loading()

    def start_threading(self, param):
        pass



def main():
    app = QApplication(sys.argv)
    layout = ThreadUI()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 12:07 PM
# © 2017 - 2018 DAMGteam. All rights reserved