# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__


from PyQt5.QtNetwork                    import QNetworkCookieJar


class NetworkCookieJar(QNetworkCookieJar):

    Type                                = 'DAMGNETWORKCOOKIEJAR'
    key                                 = 'NetworkCookieJar'
    _name                               = 'DAMG Network Cookie Jar'
    _copyright                          = __copyright__()

    def __init__(self, parent):
        super(NetworkCookieJar, self).__init__(parent)

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