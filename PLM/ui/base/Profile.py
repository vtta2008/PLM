# -*- coding: utf-8 -*-
"""

Script Name: ProFile.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from bin.Widgets import GroupGrid, LineEdit, Button, Label

class Profile(GroupGrid):

    key = 'ProFile'

    def __init__(self, parent=None):
        super(Profile, self).__init__(parent=parent)

        self.parent = parent

        self.layout.addWidget(Label({'txt': 'First Name'}), 0, 0, 1, 2)
        self.layout.addWidget(Label({'txt': 'Last Name'}), 1, 0, 1, 2)
        self.layout.addWidget(Label({'txt': 'Your Title'}), 2, 0, 1, 2)
        self.layout.addWidget(Label({'txt': 'Email'}), 3, 0, 1, 2)
        self.layout.addWidget(Label({'txt': 'Phone Number'}), 4, 0, 1, 2)

        self.firstnameField = LineEdit()
        self.lastnameField = LineEdit()
        self.titleField = LineEdit()
        self.emailField = LineEdit()
        self.phoneField = LineEdit()

        self.changeBtn = Button({'txt': "Update Profile", 'cl': self.update_profile})

        self.layout.addWidget(self.firstnameField, 0, 2, 1, 4)
        self.layout.addWidget(self.lastnameField, 1, 2, 1, 4)
        self.layout.addWidget(self.titleField, 2, 2, 1, 4)
        self.layout.addWidget(self.emailField, 3, 2, 1, 4)
        self.layout.addWidget(self.phoneField, 4, 2, 1, 4)
        self.layout.addWidget(self.changeBtn, 5, 0, 1, 6)

    def update_profile(self):
        pass

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 7:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved