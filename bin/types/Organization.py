# -*- coding: utf-8 -*-
"""

Script Name: Organization.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

from bin.types.element import DObj

class Organization(DObj):

    def __init__(self, *args,**kwargs):
        super(Organization, self).__init__(kwargs)

        self._name          = kwargs['organizationName']
        self._id            = kwargs['organizationID']
        self._slogan        = kwargs['slogan']
        self._website       = kwargs['website']

        self._founders      = kwargs['founders']
        self._coFounders    = kwargs['coFounders']

        self._authors       = kwargs['authors']
        self._emails        = kwargs['emails']

    def __emails__(self):
        return self._emails

    def __slogan__(self):
        return self._slogan

    def __website__(self):
        return self._website

    def __founders__(self):
        return self._founders

    def __authors__(self):
        return self._authors

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/08/2018 - 2:47 AM
# © 2017 - 2018 DAMGteam. All rights reserved