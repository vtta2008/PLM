# -*- coding: utf-8 -*-
"""

Script Name: RubberBand.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PySide2.QtWidgets                      import QRubberBand


class RubberBand(QRubberBand):

    Type                                    = 'DAMGGRAPHICVIEW'
    key                                     = 'GraphicView'
    _name                                   = 'DAMG Graphic View'

    def __init__(self,*__args):
        super(RubberBand, self).__init__(*__args)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 2:43 AM
# © 2017 - 2018 DAMGteam. All rights reserved