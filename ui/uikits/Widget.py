# -*- coding: utf-8 -*-
"""

Script Name: Widget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

import sys

from PyQt5.QtWidgets                        import QWidget, QVBoxLayout, QLabel, QApplication

from appData                                import SETTING_FILEPTH, ST_FORMAT, __copyright__

from cores.SignalManager                    import SignalManager
from cores.Settings                         import Settings
from cores.Loggers                          import Loggers
from ui.uikits.Icon                         import AppIcon

class Widget(QWidget):

    Type                                    = 'DAMGUI'
    key                                     = 'Widget'
    _name                                   = 'DAMG Widget'
    _copyright                              = __copyright__

    def __init__(self, parent=None):
        QWidget.__init__(self)

        self.parent         = parent

        self.signals        = SignalManager(self)
        self.logger         = Loggers(self.__class__.__name__)
        self.settings       = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)

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
        else:
            self.signals.showLayout.emit(self.key, 'show')
            event.ignore()

    def moveEvent(self, event):
        self.setValue('posX', self.x())
        self.setValue('posY', self.y())

    def resizeEvent(self, event):
        self.setValue('width', self.frameGeometry().width())
        self.setValue('height', self.frameGeometry().height())

    def sizeHint(self):
        size = super(Widget, self).sizeHint()
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
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = Widget()
    widget.setWindowTitle("Widget test layout")
    widget.setWindowIcon(AppIcon(32, 'About'))
    widget.layout = QVBoxLayout()
    widget.layout.addWidget(QLabel("this is a test layout of Widget class"))
    widget.setLayout(widget.layout)
    widget.show()
    app.exec_()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/08/2018 - 4:12 AM
# © 2017 - 2018 DAMGteam. All rights reserved