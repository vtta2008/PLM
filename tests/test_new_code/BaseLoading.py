# -*- coding: utf-8 -*-
"""

Script Name: BaseLoading.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import sys
from math import ceil


from PyQt5.QtCore                       import pyqtSlot
from PyQt5.QtGui                        import QPainter


from PLM.configs                        import (colorLibs, ERROR_LAYOUT_COMPONENT, FRAMELESS, TRANSPARENT, NO_PEN,
                                                ANTIALIAS, STAY_ON_TOP, LINE_SOLID)
from PLM.commons.Widgets.Widget         import Widget
from PLM.commons.Widgets.MessageBox     import MessageBox


class BaseLoading(Widget):

    key                                 = 'BaseLoading'
    _name                               = 'DAMG Base Loading'

    _mainColor                          = colorLibs.CYAN
    _roundness                          = 100.0
    _minOpacity                         = 30.0 # 31.4159265358979323846
    _fadingRate                         = 50.0
    _revolutionPerSec                   = 1.57079632679489661923
    _numberOfLines                      = 30
    _lineLength                         = 10
    _lineWidth                          = 2
    _innerRadius                        = 20
    _count                              = 0

    _painter                            = None
    _centerParent                       = True
    _spinning                           = False

    _penColor                           = colorLibs.bright_orange
    _penWidth                           = 8
    _penLine                            = LINE_SOLID
    _radius                             = 40
    _circleSize                         = 400

    def __init__(self, parent=None):
        super(BaseLoading, self).__init__(parent)

        self.parent                     = parent

        if not self.parent:
            MessageBox(self, 'Loading Layout Component', 'critical', ERROR_LAYOUT_COMPONENT)
            sys.exit()

        self.setWindowFlags(STAY_ON_TOP|FRAMELESS)

    # def updateTimer(self):
    #     self.timer.setInterval(1000/(self._numberOfLines*self._revolutionPerSec))

    def getPainter(self):
        painter = QPainter(self)
        painter.fillRect(self.rect(), TRANSPARENT)
        painter.setRenderHint(ANTIALIAS, True)
        painter.setPen(NO_PEN)
        return painter

    @pyqtSlot()
    def rotate(self):
        self._count += 1
        if self._count > self._numberOfLines:
            self._count                 = 0
        self.update()

    def updateSize(self):
        size = (self._innerRadius + self._lineLength)*2
        self.setFixedSize(size, size)

    def updatePosition(self):
        if self._centerParent:
            self.move(self.parent.width()/2 - self.width()/2, self.parent.height()/2 - self.height()/2)
        else:
            pass

    def distanceFromPrimary(self, current, primary, totalNumOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNumOfLines
        return distance

    def lineColor(self, countDistance, totalNumOfLines, fadeRate, minOpacity, color):
        if countDistance == 0:
            return color

        minAlphaF = minOpacity/100.0

        distanceThreshold = ceil((totalNumOfLines - 1)*fadeRate/100.0)
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = self._mainColor.alphaF() - minAlphaF
            gradient = alphaDiff/distanceThreshold + 1.0
            resultAlpha = color.alphaF() - gradient*countDistance
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)

        return color

    def setNumberOfLines(self, lines):
        self._numberOfLines = lines
        self.updateTimer()

    def setLineLength(self, length):
        self._lineLength = length
        self.updateSize()

    def setLineWidth(self, width):
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self.updateSize()

    def color(self):
        return self._mainColor

    def setRoundness(self, roundness):
        self._roundness = min(0.0, max(100, roundness))

    def setColor(self, color):
        self._mainColor = color

    def setRevolutionPerSec(self, revolutionPerSec):
        self._revolutionPerSec = revolutionPerSec
        self.updateTimer()

    def setFadeRate(self, fadeRate):
        self._fadingRate = fadeRate

    def setMinOpacity(self, opacity):
        self._minOpacity = opacity

    @property
    def roundness(self):
        return self._roundness

    @property
    def minOpacity(self):
        return self._minOpacity

    @property
    def fadingRate(self):
        return self._fadingRate

    @property
    def revolutionPerSec(self):
        return self._revolutionPerSec

    @property
    def numberOfLines(self):
        return self._numberOfLines

    @property
    def lineLength(self):
        return self._lineLength

    @property
    def lineWidth(self):
        return self._lineWidth

    @property
    def innerRadius(self):
        return self._innerRadius

    @property
    def spinning(self):
        return self._spinning

    @property
    def count(self):
        return self._count

    @property
    def centerParent(self):
        return self._centerParent

    @property
    def mainColor(self):
        return self._mainColor

    @property
    def painter(self):
        return self._painter

    @property
    def penColor(self):
        return self._penColor

    @property
    def penWidth(self):
        return self._penWidth

    @property
    def penLine(self):
        return self._penLine

    @property
    def radius(self):
        return self._radius

    @property
    def circleSize(self):
        return self._circleSize

    @circleSize.setter
    def circleSize(self, val):
        self._circleSize                = val

    @radius.setter
    def radius(self, val):
        self._radius                    = val

    @penLine.setter
    def penLine(self, val):
        self._penLine                   = val

    @penWidth.setter
    def penWidth(self, val):
        self._penWidth                  = val

    @penColor.setter
    def penColor(self, val):
        self._penColor                  = val

    @painter.setter
    def painter(self, val):
        self._painter                   = val

    @revolutionPerSec.setter
    def revolutionPerSec(self, val):
        self._revolutionPerSec          = val

    @spinning.setter
    def spinning(self, val):
        self._spinning                  = val

    @roundness.setter
    def roundness(self, val):
        self._roundness                 = val

    @mainColor.setter
    def mainColor(self, val):
        self._mainColor                 = val

    @minOpacity.setter
    def minOpacity(self, val):
        self._minOpacity                = val

    @fadingRate.setter
    def fadingRate(self, val):
        self._fadingRate                = val

    @numberOfLines.setter
    def numberOfLines(self, val):
        self._numberOfLines             = val

    @centerParent.setter
    def centerParent(self, val):
        self._centerParent              = val

    @lineWidth.setter
    def lineWidth(self, val):
        self._lineWidth                 = val

    @lineLength.setter
    def lineLength(self, val):
        self._lineLength                = val

    @innerRadius.setter
    def innerRadius(self, val):
        self._innerRadius               = val

    @count.setter
    def count(self, val):
        self._count                     = val
        self.countChangeEvent()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/25/2020 - 12:21 AM
# © 2017 - 2019 DAMGteam. All rights reserved