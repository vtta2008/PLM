# -*- coding: utf-8 -*-
"""

Script Name: Label.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PySide2.QtWidgets                      import QLabel, QLCDNumber
from .LineEdit import LineEdit
from .SizePolicy import SizePolicy
from bin.Gui import Font, Pixmap
from bin.Core import TimeZone, Time, Date, Qt

SiPoMin                     = SizePolicy.Minimum                                               # Size policy
SiPoMax                     = SizePolicy.Maximum
SiPoExp                     = SizePolicy.Expanding
SiPoPre                     = SizePolicy.Preferred
SiPoIgn                     = SizePolicy.Ignored

center                      = Qt.AlignCenter                                                    # Alignment
right                       = Qt.AlignRight
left                        = Qt.AlignLeft

PRS = dict( password    = LineEdit.Password,       center = center ,   left  = left   ,    right  = right,
            spmax       = SiPoMax           ,      sppre  = SiPoPre,   spexp = SiPoExp,    spign  = SiPoIgn,
            expanding   = SizePolicy.Expanding,    spmin  = SiPoMin,)

# -------------------------------------------------------------------------------------------------------------
class Label(QLabel):

    Type                                    = 'DAMGUI'
    key                                     = 'Label'
    _name                                   = 'DAMG Label'

    def __init__(self, preset=None, parent=None):
        QLabel.__init__(self)

        self.parent                         = parent
        self.preset                         = preset
        if self.preset:
            self.buildUI()

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'txt':
                self.setText(value)
            elif key == 'fnt':
                self.setFont(Font(value))
            elif key == 'alg':
                self.setAlignment(PRS[value])
            elif key == 'wmax':
                self.setMaximumWidth(value)
            elif key == 'wmin':
                self.setMinimumWidth(value)
            elif key == 'hmin':
                self.setMinimumHeight(value)
            elif key == 'smin':
                self.setMinimumSize(value[0], value[1])
            elif key == 'smax':
                self.setMaximumSize(value[0], value[1])
            elif key == 'sizePolicy':
                self.setSizePolicy(PRS[value[0]], PRS[value[1]])
            elif key == 'pxm':
                self.setPixmap(Pixmap(value))
            elif key == 'scc':
                self.setScaledContents(value)
            elif key == 'sfs':
                self.setFixedSize(value[0], value[1])
            elif key == 'setBuddy':
                self.setBuddy(value)
            elif key == 'link':
                self.setOpenExternalLinks(value)
            elif key == 'stt':
                self.setToolTip(value)
            elif key == 'sst':
                self.setStatusTip(value)
            elif key == 'sss':
                self.setStyleSheet(value)
            else:
                print("PresetKeyError at {0}: No such key registed in preset: {1}: {2}".format(__name__, key, value))
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


class TextLabel(QLabel):

    Type                                = 'DAMGUI'
    key                                 = 'LCDNumber'
    _name                               = 'DAMG LCD Number'

    def __init__(self, parent=None, elideMode=None):
        super(TextLabel, self).__init__(parent)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                      = val


class LCDNumber(QLCDNumber):

    Type                                    = 'DAMGUI'
    key                                     = 'LCDNumber'
    _name                                   = 'DAMG LCD Number'

    def __init__(self, parent=None):
        QLCDNumber.__init__(self)

        self.parent                         = parent
        self.time                           = Time()
        self.zone                           = TimeZone()
        self.date                           = Date()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

    def currentTime(self):
        return self.time.currentTime()

    def currentTimeZone(self):
        return self.zone.utc()

    def currentDate(self):
        return self.date.currentDate()


def user_pass_label():
    usernameLabel = Label({'txt': 'Username'})
    passwordLabel = Label({'txt': 'Password'})
    return usernameLabel, passwordLabel

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:40 PM
# © 2017 - 2018 DAMGteam. All rights reserved