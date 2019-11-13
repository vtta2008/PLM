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
from PyQt5.QtCore                           import pyqtSlot
from PyQt5.QtWidgets                        import QGroupBox, QLabel

# PLM

from appData                                import WAIT_LAYOUT_COMPLETE, SETTING_FILEPTH, ST_FORMAT, __copyright__
from ui.SignalManager import SignalManager
from cores.Settings                         import Settings
from ui.uikits.GridLayout                   import AutoPreset1, AutoPreset2, AutoPreset3, GridLayout
from ui.uikits.BoxLayout                    import HBoxLayout


# -------------------------------------------------------------------------------------------------------------
""" Groupbox presets """

class GroupBox(QGroupBox):

    Type                                    = 'DAMGUI'
    key                                     = 'GroupBox'
    _name                                   = 'DAMG Group Box'
    _copyright                              = __copyright__

    def __init__(self, title="Section Title", layouts=None, mode="IconGrid", parent=None):
        QGroupBox.__init__(self)

        self.setTitle(title)
        self.parent = parent

        self.signals = SignalManager(self)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.layouts = layouts
        self.mode = mode

        self.buildUI()

        self.values = dict(w = self.width(), h = self.height(), x = self.x(), y = self.y())

    def sizeHint(self):
        size = super(GroupBox, self).sizeHint()
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
        # print(event, event.type())
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
            # self.subLayout = self.layouts
            self.layout = HBoxLayout({'addWidget': [self.layouts]})
            # self.layout.addWidget(self.subLayout)
            self.setLayout(self.layout)
        elif self.mode == "autoGrid":
            self.subLayout = self.layouts
            if self.subLayout is None:
                self.layout = GridLayout()
                self.layout.addWidget(QLabel(WAIT_LAYOUT_COMPLETE), 0, 0, 1, 1)
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

def GroupGrid(txt=None):

    grid = GridLayout()
    # grp = QGroupBox(txt, grid, 'groupGrid')

    grp = QGroupBox(txt)

    grp.setLayout(grid)

    return grp, grid

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:32 AM
# © 2017 - 2018 DAMGteam. All rights reserved