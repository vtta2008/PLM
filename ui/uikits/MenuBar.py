# -*- coding: utf-8 -*-
"""

Script Name: Menu.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import sys

from PyQt5.QtWidgets import QMenuBar, QApplication

from appData                                import SETTING_FILEPTH, ST_FORMAT, __copyright__
from ui.SignalManager                       import SignalManager
from cores.Settings                         import Settings
from bin.dependencies.damg.damg import DAMGDICT
from ui.uikits.MainWindow                   import MainWindow

class MenuBar(QMenuBar):

    Type                                    = 'DAMGUI'
    key                                     = 'MenuBar'
    _name                                   = 'DAMG Menu Bar'
    _copyright                              = __copyright__
    menus                                   = DAMGDICT()

    def __init__(self, parent=None):
        super(MenuBar, self).__init__(parent)

        self.parent                         = parent
        self.signals                        = SignalManager(self)
        self.settings                       = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.values = dict(w = self.width(), h = self.height(), x = self.x(), y = self.y())

    def sizeHint(self):
        size = super(MenuBar, self).sizeHint()
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

class TestWidget(MainWindow):

    def __init__(self):
        super(TestWidget, self).__init__(self)

        self.menubar = MenuBar(self)
        self.menubar.addMenu('TestMenu')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWidget()
    window.show()
    app.exec_()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/10/2019 - 2:23 PM
# © 2017 - 2018 DAMGteam. All rights reserved