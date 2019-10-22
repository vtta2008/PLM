# -*- coding: utf-8 -*-
"""

Script Name: ServerCfg.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

""" Import """

# PtQt5
from PyQt5.QtCore import (pyqtSignal, QByteArray, QDataStream, QIODevice, QThread)
from PyQt5.QtNetwork import (QTcpServer, QTcpSocket)

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

from cores.Loggers import Loggers

# -------------------------------------------------------------------------------------------------------------
""" Thread connecting """

class SocketThread(QThread):

    error = pyqtSignal(QTcpSocket.SocketError)

    def __init__(self, socketDescriptor, text, parent):
        super(SocketThread, self).__init__(parent)

        self.logger = Loggers(self)
        self.socketDescriptor = socketDescriptor
        self.text = text

    def run(self):

        tcpSocket = QTcpSocket()

        if not tcpSocket.setSocketDescriptor(self.socketDescriptor):
            self.error.emit(tcpSocket.error())
            self.logger.error(tcpSocket.error())
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
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/10/2019 - 1:13 AM
# © 2017 - 2018 DAMGteam. All rights reserved