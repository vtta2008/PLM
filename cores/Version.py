# -*- coding: utf-8 -*-
"""

Script Name: Version.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os, re
from damg import DAMGTUPLE

from appData import APP_DATA_DIR, __appname__

with open(os.path.join(APP_DATA_DIR, 'metadatas.py'), 'rb') as f:
    metadata = f.read().decode('utf-8')

def parse(pattern):
    return re.search(pattern, metadata).group(1).replace('"', '').strip()

def setup_read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as f:
        return f.read()

appname = parse(__appname__)

__name__ = __appname__
__file__ = __appname__

class __version_info__(DAMGTUPLE):

    Type                            = 'DAMGVERSIONINFO'
    key                             = '__version_info__'

    metadata = metadata

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



version_info = __version_info__()

version_construct_class = dict(
                                __version_info__ = version_info,
                                __doc__='PLM documentations',
                                __name__='version',
                                __module__='PLM',
                                __type__='version: {0}'.format('.'.join(str(i) for i in version_info)),
                                __str__='.'.join(str(i) for i in version_info)

                                )


class version(type):

    def __new__(cls, *args, **kwargs):
        newType = type.__new__(version, 'version', (version, ), version_construct_class)
        return newType

    def __init__(self):
        type.__new__(version, 'version', (version, ), version_construct_class)
        super(version, self).__init__(self, version)

    def __bases__(cls):
        return type.__new__(version, 'version', (version, ), version_construct_class)

    def __str__(self):
        return self.__str__

    def __repr__(self):
        return self.__str__

    def __call__(self):
        return isinstance(self, type)

    __version__ = '.'.join(str(i) for i in version_info)

    __qualname__ = 'version'

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2019 - 4:48 PM
# © 2017 - 2018 DAMGteam. All rights reserved