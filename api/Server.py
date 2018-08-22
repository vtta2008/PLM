# -*- coding: utf-8 -*-
"""

Script Name: Server.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import os

from __rc__.element import DObj, DDict
from __rc__.paths import Paths

import docker
class User(DObj):

    def __init__(self):
        super(User, self).__init__()



class Server(DObj):

    _id         = 'objServer'
    _name       = 'Server Name'
    _data       = DDict()

    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(kwargs)

        self.kwargs             = kwargs
        self._name              = self.kwargs['serverName'],
        self._id                = self.kwargs['serverID'],
        self._organization      = self.kwargs['organization'],
        self._root              = os.getenv('ROOT'),
        self.pths = Paths()

        self._version           = self.kwargs['version'],
        self._api               = self.kwargs['api'],
        self._api_version       = self.kwargs['api_version'],
        self._docker            = self.kwargs['docker'],
        self._host              = self.kwargs['host'],

        self._check_connection = self._host + '/check'
        self._authority = self._host + '/autho'

    @property
    def data(self):
        self._data.add_item('paths', self.pths)

        for key, value in self.kwargs.items():
            self._data.add_item(key, value)

        self._data.add_item('_check_connection', self._check_connection)
        self._data.add_item('_authority', self._authority)

        return self._data

    def __organization__(self):
        return self._organization

    def __server__(self):
        return

    def __api__(self):
        return self._api.info()

    def __version__(self):
        return self._version

    def __api_version__(self):
        return self._api_version

    def __docker__(self):
        return self._docker

    def __host__(self):
        return self._host

    def __check_connection__(self):
        return self._check_connection

    def __authotity__(self):
        return self._authority

    def __google__(self):
        return 'https://google.com'

    def __info__(self):
        return '{0}/{1}: Server name: {2} - {3} | host: {4}'.format(self._id, self._api_version, self._name,
                                                                    self._version, self._host)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/08/2018 - 8:55 PM
# © 2017 - 2018 DAMGteam. All rights reserved