# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys
from math import ceil

# PLM
from PLM.configs                            import (ERROR_APPLICATION, FRAMELESS, SPLASHSCREEN, TRANSPARENT, TEXT_NORMAL,
                                                    colorLibs, ANTIALIAS, DAMG_LOGO_DIR, NO_PEN, ERROR_LAYOUT_COMPONENT,
                                                    )
from PLM.api.Widgets import SplashScreen, MessageBox, ProgressBar
from PLM.api.Gui import Font, Palette, Image, Pen, Painter, FontMetrics
from PLM.ui.framework import Timer
from PLM.cores                              import Loggers, StyleSheet



class LoadingBar(ProgressBar):

    key                                 = 'ProgressUI'
    _name                               = 'DAMG Progress UI'

    def __init__(self, parent=None):
        super(LoadingBar, self).__init__(parent)

        self.parent                     = parent

        if not self.parent:
            MessageBox(self, 'Loading Layout Component', 'critical', ERROR_LAYOUT_COMPONENT)
            sys.exit()
        else:
            self.num                    = self.parent.num
            self.pix                    = self.parent.splashPix
            self.setMinimum(0)
            self.setMaximum(100)

            self.setGeometry((self.pix.width()-self.width())/2 + 115, self.pix.height() - 115, self.pix.width()/10, 10)
            self.setTextVisible(False)
            self.setStyleSheet(StyleSheet.progressBar())



