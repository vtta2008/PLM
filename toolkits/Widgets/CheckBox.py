# -*- coding: utf-8 -*-
"""

Script Name: CheckBox.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets                        import QCheckBox

from toolkits                               import getCopyright, getSetting, getSignals, check_preset

class CheckBox(QCheckBox):

    Type                                    = 'DAMGUI'
    key                                     = 'CheckBox'
    _name                                   = 'DAMG Check Box'
    _copyright                              = getCopyright()

    def __init__(self, txt=None, preset={}, parent=None):
        super(CheckBox, self).__init__(parent)

        self.signals                        = getSignals(self)
        self.settings                       = getSetting(self)
        self.parent                         = parent
        self.txt                            = txt

        if self.txt is not None:
            self.setText(self.txt)
        self.stateChanged.connect(self.saveState)

        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'tt':
                self.setToolTip(value)

    def saveState(self, val):
        if val >= 1:
            state = True
        else:
            state = False
        self.setValue('checkState', state)

    def sizeHint(self):
        size = super(CheckBox, self).sizeHint()
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
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:53 PM
# © 2017 - 2018 DAMGteam. All rights reserved