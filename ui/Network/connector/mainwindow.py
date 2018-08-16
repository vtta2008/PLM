#!/usr/bin/python

# Copyright (c) 2018 Thomas Grime http://www.radiandynamics.com

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from ui.Network.connector.server import Server
from ui.Network.connector.resources import resource_path

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.server = None

        self.create_toolbar()
        self.create_widgets()

    def create_toolbar(self):
        self.openServer = QAction(QIcon(resource_path('ui\\Network\\images\\start.png')), 'Open Server', self)
        self.closeServer = QAction(QIcon(resource_path('ui\\Network\\images\\stop.png')), 'Close Server', self)

        self.openServer.setEnabled(True)
        self.closeServer.setEnabled(False)

        toolbar = self.addToolBar("Main Toolbar")
        toolbar.addAction(self.openServer)
        toolbar.addAction(self.closeServer)

        self.openServer.triggered.connect(self.open_server)
        self.closeServer.triggered.connect(self.close_server)

    def create_widgets(self):
        self.server = Server.Server()

        self.setCentralWidget(self.server)

    def open_server(self):
        status = self.server.open_server()

        if (status):
            self.openServer.setEnabled(False)
            self.closeServer.setEnabled(True)

    def close_server(self):
        self.server.close_server()

        self.openServer.setEnabled(True)
        self.closeServer.setEnabled(False)