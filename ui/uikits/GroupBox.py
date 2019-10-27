# -*- coding: utf-8 -*-
"""

Script Name: GroupBox.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python


# PyQt5
from PyQt5.QtCore                   import pyqtSlot
from PyQt5.QtWidgets                import QGroupBox


# PLM
from appData                        import WAIT_LAYOUT_COMPLETE, SETTING_FILEPTH, ST_FORMAT, __copyright__
from ui.uikits.GridLayout           import AutoPreset1, AutoPreset2, AutoPreset3, GridLayout
from ui.uikits.Label                import Label
from ui.uikits.HBoxLayout           import HBoxLayout
from ui.SignalManager               import SignalManager
from cores.Loggers                  import Loggers
from cores.Settings                 import Settings

# -------------------------------------------------------------------------------------------------------------
""" Groupbox presets """

class GroupBox(QGroupBox):

    Type                                    = 'DAMGUI'
    key                                     = 'GroupBox'
    _name                                   = 'DAMG Group Box'
    _copyright                              = __copyright__
    _data                                   = dict()

    def __init__(self, title="Section Title", layouts=None, mode="IconGrid", parent=None):
        QGroupBox.__init__(self)

        self.setTitle(title)
        self.parent = parent

        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.layouts = layouts
        self.mode = mode

        self.buildUI()

    def buildUI(self):
        if self.mode == "IconGrid":
            self.setLayout(AutoPreset1(self.layouts))
        elif self.mode == "BtnGrid":
            self.setLayout(AutoPreset2(self.layouts))
        elif self.mode == "ImageView":
            self.setLayout(AutoPreset3(self.layouts[0]))
        elif self.mode == "setLayout":
            for layout in self.layouts:
                self.setLayout(layout)
        elif self.mode == "qmainLayout":
            self.subLayout = self.layouts
            self.layout = HBoxLayout()
            self.layout.addWidget(self.subLayout)
            self.setLayout(self.layout)
        elif self.mode == "autoGrid":
            self.subLayout = self.layouts
            if self.subLayout is None:
                self.layout = GridLayout()
                self.layout.addWidget(Label({'txt': WAIT_LAYOUT_COMPLETE}), 0, 0, 1, 1)
            else:
                self.layout = self.subLayout
            self.setLayout(self.layout)
        elif self.mode == "groupGrid":
            self.layout = GridLayout()
            self.setLayout(self.layout)
        else:
            print("Unrecognise mode: {}".format(self.mode))


    @pyqtSlot(str)
    def changeTitle(self, title):
        if not title is None or not title:
            self.setTitle(title)

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
        size = super(GroupBox, self).sizeHint()
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

def GroupGrid(txt=None):

    grid = GridLayout()
    # grp = QGroupBox(txt, grid, 'groupGrid')

    grp = QGroupBox(txt)

    grp.setLayout(grid)

    return grp, grid

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:32 AM
# © 2017 - 2018 DAMGteam. All rights reserved