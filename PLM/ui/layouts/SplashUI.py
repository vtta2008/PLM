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
from PySide2.QtWidgets                  import QApplication

# PLM
from PLM.options                        import (FRAMELESS, SPLASHSCREEN, ANTIALIAS, TRANSPARENT, NO_PEN, AUTO_COLOR,
                                                TEXT_NORMAL, DAMG_LOGO_COLOR, peacock, DARKBLUE, deep_blue)
from bin.Widgets                        import SplashScreen, MessageBox
from bin.Gui                            import Pixmap, Image, Font, Palette, Painter, Pen, FontMetrics
from bin.Core                           import Timer, Rect
from PLM.configs                        import splashImagePth, ORG_LOGO_DIR, propText as p



class SplashProperty(SplashScreen):

    key                                 = 'SplashProperty'

    _count                              = 0

    # the amount of solid circles will be drawed
    _numOfitems                         = 15

    # the radian of solid circle
    _itemRadius                         = 25

    _revolutionPerSec                   = 1.57079632679489661923

    _num                                = float(_numOfitems)

    _minOpacity                         = 31.4159265358979323846
    _fadeRate                           = 25

    _innerRadius                        = 70

    _mainColor                          = deep_blue

    _brushColor                         = None

    _bufferH                            = 100
    _bufferW                            = 200

    progress                            = None

    _currentP                           = 0

    _fontFamily                         = 'UTM Avo'
    _fontSize                           = 12.0
    _fontAttr                           = TEXT_NORMAL
    _currentFont                        = Font(_fontFamily, _fontSize, _fontAttr)

    _textColor                          = peacock
    _penColor                           = DARKBLUE
    _textBrushColor                     = DAMG_LOGO_COLOR

    _text                               = 'Running Configurations'
    _pText                              = '0%'
    _centerW                            = True

    _bMargin                            = 10
    _tMargin                            = 10
    _lMargin                            = 10
    _rMargin                            = 10

    def __init__(self, app=None):
        SplashScreen.__init__(self)

        # make sure there is an instance of application
        if not app:
            MessageBox(self, 'Application Error', 'critical', p['ERROR_APPLICATION'])
            sys.exit()

        self.app                        = app

        # Query desktop resolution to define the center point
        self.screenH                    = self.screen().size().height()
        self.screenW                    = self.screen().size().width()

    def applySetting(self):

        """ setting layout """

        # setting 100% transperiency background
        palette = Palette(self.palette())
        palette.setColor(palette.Background, TRANSPARENT)
        self.setPalette(palette)

        # make widget frameless like splash screen style
        self.setWindowFlags(SPLASHSCREEN | FRAMELESS)
        self.setEnabled(False)

        # load splash image, this will remove the black background
        self.splashPix = Pixmap(splashImagePth)
        self.setPixmap(self.splashPix)
        self.setMask(self.splashPix.mask())

        # set new font
        self.setFont(self.currentFont)

        # Updates splash widget from the default font to the font has been set.
        self.ensurePolished()

    def updateSize(self):
        """ Adjust size of the layout """

        size = (self.innerR + self.itemR) * 3
        self.setFixedSize(size, size)

    def moveToCenter(self):
        """ Move the splash screen to center of the monitor """

        x = (self.screenW - self.width())/2
        y = (self.screenH - self.height())/2

        self.move(x, y)

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
    def itemR(self):
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
    def innerR(self):
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
    def currentP(self):
        return self._currentP

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

    @innerR.setter
    def innerR(self, val):
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

    @itemR.setter
    def itemR(self, val):
        self._itemRadius                = val

    @numOfitems.setter
    def numOfitems(self, val):
        self._numOfitems                = val

    @currentP.setter
    def currentP(self, val):
        self._currentP              = val

    @bufferW.setter
    def bufferW(self, val):
        self._bufferW                   = val

    @bufferH.setter
    def bufferH(self, val):
        self._bufferH                   = val


