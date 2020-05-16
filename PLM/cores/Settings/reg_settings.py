# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PLM.api.Core                       import Settings


class RegSettings(Settings):

    key                                 = 'ResSettings'

    _data                               = dict()
    _settingEnable                      = False

    def __init__(self, formats, scope, text, app, parent=None):
        super(RegSettings, self).__init__(formats, scope, text, app, parent)

        self.parent                     = parent

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
        self.update()


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved