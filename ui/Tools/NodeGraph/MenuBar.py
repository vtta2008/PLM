# -*- coding: utf-8 -*-
"""

Script Name: pMenuBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QMenuBar, QMenu

# -------------------------------------------------------------------------------------------------------------

class MenuBar(QMenuBar):

    def __init__(self, parent=None):
        super(MenuBar, self).__init__(parent)

        self.fm = QMenu('File')
        self.fm.addMenu(QMenu('New Scene'))
        self.fm.addMenu(QMenu('New Node'))

        self.addSeparator()

        self.addMenu(self.fm)
        self.addMenu(QMenu('Tools'))
        self.addMenu(QMenu('Nodes'))


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:08 AM
# © 2017 - 2018 DAMGteam. All rights reserved