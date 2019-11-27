# -*- coding: utf-8 -*-
"""

Script Name: MainWindow.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__

""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QMainWindow

# PLM
from toolkits.Widgets                       import AppIcon
from cores.Loggers                          import Loggers
from appData                                import SETTING_FILEPTH, ST_FORMAT
from toolkits.Core                          import Settings, SignalManager

# -------------------------------------------------------------------------------------------------------------
""" Main window layout preset """

class MainWindow(QMainWindow):

    Type                        = 'DAMGUI'
    key                         = 'MainWindow'
    _name                       = 'DAMG Main Window'
    _copyright                  = __copyright__()
    _data                       = dict()

    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self.parent             = parent
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals = SignalManager(self)
        self.logger             = Loggers(self.__class__.__name__)

        self.setWindowTitle(self.key)
        self.setWindowIcon(AppIcon(32, self.key))

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def sizeHint(self):
        size = super(MainWindow, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

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
            self.setValue('showLayout', 'close')
            self.close()
        else:
            self.setValue('showLayout', 'hide')
            self.signals.emit('showLayout', self.key, 'hide')

    def hideEvent(self, event):
        if __name__ == '__main__':
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
# Created by panda on 25/10/2019 - 12:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved