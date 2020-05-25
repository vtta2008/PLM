# -*- coding: utf-8 -*-
"""

Script Name: TextEdit.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------

from .io_widgets import QTextEdit


class TextEdit(QTextEdit):

    Type                                    = 'DAMGUI'
    key                                     = 'TextEdit'
    _name                                   = 'DAMG Text Edit'


    def __init__(self, *__args):
        super(TextEdit, self).__init__(*__args)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/20/2020 - 3:11 AM
# © 2017 - 2019 DAMGteam. All rights reserved