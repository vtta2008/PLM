# -*- coding: utf-8 -*-
"""

Script Name: Settings.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from appData import INI
from toolkits.Core import Setting

class Settings(Setting):

    key                             = 'Settings'

    def __init__(self, filename=None, fm=INI, parent=None):
        super(Settings, self).__init__(filename)

        self.parent                 = parent
        self._format                = fm

        self._settingFile           = filename
        self._groups                = self.childGroups()
        self.clean_long_keys()

    def clean_long_keys(self):
        for key in self.allKeys():
            lst = key.split('/')
            if len(lst) >= 2:
                if self._trackDeleteKey:
                    print('{0}: key: {1} has been removed.'.format(self.key, key))
                self.remove(key)
        self.update()

    def update(self):

        self._data['key'] = self.key
        for g in self.childGroups():
            grp = {}
            self.beginGroup(g)
            for k in self.childKeys():
                v = self.value(k)
                if not v is None:
                    grp[k] = v
            grp.update()
            self._data[g] = grp
            self._data.update()
            while self.group():
                self.endGroup()

        return self._data

    def changeParent(self, parent):
        self.parent             = parent
        self.key                = '{0}_{1}'.format(self.parent.key, self.key)
        self._name              = self.key.replace('_', ' ')

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 1:15 AM
# © 2017 - 2018 DAMGteam. All rights reserved