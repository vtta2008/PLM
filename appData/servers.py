# -*- coding: utf-8 -*-
"""

Script Name: servers.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# PLM
from .metadatas                     import __localServer__, __globalServer__


VANILA_LOCAL                        = __localServer__
AWS_GLOBAL                          = __globalServer__


class ConfigServer(dict):

    key                             = 'ConfigServer'

    def __init__(self):
        super(ConfigServer, self).__init__()

        self.add('vanila'           , VANILA_LOCAL)
        self.add('AWS'              , AWS_GLOBAL)

    def add(self, key, value):
        self[key]                   = value


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 12:46 AM
# © 2017 - 2019 DAMGteam. All rights reserved