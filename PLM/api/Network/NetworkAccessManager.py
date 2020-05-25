# -*- coding: utf-8 -*-
"""

Script Name: NetworkAccessManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from .io_network                import QNetworkAccessManager

class NetworkAccessManager(QNetworkAccessManager):

    Type                        = 'DAMGNETWORKACESSMANAGER'
    key                         = 'NetworkAccessManager'
    _name                       = 'DAMG Network Access Manager'

    def __init__(self, parent=None):
        super(NetworkAccessManager, self).__init__(parent)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name              = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/5/2020 - 9:02 PM
# © 2017 - 2019 DAMGteam. All rights reserved