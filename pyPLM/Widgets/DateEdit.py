# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtWidgets import QDateEdit


class DateEdit(QDateEdit):

    key = 'DateEdit'
    Type = 'DAMGDATEEDIT'
    _name = 'DAMG Date Edit'

    def __init__(self, parent=None, preset={}, *__args):
        super(DateEdit, self).__init__(parent)

        self.parent = parent
        self.preset = preset

        if not self.preset or self.preset == {}:
            self.buildUI()

    def buildUI(self):

        for k,v in self.preset.items():

            if k == 'dispfm':
                self.setDisplayFormat(v)
            elif k == 'dateRange':
                self.setDateRange(v[0], v[1])

            else:
                pass


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
