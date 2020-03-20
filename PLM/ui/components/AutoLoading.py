# -*- coding: utf-8 -*-
"""

Script Name: LoadingBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
# Python
import sys

# PyQt5
from PyQt5.QtCore                       import QRect

# PLM
from PLM.configs                        import (RELATIVE_SIZE)
from PLM.ui.base                        import BaseLoading
from PLM.ui.models.ThreadManager        import ThreadManager


class AutoLoading(BaseLoading):

    key                                 = 'LoadingUI'
    _name                               = 'DAMG Loading UI'

    def __init__(self, parent=None):
        super(AutoLoading, self).__init__(parent)

        self.threadManager              = ThreadManager(self.parent)
        self.hide()


    def paintEvent(self, event):

        self.updatePosition()
        self._painter                   = self.getPainter()
        if self._count > self._numberOfLines:
            self._count                 = 0

        self._painter.begin(self)
        for i in range(self._numberOfLines):
            rotateAngle                 = 360*i/self._numberOfLines
            opacity                     = self._minOpacity + (i+1)*((100 - self._minOpacity)/self._numberOfLines)
            distance                    = self.distanceFromPrimary(i, self._count, self._numberOfLines)
            color                       = self.lineColor(distance, self._numberOfLines, self._fadingRate, self._minOpacity, self._mainColor)
            trans1                      = self._innerRadius + self._lineLength
            r1                          = 0
            r2                          = (self._lineWidth // 2)*(-1)
            r3                          = self._lineLength
            r4                          = r3
            rect1                       = QRect(r1, r2, r3, r4)

            self._painter.save()
            self._painter.translate(trans1, trans1)
            self._painter.rotate(rotateAngle)
            self._painter.translate(self._innerRadius, 0)

            self._painter.setBrush(color)
            self._painter.drawRoundedRect(rect1, self._roundness, RELATIVE_SIZE)
            self._painter.setOpacity(opacity)
            self._painter.restore()

    def start(self):
        autoRunThread                   = self.threadManager.getThread('AutoRunLoading')
        self.thread                          = autoRunThread(self)
        self.thread.start()

    def stop(self):
        self._spinning                  = False
        self.thread._spinning           = False
        self.hide()



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/20/2020 - 9:10 AM
# © 2017 - 2019 DAMGteam. All rights reserved