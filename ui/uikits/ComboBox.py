# -*- coding: utf-8 -*-
"""

Script Name: ComboBox.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

# PyQt5
from PyQt5.QtWidgets                        import QComboBox

# PLM
from appData                                import SETTING_FILEPTH, ST_FORMAT, __copyright__
from cores.SignalManager                    import LayoutSignals
from cores.Settings                         import Settings
from ui.uikits.uiUtils                      import check_preset

class ComboBox(QComboBox):

    Type                                    = 'DAMGUI'
    key                                     = 'ComboBox'
    _name                                   = 'DAMG Combo Box'
    _copyright                              = __copyright__

    def __init__(self, preset={}, parent=None):
        super(ComboBox, self).__init__(parent)

        self.signals                        = LayoutSignals(self)
        self.settings                       = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.parent                         = parent
        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'items':
                for item in value:
                    self.addItem(item)
            elif key == 'editable':
                self.setEditable(value)
            elif key == 'curIndex':
                self.setCurrentIndex(value)
            elif key == 'setObjName':
                self.setObjectName(value)
            else:
                print("PRESETKEYERROR: There is no key in preset: {}".format(key))

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def sizeHint(self):
        size = super(ComboBox, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

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
# Created by panda on 27/10/2019 - 6:55 PM
# © 2017 - 2018 DAMGteam. All rights reserved