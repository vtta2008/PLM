#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: sql_server.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to create, modify and/or query server data

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import time, logging

# PtQt5
from PyQt5.QtCore import (pyqtSignal, QByteArray, QDataStream, QIODevice, QThread)
from PyQt5.QtNetwork import (QTcpServer, QTcpSocket)

# Plm
from appData.config import LOGPTH, LOG_FORMAT, DT_FORMAT

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

from appData.Loggers import SetLogger
logger = SetLogger()

# -------------------------------------------------------------------------------------------------------------
""" Thread connecting """

class SocketThread(QThread):

    error = pyqtSignal(QTcpSocket.SocketError)

    def __init__(self, socketDescriptor, text, parent):
        super(SocketThread, self).__init__(parent)

        self.socketDescriptor = socketDescriptor
        self.text = text

    def run(self):

        tcpSocket = QTcpSocket()

        if not tcpSocket.setSocketDescriptor(self.socketDescriptor):
            self.error.emit(tcpSocket.error())
            return

        block = QByteArray()
        outstr = QDataStream(block, QIODevice.WriteOnly)
        outstr.setVersion(QDataStream.Qt_4_0)
        outstr.writeUInt16(0)
        outstr.writeQString(self.text)
        outstr.device().seek(0)
        outstr.writeUInt16(block.size() - 2)

        tcpSocket.write(block)
        tcpSocket.disconnectFromHost()
        tcpSocket.waitForDisconnected()


class ServerCfg(QTcpServer):

    def incomingConnection(self, socketDescriptor):
        thread = SocketThread(socketDescriptor, "You have notification", self)
        thread.finished.connect(thread.deleteLater)
        thread.start()

