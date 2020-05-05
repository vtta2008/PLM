# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:




"""
# -------------------------------------------------------------------------------------------------------------

import sys

from PLM.commons.Widgets                    import MessageBox
from PLM.commons.Network                    import NetworkAccessManager, NetworkRequest, NetworkReply
from PLM.commons.Core                       import Url
from PLM.cores.models                       import DownloadChannel
from PLM.configs                            import ERROR_APPLICATION


class NetworkManger(NetworkAccessManager):

    key = 'NetworkManger'

    def __init__(self, app=None):
        super(NetworkManger, self).__init__()

        self.app                            = app
        if not self.app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()

    def getUrl(self, url):
        if url is None:
            self.url                        = Url(self.app.urlInfo['google'])
        else:
            self.url                        = Url(url)

        self.request                        = NetworkRequest(self.url)
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

    def internetStatus(self):
        """
        Realtim Checking Internet Connection, measure and return below index via a test url (google)
        :return:
        connectivity: bool
        bandwidth: int
        ping: int
        speed: speed level
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