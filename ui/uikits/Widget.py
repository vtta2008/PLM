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

from ui.SignalManager import SignalManager
from cores.Settings                         import Settings
from ui.uikits.Icon                         import AppIcon

class Widget(QWidget):

    Type                                    = 'DAMGWIDGET'
    key                                     = 'Widget'
    _name                                   = 'DAMG Widget'
    _copyright                              = __copyright__

    def __init__(self, parent=None):
        QWidget.__init__(self)

        self.parent         = parent

        self.signals        = SignalManager(self)
        self.settings       = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)

        self.values = dict(w = self.width(), h = self.height(), x = self.x(), y = self.y())

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

        if __name__=='__main__':
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