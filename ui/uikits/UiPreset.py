# -*- coding: utf-8 -*-
"""

Script Name: button.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os

# PyQt5
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QCheckBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage

# PLM
from appData        import center, left, right, SiPoMin, SiPoPre, SiPoMax, SiPoExp, SiPoIgn, appIconCfg, ST_FORMAT, SETTING_FILEPTH
from ui.SignalManager   import SignalManager
from cores.Loggers  import Loggers
from cores.Settings import Settings
from utils.utils    import get_app_icon, get_logo_icon, get_avatar_icon, data_handler, get_layout_size

PRS = dict( password = QLineEdit.Password,  center = center , left  = left   , right  = right, spmin = SiPoMin,
            spmax    = SiPoMax           ,  sppre  = SiPoPre, spexp = SiPoExp, spign  = SiPoIgn,  )

def check_preset(data):
    if data == {}:
        pass
    else:
        return True

class IconPth(QIcon):

    key = 'IconPth'

    iconInfo = data_handler(filePath=appIconCfg)

    def __init__(self, size=32, name="AboutPlt"):
        super(IconPth, self).__init__()

        self._found = False
        self.iconSize = size
        self.iconName = name

        for icon in self.iconInfo.keys():
            if self.iconName == icon:
                self._found = True

        if self._found:
            # print('Found icon: {}'.format(self.iconName))
            self.iconPth = get_app_icon(self.iconSize, self.iconName)
            self.addFile(self.iconPth, QSize(self.iconSize, self.iconSize))
        else:
            # raise FileNotFoundError("Could not find icon name: {0}".format(self.iconName))
            print("FILENOTFOUNDERROR: {0}: Could not find icon name: {1}".format(__name__, self.iconName))

class AppIcon(QIcon):

    key = 'AppIcon'

    sizes = [16, 24, 32, 48, 64, 96, 128, 256, 512]

    def __init__(self, name="Logo", parent=None):
        super(AppIcon, self).__init__(parent)

        self.parent = parent
        self.name =name

        self.find_icon()

    def find_icon(self):
        for s in self.sizes:
            self.addFile(get_logo_icon(s, self.name), QSize(s, s))
        return True

class Label(QLabel):

    key = "Label"

    def __init__(self, preset={}, parent=None):
        super(Label, self).__init__(parent)

        self.parent         = parent
        self.signals        = SignalManager(self)
        self.logger         = Loggers(self.__class__.__name__)
        self.settings       = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.preset         = preset
        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'txt':
                self.setText(value)
            elif key == 'fnt':
                self.setFont(QFont(value))
            elif key == 'alg':
                self.setAlignment(PRS[value])
            elif key == 'wmin':
                self.setMinimumWidth(value)
            elif key == 'hmin':
                self.setMinimumHeight(value)
            elif key == 'smin':
                self.setMinimumSize(value[0], value[1])
            elif key == 'sizePolicy':
                self.setSizePolicy(PRS[value])
            elif key == 'pxm':
                self.setPixmap(QPixmap.fromImage(QImage(get_avatar_icon(value))))
            elif key == 'scc':
                self.setScaledContents(value)
            elif key == 'sfs':
                self.setFixedSize(value[0], value[1])
            elif key == 'setBuddy':
                self.setBuddy(value)
            elif key == 'link':
                self.setOpenExternalLinks(value)
            else:
                self.setAlignment(center)

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
        size = super(Label, self).sizeHint()
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

class LineEdit(QLineEdit):

    key = "LineEdit"

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

class CheckBox(QCheckBox):

    key = 'CheckBox'

    def __init__(self, preset={}, parent=None):
        super(CheckBox, self).__init__(parent)

        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.parent = parent

        self.preset = preset
        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'txt':
                self.setText(value)

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
        size = super(CheckBox, self).sizeHint()
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

class ComboBox(QComboBox):

    key = "ComboBox"

    def __init__(self, preset={}, parent=None):
        super(ComboBox, self).__init__(parent)

        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.parent = parent
        self.preset = preset
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
        size = super(ComboBox, self).sizeHint()
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

class VBoxLayout(QVBoxLayout):

    key = "VBoxLayout"

    def __init__(self, preset={}, parent=None):
        super(VBoxLayout, self).__init__(parent)

        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.parent = parent
        self.preset = preset

        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'addWidget':
                for widget in value:
                    self.addWidget(widget)
            elif key == 'addLayout':
                for layout in value:
                    self.addLayout(layout)
            elif key == 'addStretch':
                self.setStretch(value, 0)
            else:
                print("Unrecognise configKey: {}".format(key))

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def sizeHint(self):
        size = super(VBoxLayout, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class HBoxLayout(QHBoxLayout):

    key = "HBoxLayout"

    def __init__(self, preset={}, parent=None):
        QHBoxLayout.__init__(self)

        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.parent = parent

        self.preset = preset

        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'addWidget':
                for widget in value:
                    self.addWidget(widget)
            elif key == 'addLayout':
                for layout in value:
                    self.addLayout(layout)
            elif key == 'addStretch':
                self.setStretch(value, 0)
            else:
                print("Unrecognise configKey: {}".format(key))

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def sizeHint(self):
        size = super(HBoxLayout, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 6:05 AM
# © 2017 - 2018 DAMGteam. All rights reserved