class BaseSplash(SplashProperty):

    key                                 = 'BaseSplash'

    def __init__(self, app=None):
        super(BaseSplash, self).__init__(app)

        # setting up palatte, windows flags, splash image
        self.applySetting()

        self.fontM                      = self.fontMetrics()

        # update splash widget size due to new content
        self.updateSize()

        # after update size, need to move to center spot of the screen
        self.moveToCenter()

    def start(self):
        """ show the layout and start counting """

        self.show()

        if not self.timer.isActive():
            self.timer.start()
            self._count = 0

    def stop(self):
        """ hide the layout and stop counting """

        self.hide()

        if self.timer.isActive():
            self.timer.stop()
            self._count = 0

    def writeNewText(self, painter=None, text='', line=1):

        """ this function is to write a new text, it requires current instance painter and the content """

        # calculate the position of text
        x, y = self.getTextPos(text, line)

        # draw a blank text to earse what ever in that position
        painter.drawText(x, y, '')
        self.update()

        # write new text
        painter.drawText(x, y, text)
        self.update()

    def distance(self, current, primary):
        distance = primary - current
        if distance < 0:
            distance += self.numOfitems
        return distance

    def getBrushColor(self, distance, color):
        if distance == 0:
            return color

        minAlphaF = self.minOpacity / 100.0
        distanceThreshold = ceil((self.numOfitems - 1) * self.fadeRate / 100.0)

        if distance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = self.mainColor.alphaF() - minAlphaF
            gradient = alphaDiff / distanceThreshold + 1.0
            resultAlpha = color.alphaF() - gradient * distance
            result = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(result)

        return color

    def getTextPos(self, text, line):

        if self.width() + (self.lMargin + self.rMargin) <= self.textW(text) or self.width() <= self.textW(text):
            self.setFixedSize(self.height() * 2, self.width() * 2)

        if self.centerW:
            x = (self.width() + self.lMargin + self.rMargin - self.textW(text))/2
        else:
            x = (self.width() + self.lMargin + self.rMargin)

        if line == 1:
            y = self.height() - self.bMargin - self.textH()
        else:
            y = self.height() - self.bMargin

        return x, y

    def textW(self, text):
        return self.fontM.width(text)

    def textH(self):
        return self.fontM.height()


class SplashUI(BaseSplash):

    key                                 = 'SplashUI'

    def __init__(self, app=None):
        super(SplashUI, self).__init__(app)

        # Setup timer for counting
        self.timer = Timer(self)
        self.timer.timeout.connect(self.rotate)
        self.updateTimer()

    def updateTimer(self):
        self.timer.setInterval(1000 / (self.numOfitems * self.revolutionPerSec))

    def rotate(self):
        self._count += 1
        if self._count > self._numOfitems:
            self._count = 0
        self.update()

    def paintEvent(self, event):

        """ start drawing animation layout """

        # setting painter for drawing
        painter = Painter()
        painter.begin(self)
        painter.setRenderHint(ANTIALIAS, True)
        painter.fillRect(event.rect(), TRANSPARENT)

        # load DAMGTEAM logo
        self.logo = Image(os.path.join(ORG_LOGO_DIR, '96x96.png'))
        self.logoRect = Rect((self.width() - self.logo.width())/2, (self.height() - self.logo.height())/2,
                             self.logo.width(), self.logo.height())

        # draw logo into layout
        painter.drawImage(self.logoRect, self.logo, self.logo.rect(), AUTO_COLOR)

        # change the setting of painter to draw animated busy loading layout
        painter.setPen(Pen(NO_PEN))

        # start a loop to draw multiple circles allocating around the logo
        for i in range(self.numOfitems):

            # calculate the distance to be able to define the position of curren circle
            distance = self.distance(i, self.count)

            # set brush color for painter
            self._brushColor = self.getBrushColor(distance, self.mainColor)
            painter.setBrush(self.brushColor)

            # start drawing a solid circle
            painter.drawEllipse(self.width() / 2 + self.innerR * cos(2 * pi * i / self.num) - (self.itemR / 2),
                                self.height() / 2 + self.innerR * sin(2 * pi * i / self.num) - (self.itemR / 2),
                                self.itemR, self.itemR)

        # adjust setting of painter for writing text
        painter.setPen(self.textColor)
        painter.setFont(self.currentFont)
        painter.setBrush(self.textBrushColor)

        # text line 1: current config which is being configured.
        self.writeNewText(painter, self.text, 1)

        # text line 2: the percentage of configurations progress
        self.writeNewText(painter, self.pText, 2)

        painter.end()

    def setText(self, text):
        self._text = text

    def setProgress(self, val):
        value = val * 100 / self.num
        for i in range(int(value)):
            self._currentP += 1
            self._pText = '{0}%'.format(str(self.currentP))

            if self.currentP == 96:
                for i in range(4):
                    self._currentP += 1
                    self._pText = '{0}%'.format(str(self.currentP))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ui = SplashUI(app)
    ui.start()
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:56 PM
# © 2017 - 2019 DAMGteam. All rights reserved