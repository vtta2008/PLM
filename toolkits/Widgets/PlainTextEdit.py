# -*- coding: utf-8 -*-
"""

Script Name: PlainTextEdit.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets                        import QPlainTextEdit

from toolkits                               import getCopyright, getSetting, getSignals, check_preset

class PlainTextEdit(QPlainTextEdit):

    Type                                    = 'DAMGPLAINTEXTEDIT'
    key                                     = 'PlainTextEdit'
    _name                                   = 'DAMG Plain Text Edit'
    _copyright                              = getCopyright()

    def __init__(self, preset={}, parent=None):
        super(PlainTextEdit, self).__init__(parent)

        self.settings                       = getSetting(self)
        self.signals                        = getSignals(self)
        self.parent                         = parent

        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def sizeHint(self):
        size = super(PlainTextEdit, self).sizeHint()
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
            self.signals.emit('setSetting', 'showLayout', 'hide', self.key)

    def hideEvent(self, event):
        if __name__=='__main__':
            self.hide()
        else:
            if self.settings._settingEnable:
                for key, value in self.values.items():
                    self.setValue(key, value)
            self.signals.emit('setSetting', 'showLayout', 'hide', self.key)

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
        if self.preset is None or self.preset == {}:
            self.preset = {'txt': ' '}

        for key, value in self.preset.items():
            if key == 'lwm': # setLineWrapMode
                self.setLineWrapMode(value)
            elif key == 'sfh': # setFixHeight
                self.setFixedHeight(value)
            elif key == 'vsbp': # setVerticalScrollBarPolicy
                self.setVerticalScrollBarPolicy(value)
            elif key == 'adr': # setAcceptDrops
                self.setAcceptDrops(value)
            elif key == 'rol': # setReadOnly
                self.setReadOnly(value)


class Detector(PlainTextEdit):

    key                                     = 'Detector'
    _name                                   = 'DAMG Detector'


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/11/2019 - 6:44 PM
# © 2017 - 2018 DAMGteam. All rights reserved