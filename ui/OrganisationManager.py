# -*- coding: utf-8 -*-
"""

Script Name: OrganisationManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from functools import partial
from toolkits.Widgets import Widget, AppIcon, GroupGrid, LineEdit, Label, VBoxLayout, HBoxLayout, Button, PlainTextEdit
from cores.Organisation import Organisation

class OrgInfo(GroupGrid):

    key = 'OrgInfo'

    def __init__(self, parent=None):
        super(OrgInfo, self).__init__()

        self.parent = parent
        self.setTitle('Organisation Info')
        self.orgName = LineEdit()
        self.orgID = LineEdit()
        self.orgAddress = LineEdit()
        self.orgWebsite = LineEdit()

        self.layout.addWidget(Label({'txt': 'Organisation Name'}), 0, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Organisation ID'}), 1, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Organisation Adress'}), 2, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Organisation Website'}), 3, 0, 1, 1)
        self.layout.addWidget(self.orgName, 0, 1, 1, 1)
        self.layout.addWidget(self.orgID, 1, 1, 1, 1)
        self.layout.addWidget(self.orgAddress, 2, 1, 1, 1)
        self.layout.addWidget(self.orgWebsite, 3, 1, 1, 1)


class OrgDetails(GroupGrid):

    key = 'OrgDetails'

    def __init__(self, parent=None):
        super(OrgDetails, self).__init__()

        self.parent = parent
        self.setTitle('Details')
        self.orgDetails = PlainTextEdit()
        self.layout.addWidget(self.orgDetails, 0, 0, 3, 2)

class OrganisationManager(Widget):

    key = 'OrganisationManager'

    def __init__(self, parent=None):
        super(OrganisationManager, self).__init__(parent)

        self.parent = parent
        self.setWindowTitle('Organisation Manager')
        self.setWindowIcon(AppIcon(32, 'OrganisationManager'))

        self.layout = VBoxLayout()
        self.layout.addLayout(self.buildLine1())
        self.layout.addLayout(self.buildLine2())
        self.setLayout(self.layout)

    def buildLine1(self):
        self.orgInfo = OrgInfo()
        self.orgDetails = OrgDetails()
        return HBoxLayout({'addWidget': [self.orgInfo, self.orgDetails]})

    def buildLine2(self):
        self.okButton = Button({'txt': 'Ok', 'cl': self.createOrganisation})
        self.editButton = Button({'txt': 'Edit', 'cl': self.editOrganisation})
        self.cancelButton = Button({'txt': 'Cancel', 'cl': partial(self.signals.emit, 'showLayout', self.key, 'hide')})
        return HBoxLayout({'addWidget': [self.okButton, self.editButton, self.cancelButton]})

    def createOrganisation(self):

        name = self.orgInfo.orgName.text()
        id = self.orgInfo.orgID.text()
        address = self.orgInfo.orgAddress.text()
        website = self.orgInfo.orgWebsite.text()
        details = self.orgDetails.orgDetails.toPlainText()
        newOrganisation = Organisation(name, id, address, website, details)

        self.newOrganisationEvent(newOrganisation)
        return newOrganisation

    def resizeEvent(self, event):
        w = int(self.width())
        self.orgInfo.setMaximumWidth(w/3)

    def editOrganisation(self):
        pass

    def newOrganisationEvent(self, org):
        pass

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 1:03 PM
# © 2017 - 2018 DAMGteam. All rights reserved