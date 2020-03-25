# -*- coding: utf-8 -*-
"""

Script Name: GridLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__

""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QGridLayout
from PLM.commons                            import SignalManager, SettingManager

# -------------------------------------------------------------------------------------------------------------
""" Gridlayout presets """

class GridLayout(QGridLayout):

    Type                                    = 'DAMGUI'
    key                                     = 'GridLayout'
    _name                                   = 'DAMG Grid Layout'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QGridLayout.__init__(self)

        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

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