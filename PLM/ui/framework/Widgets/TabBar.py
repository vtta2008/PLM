# -*- coding: utf-8 -*-
"""

Script Name: TabBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PLM                                    import __copyright__
from PLM.api                                import QTabBar
from PLM.configs                            import SETTING_FILEPTH, ST_FORMAT
from PLM.plugins.SignalManager              import SignalManager
from PLM.data.SettingManager import SettingManager

class TabBar(QTabBar):

    Type                                    = 'DAMGUI'
    key                                     = 'TabBar'
    _name                                   = 'DAMG Tab Bar'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QTabBar.__init__(self)
        self.parent                         = parent
        self.settings = SettingManager(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals = SignalManager(self)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 4:39 PM
# © 2017 - 2018 DAMGteam. All rights reserved