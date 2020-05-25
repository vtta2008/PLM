# -*- coding: utf-8 -*-
"""

Script Name: IntemDelegate.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from .io_widgets import QItemDelegate

class ItemDelegate(QItemDelegate):

    key                                     = 'ItemDelegate'
    Type                                    = 'DAMGITEMDELEGATE'
    _name                                   = 'DAMG Item Delegate'

    def __init__(self, parent=None):
        super(ItemDelegate, self).__init__(parent)

        self.parent                         = parent


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                          = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 29/11/2019 - 1:03 AM
# © 2017 - 2018 DAMGteam. All rights reserved