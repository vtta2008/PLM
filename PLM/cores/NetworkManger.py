# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:




"""
# -------------------------------------------------------------------------------------------------------------

import sys

from PLM.commons                            import DAMGDICT
from PLM.commons.Widgets                    import MessageBox
from PLM.commons.Core                       import Url
from PLM.commons.Network                    import NetworkAccessManager, NetworkRequest, NetworkReply
from PLM.cores.models                       import DownloadChannel
from PLM.cores.Loggers                      import Loggers
from PLM.cores.Errors                       import NetworkReplyError
from PLM.configs                            import ERROR_APPLICATION
from PLM.utils                              import is_url

from PyQt5.QtCore                           import pyqtSlot


class Connectivity(NetworkAccessManager):

    key                                     = 'Connectivity'
    connections                             = DAMGDICT()
    _linkCheck                              = None
    _internet                               = False

    def __init__(self, app=None, testUrl=None, server=None):
        super(Connectivity, self).__init__(app)

        self.app = app
        if not self.app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()

        self.logger                         = Loggers()

        if not is_url(testUrl):
            if not is_url(self._linkCheck):
                self._linkCheck             = Url(self.app.urlInfo['google'])
        else:
            self._linkCheck                 = testUrl

        self.setTestLink(self._linkCheck)


    def setTestLink(self, val):
        self._linkCheck                     = val

    def initTest(self):
        """
        Realtim Checking Internet Connection, measure and return below index via a test url (google)
        """
        req                                 = NetworkRequest(self.linkCheck)
        self.res                            = self.get(req)
        self.res.finished.connect(self.connectRes)
        self.res.error.connect(self.connectErr)

    def initRequest(self):
        req                                 = NetworkRequest(self.linkCheck)

    @pyqtSlot()
    def connectRes(self):
        if self.res.bytesAvailable():
            self._internet                  = True
        else:
            self._internet                  = False
        self.res.deleteLater()

    @pyqtSlot(NetworkReplyError)
    def connectErr(self, code):
        self._internet                      = False
        self.logger.error(code)

    @property
    def internet(self):
        return self._internet

    @property
    def linkCheck(self):
        return self._linkCheck

    @internet.setter
    def internet(self, val):
        self._internet                      = val

    @linkCheck.setter
    def linkCheck(self, val):
        self._linkCheck                     = val


class NetworkManger(NetworkAccessManager):

    key = 'NetworkManger'


    def __init__(self, app=None):
        super(NetworkManger, self).__init__(app)



    def getUrl(self, url):

        self.request                        = NetworkRequest(url)
        self.reply                          = NetworkReply(self)


    def max_bandwid(self):
        """
        Measure the maximum bandwidth of the network
        :return: int
        """
        pass

    def isDownloading(self):
        """
        Check if network is in downloading or not
        :return: bool
        """
        pass

    def serverStatus(self):
        """
        Realtime Checking Server Connection
        :return: bool
        """
        pass

    def createDownloadChannel(self, url):
        """
        Create a channel of downloader which containing request, reply as well as all neccessary data to manage.
        :param url: download link.
        :return: DownloadChannel object.
        """
        return DownloadChannel(url, self)




# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved