# -*- coding: utf-8 -*-
"""

Script Name: StatusBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PLM.commons.Widgets import StatusBar

class MainStatusBar(StatusBar):

    key                             = 'MainStatusBar'
    Type                            = 'DAMGSTATUSBAR'
    _name                           = 'Main Status Bar'

    def __init__(self, parent=None):
        super(MainStatusBar, self).__init__(parent)

        self.parent = parent




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:39 PM
# © 2017 - 2018 DAMGteam. All rights reserved
