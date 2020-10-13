# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

__name__ = "PLM"
from .base import BaseVersion

import bumpversion

try:
    _cmp = cmp
except NameError:
    def _cmp(a, b):
        """
        Compare two objects.
        Returns a negative number if C{a < b}, zero if they are equal, and a
        positive number if C{a > b}.
        """
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1

class IncomparableVersions(TypeError):
    """
    Two versions could not be compared.
    """


class _inf(object):
    """ An object that is bigger than all other objects """

    def __cmp__(self, other):
        """
        @param other: Another object.
        @type other: any
        @return: 0 if other is inf, 1 otherwise.
        @rtype: C{int}
        """
        if other is _inf:
            return 0
        return 1

_inf = _inf()



class Version(BaseVersion):

    key                                 = 'Version'

    def __init__(self, major, minor, micro):
        super(Version, self).__init__(major, minor, micro)



    @staticmethod
    def fromString(string):
        major, minor, micro             = string.split('.')
        return Version(major, minor, micro)

    def __str__(self):
        return '{0}.{1}.{2}'.format(self.major, self.minor, self.micro)


    def __eq__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c == 0

    def __ne__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c != 0

    def __lt__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c < 0

    def __le__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c <= 0

    def __gt__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c > 0

    def __ge__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c >= 0

    def __repr__(self):

        if self.release_candidate is None:
            release_candidate = ""
        else:
            release_candidate = ", release_candidate=%r" % (self.release_candidate,)

        if self.post is None:
            post = ""
        else:
            post = ", post=%r" % (self.post,)

        if self.dev is None:
            dev = ""
        else:
            dev = ", dev=%r" % (self.dev,)

        return '%s(%r, %r, %d, %d%s%s%s)' % (self.__class__.__name__, self.package, self.major, self.minor, self.micro,
                                            release_candidate, post, dev)


    def __cmp__(self, other):

        if not isinstance(other, self.__class__):
            return NotImplemented
        if self.package.lower() != other.package.lower():
            raise IncomparableVersions("%r != %r" % (self.package, other.package))

        if self.major == "NEXT":
            major = _inf
        else:
            major = self.major

        if self.release_candidate is None:
            release_candidate = _inf
        else:
            release_candidate = self.release_candidate

        if self.post is None:
            post = -1
        else:
            post = self.post

        if self.dev is None:
            dev = _inf
        else:
            dev = self.dev

        if other.major == "NEXT":
            othermajor = _inf
        else:
            othermajor = other.major

        if other.release_candidate is None:
            otherrc = _inf
        else:
            otherrc = other.release_candidate

        if other.post is None:
            otherpost = -1
        else:
            otherpost = other.post

        if other.dev is None:
            otherdev = _inf
        else:
            otherdev = other.dev

        x = _cmp((major, minor, release_candidate, post, dev), )
        return x

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
