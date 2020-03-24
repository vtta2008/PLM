# -*- coding: utf-8 -*-
"""

Script Name: splash.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
import os
import traceback
from math import ceil

# PyQt5
from PyQt5.QtCore                       import QRect, pyqtSlot
from PyQt5.QtGui                        import QPainter, QFont
from PyQt5.QtWidgets                    import QApplication, QDesktopWidget

# PLM
from PLM                                import globalSetting
from PLM.configs                        import (FRAMELESS, bottom, center, colorLibs, splashImagePth, ERROR_APPLICATION,
                                                LINE_SOLID, ERROR_LAYOUT_COMPONENT, TRANSPARENT, NO_PEN, AUTO_COLOR,
                                                ANTIALIAS, STAY_ON_TOP, RELATIVE_SIZE, DAMG_LOGO_DIR, TRANSPARENT_MODE,
                                                TEXT_BOLD,
                                                ConfigPython, ConfigUrl, ConfigApps, ConfigPipeline, ConfigIcon,
                                                ConfigAvatar, ConfigLogo, ConfigImage, ConfigEnvVar, ConfigMachine,
                                                ConfigServer, ConfigFormats, ConfigDirectory, ConfigPath, ConfigFonts)

from PLM.cores                          import StyleSheet
from PLM.commons.Widgets                import SplashScreen, MessageBox
from PLM.commons.Widgets.ProgressBar    import ProgressBar
from PLM.commons.Gui                    import Pixmap, Image, Font
from PLM.commons.Core                   import Timer



class ProgressLoading(ProgressBar):

    key                                 = 'ProgressUI'
    _name                               = 'DAMG Progress UI'

    def __init__(self, parent=None):
        super(ProgressLoading, self).__init__(parent)

        self.parent                     = parent

        if not self.parent:
            MessageBox(self, 'Loading Layout Component', 'critical', ERROR_LAYOUT_COMPONENT)
            sys.exit()
        else:
            self.num                    = self.parent.num
            self.pix                    = self.parent.pix
            self.setMinimum(0)
            self.setMaximum(self.num*10)
            self.setGeometry(50, self.pix.height() - 50, self.pix.width() - 100, 20)
            self.setTextVisible(True)
            self.setStyleSheet(StyleSheet.progressBar())

    def start(self):
        self.show()



class BaseSplash(SplashScreen):

    key                                 = 'BaseSplash'

    iconInfo                            = None
    appInfo                             = None
    urlInfo                             = None
    dirInfo                             = None
    pthInfo                             = None
    deviceInfo                          = None
    pythonInfo                          = None
    avatarInfo                          = None
    logoInfo                            = None
    imageInfo                           = None
    envInfo                             = None
    serverInfo                          = None
    formatInfo                          = None
    fontInfo                            = None

    _value                              = 0
    _num                                = 17

    _mainColor                          = colorLibs.deep_blue
    _textColor                          = colorLibs.peacock
    _textBrushColor                     = colorLibs.DAMG_LOGO_COLOR
    _penColor                           = colorLibs.DARKBLUE


    _brushColor                         = None

    _fontFamily                         = 'Myriad Pro'
    _fontSize                           = 10.0
    _fontAttr                           = TEXT_BOLD
    _textFont                           = QFont(_fontFamily, _fontSize, _fontAttr)
    _texts                              = ['Configuration.', 'Configuration..', 'Configuration...']
    _text                               = ''

    _roundness                          = 100.0
    _minOpacity                         = 31.4159265358979323846
    _fadingRate                         = 25
    _revolutionPerSec                   = 1.57079632679489661923
    _numberOfLines                      = 25
    _lineLength                         = 20
    _lineWidth                          = 10
    _innerRadius                        = 60

    _count                              = 0

    _painter                            = None
    _centerParent                       = True
    _spinning                           = False

    _penWidth                           = 8
    _penLine                            = LINE_SOLID
    _radius                             = 40
    _circleSize                         = 400

    _numOfSections                      = 16
    _startAngle                         = 90

    def __init__(self, app=None):
        super(BaseSplash, self).__init__(app)

        self.app                        = app

        if not self.app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()

        self.setWindowFlags(STAY_ON_TOP|FRAMELESS)
        self.screen                     = QDesktopWidget().availableGeometry()
        self.setGeometry(self.screen)
        self.cp                         = self.screen.center()   # center point
        self.move(self.cp.x()-(self.width()/2), self.cp.y()-(self.height()/2))

        self.timer                      = Timer(self)
        self.timer.timeout.connect(self.rotate)
        self.updateTimer()

    def updateTimer(self):
        self.timer.setInterval(1000/(self._numberOfLines*self._revolutionPerSec))

    def color(self):
        return self._mainColor

    @pyqtSlot()
    def rotate(self):
        self._count += 1
        if self._count > self._numberOfLines:
            self._count                 = 0
        self.update()

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

    def start_configuring(self):

        ws = ['Icons', 'Installed apps', 'Urls', 'Directories', 'Paths', 'Local Device', 'Python', 'Avatars', 'Logo',
              'Images', 'Evironment Variables', 'Server', 'Formats', 'Fonts', 'Pipeline', ]

        fs = [ConfigIcon, ConfigApps, ConfigUrl, ConfigDirectory, ConfigPath, ConfigMachine, ConfigPython, ConfigAvatar,
              ConfigLogo, ConfigImage, ConfigEnvVar, ConfigServer, ConfigFormats, ConfigFonts, ConfigPipeline]

        vs = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]

        for i in range(len(ws)):
            w = ws[i]
            f = fs[i]
            v = vs[i]
            self.process_config(w, f, v)

    def process_config(self, w, f, v):

        try:
            self.show_message('Config {0}'.format(w))
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            print(exctype, value, traceback.format_exc())
        try:
            if w == 'Icons':
                self.iconInfo = f()
            elif w == 'Installed apps':
                self.appInfo = f()
            elif w == 'Urls':
                self.urlInfo = f()
            elif w == 'Directories':
                self.dirInfo = f()
            elif w == 'Paths':
                self.pthInfo = f()
            elif w == 'Local Device':
                self.deviceInfo = f()
            elif w == 'Python':
                self.pythonInfo = f()
            elif w == 'Avatars':
                self.avatarInfo = f()
            elif w == 'Logo':
                self.logoInfo = f()
            elif w == 'Images':
                self.imageInfo = f()
            elif w == 'Evironment Variables':
                self.envInfo = f()
            elif w == 'Server':
                self.serverInfo = f()
            elif w == 'Formats':
                self.formatInfo = f()
            elif w == 'Fonts':
                self.fontInfo = f()
            else:
                self.plmInfo = f(self.iconInfo, self.appInfo, self.urlInfo, self.dirInfo, self.pthInfo)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            print(exctype, value, traceback.format_exc())

        try:
            self.updateProgress(v)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            print(exctype, value, traceback.format_exc())

    @property
    def value(self):
        return self._value

    @property
    def num(self):
        return self._num

    @property
    def textColor(self):
        return self._textColor

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

    @property
    def numOfSections(self):
        return self._numOfSections

    @property
    def startAngle(self):
        return self._startAngle

    @property
    def brushColor(self):
        return self._brushColor

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
    def textFont(self):
        return self._textFont

    @property
    def text(self):
        return self._text

    @property
    def texts(self):
        return self._texts

    @property
    def textBrushColor(self):
        return self._textBrushColor

    @textBrushColor.setter
    def textBrushColor(self, val):
        self._brushColor                = val

    @texts.setter
    def texts(self, val):
        self.texts                      = val

    @text.setter
    def text(self, val):
        self.text                       = val

    @textFont.setter
    def textFont(self, val):
        self._textFont                  = val

    @fontAttr.setter
    def fontAttr(self, val):
        self._fontAttr                  = val

    @fontSize.setter
    def fontSize(self, val):
        self._fontSize                  = val

    @fontFamily.setter
    def fontFamily(self, val):
        self._fontFamily                = val

    @brushColor.setter
    def brushColor(self, val):
        self._brushColor                = val

    @startAngle.setter
    def startAngle(self, val):
        self._startAngle                = val

    @numOfSections.setter
    def numOfSections(self, val):
        self._numOfSections             = val

    @textColor.setter
    def textColor(self, val):
        self._textColor                 = val

    @value.setter
    def value(self, val):
        self._value                     = val

    @num.setter
    def num(self, val):
        self._num                       = val

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



class SplashUI(BaseSplash):

    key                                         = 'SplashUI'

    def __init__(self, app=None):
        super(SplashUI, self).__init__(app)

        self.app                                = app

        # self.splashPix                          = Pixmap(splashImagePth)
        # self.setPixmap(self.splashPix)
        # self.setMask(self.splashPix.mask())
        # self.setEnabled(False)

        self.uiGeo                              = self.frameGeometry()
        self.show()
        self.start()
        self.app.processEvents()

    def start(self):
        self._spinning                          = True

        if not self.timer.isActive():
            self.timer.start(50)
            self._count                         = 0

    def stop(self):
        self._spinning                          = False

        if not self.timer.isActive():
            self.timer.stop()

    def show_message(self, mess):
        if globalSetting.splashLoadingMode == 'progress':
            self.showMessage(mess, bottom|center, colorLibs.DARKCYAN)

    def updateProgress(self, value):
        if globalSetting.splashLoadingMode == 'progress':
            if value == 0:
                self.progressBar.setValue(0)
            else:
                value = value*10
                for i in range(value):
                    self.value += 1
                    self.progressBar.setValue(self.value)
                    i += 1


    def paintEvent(self, event):

        self.eRect                      = event.rect()
        self.damgLogoImg                = Image(os.path.join(DAMG_LOGO_DIR, '96x96.png'))
        self.damgLogoImgTargetRect      = QRect(32, 32, self.damgLogoImg.width(), self.damgLogoImg.height())

        self._painter                   = QPainter(self)

        self._painter.begin(self)
        self._painter.setBackgroundMode(TRANSPARENT_MODE)
        self._painter.setRenderHint(ANTIALIAS)
        self._painter.fillRect(self.eRect, TRANSPARENT)

        self._painter.drawImage(self.damgLogoImgTargetRect, self.damgLogoImg, self.damgLogoImg.rect(), AUTO_COLOR)

        self._painter.setPen(NO_PEN)
        # self._painter.save()

        if self._count > self._numberOfLines:
            self._count                     = 0

        factor                          = self._numberOfLines // len(self._texts)
        next_i                          = 0
        next_index                      = 0

        for i in range(self._numberOfLines):
            x                               = 0
            y                               = (self._lineWidth // 2)*(-1)
            w                               = self._lineLength
            h                               = w
            rotateAngle                     = 360*i/self._numberOfLines
            distance                        = self.distanceFromPrimary(i, self._count, self._numberOfLines)
            translate                       = self._innerRadius + self._lineLength
            self._brushColor                = self.lineColor(distance, self._numberOfLines, self._fadingRate, self._minOpacity, self._mainColor)

            self.autoLoadingTargetRect      = QRect(x, y, w, h)
            self.autoLoadingTargetRect.moveCenter(self.cp)

            self.painter.setPen(NO_PEN)
            self._painter.save()
            self._painter.translate(translate, translate)
            self._painter.rotate(rotateAngle)
            self._painter.translate(self._innerRadius, 0)
            self._painter.translate(self.cp.x(), self.cp.y())
            self._painter.setBrush(self._brushColor)
            self._painter.drawRoundedRect(self.autoLoadingTargetRect, self._roundness, self._roundness, RELATIVE_SIZE)
            self._painter.restore()

            if i == next_i:
                self._painter.setPen(self._textColor)
                self._painter.setFont(self._textFont)
                self._painter.setBrush(self._textBrushColor)

                x = ((self.eRect.width()-(len(self._text)*(self._fontSize/2)))/2) - 5
                y = self.eRect.height()*0.9

                self._text                  = ''
                self._painter.drawText(x, y, self._text)
                self.update()

                self._text                  = self._texts[next_index]
                self._painter.drawText(x, y, self._text)

                next_i = next_i + (i + factor)
                next_index += 1

        self._painter.end()

        # r                               = self._radius
        # s                               = self._circleSize
        # start                           = self._startAngle*16
        # end                             = ((360/self._numOfSections)*self._count)*16
        # print(end)
        # self._painter.setPen(Pen(self._penColor, self._penWidth, self._penLine))
        # self._painter.setBrush(NO_BRUSH)
        # self._painter.drawArc(r, r, s, s, start, end)
        #
        # self._painter.end()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ui = SplashUI(app)
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/25/2020 - 12:49 AM
# © 2017 - 2019 DAMGteam. All rights reserved