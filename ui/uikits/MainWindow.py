# -*- coding: utf-8 -*-
"""

Script Name: MainWindow.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets import QMainWindow

from ui.UiSignals import UiSignals
from utils.utils import get_layout_size

class MainWindow(QMainWindow):

    def __init__(self, preset={}, parent=None):
        QMainWindow.__init__(self)

        self.preset = preset
        self.parent = parent
        self.signals = UiSignals(self)

    def moveEvent(self, event):
        position = "{0},{1}".format(self.x(), self.y())
        self.signals.setSetting.emit('position', position, self.objectName(), )

    def resizeEvent(self, event):
        sizeW, sizeH = get_layout_size(self)
        self.signals.setSetting.emit('width', str(sizeW), self.objectName())
        self.signals.setSetting.emit('height', str(sizeH), self.objectName())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 12:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved