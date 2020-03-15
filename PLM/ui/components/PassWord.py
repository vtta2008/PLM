# -*- coding: utf-8 -*-
"""

Script Name: PassWord.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PLM.commons.Widgets import GroupGrid, LineEdit, Button, Label, MessageBox
from PLM.utils import text_to_hex, check_match
from configs            import PW_BLANK, PW_UNMATCH

class PassWord(GroupGrid):

    key = 'PassWord'

    def __init__(self, parent=None):
        super(PassWord, self).__init__(parent=parent)

        self.parent     = parent

        self.oldPW      = LineEdit({'echo': 'password'})
        self.newPW      = LineEdit({'echo': 'password'})
        self.cfgPW      = LineEdit({'echo': 'password'})
        self.changeBtn  = Button({'txt': 'Change Password', 'cl': self.update_password})

        self.layout.addWidget(Label({'txt': 'Old Password'}), 0, 0, 1, 2)
        self.layout.addWidget(Label({'txt': 'New Password'}), 1, 0, 1, 2)
        self.layout.addWidget(Label({'txt': 'Confirm Password'}), 2, 0, 1, 2)
        self.layout.addWidget(self.oldPW, 0, 2, 1, 4)
        self.layout.addWidget(self.newPW, 1, 2, 1, 4)
        self.layout.addWidget(self.cfgPW, 2, 2, 1, 4)
        self.layout.addWidget(self.changeBtn, 3, 0, 1, 6)

    def update_password(self):

        old_pass        = text_to_hex(self.oldPW.text())
        new_pass        = text_to_hex(self.newPW.text())
        confirm_pass    = text_to_hex(self.cfgPW.text())

        if len(old_pass) == 0 or len(new_pass) == 0 or len(confirm_pass) == 0:
            MessageBox(self, title='Failed', level='critical', message=PW_BLANK, btn='ok')
            return
        elif new_pass is not confirm_pass:
            MessageBox(self, title='Failed', level='critical', message=PW_UNMATCH, btn='ok')
            return
        else:
            checkPass = check_match(self.username, old_pass)
            if not checkPass:
                MessageBox(self, title='Failed', level='critical', message=PW_UNMATCH, btn='ok')
                return
            else:
                new_pass = text_to_hex(self.newPW.text())
                self.updatePassWordEvent(new_pass)

    def updatePasswordEvent(self, new_pass):
        pass


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 7:41 PM
# © 2017 - 2018 DAMGteam. All rights reserved