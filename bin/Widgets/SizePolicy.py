# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtWidgets                      import QSizePolicy


class SizePolicy(QSizePolicy):

    Type                                    = 'DAMGPOLICY'
    key                                     = 'SizePolicy'
    _name                                   = 'DAMG Size Policy'

    def __init__(self,*__args):
        super(SizePolicy, self).__init__(*__args)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved