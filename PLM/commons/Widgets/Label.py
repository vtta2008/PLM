# -*- coding: utf-8 -*-
"""

Script Name: Label.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QLabel, QLCDNumber
from PyQt5.QtGui                            import QFont, QPixmap
from PyQt5.QtCore                           import QTimeZone, QTime, QDate

# PLM
from PLM.utils                              import check_preset
from PLM.configs                            import PRS
from PLM.cores                              import SettingManager
from PLM.cores                              import SignalManager

# -------------------------------------------------------------------------------------------------------------
class Label(QLabel):

    Type                                    = 'DAMGUI'
    key                                     = 'Label'
    _name                                   = 'DAMG Label'
    _copyright                              = __copyright__()

    def __init__(self, preset={}, parent=None):
        QLabel.__init__(self)

        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)

        self.preset                         = preset
        if check_preset(self.preset):
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
                self.setFont(QFont(value))
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
                self.setPixmap(QPixmap(value))
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
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

class LCDNumber(QLCDNumber):

    Type                                    = 'DAMGUI'
    key                                     = 'LCDNumber'
    _name                                   = 'DAMG LCD Number'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QLCDNumber.__init__(self)

        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)
        self.time                           = QTime()
        self.zone                           = QTimeZone()
        self.date                           = QDate()

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def copyright(self):
        return self._copyright

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