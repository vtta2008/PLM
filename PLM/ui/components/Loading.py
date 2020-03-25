# -*- coding: utf-8 -*-
"""

Script Name: Loading.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
import math
from math                               import ceil

# PyQt5
from PyQt5.QtGui                        import QPainter, QPalette, QPen, QFont, QFontMetrics
from PyQt5.QtCore                       import QRect

# PLM
from PLM.configs                        import (TRANSPARENT, NO_PEN, TEXT_NORMAL, AUTO_COLOR, ANTIALIAS, DAMG_LOGO_DIR,
                                                colorLibs, )
from PLM.commons.Widgets.Widget         import Widget
from PLM.commons.Core                   import Timer
from PLM.commons.Gui                    import Image




class StaticLoading(Widget):

    key                                 = 'BusyLoading'

    _count                              = 0

    _numOfitems                         = 20
    _num                                = float(_numOfitems)
    _itemRadius                         = 25

    _revolutionPerSec                   = 1.57079632679489661923
    _minOpacity                         = 31.4159265358979323846
    _fadeRate                           = 25

    _innerRadius                        = 70

    _mainColor                          = colorLibs.deep_blue
    _brushColor                         = None

    def __init__(self, parent):
        super(StaticLoading, self).__init__(parent)

        palette                         = QPalette(self.palette())
        palette.setColor(palette.Background, TRANSPARENT)
        self.setPalette(palette)

        self.timer                                  = Timer(self)
        self.timer.timeout.connect(self.rotate)
        self.updateTimmer()

    def rotate(self):
        self._count += 1
        if self._count > self._numOfitems:
            self._count                 = 0
        self.update()
        print('count: {0}'.format(self._count))

    def paintEvent(self, event):

        painter                         = QPainter()
        painter.begin(self)
        painter.setRenderHint(ANTIALIAS)
        painter.fillRect(event.rect(), TRANSPARENT)

        self.damgLogoImg                = Image(os.path.join(DAMG_LOGO_DIR, '96x96.png'))
        self.damgLogoImgTargetRect      = QRect(self.width()/2 - self.damgLogoImg.width()/2,
                                                self.height()/2 - self.damgLogoImg.height()/2,
                                                self.damgLogoImg.width(), self.damgLogoImg.height())

        painter.drawImage(self.damgLogoImgTargetRect, self.damgLogoImg, self.damgLogoImg.rect(), AUTO_COLOR)

        painter.setPen(QPen(NO_PEN))

        if self.count > self.numOfitems:
            self._count                 = 0

        for i in range(self.numOfitems):

            distance                    = self.distance(i, self.count)
            self._brushColor            = self.getBrushColor(distance, self.mainColor)
            painter.setBrush(self.brushColor)
            painter.drawEllipse(self.width()/2 + self.innerRadius*math.cos(2*math.pi*i/self.num) - (self.itemRadius/2),
                                self.height()/2 + self.innerRadius*math.sin(2*math.pi*i/self.num) - (self.itemRadius/2),
                                self.itemRadius, self.itemRadius)

        painter.end()

    def distance(self, current, primary):
        distance                        = primary - current
        if distance < 0:
            distance += self.numOfitems
        return distance

    def getBrushColor(self, distance, color):
        if distance == 0:
            return color

        minAlphaF = self.minOpacity/100.0
        distanceThreshold = ceil((self.numOfitems - 1)*self.fadeRate/100.0)

        if distance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff                   = self.mainColor.alphaF() - minAlphaF
            gradient                    = alphaDiff/distanceThreshold + 1.0
            resultAlpha                 = color.alphaF() - gradient*distance
            result                      = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(result)

        return color

    def updateTimmer(self):
        return self.timer.setInterval(1000/(self.numOfitems*self.revolutionPerSec))

    def showEvent(self, event):
        self._count                     = 0
        self.timer.start(50)
        event.accept()

    @property
    def numOfitems(self):
        return self._numOfitems

    @property
    def itemRadius(self):
        return self._itemRadius

    @property
    def mainColor(self):
        return self._mainColor

    @property
    def minOpacity(self):
        return self._minOpacity

    @property
    def fadeRate(self):
        return self._fadeRate

    @property
    def innerRadius(self):
        return self._innerRadius

    @property
    def brushColor(self):
        return self._brushColor

    @property
    def count(self):
        return self._count

    @property
    def num(self):
        return self._num

    @property
    def revolutionPerSec(self):
        return self._revolutionPerSec

    @revolutionPerSec.setter
    def revolutionPerSec(self, val):
        self._revolutionPerSec          = val

    @num.setter
    def num(self, val):
        self._num                       = val

    @count.setter
    def count(self, val):
        self._count                     = val

    @brushColor.setter
    def brushColor(self, val):
        self._brushColor                = val

    @innerRadius.setter
    def innerRadius(self, val):
        self._innerRadius               = val

    @fadeRate.setter
    def fadeRate(self, val):
        self._fadeRate                  = val

    @minOpacity.setter
    def minOpacity(self, val):
        self._minOpacity                = val

    @mainColor.setter
    def mainColor(self, val):
        self._mainColor                 = val

    @itemRadius.setter
    def itemRadius(self, val):
        self._itemRadius                = val

    @numOfitems.setter
    def numOfitems(self, val):
        self._numOfitems                = val



class RealtimeLoading(Widget):

    key                                 = 'RealtimeLoading'

    _configs                            = 16

    _fontFamily                         = 'UTM Avo'
    _fontSize                           = 12.0
    _fontAttr                           = TEXT_NORMAL
    _currentFont                        = QFont(_fontFamily, _fontSize, _fontAttr)

    _textColor                          = colorLibs.peacock
    _penColor                           = colorLibs.DARKBLUE
    _textBrushColor                     = colorLibs.DAMG_LOGO_COLOR

    _text                               = 'Running Configurations'
    _pText                              = '0%'
    _centerW                            = True

    _bMargin                            = 10
    _tMargin                            = 10
    _lMargin                            = 10
    _rMargin                            = 10

    def __init__(self, parent):
        super(RealtimeLoading, self).__init__(parent)

        self.screen                     = self.parent.screen
        palette                         = QPalette(self.palette())
        palette.setColor(palette.Background, TRANSPARENT)
        self.setPalette(palette)

    def paintEvent(self, event):

        painter                         = QPainter()
        painter.begin(self)
        painter.setRenderHint(ANTIALIAS)
        painter.fillRect(event.rect(), TRANSPARENT)

        painter.setPen(self.textColor)
        painter.setFont(self.currentFont)
        painter.setBrush(self.textBrushColor)

        x, y                            = self.getTextPos()
        painter.drawText(x, y, '')
        self.update()
        painter.drawText(x, y, self.text)
        self.update()

        x, y                            = self.getProgressTextPos()
        painter.drawText(x, y, '')
        self.update()
        painter.drawText(x, y, self.pText)
        self.update()

        painter.end()

    def getTextPos(self):

        if self.centerW:
            x                           = (self.width() + self.rMargin + self.lMargin)/2 - self.textWidth()/2
        else:
            x                           = (self.width() + self.rMargin + self.lMargin)

        y                               = self.height() - self.parent.bufferH + self.textHeight() + self.bMargin

        return x, y

    def getProgressTextPos(self):

        if self.centerW:
            x                           = (self.width() + self.rMargin + self.lMargin)/2 - self.pTextWidth()/2
        else:
            x                           = (self.width() + self.rMargin + self.lMargin)

        y                               = self.height() - self.parent.bufferH + self.textHeight() + self.bMargin*4

        return x, y

    def setText(self, text):
        self._text                      = text

    def setProgress(self, val):
        self._pText                     = val

    def textWidth(self):
        fm = QFontMetrics(self.currentFont)
        return fm.width(self.text)

    def pTextWidth(self):
        fm = QFontMetrics(self.currentFont)
        return fm.width(str(self.pText))

    def textHeight(self):
        fm = QFontMetrics(self.currentFont)
        return fm.height()

    @property
    def configs(self):
        return self._configs

    @property
    def fontFamily(self):
        return self._fontFamily

    @property
    def fontSize(self):
        return self._fontSize

    @property
    def fontAttr(self):
        return self._fontAttr

    @property
    def currentFont(self):
        return self._currentFont

    @property
    def text(self):
        return self._text

    @property
    def textColor(self):
        return self._textColor

    @property
    def textBrushColor(self):
        return self._textBrushColor

    @property
    def penColor(self):
        return self._penColor

    @property
    def centerW(self):
        return self._centerW

    @property
    def bMargin(self):
        return self._bMargin

    @property
    def tMargin(self):
        return self._tMargin

    @property
    def lMargin(self):
        return self._lMargin

    @property
    def rMargin(self):
        return self._rMargin

    @property
    def pText(self):
        return self._pText

    @pText.setter
    def pText(self, val):
        self._pText                     = val

    @rMargin.setter
    def rMargin(self, val):
        self._rMargin                   = val

    @lMargin.setter
    def lMargin(self, val):
        self._lMargin                   = val

    @tMargin.setter
    def tMargin(self, val):
        self._tMargin                   = val

    @bMargin.setter
    def bMargin(self, val):
        self._bMargin                   = val

    @centerW.setter
    def centerW(self, val):
        self._centerW                   = val

    @text.setter
    def text(self, val):
        self._text                      = val

    @currentFont.setter
    def currentFont(self, val):
        self._currentFont               = QFont(self.fontFamily, self.fontSize, self.fontAttr)

    @fontAttr.setter
    def fontAttr(self, val):
        self._fontAttr                  = val

    @fontSize.setter
    def fontSize(self, val):
        self._fontSize                  = val

    @fontFamily.setter
    def fontFamily(self, val):
        self._fontFamily                = val

    @textColor.setter
    def textColor(self, val):
        self._textColor                 = val

    @textBrushColor.setter
    def textBrushColor(self, val):
        self._brushColor                = val

    @penColor.setter
    def penColor(self, val):
        self._penColor                  = val

    @configs.setter
    def configs(self, val):
        self._configs                   = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/25/2020 - 7:27 PM
# © 2017 - 2019 DAMGteam. All rights reserved