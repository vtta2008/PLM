# -*- coding: utf-8 -*-
"""

Script Name: Errors.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

from __rc__.element import DError

class AuthorityError(DError):
    pass

class IsADirectoryError(DError):
    pass

class FileNotFoundError(DError):
    pass

class DropException(DError):
    pass

class MetaValueError(DError):
    pass

class FormatSettingError(DError):
    pass

class PathSettingError(DError):
    pass

class KeySettingError(DError):
    pass

class ScopeSettingError(DError):
    pass

class QtNodesError(DError):
    """Base custom exception."""
    pass

class UnregisteredNodeClassError(DError):
    """The Node class is not registered."""
    pass

class UnknownFlowError(DError):
    """The flow style can not be recognized."""
    pass

class KnobConnectionError(DError):
    """Something went wrong while trying to connect two Knobs."""
    pass

class DuplicateKnobNameError(DError):
    """A Node's Knobs must have unique names."""
    pass

class StandardError(DError):
    pass

class SettingError(DError):
    pass


class InvalidSlot(DError):
    """Slot is not longer valid"""
    pass

class NotRregisteredSignal(DError):
    """Signal not registered in factory beforehand"""
    pass

class DockerException(DError):
    pass
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/08/2018 - 9:58 PM
# © 2017 - 2018 DAMGteam. All rights reserved