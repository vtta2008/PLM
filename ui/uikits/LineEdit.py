# -*- coding: utf-8 -*-
"""

Script Name: Label.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets            import QLineEdit

from appData                    import SETTING_FILEPTH, ST_FORMAT, __copyright__, PRS

from ui.SignalManager           import SignalManager
from ui.uikits.UiPreset         import check_preset
from cores.Loggers              import Loggers
from cores.Settings             import Settings

class LineEdit(QLineEdit):

    Type                                    = 'DAMGUI'
    key                                     = 'LineEdit'
    _name                                   = 'DAMG Line Edit'
    _copyright                              = __copyright__
    _data                                   = dict()

    def __init__(self, preset={}, parent=None):
        super(LineEdit, self).__init__(parent)

        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.parent = parent
        self.preset = preset

        if check_preset(self.preset):
            self.buildUI()


    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'fn':
                self.setEchoMode(PRS[value])
            elif key == 'txt':
                self.setText(value)
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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:40 PM
# © 2017 - 2018 DAMGteam. All rights reserved