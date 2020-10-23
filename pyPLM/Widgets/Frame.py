# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtWidgets                  import QFrame


class Frame(QFrame):

    key                                 = 'QFrame'
    Type                                = 'DAMGFRAME'
    _name                               = 'DAMG Frame'

    def __init__(self, parent, PySide2_QtWidgets_QWidget=None, NoneType=None, *args, **kwargs):
        QFrame.__init__(parent, PySide2_QtWidgets_QWidget, NoneType, *args, **kwargs)

        self.parent                     = parent

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
