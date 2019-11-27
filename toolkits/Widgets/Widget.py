# -*- coding: utf-8 -*-
"""

Script Name: Widget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __buildtins__ import __copyright__, signals, settings

# PyQt5
from PyQt5.QtWidgets                        import QWidget

# PLM
from .Icon                                  import AppIcon


class Widget(QWidget):

    Type                                    = 'DAMGWIDGET'
    key                                     = 'Widget'
    _name                                   = 'DAMG Widget'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.parent                         = parent
        self.settings                       = settings
        self.signals                        = signals
        self.settings.changeParent(self)
        self.signals.changeParent(self)

        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)

    def sizeHint(self):
        size = super(Widget, self).sizeHint()
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
            self.setValue('showLayout', 'close')
            self.close()
        else:
            self.setValue('showLayout', 'hide')
            self.signals.emit('showLayout', self.key, 'hide')

    def hideEvent(self, event):
        if __name__=='__main__':
            self.setValue('showLayout', 'hide')
            self.hide()
        else:
            self.setValue('showLayout', 'hide')
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

            self.resize(int(w)-1, int(h)-1)
            self.resize(int(w), int(h))
            self.move(int(x), int(h))

        if __name__=='__main__':
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
# Created by panda on 1/08/2018 - 4:12 AM
# © 2017 - 2018 DAMGteam. All rights reserved