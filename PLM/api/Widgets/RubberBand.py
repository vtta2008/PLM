# -*- coding: utf-8 -*-
"""

Script Name: RubberBand.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM                                    import __copyright__
from PLM.api.Widgets.io_widgets             import QRubberBand


class RubberBand(QRubberBand):

    Type                                    = 'DAMGGRAPHICVIEW'
    key                                     = 'GraphicView'
    _name                                   = 'DAMG Graphic View'
    _copyright                              = __copyright__()

    def __init__(self, shape, parent=None):
        QRubberBand.__init__(self, shape, parent)

        self.parent                         = parent

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
# Created by panda on 3/12/2019 - 2:43 AM
# © 2017 - 2018 DAMGteam. All rights reserved