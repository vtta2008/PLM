#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Footer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM.ui.framework.Widgets import Widget, Label, GridLayout

# -------------------------------------------------------------------------------------------------------------
""" Footer """

class Footer(Widget):

    key                         = 'Footer'
    _name                       = 'DAMG Footer'

    tags = dict(python          = "https://docs.anaconda.com/anaconda/reference/release-notes/",
                licence         = "https://github.com/vtta2008/damgteam/blob/master/LICENCE",
                version         = "https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst")

    def __init__(self, buttonManager, threadManager, parent=None):
        super(Footer, self).__init__(parent)

        self.parent             = parent
        self.buttonManager      = buttonManager
        self.threadManager      = threadManager

        layout = self.buildUI()
        self.setLayout(layout)

    def buildUI(self):
        layout          = GridLayout()

        for i in range(5):
            layout.addWidget(Label({'txt': " "}), 0, i, 1, 1)
            i += 1

        for button in self.buttonManager.tagButtonsFooterWidget(self.parent):
            layout.addWidget(button, 0, i, 1, 2)
            i = i + 2

        return layout

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/06/2018 - 4:24 AM