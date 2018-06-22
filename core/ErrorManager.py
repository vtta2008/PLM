# -*- coding: utf-8 -*-
"""

Script Name: ErrorManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from appData.Loggers import SetLogger
logger = SetLogger()

class ErrorManager(Exception):

    def __init__(self, error=None, parent=None):
        super(ErrorManager, self).__init__(parent)

        self.error = "__" + str(error).split('__main__')[-1].split('.')[-1].split("\'>")[0].upper() + "__"

        # self.errorEvent(self.error)

    def errorEvent(self, error):
        mess = "An error occur during prosess: {0}".format(error)
        logger.debug(mess)

class QtNodesError(ErrorManager):
    """Base custom exception."""
    def __init__(self):
        ErrorManager(error=self.__class__)

class UnregisteredNodeClassError(QtNodesError):
    """The Node class is not registered."""
    def __init__(self):
        ErrorManager(error=self.__class__)

class UnknownFlowError(QtNodesError):
    """The flow style can not be recognized."""
    def __init__(self):
        ErrorManager(error=self.__class__)

class KnobConnectionError(QtNodesError):
    """Something went wrong while trying to connect two Knobs."""
    def __init__(self):
        ErrorManager(error=self.__class__)

class DuplicateKnobNameError(QtNodesError):
    """A Node's Knobs must have unique names."""
    def __init__(self):
        ErrorManager(error=self.__class__)

class StandardError(ErrorManager):
    def __init__(self):
        ErrorManager(error=self.__class__)


class SettingError(ErrorManager):
    def __init__(self):
        ErrorManager(error=self.__class__)


class KeySettingError(ErrorManager):
    def __init__(self):
        ErrorManager(error=self.__class__)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/06/2018 - 6:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved