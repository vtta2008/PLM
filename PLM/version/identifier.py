# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:

    Public version identifiers
    [Epoch: N!]Release: N(.N)*[Pre-release: {a|b|rc}N][Post-release: .postN][Development release: .devN]

    Local version identifiers
    <public version identifier>[+<local version label>]

    Final releases
    Release: N(.N)*

    Pre-releases
    A version identifier that consists solely of a release segment and a pre-release segment is termed a "pre-release".

    Some projects use an "alpha, beta, release candidate" pre-release cycle to support testing by their users prior to a
    final release.

    If used as part of a project's development cycle, these pre-releases are indicated by including a pre-release
    segment in the version identifier:

    X.YaN   # Alpha release
    X.YbN   # Beta release
    X.YrcN  # Release Candidate
    X.Y     # Final release

"""
# -------------------------------------------------------------------------------------------------------------
import functools



class Max(object):
    __slots__ = []

    def __repr__(self):
        return 'Max()'

    def __eq__(self, other):
        return isinstance(other, self.__class__)


@functools.total_ordering
class Numeric(object):

    __slots__ = ['value']

    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return 'Numeric(%r)' % self.value

    def __eq__(self, other):
        if isinstance(other, Numeric):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Max):
            return True
        elif isinstance(other, Alpha):
            return True
        elif isinstance(other, Numeric):
            return self.value < other.value
        else:
            return NotImplemented


@functools.total_ordering
class Alpha(object):

    __slots__ = ['value']

    def __init__(self, value):
        self.value = value.encode('ascii')

    def __repr__(self):
        return 'Alpha(%r)' % self.value

    def __eq__(self, other):
        if isinstance(other, Alpha):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Max):
            return True
        elif isinstance(other, Numeric):
            return False
        elif isinstance(other, Alpha):
            return self.value < other.value
        else:
            return NotImplemented



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
