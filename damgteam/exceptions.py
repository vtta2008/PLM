# -*- coding: utf-8 -*-
"""

Script Name: exceptions.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from damgteam.base import DAMGERROR
from damgteam.five import python_2_unicode_compatible

try:
    from multiprocessing import ProcessError, BufferTooShort, TimeoutError, AuthenticationError
except ImportError:
    class ProcessError(DAMGERROR):
        pass

    class BufferTooShort(ProcessError):
        pass

    class TimeoutError(ProcessError):
        pass

    class AuthenticationError(ProcessError):
        pass


class TimeLimitExceeded(DAMGERROR):
    """ The time limit has been exceeded and the job has been terminated. """

    def __str__(self):
        return "TimeLimitExceeded%s" % (self.args, )


class SoftTimeLimitExceeded(DAMGERROR):
    """ The soft time limit has been exceeded. This exception is raised to give the task a chance to clean up. """

    def __str__(self):
        return "SoftTimeLimitExceeded%s" % (self.args, )


class WorkerLostError(DAMGERROR):
    """ The worker processing a job has exited prematurely. """


class Terminated(DAMGERROR):
    """ The worker processing a job has been terminated by user request. """


class RestartFreqExceeded(DAMGERROR):
    """ Restarts too fast. """


class CoroStop(DAMGERROR):
    """ Coroutine exit, as opposed to StopIteration which may mean it should be restarted. """
    pass


class OperationalError(DAMGERROR):
    """ Recoverable message transport connection error. """


class QtNodesError(DAMGERROR):
    """ Base custom exception."""


class UnregisteredNodeClassError(DAMGERROR):
    """ The Node class is not registered. """


class UnknownFlowError(DAMGERROR):
    """ The flow style can not be recognized. """


class KnobConnectionError(DAMGERROR):
    """ Something went wrong while trying to connect two Knobs. """


class DuplicateKnobNameError(DAMGERROR):
    """ A Node's Knobs must have unique names. """


class InvalidSlot(DAMGERROR):
    """ Slot is not longer valid """


class NotRregisteredSignal(DAMGERROR):
    """ Signal not registered in factory beforehand """


class SerializationError(DAMGERROR):
    """Failed to serialize/deserialize content."""


class EncodeError(SerializationError):
    """Cannot encode object."""


class DecodeError(SerializationError):
    """Cannot decode object."""


class NotBoundError(DAMGERROR):
    """Trying to call channel dependent method on unbound entity."""


class MessageStateError(DAMGERROR):
    """The message has already been acknowledged."""


class LimitExceeded(DAMGERROR):
    """Limit exceeded."""


class ConnectionLimitExceeded(LimitExceeded):
    """Maximum number of simultaneous connections exceeded."""


class ChannelLimitExceeded(LimitExceeded):
    """Maximum number of simultaneous channels exceeded."""


class VersionMismatch(DAMGERROR):
    """Library dependency version mismatch."""


class SerializerNotInstalled(DAMGERROR):
    """Support for the requested serialization type is not installed."""


class ContentDisallowed(SerializerNotInstalled):
    """Consumer does not allow this content-type."""


class InconsistencyError(ConnectionError):
    """Data or environment has been found to be inconsistent.
    Depending on the cause it may be possible to retry the operation.
    """


@python_2_unicode_compatible
class HttpError(Exception):
    """HTTP Client Error."""

    def __init__(self, code, message=None, response=None):
        self.code = code
        self.message = message
        self.response = response
        super(HttpError, self).__init__(code, message, response)

    def __str__(self):
        return 'HTTP {0.code}: {0.message}'.format(self)


class SystemConfused(DAMGERROR):
    """ Python version is not compatible """


class AuthorityError(DAMGERROR):
    pass


class IsADirectoryError(DAMGERROR):
    pass


class FileNotFoundError(DAMGERROR):
    pass


class DropException(DAMGERROR):
    pass


class MetaValueError(DAMGERROR):
    pass


class FormatSettingError(DAMGERROR):
    pass


class PathSettingError(DAMGERROR):
    pass


class KeySettingError(DAMGERROR):
    pass


class ScopeSettingError(DAMGERROR):
    pass


class StandardError(DAMGERROR):
    pass


class SettingError(DAMGERROR):
    pass


class DockerException(DAMGERROR):
    pass


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 8/09/2018 - 5:11 PM
# © 2017 - 2018 DAMGteam. All rights reserved