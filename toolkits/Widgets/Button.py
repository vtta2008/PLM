# -*- coding: utf-8 -*-
"""

Script Name: Button.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __buildtins__ import __copyright__, settings, signals
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QPushButton, QToolButton

# PLM
from .Icon                                  import AppIcon, TagIcon
from utils                                  import check_preset

# -------------------------------------------------------------------------------------------------------------
""" Button presets """

class Button(QPushButton):

    Type                                    = 'DAMGUI'
    key                                     = 'Button'
    _name                                   = 'DAMG Button'
    _copyright                              = __copyright__()

    def __init__(self, preset={}, parent=None):
        QPushButton.__init__(self)
        self.parent                         = parent
        self.settings                       = settings
        self.signals                        = signals
        self.settings.changeParent(self)
        self.signals.changeParent(self)

        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'txt':
                self.setText(value)
            elif key == 'tt':
                self.setToolTip(value)
            elif key == 'cl':
                self.clicked.connect(value)
            elif key == 'icon':
                self.setIcon(AppIcon(32, value))
            elif key == 'tag':
                self.setIcon(TagIcon(value))
            elif key == 'icon24':
                self.setIcon(AppIcon(24, value))
            elif key == 'fix':
                self.setFixedSize(value)
            elif key == 'ics':
                self.setIconSize(value)
            elif key == 'stt':
                self.setToolTip(value)
            else:
                print("PresetKeyError at {0}: No such key registed in preset: {1}: {2}".format(__name__, key, value))

    def sizeHint(self):
        size = super(Button, self).sizeHint()
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

class ToolButton(QToolButton):

    Type                                    = 'DAMGUI'
    key                                     = 'ToolButton'
    _name                                   = 'DAMG Tool Button'
    _copyright                              = getCopyright()

    def __init__(self, text, parent=None):
        QToolButton.__init__(self)

        self.signals                        = getSignals(self)
        self.settings                       = getSetting(self)
        self.parent                         = parent
        self.setText(text)

    def sizeHint(self):
        size = super(ToolButton, self).sizeHint()
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
        if __name__ == '__main__':
            self.close()
        else:
            self.signals.emit('showLayout', self.key, 'hide')

    def hideEvent(self, event):
        if __name__ == '__main__':
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

            vals = [w, h, x, y]

            for i in range(len(vals)):
                if vals[i] is None:
                    key = [k for k in self.values.keys()]
                    value = self.values[key[i]]
                    for index, element in enumerate(vals):
                        if element == vals[i]:
                            vals[index] = value
                    self.setValue(key[i], self.values[key[i]])

            for v in vals:
                if not type(v) in [int]:
                    v = int(v)

            self.resize(vals[0], vals[1])
            self.move(vals[2], vals[3])

        if __name__ == '__main__':
            self.show()
        else:
            self.signals.emit('showLayout', self.key, 'show')

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:37 AM
# © 2017 - 2018 DAMGteam. All rights reserved