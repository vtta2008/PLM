# -*- coding: utf-8 -*-
"""

Script Name: dobj.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import json

from damgdock.types.base import DAMGDICT, DAMG


class COPYRIGHT(DAMG):

    _id                                 = "(c)"
    _name                               = "Copyright"
    _data                               = DAMGDICT(_id, _name)

    _year_start                         = "2017"
    _status                             = "Continuing"
    _year_end                           = "2018"

    _owner                              = "DAMGTEAM"
    _tm                                 = "\u2122"
    _string                             = "All Rights Reserved"

    _copyright                          = "{0}{1} {2} - {3} {4}. {5}{6}".format(_name, _id, _year_start, _year_end, _owner, _string, _tm)

    def __init__(self):
        super(COPYRIGHT, self).__init__()

        self.initialize()


    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    def update_status(self, status="Continuing"):
        self._status                    = status

    def update_year(self, yearend=2018):
        self._year_end                  = yearend

    def update_copyright(self):
        self._copyright                 = "{0}{1} {2} - {3} {4}. {5}{6}".format(self._name, self._id, self._year_start, self._year_end, self._owner, self._string, self._tm)
        self._data.edit_item('copyright', self._copyright)
        self.__dict__['copyright']      = self._copyright

    def initialize(self):

        self.__dict__['name']           = self._name
        self.__dict__['id']             = self._id
        self.__dict__['start']          = self._year_start
        self.__dict__['end']            = self._year_end
        self.__dict__['owner']          = self._owner
        self.__dict__['copyright']      = self._copyright

    @property
    def data(self):

        self._data.add_item('name'      , self._name)
        self._data.add_item('id'        , self._id)
        self._data.add_item('start'     , self._year_start)
        self._data.add_item('end'       , self._year_end)
        self._data.add_item('status'    , self._status)
        self._data.add_item('copyright' , self._copyright)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def yearstart(self):
        return self._year_start

    @property
    def yearend(self):
        return self._year_end

    @yearend.setter
    def yearend(self, year):
        self._year_end = year

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, stt):
        self._status = stt

    @property
    def owner(self):
        return self._owner

    @property
    def copyright(self):
        return self._copyright

    __copyright__                       = _copyright
    __info__                            = _data._copyright


class VERSION(DAMG):

    _id                             = "VER"
    _name                           = "Version"
    _data                           = DAMGDICT(_id, _name)

    _state_major                    = 'dev'
    _state_ver                      = 1
    _state_rev                      = 2
    _state_sub                      = 0

    _state_version                  = float("{0}.{1}{2}".format(_state_ver, _state_rev, _state_sub))
    _state_version_full             = "{0}.{1}.{2}{3}".format(_state_major, _state_version, _state_rev, _state_sub)

    _main_major                     = "ver"
    _main_ver                       = 13
    _main_rev                       = 0
    _main_sub                       = 1

    _main_version                   = "{0}.{1}.{2}".format(_main_ver, _main_rev, _main_sub)
    _main_version_full              = "{0}.{1}.{2}.{3} {4}".format(_main_major, _main_ver, _main_rev, _main_sub, _state_version_full)

    _api_major                      = 'api'
    _api_ver                        = 0
    _api_rev                        = 69
    _api_sub                        = 0

    _api_version                    = float('{0}.{1}{2}'.format(_api_ver, _api_rev, _api_sub))
    _api_version_full               = "{0}.{1}.{2}{3}".format(_api_major, _api_ver, _api_rev, _api_sub)

    _plugin_major                   = 'plg'
    _plugin_ver                     = 13
    _plugin_rev                     = 0
    _plugin_sub                     = 1

    _plugin_version                 = float("{0}.{1}{2}".format(_plugin_ver, _plugin_rev, _plugin_sub))
    _plugin_version_full            = "{0}.{1}.{2}{3}".format(_plugin_major, _plugin_version, _plugin_rev, _plugin_sub)

    _server_major                   = 'ser'
    _server_ver                     = 13
    _server_rev                     = 0
    _server_sub                     = 1

    _server_version                 = float("{0}.{1}{2}".format(_server_ver, _server_rev, _server_sub))
    _server_version_full            = "{0}.{1}.{2}{3}".format(_server_major, _server_ver, _server_rev, _server_sub)

    def __init__(self):
        super(VERSION, self).__init__()

        self.initialize()

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def update_state(self, major='dev', ver=1, rev=2, sub=0):
        self._state_major                   = major
        self._state_version                 = ver
        self._state_rev                     = rev
        self._state_sub                     = sub

        self._state_version                 = float("{0}.{1}{2}".format(self._state_version, self._state_rev, self._state_sub))
        self._state_version_full            = "{0}.{1}.{2}{3}".format(self._state_major, self._state_version, self._state_rev, self._state_sub)

    def update_main(self, major='ver', ver=13, rev=0, sub=1):
        self._main_major                    = major
        self._main_ver                      = ver
        self._main_rev                      = rev
        self._main_sub                      = sub

        self._main_version                  = "{0}.{1}.{2}".format(self._main_ver, self._main_rev, self._main_sub)
        self._main_version_full             = "{0}.{1}.{2}.{3} {4}".format(self._main_major, self._main_ver, self._main_rev, self._main_sub, self._state_version_full)

    def update_server(self, major='ser', ver=13, rev=0, sub=1):
        self._server_major                  = major
        self._server_ver                    = ver
        self._server_rev                    = rev
        self._server_sub                    = sub

        self._server_version                = float("{0}.{1}{2}".format(self._server_ver, self._server_rev, self._server_sub))
        self._server_version_full           = "{0}.{1}.{2}{3}".format(self._server_major, self._server_ver, self._server_rev, self._server_sub)

    def update_plugin(self, major='plg', ver=13, rev=0, sub=1):
        self._plugin_major                  = major
        self._plugin_ver                    = ver
        self._plugin_rev                    = rev
        self._plugin_sub                    = sub

        self._plugin_version                = float( "{0}.{1}{2}".format(self._plugin_ver, self._plugin_rev, self._plugin_sub))
        self._plugin_version_full           = "{0}.{1}.{2}{3}".format(self._plugin_major, self._plugin_version, self._plugin_rev, self._plugin_sub)

    def update_api(self, major='api', ver=13, rev=0, sub=1):
        self._api_major                     = major
        self._api_ver                       = ver
        self._api_rev                       = rev
        self._api_sub                       = sub

        self._api_version                   = float('{0}.{1}{2}'.format(self._api_ver, self._api_rev, self._api_sub))
        self._api_version_full              = "{0}.{1}.{2}{3}".format(self._api_major, self._api_ver, self._api_rev, self._api_sub)

    def initialize(self):
        self.__dict__['id']                 = self._id
        self.__dict__['name']               = self._name

        self.__dict__['version']            = self._main_version
        self.__dict__['server version']     = self._server_version
        self.__dict__['plugin version']     = self._plugin_version
        self.__dict__['api version']        = self._api_version

        self.__dict__['__api__']            = self._api_version_full
        self.__dict__['__ver__']            = self._main_version_full
        self.__dict__['__plugin__']         = self._plugin_version_full
        self.__dict__['__server__']         = self._server_version_full

    @property
    def data(self):

        self._data.add_item('id'            , self._id)
        self._data.add_item('name'          , self._name)

        self._data.add_item('version'       , self._main_version)
        self._data.add_item('server version', self._server_version)
        self._data.add_item('plugin version', self._plugin_version)
        self._data.add_item('api version'   , self._api_version)

        self._data.add_item('__api__'       , self._api_version_full)
        self._data.add_item('__ver__'       , self._main_version_full)
        self._data.add_item('__plugin__'    , self._plugin_version_full)
        self._data.add_item('__server__'    , self._server_version_full)

        return self._data

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._main_version

    @property
    def plugin_version(self):
        return self._plugin_version

    @property
    def api_version(self):
        return self._api_version

    @property
    def server_version(self):
        return self._server_version

    __id__                                  = _id
    __name__                                = _name

    __version__                             = _main_version
    __server_version__                      = _server_version
    __plugin_version__                      = _plugin_version
    __api_version__                         = _api_version

    __ver__                                 = _main_version_full
    __api__                                 = _api_version_full
    __plugin__                              = _plugin_version_full
    __server__                              = _server_version_full

    __info__                                = _data._copyright


class SERVER(DAMG):

    _id                                     = "SV"
    _name                                   = "Damg server"

    _url                                    = "https://pipeline.damgteam.com"
    _check                                  = "https://pipeline.damgteam.com/check"
    _autho                                  = "https://pipeline.damgteam.com/auth"

    _data                                   = DAMGDICT(_id, _name)

    def __init__(self):
        super(SERVER, self).__init__()

        self.initialize()

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    def initialize(self):
        self.__dict__['url']                = self._url
        self.__dict__['check']              = self._check
        self.__dict__['autho']              = self._autho

    @property
    def data(self):
        self._data.add_item('url'           , self._url)
        self._data.add_item('check'         , self._check)
        self._data.add_item('autho'         , self._autho)

        return self._data

    @property
    def url(self):
        return self._url

    @property
    def check(self):
        return self._check

    @property
    def autho(self):
        return self._autho

    __id__                                  = _id
    __name__                                = _name

    __url__                                 = _url
    __check__                               = _check
    __autho__                               = _autho

    __info__                                = _data._copyright

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/08/2018 - 8:35 PM
# © 2017 - 2018 DAMGteam. All rights reserved