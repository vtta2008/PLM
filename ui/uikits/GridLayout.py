# -*- coding: utf-8 -*-
"""

Script Name: GridLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python


# PyQt5
from PyQt5.QtWidgets        import QGridLayout

# PLM
from appData                    import SETTING_FILEPTH, ST_FORMAT, SiPoMin
from ui.SignalManager               import SignalManager
from cores.Loggers              import Loggers
from cores.Settings             import Settings

# -------------------------------------------------------------------------------------------------------------
""" Gridlayout presets """

class GridLayout(QGridLayout):

    key = "GridLayout"

    def __init__(self, parent=None):
        QGridLayout.__init__(self)

        self.parent = parent
        self._name = self.__class__.__name__
        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

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
        size = super(GridLayout, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class AutoPreset1(GridLayout):

    def __init__(self, btns=[], parent=None):
        super(AutoPreset1, self).__init__(parent)

        self.parent     = parent
        self.btns       = btns

        self.buildUI()

    def buildUI(self):

        if self.btns is None:
            pass
        elif not len(self.btns) == 0:
            for i in range(len(self.btns)):
                if i == 0:
                    self.addWidget(self.btns[i], 0, 0, 1, 1)
                elif i == 1:
                    self.addWidget(self.btns[i], 0, 1, 1, 1)
                elif i == 2:
                    self.addWidget(self.btns[i], 0, 2, 1, 1)
                elif i == 3:
                    self.addWidget(self.btns[i], 1, 0, 1, 1)
                elif i == 4:
                    self.addWidget(self.btns[i], 1, 1, 1, 1)
                elif i == 5:
                    self.addWidget(self.btns[i], 1, 2, 1, 1)
                elif i == 6:
                    self.addWidget(self.btns[i], 2, 0, 1, 1)
                elif i == 7:
                    self.addWidget(self.btns[i], 2, 1, 1, 1)
                elif i == 8:
                    self.addWidget(self.btns[i], 2, 2, 1, 1)
                i += 1

class AutoPreset2(GridLayout):

    def __init__(self, btns=[], parent=None):
        super(AutoPreset2, self).__init__(parent)

        self.parent     = parent
        self.btns       = btns

        self.buildUI()

    def buildUI(self):
        if not len(self.btns) == 0:
            for i in range(len(self.btns)):
                if i == 0:
                    self.addWidget(self.btns[i], 0, 0, 1, 2)
                elif i == 1:
                    self.addWidget(self.btns[i], 1, 0, 1, 2)
                elif i == 2:
                    self.addWidget(self.btns[i], 2, 0, 1, 2)
                elif i == 3:
                    self.addWidget(self.btns[i], 3, 0, 1, 2)
                elif i == 4:
                    self.addWidget(self.btns[i], 4, 0, 1, 2)
                elif i == 5:
                    self.addWidget(self.btns[i], 5, 0, 1, 2)
                elif i == 6:
                    self.addWidget(self.btns[i], 6, 0, 1, 2)
                elif i == 7:
                    self.addWidget(self.btns[i], 7, 0, 1, 2)
                elif i == 8:
                    self.addWidget(self.btns[i], 8, 0, 1, 2)
                i += 1

class AutoPreset3(GridLayout):

    def __init__(self, imageView, parent=None):
        super(AutoPreset3, self).__init__(parent)

        self.parent     = parent
        self.imageView  = imageView

        self.buildUI()

    def buildUI(self):
        if self.imageView:
            self.addWidget(self.imageView, 0, 0, 1, 1)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:35 AM
# © 2017 - 2018 DAMGteam. All rights reserved