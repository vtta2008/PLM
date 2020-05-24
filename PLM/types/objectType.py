# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from .baseType                          import BaseInfo, construct_class

infoDoc                                 = 'PLM documentations'

# -------------------------------------------------------------------------------------------------------------
""" Type Version """

__majorVersion__                        = 13
__minorVersion__                        = 0
__microVersion__                        = 1

versionContent                          = (__majorVersion__, __minorVersion__, __microVersion__)
versionInfo                             = BaseInfo(versionContent)
versionInfo.key                         = 'VersionInfo'
versionInfo.Type                        = 'DAMGVERSIONINFO'
versionDataInfo                         = {'doc': infoDoc, 'name': 'Version', 'module': 'PLM'}
versionConstruct                        = construct_class(versionInfo, versionDataInfo)


class VersionType(type):

    key                                 = 'VersionType'
    Type                                = 'DAMGVERSION'

    _step                               = 1
    _majo_step                          = 1
    _mino_step                          = 1
    _micro_step                         = 1

    def __new__(cls, *args, **kwargs):
        newType = type.__new__(VersionType, 'Version', (VersionType,), versionConstruct)
        return newType

    def __init__(self):
        self.__new__()
        super(VersionType, self).__init__(self, VersionType)

    def increase_majo_step(self):
        return self._majo_step + self._step

    def increase_mino_step(self):
        return self._mino_step + self._step

    def increase_micro_step(self):
        return self._micro_step + self._step

    def __bases__(cls):
        return type.__new__(VersionType, 'Version', (VersionType,), versionConstruct)

    def __str__(self):
        return self.__str__

    def __repr__(self):
        return self.__str__

    def __call__(self):
        return isinstance(self, type)

    @property
    def step(self):
        return self._step

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
    def majo_step(self, val):
        self._majo_step                     = val

    @mino_step.setter
    def mino_step(self, val):
        self._mino_step                     = val

    @micro_step.setter
    def micro_step(self, val):
        self._micro_step                    = val

    @step.setter
    def step(self, val):
        self._step                          = val


    __version__                             = '.'.join(str(i) for i in versionInfo)

    __qualname__                            = 'Version'



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved