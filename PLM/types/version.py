# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from .objectType                        import VersionType, __majorVersion__, __minorVersion__, __microVersion__


class Version(VersionType):

    key                                 = 'Version'

    def __init__(self, major=__majorVersion__, minor=__minorVersion__, micro=__microVersion__):
        super(Version, self).__init__(major, minor, micro)

        assert(isinstance(major, int))
        assert(isinstance(minor, int))
        assert(isinstance(micro, int))

        self._major                     = major
        self._minor                     = minor
        self._micro                     = micro

    @staticmethod
    def fromString(string):
        major, minor, micro             = string.split('.')
        return Version(major, minor, micro)

    def __str__(self):
        return '{0}.{1}.{2}'.format(self.major, self.minor, self.micro)

    def __eq__(self, other):
        return all([self.major == other.major, self.minor == other.minor, self.micro == other.micro])

    def __ge__(self, other):
        lhs                             = int("".join([str(self.major), str(self.minor), str(self.micro)]))
        rhs                             = int("".join([str(other.major), str(other.minor), str(other.micro)]))
        return lhs >= rhs

    def __gt__(self, other):
        lhs                             = int("".join([str(self.major), str(self.minor), str(self.micro)]))
        rhs                             = int("".join([str(other.major), str(other.minor), str(other.micro)]))
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