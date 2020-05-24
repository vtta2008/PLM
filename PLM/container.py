# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

class Iterator(object):

    """ Make object Iterable """

    def __init__(self, sorted_dict):

        self._dict                      = sorted_dict
        self._keys                      = sorted(self._dict.keys())
        self._nr_items                  = len(self._keys)
        self._idx                       = 0

    def __iter__(self):
        return self

    def next(self):
        if self._idx >= self._nr_items:
            raise StopIteration

        key                             = self._keys[self._idx]
        value                           = self._dict[key]
        self._idx += 1

        return key, value

    __next__                            = next


class Reserved(object):

    """ Make object Reservable """

    def __init__(self, sorted_dict):

        self._dict                      = sorted_dict
        self._keys                      = sorted(self._dict.keys())
        self._nr_items                  = len(self._keys)
        self._idx                       = 0

    def __iter__(self):
        return self

    def next(self):
        if self._idx >= self._nr_items:
            raise StopIteration

        key                             = self._keys[self._idx]
        value                           = self._dict[key]
        self._idx -= 1

        return key, value

    __next__                            = next



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved