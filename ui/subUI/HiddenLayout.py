# -*- coding: utf-8 -*-
"""

Script Name: HiddenLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from ui.uikits.Widget import Widget
from ui.uikits.LineEdit import PlainTextEdit
from ui.uikits.BoxLayout import VBoxLayout

class HiddenLayout(Widget):

    key = 'HiddenLayout'

    def __init__(self, parent=None):
        super(HiddenLayout, self).__init__(parent)

        self.parent = parent
        self.layout = VBoxLayout()
        self.commandLine = PlainTextEdit()
        self.commandLine.resize(120, 40)
        self.layout.addWidget(self.commandLine)
        self.setLayout(self.layout)




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/11/2019 - 5:30 PM
# © 2017 - 2018 DAMGteam. All rights reserved