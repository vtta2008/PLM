# -*- coding: utf-8 -*-
"""

Script Name: UpdateUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM.configs                        import NO_BRUSH
from PLM.commons.Gui                    import Pen
from PLM.ui.base                        import BaseLoading



class CircleLoading(BaseLoading):

    key                                 = 'UpdateUI'
    _name                               = 'DAMG Update UI'
    _numOfSections                      = 16
    _startAngle                         = 90

    def __init__(self, parent=None):
        super(CircleLoading, self).__init__(parent)

        self._numOfSections             = self.parent.num
        self._count                     = 0
        self.updatePosition()

    def setProgress(self, value):
        self._count                     += value
        self.update()

    def paintEvent(self, event):

        self.updatePosition()
        self._painter                   = self.getPainter()

        self._painter.save()

        r                               = self._radius
        s                               = self._circleSize
        start                           = self._startAngle*16
        end                             = ((360/self._numOfSections)*self._count)*16
        print(end)
        self._painter.setPen(Pen(self._penColor, self._penWidth, self._penLine))
        self._painter.setBrush(NO_BRUSH)
        self._painter.drawArc(r, r, s, s, start, end)

        self._painter.end()

    def start(self):
        self.show()


    @property
    def numOfSections(self):
        return self._numOfSections

    @property
    def startAngle(self):
        return self._startAngle

    @startAngle.setter
    def startAngle(self, val):
        self._startAngle                = val

    @numOfSections.setter
    def numOfSections(self, val):
        self._numOfSections             = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/20/2020 - 11:55 AM
# © 2017 - 2019 DAMGteam. All rights reserved