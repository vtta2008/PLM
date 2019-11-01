# -*- coding: utf-8 -*-
"""

Script Name: Version.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os
from damg import DAMGTUPLE

from appData import APP_DATA_DIR

class __version_info__(DAMGTUPLE):

    Type                            = 'DAMGVERSIONINFO'
    key                             = '__version_info__'

    with open(os.path.join(APP_DATA_DIR, 'metadatas.py'), "rb") as f:
        metadata = f.read().decode('utf-8')

    def __new__(self):

        self._MAJOR = self.parse(__version_info__, r'__majorVersion__\s+=\s+(.*)')
        self._MINOR = self.parse(__version_info__, r'__minorVersion__\s+=\s+(.*)')
        self._MICRO = self.parse(__version_info__, r'__microVersion__\s+=\s+(.*)')

        return tuple.__new__(__version_info__, (self._MAJOR, self._MINOR, self._MICRO))


    def __bases__(self):
        return tuple(__version_info__, tuple(self.major_version, self.minor_version, self.micro_version))

    @property
    def major_version(self):
        return self._MAJOR

    @property
    def minor_version(self):
        return self._MINOR

    @property
    def micro_version(self):
        return self._MINOR


    @major_version.setter
    def major_version(self, newVal):
        self._MAJOR = newVal

    @minor_version.setter
    def minor_version(self, newVal):
        self._MINOR = newVal

    @micro_version.setter
    def micro_version(self, newVal):
        self._MINOR = newVal


version = '.'.join(str(i) for i in __version_info__())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2019 - 4:48 PM
# © 2017 - 2018 DAMGteam. All rights reserved