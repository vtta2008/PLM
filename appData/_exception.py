# -*- coding: utf-8 -*-
"""

Script Name: _exception.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" _exception """

class QtNodesError(Exception):
    """Base custom exception."""


class UnregisteredNodeClassError(QtNodesError):
    """The Node class is not registered."""


class UnknownFlowError(QtNodesError):
    """The flow style can not be recognized."""


class KnobConnectionError(QtNodesError):
    """Something went wrong while trying to connect two Knobs."""


class DuplicateKnobNameError(QtNodesError):
    """A Node's Knobs must have unique names."""

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 17/06/2018 - 6:54 PM
# © 2017 - 2018 DAMGteam. All rights reserved