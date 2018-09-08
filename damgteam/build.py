# -*- coding: utf-8 -*-
"""

Script Name: dorg.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

from damgteam.base import DAMGDICT, DAMG
from damgteam.types.api import FOUNDER, COFOUNDER
from damgteam.types.model import VERSION, COPYRIGHT, SERVER
from damgteam.types.asset import PLM
from app.config import CONFIGS

version                                     = VERSION()
copyright                                   = COPYRIGHT()
server                                      = SERVER()
founder                                     = FOUNDER()
cofounder                                   = COFOUNDER()



class DAMGTEAM(DAMG):

    configs                                 = CONFIGS()

    _organization                           = "Digital Animation Motion Graphic"

    _envKey                                 = "DAMG_TEAM"

    _slogan                                 = "Comprehensive Design Solution"
    _website                                = "https://damgteam.com"


    def __init__(self, version=None, copyright=None, server=None, founder=None, cofounder=None):
        super(DAMGTEAM, self).__init__()

        self._founder                       = founder.__dict__
        self._cofounder                     = cofounder.__dict__

        self.register_member(founder)
        self.register_member(cofounder)

        self.__version__                    = version.__version__
        self.__server_version__             = version.__server_version__
        self.__plugin_version__             = version.__plugin_version__
        self.__api_version__                = version.__api_version__

        self.__copyright__                  = copyright.__copyright__

        self.__server_url__                 = server.__url__
        self.__server_check__               = server.__check__
        self.__server_autho__               = server.__autho__

        self.__email__                      = "{0}; {1}".format(self._founder['email'], self._cofounder['email'])

        self.asset_PLM                      = PLM()
        self.register_asset(self.asset_PLM)

        self.initialize()


    def register_member(self, member):

        key                                     = member.__name__
        value                                   = member.__dict__
        self._members.add_item(key, value)
        self.__members__                        = self._members

    def register_asset(self, asset):
        key                                     = asset.__name__
        value                                   = asset.__dict__
        self._assets.add_item(key, value)
        self.__assets___                        = self._assets

    def check_asset_registered(self, asset):
        if asset.__name__ in self._assets.keys():
            return True
        else:
            return False

    def deregister_member(self, member):

        key                                     = member.__fullname__
        self._members.remove_item(key)
        self.__members__                        = self._members

    def deregister_asset(self, asset):
        key                                     = asset.__fullname__
        self._assets.remove_item(key)
        self.__assets__                         = self._assets

    def initialize(self):
        self.__dict__['id']                 = self.__id__
        self.__dict__['name']               = self.__name__
        self.__dict__['organization']       = self.__organization__
        self.__dict__['envKey']             = self.__envKey__

        self.__dict__['slogan']             = self.__slogan__
        self.__dict__['website']            = self.__website__
        self.__dict__['email']              = self.__email__

        self.__dict__['version']            = self.__version__
        self.__dict__['server version']     = self.__server_version__
        self.__dict__['plugin version']     = self.__plugin_version__
        self.__dict__['api version']        = self.__api_version__

        self.__dict__['founder']            = self._founder
        self.__dict__['cofounder']          = self._cofounder

        self.__dict__['serverUrl']          = self.__server_url__
        self.__dict__['serverautho']        = self.__server_autho__
        self.__dict__['servercheck']        = self.__server_check__

        self.__dict__['copyright']          = self.__copyright__

    @property
    def data(self):

        self._data.add_item('id'            , self.__id__)
        self._data.add_item('name'          , self.__name__)
        self._data.add_item('organization'  , self.__organization__)
        self._data.add_item('envKey'        , self.__envKey__)

        self._data.add_item('slogan'        , self.__slogan__)
        self._data.add_item('website'       , self.__website__)
        self._data.add_item('email'         , self.__email__)

        self._data.add_item('version'       , self.__version__)
        self._data.add_item('plugin version', self.__plugin_version__)
        self._data.add_item('api version'   , self.__api_version__)

        self._data.add_item('founder'       , self._founder.__fullname__)
        self._data.add_item('cofounder'     , self._cofounder.__fullname__)

        self._data.add_item('serverUrl'     , self.__server_url__)
        self._data.add_item('serverautho'   , self.__server_autho__)
        self._data.add_item('servercheck'   , self.__server_check__)

        self._data.add_item('copyright'     , self.__copyright__)

        return self._data

    @property
    def id(self):
        return self.__id__

    @property
    def name(self):
        return self.__name__

    @property
    def organization(self):
        return self.__organization__

    @property
    def envKey(self):
        return self.__envKey__

    @property
    def servercheck(self):
        return self.__server_check__

    @property
    def serverautho(self):
        return self.__server_autho__

    @property
    def serverurl(self):
        return self.__server_url__

    @property
    def website(self):
        return self.__website__

    @property
    def slogan(self):
        return self.__slogan__

    @property
    def founder(self):
        return self._founder

    @property
    def cofounder(self):
        return self._cofounder

    @property
    def email(self):
        return self.__email__

    @property
    def version(self):
        return self.__version__

    @property
    def api_version(self):
        return self.__api_version__

    @property
    def plugin_version(self):
        return self.__plugin_version__

    @property
    def copyright(self):
        return self.__copyright__

    @property
    def members(self):
        return self._members

    @property
    def assets(self):
        return self._assets

    __id__                                      = _id
    __name__                                    = _name
    __info__                                    = _data._copyright

    __organization__                            = _organization
    __envKey__                                  = _envKey

    __slogan__                                  = _slogan
    __website__                                 = _website

obj = DAMGTEAM(version, copyright, server, founder, cofounder)
print(obj._members)
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/08/2018 - 8:55 PM
# © 2017 - 2018 DAMGteam. All rights reserved