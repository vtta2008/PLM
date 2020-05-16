# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------


__majorVersion__                        = 13
__minorVersion__                        = 0
__microVersion__                        = 1



class BaseTuple(tuple):

    Type                                = 'DAMGTUPLE'
    key                                 = 'BaseTuple'
    _name                               = 'DAMG Base Tuple'
    _copyright                          = 'Copyright (C) 2017 - 2020 by DAMGTEAM.'

    def __new__(cls, *args):
        cls.args                        = args

        return tuple.__new__(BaseTuple, tuple(cls.args))

    def __bases__(self):
        return tuple(BaseTuple, tuple(self.args))

    def __call__(self):

        """ Make object callable """

        if isinstance(self, object):
            return True
        else:
            return False

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName



class VersionTuple(BaseTuple):

    key                                 = 'VersionTuple'

    def __init__(self, *args, **kwargs):
        BaseTuple.__new__(self)

        self.metadata                   = kwargs
        self.args                       = args



class VersionInfo(VersionTuple):


    Type                            = 'DAMGVERSIONINFO'
    key                             = '__version_info__'


    def __new__(self):

        self._MAJOR                 = __majorVersion__
        self._MINOR                 = __minorVersion__
        self._MICRO                 = __microVersion__

        return tuple.__new__(VersionInfo, (self._MAJOR, self._MINOR, self._MICRO))

    def __bases__(self):
        return tuple(VersionInfo, tuple(self.major_version, self.minor_version, self.micro_version))

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



version_info = VersionInfo()



version_construct_class = dict(

    __version_info__                = version_info,
    __doc__                         = 'PLM documentations',
    __name__                        = 'version',
    __module__                      = 'PLM',
    __type__                        = 'version: {0}'.format('.'.join(str(i) for i in version_info)),
    __str__                         = '.'.join(str(i) for i in version_info)

)


class VersionType(type):

    key                             = 'VersionType'
    Type                            = 'DamgVersion'

    _step                           = 1
    _majo_step                      = 1
    _mino_step                      = 1
    _micro_step                     = 1

    def __new__(cls, *args, **kwargs):
        newType = type.__new__(VersionType, 'version', (VersionType,), version_construct_class)
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
        return type.__new__(VersionType, 'version', (VersionType,), version_construct_class)

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
        self._majo_step             = val

    @mino_step.setter
    def mino_step(self, val):
        self._mino_step             = val

    @micro_step.setter
    def micro_step(self, val):
        self._micro_step            = val

    @step.setter
    def step(self, val):
        self._step                  = val


    __version__                 = '.'.join(str(i) for i in version_info)

    __qualname__                = 'version'


class Version(VersionType):

    key                         = 'version'

    def __init__(self, major=__majorVersion__, minor=__minorVersion__, micro=__minorVersion__):
        super(Version, self).__init__(major, minor, micro)

        assert(isinstance(major, int))
        assert(isinstance(minor, int))
        assert(isinstance(micro, int))

        self._major             = major
        self._minor             = minor
        self._micro             = micro

    @staticmethod
    def fromString(string):
        major, minor, micro     = string.split('.')
        return Version(major, minor, micro)

    def __str__(self):
        return '{0}.{1}.{2}'.format(self.major, self.minor, self.micro)

    def __eq__(self, other):
        return all([self.major == other.major, self.minor == other.minor, self.micro == other.micro])

    def __ge__(self, other):
        lhs = int("".join([str(self.major), str(self.minor), str(self.micro)]))
        rhs = int("".join([str(other.major), str(other.minor), str(other.micro)]))
        return lhs >= rhs

    def __gt__(self, other):
        lhs = int("".join([str(self.major), str(self.minor), str(self.micro)]))
        rhs = int("".join([str(other.major), str(other.minor), str(other.micro)]))
        return lhs >= rhs

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def micro(self):
        return self._micro


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved