# -*- coding: utf-8 -*-
"""

Script Name: pMenuBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""

from PyQt5.QtWidgets import QMenuBar, QMenu

# -------------------------------------------------------------------------------------------------------------

class pMenuBar(QMenuBar):

    def __init__(self, parent=None):
        super(pMenuBar, self).__init__(parent)

        self.fm = QMenu('File')
        self.fm.addMenu(QMenu('New Scene'))
        self.fm.addMenu(QMenu('New Node'))

        self.addSeparator()

        self.addMenu(self.fm)
        self.addMenu(QMenu('Tools'))
        self.addMenu(QMenu('Nodes'))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 4:17 AM
# © 2017 - 2018 DAMGteam. All rights reserved