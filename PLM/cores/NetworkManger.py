# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:




"""
# -------------------------------------------------------------------------------------------------------------

import sys

from PLM.commons.Widgets                    import MessageBox
from PLM.commons.Network                    import NetworkAccessManager, NetworkRequest
from PLM.commons.Core                       import Url
from PLM.configs                            import ERROR_APPLICATION



class NetworkManger(NetworkAccessManager):

    key = 'NetworkManger'

    def __init__(self, app=None, url=None):
        super(NetworkManger, self).__init__()

        self.app                            = app
        if not self.app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()

        self.urlLibs                        = self.app.urlInfo

        if url is None:
            self.url                        = Url(self.urlLibs['google'])
        else:
            self.url = Url(url)

        self.request                        = NetworkRequest(self.url)

    def max_bandwid(self):
        """
        Measure the maximum bandwidth of the network
        :return: int
        """
        pass

    def internetConnection(self):
        """
        Check Internet Connection, measure and return below index via a test url (google)
        :return:
        connectivity: bool -> realtime internet connection status.
        bandwidth: int -> realtime bandwidth available
        ping: int -> ping return from test url
        """
        pass


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved