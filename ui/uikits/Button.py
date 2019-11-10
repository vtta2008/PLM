# -*- coding: utf-8 -*-
"""

Script Name: Button.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
from functools                              import partial

# PyQt5
from PyQt5.QtWidgets                        import QPushButton, QToolButton

# PLM
from appData                                import SETTING_FILEPTH, ST_FORMAT, __copyright__
from cores.SignalManager                    import SignalManager
from cores.Settings                         import Settings
from ui.uikits.uiUtils                      import check_preset
from ui.uikits.Icon                         import AppIcon, TagIcon

# -------------------------------------------------------------------------------------------------------------
""" Button presets """

class Button(QPushButton):

    Type                                    = 'DAMGUI'
    key                                     = 'Button'
    _name                                   = 'DAMG Button'
    _copyright                              = __copyright__

    def __init__(self, preset={}, parent=None):
        super(Button, self).__init__(parent)

        self.signals        = SignalManager(self)
        self.settings       = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.preset = preset
        if check_preset(self.preset):
            self.procedural()

    def procedural(self):
        for key, value in self.preset.items():
            if key == 'txt':
                self.setText(value)
            elif key == 'tt':
                self.setToolTip(value)
            elif key == 'cl':
                self.clicked.connect(value)
            elif key == 'icon':
                self.setIcon(AppIcon(32, value))
            elif key == 'tag':
                self.setIcon(TagIcon(value))
            elif key == 'icon24':
                self.setIcon(AppIcon(24, value))
            elif key == 'fix':
                self.setFixedSize(value)
            elif key == 'ics':
                self.setIconSize(value)
            elif key == 'stt':
                self.setToolTip(value)
            else:
                print("PresetKeyError at {0}: No such key registed in preset: {1}: {2}".format(__name__, key, value))

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

    def moveEvent(self, event):
        self.setValue('posX', self.x())
        self.setValue('posY', self.y())

    def resizeEvent(self, event):
        self.setValue('width', self.frameGeometry().width())
        self.setValue('height', self.frameGeometry().height())

    def sizeHint(self):
        size = super(Button, self).sizeHint()
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

class ToolButton(QToolButton):

    Type                                    = 'DAMGUI'
    key                                     = 'ToolButton'
    _name                                   = 'DAMG Tool Button'
    _copyright                              = __copyright__

    def __init__(self, text, parent=None):
        QToolButton.__init__(self)

        self.parent = parent

        self.signals = SignalManager(self)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.resize(40, 40)

        self.setText(text)

        # self.setSizePolicy(SiPoExp, SiPoPre)

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
        size = super(ToolButton, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

    def closeEvent(self, event):
        if __name__=='__main__':
            self.close()
        else:
            self.signals.emit('showLayout', 'hide')
            event.ignore()

    def hideEvent(self, event):
        if __name__=='__main__':
            self.hide()
        else:
            self.signals.emit('showLayout', 'hide')
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
# Created by panda on 18/07/2018 - 8:37 AM
# © 2017 - 2018 DAMGteam. All rights reserved