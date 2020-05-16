# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM                            import __copyright__, QNetworkRequest


class NetworkRequest(QNetworkRequest):

    Type                            = 'DAMGNETWORKREQUEST'
    key                             = 'NetworkRequest'
    _name                           = 'DAMG Network Request'
    _copyright                      = __copyright__()

    def __init__(self, *__args):
        super(NetworkRequest, self).__init__(*__args)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def copyright(self):
        return self._copyright

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved