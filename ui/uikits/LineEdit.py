# -*- coding: utf-8 -*-
"""

Script Name: Label.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets                        import QLineEdit, QPlainTextEdit
from PyQt5.QtGui                            import QIntValidator

# PLM
from appData                                import SETTING_FILEPTH, ST_FORMAT, __copyright__, PRS
from cores.Settings                         import Settings
from ui.SignalManager import SignalManager
from ui.uikits.uiUtils                      import check_preset



class PlainTextEdit(QPlainTextEdit):

    Type                                    = 'DAMGUI'
    key                                     = 'PlainTextEdit'
    _name                                   = 'DAMG Plain Text Edit'
    _copyright                              = __copyright__

    def __init__(self, preset={}, parent=None):
        super(PlainTextEdit, self).__init__(parent)

        self.signals = SignalManager(self)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.parent = parent
        self.preset = preset

        if check_preset(self.preset):
            self.buildUI()

        self.values = dict(w = self.width(), h = self.height(), x = self.x(), y = self.y())

    def sizeHint(self):
        size = super(PlainTextEdit, self).sizeHint()
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
            self.signals.emit('setSetting', 'showLayout', 'hide', self.key)

    def hideEvent(self, event):
        if __name__=='__main__':
            self.hide()
        else:
            if self.settings._settingEnable:
                for key, value in self.values.items():
                    self.setValue(key, value)
            self.signals.emit('setSetting', 'showLayout', 'hide', self.key)

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
            self.signals.emit('setSetting', self.key, 'showLayout', 'show')
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

    def buildUI(self):
        if self.preset is None or self.preset == {}:
            self.preset = {'txt': ' '}

        for key, value in self.preset.items():
            if key == 'lwm': # setLineWrapMode
                self.setLineWrapMode(value)
            elif key == 'sfh': # setFixHeight
                self.setFixedHeight(value)
            elif key == 'vsbp': # setVerticalScrollBarPolicy
                self.setVerticalScrollBarPolicy(value)
            elif key == 'adr': # setAcceptDrops
                self.setAcceptDrops(value)
            elif key == 'rol': # setReadOnly
                self.setReadOnly(value)


class Detector(QPlainTextEdit):

    Type = 'DAMGDETECTOR'
    key = 'Detector'
    _name = 'DAMG Detector'
    _copyright                              = __copyright__

    def sizeHint(self):
        size = super(Detector, self).sizeHint()
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
            self.signals.emit('setSetting', 'showLayout', 'hide', self.key)

    def hideEvent(self, event):
        if __name__=='__main__':
            self.hide()
        else:
            if self.settings._settingEnable:
                for key, value in self.values.items():
                    self.setValue(key, value)
            self.signals.emit('setSetting', 'showLayout', 'hide', self.key)

    def showEvent(self, event):

        self.values = dict(w = self.width(), h = self.height(), x = self.x(), y = self.y())

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
            self.signals.emit('setSetting', self.key, 'showLayout', 'show')
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

class LineEdit(QLineEdit):

    Type                                    = 'DAMGUI'
    key                                     = 'LineEdit'
    _name                                   = 'DAMG Line Edit'
    _copyright                              = __copyright__

    def __init__(self, preset={}, parent=None):
        super(LineEdit, self).__init__(parent)

        self.signals = SignalManager(self)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.parent = parent
        self.preset = preset

        if check_preset(self.preset):
            self.buildUI()

        self.values = dict(w = self.width(), h = self.height(), x = self.x(), y = self.y())

    def sizeHint(self):
        size = super(LineEdit, self).sizeHint()
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

    def buildUI(self):
        if self.preset is None or self.preset == {}:
            self.preset = {'txt': ' '}

        for key, value in self.preset.items():
            if key == 'fn':
                self.setEchoMode(PRS[value])
            elif key == 'txt':
                self.setText(value)
            elif key == 'validator':
                if value == 'int':
                    self.setValidator(QIntValidator())
            elif key == 'echo':
                if value == 'password':
                    self.setEchoMode(QLineEdit.Password)
            else:
                print("PresetKeyError at {0}: No such key registed in preset: {1}: {2}".format(__name__, key, value))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:40 PM
# © 2017 - 2018 DAMGteam. All rights reserved