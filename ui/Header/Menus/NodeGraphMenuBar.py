# -*- coding: utf-8 -*-
"""

Script Name: pMenuBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from toolkits.Widgets           import MenuBar, Menu


# -------------------------------------------------------------------------------------------------------------

class NodeGraphMenuBar(MenuBar):

    key                 = 'NodeGraphMenuBar'

    def __init__(self, parent=None):
        super(NodeGraphMenuBar, self).__init__(parent)

        self.fm = Menu('File')
        self.fm.addMenu(Menu('New Scene'))
        self.fm.addMenu(Menu('New Node'))

        self.addSeparator()

        self.addMenu(self.fm)
        self.addMenu(Menu('Tools'))
        self.addMenu(Menu('Nodes'))


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:08 AM
# © 2017 - 2018 DAMGteam. All rights reserved