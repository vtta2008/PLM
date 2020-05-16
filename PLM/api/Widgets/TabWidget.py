# -*- coding: utf-8 -*-
"""

Script Name: TabBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM                                    import __copyright__
from PLM.api.Widgets.io_widgets             import QTabWidget


class TabWidget(QTabWidget):

    Type                                    = 'DAMGUI'
    key                                     = 'TabWidget'
    _name                                   = 'DAMG Tab Widget'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)

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

    def getCurrentTab(self):
        return self.tabLst[self.currentIndex()]

    def getCurrentKey(self):
        return self.getCurrentTab().key


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 4:39 PM
# © 2017 - 2018 DAMGteam. All rights reserved