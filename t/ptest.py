# -*- coding: utf-8 -*-
"""

Script Name: ptest.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PyQt5.QtNetwork import QHostInfo, QNetworkInterface, QTcpSocket, QHostAddress
import socket, time

from appData.config import __localPort__, __localHost__, __serverLocal__
from cores.base import DAMG

ip = "google.com"
lc = __localHost__
ls = __serverLocal__
lp = __localPort__
port = 443
retry = 5
delay = 1
timeout = 3

class ConnectStatus(DAMG):

    def __init__(self, host=None, port=None):
        super(ConnectStatus, self).__init__(self)

        self.host = host
        self.port = port
        self.socket = QTcpSocket(self)

        # c = self.socket.connectToHost(QHostAddress(self.host), int(self.port))

        a = self.socket.socketDescriptor()

a = ConnectStatus(__localHost__, __localPort__)

for ip in QNetworkInterface.allAddresses():
    print(ip.toString())

def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

def checkHost(ip, port):
    ipup = False
    for i in range(retry):
        print(isOpen(ip, port))

        if isOpen(ip, port):
            ipup = True
        else:
            time.sleep(delay)
    return ipup

if checkHost(ip, port):
    print(ip + " is UP")

if checkHost(lc, lp):
    print(ip + " is Connectable")

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/08/2018 - 8:42 PM
# © 2017 - 2018 DAMGteam. All rights reserved