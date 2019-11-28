# -*- coding: utf-8 -*-
"""

Script Name: Location.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from toolkits.Widgets import GridLayout, GroupBox, LineEdit, Button, Label

class Location(GroupBox):

    key = 'Location'

    def __init__(self, parent=None):
        super(Location, self).__init__(parent=parent)

        self.parent = parent
        self.layout = GridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(Label({'txt': 'Address Line 1'}), 0, 0, 1, 2)
        self.layout.addWidget(Label({'txt': 'Address Line 2'}), 1, 0, 1, 2)
        self.layout.addWidget(Label({'txt': 'Postal'}), 2, 0, 1, 2)
        self.layout.addWidget(Label({'txt': 'City'}), 3, 0, 1, 2)
        self.layout.addWidget(Label({'txt': 'Country'}), 4, 0, 1, 2)

        self.address1Field = LineEdit()
        self.address2Field = LineEdit()
        self.postalField = LineEdit()
        self.cityField = LineEdit()
        self.countryField = LineEdit()

        change_location_btn = Button({'txt': "Update Location", 'cl': self.update_location})

        self.layout.addWidget(self.address1Field, 0, 2, 1, 4)
        self.layout.addWidget(self.address2Field, 1, 2, 1, 4)
        self.layout.addWidget(self.postalField, 2, 2, 1, 4)
        self.layout.addWidget(self.cityField, 3, 2, 1, 4)
        self.layout.addWidget(self.countryField, 4, 2, 1, 4)
        self.layout.addWidget(change_location_btn, 5, 0, 1, 6)

    def update_location(self):
        pass

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 7:52 PM
# © 2017 - 2018 DAMGteam. All rights reserved