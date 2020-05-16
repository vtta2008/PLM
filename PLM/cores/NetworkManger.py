# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:




"""
# -------------------------------------------------------------------------------------------------------------

import sys


from PLM.api.Widgets import MessageBox
from PLM.ui.framework import NetworkAccessManager
from PLM.cores.models                       import DownloadChannel
from PLM.configs                            import ERROR_APPLICATION


class NetworkManger(NetworkAccessManager):

    key = 'NetworkManger'

    def __init__(self, app=None):
        super(NetworkManger, self).__init__(app)

        if not app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()

        self.app                            = app

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