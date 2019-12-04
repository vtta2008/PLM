# -*- coding: utf-8 -*-
"""

Script Name: HiddenLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from toolkits.Widgets           import LineEdit, ShortCut
from appData                    import FRAMELESS, KEY_RETURN

class ShortcutCMD(LineEdit):

    key                     = 'ShortcutCMD'

    def __init__(self, parent=None):
        super(ShortcutCMD, self).__init__(parent)

        self.parent         = parent
        self.setFixedSize(250, 25)
        self.setWindowFlags(FRAMELESS)
        self.addAction(ShortCut(shortcut='Esc', trigger=self.hide, parent=self))

    def keyReleaseEvent(self, event):
        if event.key() == KEY_RETURN:
            self.run()

    def eventFilter(self, source, event):
        pass

    def run(self):
        cmd = self.text()
        print('RUN: {0}'.format(cmd))
        self.hide()




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/11/2019 - 5:30 PM
# © 2017 - 2018 DAMGteam. All rights reserved