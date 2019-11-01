# -*- coding: utf-8 -*-
"""

Script Name: Label.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets                        import QLineEdit
from PyQt5.QtGui                            import QIntValidator

# PLM
from appData                                import SETTING_FILEPTH, ST_FORMAT, __copyright__, PRS
from cores.Settings                         import Settings
from cores.SignalManager                    import SignalManager
from ui.uikits.uiUtils                      import check_preset

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
                print("{0}: Unrecognise configKey: {1}".format(__file__, key))

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

        if __name__ == '__main__':
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
        size = super(LineEdit, self).sizeHint()
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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:40 PM
# © 2017 - 2018 DAMGteam. All rights reserved