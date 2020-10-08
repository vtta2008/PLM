# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

from bin.damg import DAMG


class ServerProfile(DAMG):

    key                         = 'ServerProfile'

    def __init__(self, name, domain, port):
        super(ServerProfile, self).__init__()

        self._name = name
        self._domain = domain
        self._port = port

    def status(self):
        pass

    def description(self):
        pass

    def authorization(self):
        pass


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved