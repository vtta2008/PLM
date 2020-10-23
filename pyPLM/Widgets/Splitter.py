# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtWidgets import QSplitter




class Splitter(QSplitter):

    Type                                    = 'DAMGSPLASHSCREEN'
    key                                     = 'SplashScreen'
    _name                                   = 'DAMG Splash Screen'

    def __init__(self, arg__1, parent=None, PySide2_QtWidgets_QWidget=None, NoneType=None, *args, **kwargs):
        QSplitter.__init__(arg__1, parent, PySide2_QtWidgets_QWidget, NoneType, *args, **kwargs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                          = newName

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
