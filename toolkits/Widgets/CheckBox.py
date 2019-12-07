# -*- coding: utf-8 -*-
"""

Script Name: CheckBox.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__

from PyQt5.QtWidgets                        import QCheckBox
from utils                                  import check_preset
from cores.Settings                         import Settings
from cores.SignalManager                    import SignalManager

class CheckBox(QCheckBox):

    Type                                    = 'DAMGUI'
    key                                     = 'CheckBox'
    _name                                   = 'DAMG Check Box'
    _copyright                              = __copyright__()

    def __init__(self, txt=None, preset={}, parent=None):
        QCheckBox.__init__(self)

        self.parent                         = parent
        self.settings = Settings(self)
        self.signals = SignalManager(self)

        self.txt                            = txt

        if self.txt is not None:
            self.setText(self.txt)
        self.stateChanged.connect(self.saveState)

        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def saveState(self):
        self.setValue('checkState', self.checkState())

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    def closeEvent(self, event):
        if self.settings._settingEnable:
            geometry = self.saveGeometry()
            self.setValue('geometry', geometry)

        if __name__ == '__main__':
            self.setValue('showLayout', 'hide')
            self.hide()
        else:
            self.setValue('showLayout', 'hide')
            self.signals.emit('showLayout', self.key, 'hide')

    def hideEvent(self, event):
        if self.settings._settingEnable:
            geometry = self.saveGeometry()
            self.setValue('geometry', geometry)

        if __name__ == '__main__':
            self.setValue('showLayout', 'hide')
            self.hide()
        else:
            self.setValue('showLayout', 'hide')
            self.signals.emit('showLayout', self.key, 'hide')

    def showEvent(self, event):

        geometry = self.getValue('geometry', bytes('', 'utf-8'))
        if geometry is not None:
            self.restoreGeometry(geometry)

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
# Created by panda on 27/10/2019 - 6:53 PM
# © 2017 - 2018 DAMGteam. All rights reserved