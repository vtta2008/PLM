# -*- coding: utf-8 -*-
"""

Script Name: ComboBox.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__, settings, signals

# PyQt5
from PyQt5.QtWidgets                        import QComboBox

# PLM
from utils                                  import check_preset

class ComboBox(QComboBox):

    Type                                    = 'DAMGUI'
    key                                     = 'ComboBox'
    _name                                   = 'DAMG Combo Box'
    _copyright                              = __copyright__()

    def __init__(self, preset={}, parent=None):
        QComboBox.__init__(self)

        self.parent                         = parent
        self.settings                       = settings
        self.signals                        = signals
        self.settings.changeParent(self)
        self.signals.changeParent(self)
        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def sizeHint(self):
        size = super(ComboBox, self).sizeHint()
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
            if key == 'items':
                for item in value:
                    self.addItem(item)
            elif key == 'editable':
                self.setEditable(value)
            elif key == 'curIndex':
                self.setCurrentIndex(value)
            elif key == 'setObjName':
                self.setObjectName(value)
            else:
                print("PRESETKEYERROR: There is no key in preset: {}".format(key))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:55 PM
# © 2017 - 2018 DAMGteam. All rights reserved