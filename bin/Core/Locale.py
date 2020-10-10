# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtCore import QLocale



class Locale(QLocale):

    Type = 'DAMGLOCALE'
    key = 'Locale'
    _name = 'DAMG LOCALE'


    def __init__(self, *__args):
        super(Locale, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                  = val






# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
