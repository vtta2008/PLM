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
from ui.SignalManager import SignalManager
from cores.Settings                         import Settings

from ui.uikits.MainWindow import MainWindow

class MenuBar(QMenuBar):

    Type                                    = 'DAMGUI'
    key                                     = 'MenuBar'
    _name                                   = 'DAMG Menu Bar'
    _copyright                              = __copyright__

    def __init__(self, parent=None):
        super(MenuBar, self).__init__(parent)

        self.parent                         = parent
        self.signals                        = SignalManager(self)
        self.settings                       = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

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

        if __name__=='__main__':
            self.show()

    def moveEvent(self, event):
        self.setValue('posX', self.x())
        self.setValue('posY', self.y())

    def resizeEvent(self, event):
        self.setValue('width', self.frameGeometry().width())
        self.setValue('height', self.frameGeometry().height())

    def sizeHint(self):
        size = super(MenuBar, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

    def closeEvent(self, event):
        if __name__=='__main__':
            self.close()
        else:
            self.signals.emit('showLayout', self.key, 'hide')
            event.ignore()

    def hideEvent(self, event):
        if __name__=='__main__':
            self.hide()
        else:
            self.signals.emit('showLayout', self.key, 'hide')
            event.ignore()

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