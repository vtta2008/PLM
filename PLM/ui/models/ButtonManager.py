# -*- coding: utf-8 -*-
"""

Script Name: ButtonManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PLM import BaseKeys

class ButtonManager(BaseKeys):

    key                 = 'ButtonManager'
    _name               = 'ButtonManager'

    def __init__(self, parent=None):
        super(ButtonManager, self).__init__(parent)
        self.parent                 = parent


    def register(self, button):
        if not button.key in self.keys():
            self[button.key] = button
        else:
            self.buttonRegisterError(button.key)
            return self[button.key]

    def buttons(self):
        return self.values()

    def managerButtonGroupBox(self, parent):
        return self.createButtons(self.managerButtons, parent)

    def tagButtonsFooterWidget(self, parent):
        return self.createButtons(self.tagButtons, parent)

    def userButtonGroupBox(self, parent):
        return self.createButtons(self.userButtons, parent)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 10:22 AM
# © 2017 - 2018 DAMGteam. All rights reserved