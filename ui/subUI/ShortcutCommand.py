# -*- coding: utf-8 -*-
"""

Script Name: HiddenLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore           import Qt

from toolkits.Widgets       import Widget, PlainTextEdit, VBoxLayout

class ShortcutCommand(Widget):

    key = 'ShortcutCommand'

    def __init__(self, parent=None):
        super(ShortcutCommand, self).__init__(parent)

        self.parent         = parent
        self.setWindowTitle('Shortcut Command')

        self.layout         = VBoxLayout()
        self.commandLine    = PlainTextEdit()
        self.layout.addWidget(self.commandLine)
        self.setLayout(self.layout)
        self.commandLine.setFixedSize(250, 25)

    def eventFilter(self, source, event):
        if source == self.commandLine:
            if event.key() == Qt.Key_Return:
                self.run()
                return True

    def run(self):
        print('run')
        pass

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/11/2019 - 5:30 PM
# © 2017 - 2018 DAMGteam. All rights reserved