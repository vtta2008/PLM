# -*- coding: utf-8 -*-
"""

Script Name: Menu.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM                                    import __copyright__
from PLM.api.Widgets.io_widgets             import QMenuBar, QMenu
from PLM.api.damg                           import DAMGDICT


class Menu(QMenu):

    Type                                    = 'DAMGMENU'
    key                                     = 'Menu'
    _name                                   = 'DAMG Menu'
    _copyright                              = __copyright__()

    def __init__(self, title="", parent=None):
        QMenu.__init__(self)

        self._title                         = title
        self.parent                         = parent

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

class MenuBar(QMenuBar):

    Type                                    = 'DAMGUI'
    key                                     = 'MenuBar'
    _name                                   = 'DAMG Menu Bar'
    _copyright                              = __copyright__()
    menus                                   = DAMGDICT()

    def __init__(self, parent=None):
        QMenuBar.__init__(self)

        self.parent                         = parent

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

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
# Created by panda on 30/10/2019 - 2:23 PM
# © 2017 - 2018 DAMGteam. All rights reserved