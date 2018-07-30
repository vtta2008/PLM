#!/usr/bin/python

# Copyright (c) 2018 Thomas Grime http://www.radiandynamics.com

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from ui.Network.connector.mainwindow import MainWindow
from ui.Network.connector.resources import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow.MainWindow()

    mainWindow.resize(320, 320)
    mainWindow.setWindowTitle('PyQt5-Socket-Server')
    mainWindow.setWindowIcon(QIcon(resource_path('lib\\images\\window.png')))
    mainWindow.show()

    sys.exit(app.exec_())