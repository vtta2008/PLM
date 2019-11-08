# -*- coding: utf-8 -*-
"""

Script Name: Version.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os, re
from bin.data.damg import DAMGTUPLE

from appData import APP_DATA_DIR, __appname__

with open(os.path.join(APP_DATA_DIR, 'metadatas.py'), 'rb') as f:
    metadata = f.read().decode('utf-8')

def parse(pattern):
    return re.search(pattern, metadata).group(1).replace('"', '').strip()

def setup_read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as f:
        return f.read()

appname = parse(r'__appname__\s+=\s+(.*)')

__name__ = appname
__file__ = appname

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


class _version(type):

    key                             = 'DAMGVERSION'
    Type                            = 'DamgVersion'

    _step                           = 1
    _majo_step                      = 1
    _mino_step                      = 1
    _micro_step                     = 1

    def __new__(cls, *args, **kwargs):
        newType = type.__new__(_version, 'version', (_version,), version_construct_class)
        return newType

    def __init__(self):
        self.__new__()
        super(_version, self).__init__(self, _version)

    def increase_majo_step(self):
        return self._majo_step + self._step

    def increase_mino_step(self):
        return self._mino_step + self._step

    def increase_micro_step(self):
        return self._micro_step + self._step

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, newVal):
        self._step = newVal

    @property
    def majo_step(self):
        return self._majo_step

    @property
    def mino_step(self):
        return self._mino_step

    @property
    def micro_step(self):
        return self._micro_step

    @majo_step.setter
    def majo_step(self, newVal):
        self._majo_step = newVal

    @mino_step.setter
    def mino_step(self, newVal):
        self._mino_step = newVal

    @micro_step.setter
    def micro_step(self, newVal):
        self._micro_step = newVal

    def __bases__(cls):
        return type.__new__(_version, 'version', (_version,), version_construct_class)

    def __str__(self):
        return self.__str__

    def __repr__(self):
        return self.__str__

    def __call__(self):
        return isinstance(self, type)

    __version__ = '.'.join(str(i) for i in version_info)

    __qualname__ = 'version'


class version(_version):

    def __init__(self):
        super(version, self).__init__()
        print(self)

    def release_note(self):
        pass

ver = version()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2019 - 4:48 PM
# © 2017 - 2018 DAMGteam. All rights reserved