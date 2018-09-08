# -*- coding: utf-8 -*-
"""

Script Name: exceptions.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from damgdock.base import DAMGError


try:
    from multiprocessing import ProcessError, BufferTooShort, TimeoutError, AuthenticationError
except ImportError:
    class ProcessError(DAMGError):
        pass

    class BufferTooShort(ProcessError):
        pass

    class TimeoutError(ProcessError):
        pass

    class AuthenticationError(ProcessError):
        pass


class TimeLimitExceeded(DAMGError):
    """ The time limit has been exceeded and the job has been terminated. """

    def __str__(self):
        return "TimeLimitExceeded%s" % (self.args, )


class SoftTimeLimitExceeded(DAMGError):
    """ The soft time limit has been exceeded. This exception is raised to give the task a chance to clean up. """

    def __str__(self):
        return "SoftTimeLimitExceeded%s" % (self.args, )


class WorkerLostError(DAMGError):
    """ The worker processing a job has exited prematurely. """


class Terminated(DAMGError):
    """ The worker processing a job has been terminated by user request. """


class RestartFreqExceeded(DAMGError):
    """ Restarts too fast. """


class CoroStop(DAMGError):
    """ Coroutine exit, as opposed to StopIteration which may mean it should be restarted. """
    pass


class OperationalError(DAMGError):
    """ Recoverable message transport connection error. """


class QtNodesError(DAMGError):
    """ Base custom exception."""


class UnregisteredNodeClassError(DAMGError):
    """ The Node class is not registered. """


class UnknownFlowError(DAMGError):
    """ The flow style can not be recognized. """


class KnobConnectionError(DAMGError):
    """ Something went wrong while trying to connect two Knobs. """


class DuplicateKnobNameError(DAMGError):
    """ A Node's Knobs must have unique names. """


class InvalidSlot(DAMGError):
    """ Slot is not longer valid """


class NotRregisteredSignal(DAMGError):
    """ Signal not registered in factory beforehand """


class SystemConfused(DAMGError):
    """ Python version is not compatible """

class AuthorityError(DAMGError):
    pass


class IsADirectoryError(DAMGError):
    pass


class FileNotFoundError(DAMGError):
    pass


class DropException(DAMGError):
    pass


class MetaValueError(DAMGError):
    pass


class FormatSettingError(DAMGError):
    pass


class PathSettingError(DAMGError):
    pass


class KeySettingError(DAMGError):
    pass


class ScopeSettingError(DAMGError):
    pass


class StandardError(DAMGError):
    pass


class SettingError(DAMGError):
    pass


class DockerException(DAMGError):
    pass


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 8/09/2018 - 5:11 PM
# © 2017 - 2018 DAMGteam. All rights reserved