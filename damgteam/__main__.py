# -*- coding: utf-8 -*-
'''

Script Name: main.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

'''
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import os, sys, requests
import docker

from PyQt5.QtWidgets import QApplication

from damgteam.types.api import FOUNDER, COFOUNDER
from damgteam.types.model import VERSION, COPYRIGHT, SERVER
from damgteam.types.asset import PLM
from damgteam.types.build import DAMGTEAM

from core.Cores import CoreApplication
from core.Settings import Settings

version                                     = VERSION()
copyright                                   = COPYRIGHT()
server                                      = SERVER()
founder                                     = FOUNDER()
cofounder                                   = COFOUNDER()


class DamgDock(QApplication):

    def __init__(self):
        super(DamgDock, self).__init__(sys.argv)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/08/2018 - 12:24 AM
# © 2017 - 2018 DAMGteam. All rights reserved