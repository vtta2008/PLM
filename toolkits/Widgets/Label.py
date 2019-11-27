# -*- coding: utf-8 -*-
"""

Script Name: Label.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QLabel, QLCDNumber
from PyQt5.QtGui                            import QFont, QPixmap
from PyQt5.QtCore                           import QTimeZone, QTime, QDate
print(1)
# PLM
from utils                                  import check_preset
from appData                                import PRS, SETTING_FILEPTH, ST_FORMAT
from toolkits.Core                          import Settings, SignalManager
print(2)
class Label(QLabel):

    Type                                    = 'DAMGUI'
    key                                     = 'Label'
    _name                                   = 'DAMG Label'
    _copyright                              = __copyright__()

    def __init__(self, preset={}, parent=None):
        QLabel.__init__(self)
        print(5)
        self.parent                         = parent
        print(6)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        print(7)
        self.signals = SignalManager(self)
        print(8)
        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def sizeHint(self):
        size = super(Label, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def moveEvent(self, event):
        if self.settings._settingEnable:
            self.setValue('x', self.x())
            self.setValue('y', self.y())

    def resizeEvent(self, event):
        if self.settings._settingEnable:
            self.setValue('w', self.width())
            self.setValue('h', self.height())

    def closeEvent(self, event):
        if __name__=='__main__':
            self.close()
        else:
            self.signals.emit('showLayout', self.key, 'hide')

    def hideEvent(self, event):
        if __name__=='__main__':
            self.hide()
        else:
            if self.settings._settingEnable:
                for key, value in self.values.items():
                    self.setValue(key, value)
            self.signals.emit('showLayout', self.key, 'hide')

    def showEvent(self, event):

        if self.settings._settingEnable:
            w = self.getValue('w')
            h = self.getValue('h')
            x = self.getValue('x')
            y = self.getValue('x')

            if w is None:
                w = self.width()
            if h is None:
                h = self.height()
            if x is None:
                x = 0
            if y is None:
                y = 0
            self.resize(int(w), int(h))
            self.move(int(x), int(h))

        if __name__ == '__main__':
            self.setValue('showLayout', 'show')
            self.show()
        else:
            self.setValue('showLayout', 'show')
            self.signals.emit('showLayout', self.key, 'show')

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

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

class LCDNumber(QLCDNumber):

    Type                                    = 'DAMGUI'
    key                                     = 'LCDNumber'
    _name                                   = 'DAMG LCD Number'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QLCDNumber.__init__(self)

        self.parent                         = parent
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals = SignalManager(self)
        self.time                           = QTime()
        self.zone                           = QTimeZone()
        self.date                           = QDate()

    def sizeHint(self):
        size = super(LCDNumber, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def moveEvent(self, event):
        if self.settings._settingEnable:
            self.setValue('x', self.x())
            self.setValue('y', self.y())

    def resizeEvent(self, event):
        if self.settings._settingEnable:
            self.setValue('w', self.width())
            self.setValue('h', self.height())

    def closeEvent(self, event):
        if __name__=='__main__':
            self.close()
        else:
            self.signals.emit('showLayout', self.key, 'hide')

    def hideEvent(self, event):
        if __name__=='__main__':
            self.hide()
        else:
            if self.settings._settingEnable:
                for key, value in self.values.items():
                    self.setValue(key, value)
            self.signals.emit('showLayout', self.key, 'hide')

    def showEvent(self, event):

        if self.settings._settingEnable:
            w = self.getValue('w')
            h = self.getValue('h')
            x = self.getValue('x')
            y = self.getValue('x')

            if w is None:
                w = self.width()
            if h is None:
                h = self.height()
            if x is None:
                x = 0
            if y is None:
                y = 0
            self.resize(int(w), int(h))
            self.move(int(x), int(h))

        if __name__ == '__main__':
            self.setValue('showLayout', 'show')
            self.show()
        else:
            self.setValue('showLayout', 'show')
            self.signals.emit('showLayout', self.key, 'show')

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

print('solve')

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:40 PM
# © 2017 - 2018 DAMGteam. All rights reserved