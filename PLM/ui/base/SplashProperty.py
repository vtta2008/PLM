# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import sys


# PLM
from PLM.options                        import (FRAMELESS, SPLASHSCREEN, TRANSPARENT, TEXT_NORMAL, DAMG_LOGO_COLOR,
                                                peacock, DARKBLUE, deep_blue)

from bin.Widgets                        import SplashScreen, MessageBox
from bin.Gui                            import Pixmap, Font, Palette
from PLM.configs                        import splashImagePth, propText as p



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
        self._currentP                  = val

    @bufferW.setter
    def bufferW(self, val):
        self._bufferW                   = val

    @bufferH.setter
    def bufferH(self, val):
        self._bufferH                   = val



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
