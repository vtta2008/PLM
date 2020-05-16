# -*- coding: utf-8 -*-
"""

Script Name: TextEdit.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PLM                                    import __copyright__
from PLM.api                                import QTextEdit


class TextEdit(QTextEdit):

    Type                                    = 'DAMGUI'
    key                                     = 'TextEdit'
    _name                                   = 'DAMG Text Edit'
    _copyright                              = __copyright__()

    def __init__(self, *__args):
        super(TextEdit, self).__init__(*__args)


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
# Created by panda on 3/20/2020 - 3:11 AM
# © 2017 - 2019 DAMGteam. All rights reserved