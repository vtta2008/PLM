# -*- coding: utf-8 -*-
"""

Script Name: Widget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PyQt5.QtWidgets import QWidget

from assets.Storage import UiObj


class Widget(QWidget):

    def __init__(self, parent=None, **kwargs):
        super(Widget, self).__init__(parent)

        self.uiObj = UiObj(self)
        self._width = self.width()
        self._height = self.height()
        self._pos = self.pos()



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/08/2018 - 4:12 AM
# © 2017 - 2018 DAMGteam. All rights reserved