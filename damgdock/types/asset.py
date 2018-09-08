# -*- coding: utf-8 -*-
"""

Script Name: dasset.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import json

from damgdock.types.base import DAMGDICT, DAMG
from bin.data._docs import PLM_ABOUT

class PLM(DAMG):

    _id                                     = "PLM"
    _name                                   = "Pipeline Manager"
    _data                                   = DAMGDICT(_id, _name)

    _envKey                                 = "PIPELINE_MANAGER"
    _fullname                               = "{0} ({1})".format(_name, _id)
    _slogan                                 = "Comprehensive Design Solution"
    _about                                  = PLM_ABOUT

    _product                                = "application/software"
    _shortcut                               = "PLM.ink"
    _state                                  = "2"
    _status                                 = "Development/Unstable"
    _wiki                                   = "https://github.com/vtta2008/PipelineTool/wiki"

    def __init__(self):
        super(PLM, self).__init__()

        self.initialize()


    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def initialize(self):

        self.__dict__.add_item('id'         , self._id)
        self.__dict__.add_item('name'       , self._name)

        self.__dict__.add_item('envKey'     , self._envKey)
        self.__dict__.add_item('fullname'   , self._fullname)
        self.__dict__.add_item('slogan'     , self._slogan)
        self.__dict__.add_item('about'      , self._about)

        self.__dict__.add_item('product'    , self._product)
        self.__dict__.add_item('shortcut'   , self._shortcut)
        self.__dict__.add_item('state'      , self._state)
        self.__dict__.add_item('status'     , self._status)
        self.__dict__.add_item('wiki'       , self._wiki)

    @property
    def data(self):

        self._data.add_item('id'            , self._id)
        self._data.add_item('name'          , self._name)

        self._data.add_item('envKey'        , self._envKey)
        self._data.add_item('fullname'      , self._fullname)
        self._data.add_item('slogan'        , self._slogan)
        self._data.add_item('about'         , self._about)

        self._data.add_item('product'       , self._product)
        self._data.add_item('shortcut'      , self._shortcut)
        self._data.add_item('state'         , self._state)
        self._data.add_item('status'        , self._status)
        self._data.add_item('wiki'          , self._wiki)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def product(self):
        return self._product

    @property
    def shortcut(self):
        return self._shortcut

    @property
    def state(self):
        return self._state

    @property
    def status(self):
        return self._status

    @property
    def slogan(self):
        return self._slogan

    @property
    def wiki(self):
        return self._wiki

    @property
    def about(self):
        return self._about

    __about__                                   = _about
    __name__                                    = _fullname
    __slogan__                                  = _slogan

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/08/2018 - 1:17 AM
# © 2017 - 2018 DAMGteam. All rights reserved