class BaseSplash(SplashScreen):

    key                                     = 'BaseSplash'

    _count                                  = 0
    _numOfitems                             = 20
    _revolutionPerSec                       = 1.57079632679489661923
    _num                                    = float(_numOfitems)
    _itemRadius                             = 25

    _minOpacity                             = 31.4159265358979323846
    _fadeRate                               = 25

    _innerRadius                            = 70

    _mainColor                              = colorLibs.deep_blue
    _brushColor                             = None

    _bufferH                                = 100
    _bufferW                                = 200

    _cfgCount                               = 0
    _percentCount                           = 0

    _configs                                = 16

    _fontFamily                             = 'UTM Avo'
    _fontSize                               = 12.0
    _fontAttr                               = TEXT_NORMAL
    _currentFont                            = Font(_fontFamily, _fontSize, _fontAttr)

    _textColor                              = colorLibs.peacock
    _penColor                               = colorLibs.DARKBLUE
    _textBrushColor                         = colorLibs.DAMG_LOGO_COLOR

    _text                                   = 'Running Configurations'
    _pText                                  = '0%'
    _centerW                                = True

    _bMargin                                = 10
    _tMargin                                = 10
    _lMargin                                = 10
    _rMargin                                = 10

    logo                                    = None

    pythonInfo                              = None
    dirInfo                                 = None
    pthInfo                                 = None
    urlInfo                                 = None
    envInfo                                 = None
    iconInfo                                = None
    avatarInfo                              = None
    logoInfo                                = None
    imageInfo                               = None
    serverInfo                              = None
    formatInfo                              = None
    fontInfo                                = None
    deviceInfo                              = None
    appInfo                                 = None
    plmInfo                                 = None


    def __init__(self, app=None):
        SplashScreen.__init__(app)

        self.app = app

        if not app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()

        if not self.logo:
            self.logo                       = Image(os.path.join(DAMG_LOGO_DIR, '96x96.png'))

        # set logger
        self.logger                         = Loggers(self)

        # set flag
        self.setWindowFlags(SPLASHSCREEN | FRAMELESS)
        self.setFont(self.currentFont)

        # set palette
        palette = Palette()
        palette.setColor(palette.Background, TRANSPARENT)
        self.setPalette(palette)

        # set painter
        self.painter                        = Painter()
        self.painter.setRenderHint(ANTIALIAS)

        self.progress                       = LoadingBar(self)
        self.progress.show()
        self.updatePosition()

        self.timer                          = Timer(self)


    def rotate(self):
        self._count += 1
        if self._count > self._numOfitems:
            self._count                     = 0
        self.update()

    def setImage(self, image):
        self.setPixmap(image)
        self.setMask(image.mask())

    def setLogo(self, logo):
        self.logo                           = logo

    def setNoPen(self):
        self.painter.setPen(Pen(NO_PEN))

    def setTextPen(self):
        self.painter.setPen(self.textColor)
        self.painter.setFont(self.currentFont)
        self.painter.setBrush(self.textBrushColor)

    def updatePosition(self):
        return self.move((self.screen.width() - self.width())/2, (self.screen.height() - self.height())/2)

    def distance(self, current, primary):
        distance                            = primary - current
        if distance < 0:
            distance += self.numOfitems
        return distance

    def getBrushColor(self, distance, color):
        if distance == 0:
            return color

        minAlphaF                           = self.minOpacity / 100.0
        distanceThreshold                   = ceil((self.numOfitems - 1) * self.fadeRate / 100.0)

        if distance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff                       = self.mainColor.alphaF() - minAlphaF
            gradient                        = alphaDiff / distanceThreshold + 1.0
            resultAlpha                     = color.alphaF() - gradient * distance
            result                          = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(result)

        return color

    def processEvents(self):
        if not self.app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()
        else:
            return self.app.processEvents()

    def getTextPos(self):

        if self.centerW:
            x = (self.width() + self.rMargin + self.lMargin) / 2 - self.textWidth() / 2
        else:
            x = (self.width() + self.rMargin + self.lMargin)

        y = self.height() - self.bufferH - self.textHeight() - self.bMargin

        return x, y

    def getProgressTextPos(self):

        if self.centerW:
            x = (self.width() + self.rMargin + self.lMargin) / 2 - self.pTextWidth() / 2
        else:
            x = (self.width() + self.rMargin + self.lMargin)

        y = self.height() - self.bufferH - self.textHeight() + self.bMargin * 2

        return x, y

    def setText(self, text):
        self._text                          = text

    def setProgress(self, val):
        value = (100 * val) / self.num
        for i in range(int(value)):
            self._percentCount += 1
            if self.progress:
                self.progress.setValue(self.percentCount)
            self._pText = '{0}%'.format(str(self.percentCount))

            if self.percentCount == 96:
                for i in range(4):
                    self._percentCount += 1
                    if self.progress:
                        self.progress.setValue(self.percentCount)
                    self._pText = '{0}%'.format(str(self.percentCount))


    def textWidth(self):
        fm = FontMetrics(self.currentFont)
        return fm.width(self.text)

    def pTextWidth(self):
        fm = FontMetrics(self.currentFont)
        return fm.width(str(self.pText))

    def textHeight(self):
        fm = FontMetrics(self.currentFont)
        return fm.height()

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

    @property
    def bufferH(self):
        return self._bufferH

    @property
    def bufferW(self):
        return self._bufferW

    @property
    def cfgCount(self):
        return self._cfgCount

    @property
    def percentCount(self):
        return self._percentCount

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
        self._pText                         = val

    @rMargin.setter
    def rMargin(self, val):
        self._rMargin                       = val

    @lMargin.setter
    def lMargin(self, val):
        self._lMargin                       = val

    @tMargin.setter
    def tMargin(self, val):
        self._tMargin                       = val

    @bMargin.setter
    def bMargin(self, val):
        self._bMargin                       = val

    @centerW.setter
    def centerW(self, val):
        self._centerW                       = val

    @text.setter
    def text(self, val):
        self._text                          = val

    @currentFont.setter
    def currentFont(self, val):
        self._currentFont                   = Font(self.fontFamily, self.fontSize, self.fontAttr)

    @fontAttr.setter
    def fontAttr(self, val):
        self._fontAttr                      = val

    @fontSize.setter
    def fontSize(self, val):
        self._fontSize                      = val

    @fontFamily.setter
    def fontFamily(self, val):
        self._fontFamily                    = val

    @textColor.setter
    def textColor(self, val):
        self._textColor                     = val

    @textBrushColor.setter
    def textBrushColor(self, val):
        self._brushColor                    = val

    @penColor.setter
    def penColor(self, val):
        self._penColor                      = val

    @configs.setter
    def configs(self, val):
        self._configs                       = val

    @percentCount.setter
    def percentCount(self, val):
        self._percentCount                  = val

    @cfgCount.setter
    def cfgCount(self, val):
        self._cfgCount                      = val

    @bufferW.setter
    def bufferW(self, val):
        self._bufferW                       = val

    @bufferH.setter
    def bufferH(self, val):
        self._bufferH                       = val

    @revolutionPerSec.setter
    def revolutionPerSec(self, val):
        self._revolutionPerSec              = val

    @num.setter
    def num(self, val):
        self._num                           = val

    @count.setter
    def count(self, val):
        self._count                         = val

    @brushColor.setter
    def brushColor(self, val):
        self._brushColor                    = val

    @innerRadius.setter
    def innerRadius(self, val):
        self._innerRadius                   = val

    @fadeRate.setter
    def fadeRate(self, val):
        self._fadeRate                      = val

    @minOpacity.setter
    def minOpacity(self, val):
        self._minOpacity                    = val

    @mainColor.setter
    def mainColor(self, val):
        self._mainColor                     = val

    @itemRadius.setter
    def itemRadius(self, val):
        self._itemRadius                    = val

    @numOfitems.setter
    def numOfitems(self, val):
        self._numOfitems                    = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved