# -*- coding: utf-8 -*-
"""

Script Name: ServerConnection.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import socket, time

from appData                    import __google__
from bin.dependencies.damg.damg import DAMG

class TestConnection(DAMG):

    retry = 5
    delay = 1
    timeout = 3

    def __init__(self, url=__google__, port=443):
        super(TestConnection, self).__init__()

        self.ip = url
        self.port = port
        self._connectable = False

        self.checkHost()

    def isOpen(self, ip, port):
        print("open a socket")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)

        if port is not None:
            port = int(port)
        try:
            s.connect((ip, port))
            s.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False
        finally:
            print("close a socket")
            s.close()

    def checkHost(self):

        for i in range(self.retry):
            if self.isOpen(self.ip, self.port):
                self._connectable = True
                print('Connection to {0} via port {1}: {2}'.format(self.ip, self.port, self._connectable))
            else:
                self._connectable = False
                print('Connection to {0} via port {1}: {2}'.format(self.ip, self.port, self._connectable))
            time.sleep(self.delay)

        return self._connectable

    @property
    def connectable(self):
        return self._connectable

    @connectable.setter
    def connectable(self, val):
        self._connectable = val


if __name__ == "__main__":
    TestConnection()
    # TestConnection(__localHost__, __localPort__)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/10/2019 - 1:47 PM
# © 2017 - 2018 DAMGteam. All rights reserved