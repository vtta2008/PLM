# -*- coding: utf-8 -*-
"""

Script Name: ErrorManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """


from cores.base import DAMGERROR

# -------------------------------------------------------------------------------------------------------------

class PopupMessageLevelError(DAMGERROR):
    """ When an DAMG object already regiested """

class DuplicateKnobNameError(DAMGERROR):
    """ When an DAMG object already regiested """

class DuplicatedObjectError(DAMGERROR):
    """ When an DAMG object already regiested """

class DropException(DAMGERROR):
    """ When an DAMG object already regiested """

class FileNotFoundError(DAMGERROR):
    """ When an DAMG object already regiested """

class FormatSettingError(DAMGERROR):
    """ When an DAMG object already regiested """

class IsADirectoryError(DAMGERROR):
    """ When an DAMG object already regiested """

class KeySettingError(DAMGERROR):
    """ When an DAMG object already regiested """

class KnobConnectionError(DAMGERROR):
    """ When an DAMG object already regiested """

class PathSettingError(DAMGERROR):
    """ When an DAMG object already regiested """

class QtNodesError(DAMGERROR):
    """ When an DAMG object already regiested """

class ScopeSettingError(DAMGERROR):
    """ When an DAMG object already regiested """

class UnregisteredNodeClassError(DAMGERROR):
    """ When an DAMG object already regiested """

class UnknownFlowError(DAMGERROR):
    """ When an DAMG object already regiested """

class StandardError(DAMGERROR):
    """ When an DAMG object already regiested """

class SettingError(DAMGERROR):
    """ When an DAMG object already regiested """

class MetaValueError(DAMGERROR):
    """ When an DAMG object already regiested """

class BuildingUIError(DAMGERROR):
    """ When an DAMG object already regiested """

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/06/2018 - 6:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved