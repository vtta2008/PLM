# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from .io_gui                            import QTextTableFormat

class TextTableFormat(QTextTableFormat):

    Type                                = 'DAMGFORMAT'
    key                                 = 'TextTableFormat'
    _name                               = 'DAMG Text Table Format'

    def __init__(self, *__args):
        super(TextTableFormat, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                      = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved