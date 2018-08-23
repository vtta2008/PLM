#!/usr/bin/python

# Copyright (c) 2018 Thomas Grime http://www.radiandynamics.com

from PyQt5.QtGui import QTextCursor
from PyQt5.QtNetwork import QHostAddress
from PyQt5.QtNetwork import QTcpServer
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from app import __serverUrl__


class Server(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.serverOpen = False
        self.tcpServer = None
        self.tcpServerConnection = None

        self.textEdit = None
        self.lineEdit = None

        self.create_widgets()

    def create_widgets(self):
        self.tcpServer = QTcpServer()

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Enter response")
        self.lineEdit.setMaxLength(50)
        self.lineEdit.setEnabled(True)

        vBox = QVBoxLayout()
        vBox.addWidget(self.textEdit)
        vBox.addWidget(self.lineEdit)
        self.setLayout(vBox)

        self.tcpServer.newConnection.connect(self.accept_connection)

    def add_message(self, message):
        self.textEdit.moveCursor(QTextCursor.End)
        self.textEdit.insertPlainText(message)
        self.textEdit.moveCursor(QTextCursor.End)

    def open_server(self):
        if (len(self.lineEdit.text()) == 0):
            self.add_message("You must enter a response\n")
            QMessageBox.critical(self, "Error", "You must enter a response")
            return False

        self.tcpServer.listen(QHostAddress(__serverUrl__), 9000)

        self.serverOpen = self.tcpServer.isListening()

        if (self.serverOpen):
            serverAddress = self.tcpServer.serverAddress().toString()
            serverPort = self.tcpServer.serverPort()
            self.add_message("Server opened on %s on port %d\n" %(serverAddress, serverPort))
            self.lineEdit.setEnabled(False)
        else:
            self.add_message(self.tcpServer.errorString())
            QMessageBox.critical(self, "Error", self.tcpServer.errorString())

        return True

    def accept_connection(self):
        self.tcpServerConnection = self.tcpServer.nextPendingConnection()
        self.tcpServerConnection.readyRead.connect(self.receive_data)
        self.tcpServerConnection.disconnected.connect(self.socket_disconnected)

        peerAddress = self.tcpServerConnection.peerAddress().toString()
        peerPort = self.tcpServerConnection.peerPort()
        self.add_message("Connected to %s on port %d\n" %(peerAddress, peerPort))

    def receive_data(self):
        rxData = self.tcpServerConnection.readAll()
        self.add_message("Received '" + rxData.data().decode('utf8') + "'\n")
        txString = self.lineEdit.text()
        self.tcpServerConnection.write(txString.encode())
        self.add_message("Wrote '" + txString + "'\n")

    def socket_disconnected(self):
        self.add_message("Disconnected from client\n")

    def close_server(self):
        if (self.serverOpen):
            self.tcpServer.close()
            self.lineEdit.setEnabled(True)



import sys
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)
layout = Server()
layout.show()
app.exec_()
