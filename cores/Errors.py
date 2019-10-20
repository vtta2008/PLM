# -*- coding: utf-8 -*-
"""

Script Name: ErrorManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# Python
import os

# Plm
from cores.Loggers import Loggers
logger = Loggers(__file__)


from cores.base import DAMGERROR

# -------------------------------------------------------------------------------------------------------------

class DuplicateKnobNameError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class DuplicatedObjectError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class DropException(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class FileNotFoundError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class FormatSettingError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class IsADirectoryError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class KeySettingError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class KnobConnectionError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class PathSettingError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class QtNodesError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class ScopeSettingError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class UnregisteredNodeClassError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class UnknownFlowError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class StandardError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class SettingError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

class MetaValueError(DAMGERROR):
    """ When an DAMG object already regiested """
    pass

#-------------------------------------------------------------------------------------------------------------
""" Error handle """

def handle_path_error(directory=None):
    if not os.path.exists(directory) or directory is None:
        try:
            raise IsADirectoryError("Path is not exists: {directory}".format(directory=directory))
        except IsADirectoryError as error:
            raise('Caught error: ' + repr(error))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/06/2018 - 6:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved