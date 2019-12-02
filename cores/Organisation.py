# -*- coding: utf-8 -*-
"""

Script Name: Organisation.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import json, os
from cores.base import OrgBase
from appData import ORG_DIR

class Organisation(OrgBase):

    def __init__(self, name=None, id=None, address=None, website=None, details={}):
        super(Organisation, self).__init__()

        self._name = name
        self._id = id
        self._address = address
        self._website = website
        self._details = details

        with open(os.path.join(ORG_DIR, '{0}.organisation'.format(self.id)), 'w') as f:
            json.dump(self.taskData, f, indent=4)

    def change_name(self, name):
        self._name = name

    def change_id(self, id):
        self._id = id

    def change_address(self, address):
        self._address = address

    def change_website(self, website):
        self._website = website

    def change_details(self, details):
        self._details = details

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 12:54 PM
# © 2017 - 2018 DAMGteam. All rights reserved