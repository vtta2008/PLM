# -*- coding: utf-8 -*-
"""

Script Name: MainWindow.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtWidgets            import QMainWindow, QApplication

# PLM
from appData                    import SETTING_FILEPTH, ST_FORMAT, __copyright__
from ui.uikits.Icon             import AppIcon
from ui.SignalManager           import SignalManager
from cores.Loggers              import Loggers
from cores.Settings             import Settings

# -------------------------------------------------------------------------------------------------------------
""" Main window layout preset """

class MainWindow(QMainWindow):

    Type                        = 'DAMGUI'
    key                         = 'MainWindow'
    _name                       = 'DAMG Main Window'
    _copyright                  = __copyright__
    _data                       = dict()



    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self.parent             = parent
        self.signals            = SignalManager(self)
        self.logger             = Loggers(self.__class__.__name__)
        self.settings           = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.setWindowTitle(self.key)
        self.setWindowIcon(AppIcon(32, self.key))

        self.values = dict(w = self.width(), h = self.height(), x = self.x(), y = self.y())

    def sizeHint(self):
        size = super(MainWindow, self).sizeHint()
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
        self._name                      = newName

def main():
    app = QApplication(sys.argv)
    layout = MainWindow()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 12:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved