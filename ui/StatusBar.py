# -*- coding: utf-8 -*-
"""

Script Name: StatusBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtWidgets        import QApplication, QStatusBar

# Plm
from appData                    import SETTING_FILEPTH, ST_FORMAT, __copyright__
from ui.SignalManager           import SignalManager
from cores.Loggers              import Loggers
from cores.Settings             import Settings


# -------------------------------------------------------------------------------------------------------------
""" StatusBar """


class StatusBar(QStatusBar):

    Type                                    = "DAMGUI"
    key                                     = 'StatusBar'
    _name                                   = "DAMG Status Bar"
    _copyright                              = __copyright__
    _data                                   = dict()

    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)

        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def showEvent(self, event):
        sizeX = self.getValue('width')
        sizeY = self.getValue('height')

        if not sizeX is None and not sizeY is None:
            self.resize(int(sizeX), int(sizeY))

        posX = self.getValue('posX')
        posY = self.getValue('posY')

        if not posX is None and not posX is None:
            self.move(posX, posY)

    def moveEvent(self, event):
        self.setValue('posX', self.x())
        self.setValue('posY', self.y())

    def resizeEvent(self, event):
        self.setValue('width', self.frameGeometry().width())
        self.setValue('height', self.frameGeometry().height())

    def sizeHint(self):
        size = super(StatusBar, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

    def closeEvent(self, event):
        if __name__=='__main__':
            self.close()
        else:
            self.signals.showLayout.emit(self.key, 'hide')
            event.ignore()

    def hideEvent(self, event):
        if __name__=='__main__':
            self.hide()
        else:
            self.signals.showLayout.emit(self.key, 'hide')
            event.ignore()

    @property
    def copyright(self):
        return self._copyright

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @name.setter
    def name(self, newName):
        self._name                      = newName


def main():
    app = QApplication(sys.argv)
    layout = StatusBar()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:39 PM
# © 2017 - 2018 DAMGteam. All rights reserved
