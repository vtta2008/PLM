# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from .obj import Base


class Server(Base):

    key                         = 'ServerBase'
    Type                        = 'DAMGSERVER'

    def __init__(self, profile=None):
        super(Server, self).__init__(profile)

        self.profile            = profile

        if self.profile:
            self.loadProfile(self.profile)


    def loadProfile(self, profile):
        if profile.Type == 'DAMGSERVERPROFILE':
            self._name          = profile.name
            self._url           = profile.url
            self._port          = profile.port

            if self._url is None:
                self._url       = "http://localhost:"

            if self._port is not None:
                self._url       = "{0}{1}"

        self.update()

    def update(self):
        self.__dict__.update()

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @name.setter
    def name(self, val):
        self._name              = val

    @url.setter
    def url(self, val):
        self._url               = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved