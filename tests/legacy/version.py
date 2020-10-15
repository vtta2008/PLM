# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import logging
import re
import sre_constants
import string

from PLM.cores.Errors import MissingValueForSerializationException, IncompleteVersionRepresentationException
from PLM.utils import keyvaluestring

from PLM import VERSION_LOG
from bin.loggers import DamgLogger
logger = DamgLogger(__name__, filepth=VERSION_LOG)



class VersionPart:

    """
    This class represents part of a version number. It contains a self.config
    object that rules how the part behaves when increased or reset.
    """

    def __init__(self, value, config=None):
        self._value = value

        if config is None:
            config = NumericVersionPartConfiguration()

        self.config = config

    @property
    def value(self):
        return self._value or self.config.optional_value

    def copy(self):
        return VersionPart(self._value)

    def bump(self):
        return VersionPart(self.config.bump(self.value), self.config)

    def is_optional(self):
        return self.value == self.config.optional_value

    def __format__(self, format_spec):
        return self.value

    def __repr__(self):
        return "<bumpversion.VersionPart:{}:{}>".format(
            self.config.__class__.__name__, self.value
        )

    def __eq__(self, other):
        return self.value == other.value

    def null(self):
        return VersionPart(self.config.first_value, self.config)


class Version:

    def __init__(self, values, original=None):
        self._values = dict(values)
        self.original = original

    def __getitem__(self, key):
        return self._values[key]

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def __repr__(self):
        return "<bumpversion.Version:{}>".format(keyvaluestring(self._values))

    def bump(self, part_name, order):
        bumped = False

        new_values = {}

        for label in order:
            if label not in self._values:
                continue
            if label == part_name:
                new_values[label] = self._values[label].bump()
                bumped = True
            elif bumped:
                new_values[label] = self._values[label].null()
            else:
                new_values[label] = self._values[label].copy()

        new_version = Version(new_values)

        return new_version



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
