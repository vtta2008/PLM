# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from .obj import Base



class Profile(Base):

    key                         = 'Profile'
    Type                        = 'DAMGPROFILE'


    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

        self.update()


class ServerProfile(Profile):

    key                         = 'ServerProfile'
    Type                        = 'DAMGSERVERPROFILE'

    def __init__(self, name=None, url=None, port=None):
        super(ServerProfile, self).__init__(name, url, port)

        if name is not None:
            self._name          = None

        self._url               = url
        self._port              = port

        self.update()

    @property
    def url(self):
        return self._url

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, val):
        self._port              = val

    @url.setter
    def url(self, val):
        self._url               = val




# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved