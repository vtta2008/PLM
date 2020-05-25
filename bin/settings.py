# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from .base import Setting

class GlbSettingBase(Setting):

    key                                 = 'GlobalSettings'
    Type                                = 'DAMGSETTING'
    _name                               = 'PLM Global Setting'

    def __init__(self):
        object.__init__(self)

        self.update()

    def createSetting(self, name, value):
        setattr(self, name, value)
        self.update()

# -------------------------------------------------------------------------------------------------------------
""" Config global """

loading_options                         = ['loading', 'progress']
binding_options                         = ['PyQt5', 'PySide2']
saving_options                          = ['json', 'yaml']


class GlobalSettings(GlbSettingBase):

    cfgAble                             = True

    saveCfgInfo                         = True
    saveIconInfo                        = True
    savePlmInfo                         = True
    savePcInfo                          = True
    saveSettingInfo                     = True

    qtBinding                           = 'PyQt5'
    qtVersion                           = '5.14.1'
    formatSaving                        = 'json'

    allowAllErrors                      = True
    actionRegisterError                 = True

    emittable                           = False
    autoChangeEmittable                 = True
    trackRecieveSignal                  = False
    trackBlockSignal                    = False
    trackCommand                        = False
    trackRegistLayout                   = False

    def __init__(self):
        super(GlobalSettings, self).__init__()

        self.update()


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved