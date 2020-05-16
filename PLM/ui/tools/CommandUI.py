# -*- coding: utf-8 -*-
"""

Script Name: HiddenLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PLM.api.Widgets                import LineEdit
from PLM.api.Widgets                import ShortCut
from PLM.configs                    import FRAMELESS, KEY_RETURN

class CommandUI(LineEdit):

    key                         = 'CommandUI'

    def __init__(self, parent=None):
        super(CommandUI, self).__init__({}, parent)

        self.parent             = parent
        self.setFixedSize(250, 25)
        self.setWindowFlags(FRAMELESS)
        self.addAction(ShortCut(shortcut='Esc', trigger=self.hide, parent=self))

    def keyReleaseEvent(self, event):
        if event.key() == KEY_RETURN:
            self.run()

    def run(self):
        key                     = self.text()
        self.setText('')
        self.parent.command(key)
        self.close()




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/11/2019 - 5:30 PM
# © 2017 - 2018 DAMGteam. All rights reserved