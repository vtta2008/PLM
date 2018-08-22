# -*- coding: utf-8 -*-
"""

Script Name: Server.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

from __rc__.element import DObj, DDict
from __rc__.paths import Paths

import docker
class User(DObj):

    def __init__(self):
        super(User, self).__init__()

class Organization(DObj):

    def __init__(self, organizationName, organizationID, slogan, website, founders, authors):
        super(Organization, self).__init__()

        self._name      = organizationName
        self._id        = organizationID

        self._slogan    = slogan
        self._website   = website
        self._founder   = founders
        self._authors   = authors


    def __slogan__(self):
        return self._slogan

    def __website__(self):
        return self._website

    def __founder__(self):
        return self._founder

    def __authors__(self):
        return self._authors

class Server(DObj):

    _id         = 'objServer'
    _name       = 'Server Name'
    _data       = DDict()

    def __init__(self, organization=None, root=None, version=None, api=None, api_version=None, docker=None, serverID=None, serverName=None,  host=None):
        super(Server, self).__init__()

        self._name          = serverName
        self._id            = serverID
        self._organization  = organization
        self._root = root
        self.pths = Paths(self._root, self)

        self._version = version
        self._api = api
        self._api_version = api_version
        self._docker = docker
        self._host = host
        self._check_connection = self._host + '/check'
        self._authority = self._host + '/autho'

    @property
    def data(self):
        self._data.add_item('servername', self._name)
        self._data.add_item('serverID', self._id)
        self._data.add_item('organization', self._organization)
        self._data.add_item('root', self._root)
        self._data.add_item('version', self._version)
        self._data.add_item('api', self._api)
        self._data.add_item('api_version', self._api_version)
        self._data.add_item('docker', self._docker)
        self._data.add_item('host', self._host)
        self._data.add_item('check connection', self._check_connection)
        self._data.add_item('authority', self._authority)
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