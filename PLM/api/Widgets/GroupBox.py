# -*- coding: utf-8 -*-
"""

Script Name: GroupBox.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
from PLM.api.Widgets.io_widgets             import QGroupBox
from PLM.configs                            import WAIT_LAYOUT_COMPLETE
from .BoxLayout                             import VBoxLayout, HBoxLayout
from .GridLayout                            import GridLayout, AutoPreset1, AutoPreset2, AutoPreset3
from .Label                                 import Label

# -------------------------------------------------------------------------------------------------------------
""" Groupbox presets """

class GroupBoxBase(QGroupBox):

    Type                                    = 'DAMGGROUPBOX'
    key                                     = 'GroupBoxBase'
    _name                                   = 'DAMG Group Box Base'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QGroupBox.__init__(self)

        self.parent                         = parent

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

class GroupBox(GroupBoxBase):

    key                                     = 'GroupBox'
    _name                                   = 'DAMG Group Box'

    def __init__(self, title="Section Title", layouts=None, mode=None, parent=None):
        super(GroupBox, self).__init__(parent)

        self._title                         = title
        self.parent                         = parent
        self.layouts                        = layouts
        self.mode                           = mode
        self.setTitle(self._title)

        if not self.mode is None:
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
            self.layout = HBoxLayout({'addWidget': [self.layouts]})
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
            self.layout = GridLayout(self)
            self.setLayout(self.layout)
        else:
            print("Unrecognise mode: {}".format(self.mode))

    def changeTitle(self, title):
        if not title is None or not title:
            self.setTitle(title)

class GroupGrid(GroupBoxBase):

    key = 'GroupGrid'

    def __init__(self, title="", parent=None):
        super(GroupGrid, self).__init__(parent)

        self._title = title
        self.setTitle(self._title)
        self.layout = GridLayout(self)
        self.setLayout(self.layout)

class GroupVBox(GroupBoxBase):

    key = 'GroupVBox'

    def __init__(self, parent=None):
        super(GroupVBox, self).__init__(parent)

        self.layout = VBoxLayout(self)
        self.setLayout(self.layout)

class GroupHBox(GroupBoxBase):

    key = 'GroupHBox'

    def __init__(self, parent=None):
        super(GroupHBox, self).__init__(parent)

        self.layout = HBoxLayout(self)
        self.setLayout(self.layout)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:32 AM
# © 2017 - 2018 DAMGteam. All rights reserved