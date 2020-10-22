# -*- coding: utf-8 -*-
"""

Script Name: GraphicScene.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PySide2.QtWidgets                      import QGraphicsScene



class GraphicsScene(QGraphicsScene):

    Type                                    = 'DAMGGRAPHICSScene'
    key                                     = 'GraphicsScene'
    _name                                   = 'DAMG Graphic Scene'

    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)

        self.parent                         = parent

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 2:30 AM
# © 2017 - 2018 DAMGteam. All rights reserved