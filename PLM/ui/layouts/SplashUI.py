# -*- coding: utf-8 -*-
"""

Script Name: SplashUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, os
from math import sin, cos, pi, ceil

# PyQt5
from PyQt5.QtWidgets                    import QApplication
from PyQt5.QtGui import QPainter, QPen, QPalette
from PyQt5.QtCore import QRect

# PLM
from PLM                                import globalSetting
from PLM.configs                        import (ERROR_APPLICATION, FRAMELESS, SPLASHSCREEN, ERROR_LAYOUT_COMPONENT,
                                                splashImagePth, colorLibs, ANTIALIAS, TRANSPARENT, NO_PEN, AUTO_COLOR,
                                                DAMG_LOGO_DIR, TEXT_NORMAL, TEXT_BOLD,
                                                ConfigPython, ConfigUrl, ConfigApps, ConfigPipeline, ConfigIcon,
                                                ConfigAvatar, ConfigLogo, ConfigImage, ConfigEnvVar, ConfigMachine,
                                                ConfigServer, ConfigFormats, ConfigDirectory, ConfigPath, ConfigFonts)
from PLM.commons.Widgets                import SplashScreen, MessageBox, ProgressBar
from PLM.commons.Gui                    import Image, Font, FontMetrics
from PLM.commons.Core                   import Timer, Rect
from PLM.cores                          import StyleSheet



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


class SplashUI(SplashScreen):

    key                                 = 'SplashUI'

    _count                              = 0

    _numOfitems                         = 20
    _revolutionPerSec                   = 1.57079632679489661923
    _num                                = float(_numOfitems)
    _itemRadius                         = 25

    _minOpacity                         = 31.4159265358979323846
    _fadeRate                           = 25

    _innerRadius                        = 70

    _mainColor                          = colorLibs.deep_blue
    _brushColor                         = None

    _bufferH                            = 100
    _bufferW                            = 200

    pythonInfo                          = None
    dirInfo                             = None
    pthInfo                             = None
    urlInfo                             = None
    envInfo                             = None
    iconInfo                            = None
    avatarInfo                          = None
    logoInfo                            = None
    imageInfo                           = None
    serverInfo                          = None
    formatInfo                          = None
    fontInfo                            = None
    deviceInfo                          = None
    appInfo                             = None
    plmInfo                             = None

    progress                            = None

    _cfgCount                           = 0
    _percentCount                       = 0

    _configs                            = 16

    _fontFamily                         = 'UTM Avo'
    _fontSize                           = 12.0
    _fontAttr                           = TEXT_NORMAL
    _currentFont                        = Font(_fontFamily, _fontSize, _fontAttr)

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

    def __init__(self, app=None):
        super(SplashUI, self).__init__(app)

        self.app                        = app

        if not self.app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()

        # setting 100% transperiency background
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, TRANSPARENT)
        self.setPalette(palette)

        # make widget frameless like splash screen style
        self.setWindowFlags(SPLASHSCREEN | FRAMELESS)
        self.setEnabled(False)

        # set new font
        self.setFont(self.currentFont)

        # Updates splash widget from the default font to the font has been set.
        self.ensurePolished()

        # Query desktop resolution to find the center point
        self.screen                     = self.app.desktop().screenGeometry()

        # Setup timer for counting
        self.timer                      = Timer(self)
        self.timer.timeout.connect(self.rotate)
        self.updateTimer()

        # update splash widget size due to new content
        self.updateSize()

        # after update size, need to move to center spot of the screen
        self.updatePosition()

    def start(self):

        self.show()

        if not self.timer.isActive():
            self.timer.start()
            self._count                 = 0

        self.runConfigs()

    def stop(self):

        self.hide()

        if self.timer.isActive():
            self.timer.stop()
            self._count                 = 0

    def updateTimer(self):
        self.timer.setInterval(1000 / (self.numOfitems * self.revolutionPerSec))

    def updateSize(self):
        size = (self.innerRadius + self.itemRadius)*3
        self.setMinimumSize(size, size)

    def updatePosition(self):
        x = self.screen.width()/2 - self.width()/2
        y = self.screen.height()/2 - self.height()/2
        self.move(x, y)

    def runConfigs(self):

        words = ['Python', 'Directories', 'File Paths', 'Urls & Links', 'Environment Variable', 'Icons', 'Avatars',
                 'Logo', 'Images', 'Servers', 'Formats', 'Fonts', 'Local Devices', 'Installed Apps', 'Pipeline Functions']

        configs = [ConfigPython, ConfigDirectory, ConfigPath, ConfigUrl, ConfigEnvVar, ConfigIcon, ConfigAvatar,
                   ConfigLogo, ConfigImage, ConfigServer, ConfigFormats, ConfigFonts, ConfigMachine, ConfigApps,
                   ConfigPipeline]

        for i in range(len(words)):
            if not i == (len(words) - 1):
                self.setText('Config {0}'.format(words[i]))
                if i == 0:
                    self.pythonInfo = configs[i]()
                elif i == 1:
                    self.dirInfo    = configs[i]()
                elif i == 2:
                    self.pthInfo    = configs[i]()
                elif i == 3:
                    self.urlInfo    = configs[i]()
                elif i == 4:
                    self.envInfo    = configs[i]()
                elif i == 5:
                    self.iconInfo   = configs[i]()
                elif i == 6:
                    self.avatarInfo = configs[i]()
                elif i == 7:
                    self.logoInfo   = configs[i]()
                elif i == 8:
                    self.imageInfo  = configs[i]()
                elif i == 9:
                    self.serverInfo = configs[i]()
                elif i == 10:
                    self.formatInfo = configs[i]()
                elif i == 11:
                    self.fontInfo   = configs[i]()
                elif i == 12:
                    self.deviceInfo = configs[i]()
                elif i == 13:
                    self.appInfo    = configs[i]()
                self.setProgress(1)
            else:
                self.setText('Config {0}'.format('Pipeline Functions'))
                if self.iconInfo and self.appInfo and self.urlInfo and self.dirInfo and self.pthInfo:
                    self.plmInfo = ConfigPipeline(self.iconInfo, self.appInfo, self.urlInfo, self.dirInfo, self.pthInfo)
                    self.setProgress(2)
                else:
                    print('Can not conducting Pipeline Functions configurations, some of other configs has not been done yet.')
                    self.app.exit()

            self._cfgCount += 1

        check = False

        if self.cfgCount == len(words):
            for info in [self.pythonInfo, self.dirInfo, self.pthInfo, self.urlInfo, self.envInfo, self.iconInfo,
                         self.avatarInfo, self.logoInfo, self.imageInfo, self.serverInfo, self.formatInfo,
                         self.fontInfo, self.deviceInfo, self.appInfo, self.plmInfo]:
                if not info:
                    print('{0} is None.'.format(info.key))
                    check = False
                else:
                    check = True

        globalSetting.setCfgAll(check)


    def rotate(self):
        self._count += 1
        if self._count > self._numOfitems:
            self._count                 = 0
        self.update()


    def paintEvent(self, event):

        painter                         = QPainter()
        painter.begin(self)
        painter.setRenderHint(ANTIALIAS, True)
        painter.fillRect(event.rect(), TRANSPARENT)


        # Indicating DAMG logo
        self.logo                       = Image(os.path.join(DAMG_LOGO_DIR, '96x96.png'))
        self.logoRect                   = Rect(self.width() / 2 - self.logo.width() / 2,
                                                self.height() / 2 - self.logo.height() / 2,
                                                self.logo.width(), self.logo.height())

        # Indiating busy loading animation layout
        painter.drawImage(self.logoRect, self.logo, self.logo.rect(), AUTO_COLOR)

        painter.setPen(QPen(NO_PEN))

        for i in range(self.numOfitems):

            distance                    = self.distance(i, self.count)
            self._brushColor            = self.getBrushColor(distance, self.mainColor)
            painter.setBrush(self.brushColor)
            painter.drawEllipse(self.width()/2 + self.innerRadius*cos(2*pi*i/self.num) - (self.itemRadius/2),
                                self.height()/2 + self.innerRadius*sin(2*pi*i/self.num) - (self.itemRadius/2),
                                self.itemRadius, self.itemRadius)

        painter.setPen(self.textColor)
        painter.setFont(self.currentFont)
        painter.setBrush(self.textBrushColor)

        # line 1: indicating configuration name working on.
        x, y = self.getTextPos()
        painter.drawText(x, y, '')
        self.update()
        painter.drawText(x, y, self.text)
        self.update()

        # line 2: indicating percentage of configurations done in progress
        x, y = self.getProgressTextPos()
        painter.drawText(x, y, '')
        self.update()
        painter.drawText(x, y, self.pText)
        self.update()

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


    def getTextPos(self):

        if self.width() + (self.lMargin + self.rMargin) <= self.textWidth() or self.width() <= self.textWidth():
            self.setMinimumSize(self.height() * 2, self.width() * 2)

        validW = self.width() + (self.lMargin + self.rMargin)

        if self.centerW:
            x = (validW - self.textWidth()) / 2
        else:
            x = validW

        y = self.height() - self.bMargin - self.textHeight()

        return x, y

    def getProgressTextPos(self):

        if self.width() + (self.lMargin + self.rMargin) <= self.pTextWidth() or self.width() <= self.pTextWidth():
            self.setMinimumSize(self.height()*2, self.width()*2)

        validW = self.width() + (self.lMargin + self.rMargin)


        if self.centerW:
            x                           = (validW - self.pTextWidth())/2
        else:
            x                           = validW

        y                               = self.height() - self.bMargin

        return x, y

    def setText(self, text):
        self._text                      = text

    def setProgress(self, val):
        value                           = val*100/self.num
        for i in range(int(value)):
            self._percentCount += 1
            if self.progress:
                self.progress.setValue(self.percentCount)

            self._pText                 = '{0}%'.format(str(self.percentCount))

            if self.percentCount == 96:
                for i in range(4):
                    self._percentCount += 1
                    if self.progress:
                        self.progress.setValue(self.percentCount)
                    self._pText         = '{0}%'.format(str(self.percentCount))

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
        self._currentFont               = val

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

    @percentCount.setter
    def percentCount(self, val):
        self._percentCount              = val

    @cfgCount.setter
    def cfgCount(self, val):
        self._cfgCount                  = val

    @bufferW.setter
    def bufferW(self, val):
        self._bufferW                   = val

    @bufferH.setter
    def bufferH(self, val):
        self._bufferH                   = val


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ui = SplashUI(app)
    ui.start()
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:56 PM
# © 2017 - 2019 DAMGteam. All rights reserved