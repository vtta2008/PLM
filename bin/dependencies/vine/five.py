# -*- coding: utf-8 -*-
"""

Script Name: five.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os, sys, errno, io, platform
from six import PY2, PY3

from damgdock.exceptions import SystemConfused

try:
    from collections import Counter
except ImportError:
    from collections import defaultdict

    def Counter():
        """
        Create counter
        """
        return defaultdict(int)

try:
    import ctypes
except ImportError:
    ctypes = None


if PY2 and not PY3:

    buffer_t = buffer
    from UserList import UserList, UserDict
    import __builtin__ as builtins
    from array import array as _array
    from Queue import Queue, Empty, Full, LifoQueue  # noqa
    from itertools import imap as map, izip as zip, izip_longest as zip_longest

    string = unicode  # noqa
    string_t = basestring  # noqa
    text_t = unicode
    long_t = long  # noqa
    range = xrange
    module_name_t = str
    int_types = (int, long)


    def array(typecode, *args, **kwargs):
        """Create array."""
        if isinstance(typecode, unicode):
            typecode = typecode.encode()
        return _array(typecode, *args, **kwargs)

    def bytes_if_py2(s):
        """Convert str to bytes if running under Python 2."""
        if isinstance(s, unicode):
            return s.encode()
        return s

    def items(d):  # noqa
        """Return dict items iterator."""
        return d.iteritems()

    def keys(d):  # noqa
        """Return dict key iterator."""
        return d.iterkeys()

    def values(d):  # noqa
        """Return dict values iterator."""
        return d.itervalues()

    def nextfun(it):  # noqa
        """Return iterator next method."""
        return it.next

    def exec_(code, globs=None, locs=None):  # pragma: no cover
        """Execute code in a namespace."""
        if globs is None:
            frame = sys._getframe(1)
            globs = frame.f_globals
            if locs is None:
                locs = frame.f_locals
            del frame
        elif locs is None:
            locs = globs
        exec("""exec code in globs, locs""")


    exec_("""def reraise(tp, value, tb=None): raise tp, value, tb""")

elif PY3 and not PY2:

    from collections import UserList, UserDict

    class buffer_t(object):
        """Python 3 does not have a buffer type."""

    try:
        from importlib import reload
    except ImportError:
        from imp import reload

    import builtins

    from array import array
    from queue import Queue, Empty, Full, LifoQueue
    from itertools import zip_longest

    map = map
    zip = zip
    string = str
    string_t = str
    long_t = int
    text_t = str
    range = range
    int_types = (int,)
    module_name_t = str


    def bytes_if_py2(s):
        """Convert str to bytes if running under Python 2."""
        return s

    def items(d):
        """Get dict items iterator."""
        return d.items()

    def keys(d):
        """Get dict keys iterator."""
        return d.keys()

    def values(d):
        """Get dict values iterator."""
        return d.values()

    def nextfun(it):
        """Get iterator next method."""
        return it.__next__

    exec_ = getattr(builtins, 'exec')

    def reraise(tp, value, tb=None):
        """Reraise exception."""
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value

elif PY2 and PY3:
    raise SystemConfused('Can not handle this error due to Python version is not compatible')

else:
    raise SystemConfused('Can not handle this error due to Python version is not compatible')

bytes_t = bytes

try:
    from time import monotonic
except ImportError:
    if sys.version_info < (3, 3):
        SYSTEM = platform.system()

        if SYSTEM == 'Darwin' and ctypes is not None:
            from ctypes.util import find_library

            libSystem = ctypes.CDLL(find_library('libSystem.dylib'))
            CoreServices = ctypes.CDLL(find_library('CoreServices'), use_errno=True)
            mach_absolute_time = libSystem.mach_absolute_time
            mach_absolute_time.restype = ctypes.c_uint64
            absolute_to_nanoseconds = CoreServices.AbsoluteToNanoseconds
            absolute_to_nanoseconds.restype = ctypes.c_uint64
            absolute_to_nanoseconds.argtypes = [ctypes.c_uint64]

            def _monotonic():
                return absolute_to_nanoseconds(mach_absolute_time()) * 1e-9

        elif SYSTEM == 'Linux' and ctypes is not None:
            # from stackoverflow: questions/1205722/how-do-i-get-monotonic-time-durations-in-python

            CLOCK_MONOTONIC = 1  # see <linux/time.h>


            class timespec(ctypes.Structure):
                _fields_ = [('tv_sec', ctypes.c_long), ('tv_nsec', ctypes.c_long), ]


            try:
                librt = ctypes.CDLL('librt.so.1', use_errno=True)
            except Exception:
                try:
                    librt = ctypes.CDLL('librt.so.0', use_errno=True)
                except Exception as exc:
                    error = OSError(
                        "Could not detect working librt library: {0}".format(exc))
                    error.errno = errno.ENOENT
                    raise error

            clock_gettime = librt.clock_gettime
            clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec), ]


            def _monotonic():
                t = timespec()
                if clock_gettime(CLOCK_MONOTONIC, ctypes.pointer(t)) != 0:
                    errno_ = ctypes.get_errno()
                    raise OSError(errno_, os.strerror(errno_))
                return t.tv_sec + t.tv_nsec * 1e-9
        else:
            from time import time as _monotonic

def with_metaclass(Type, skip_attrs=None):
    """

    Class decorator to set metaclass.
    Works with both Python 2 and Python 3 and it does not add
    an extra class in the lookup order like ``six.with_metaclass`` does
    (that is -- it copies the original class instead of using inheritance).

    """
    if skip_attrs is None:
        skip_attrs = {'__dict__', '__weakref__'}

    def _clone_with_metaclass(Class):
        attrs = {key: value for key, value in items(vars(Class))
                 if key not in skip_attrs}
        return Type(Class.__name__, Class.__bases__, attrs)

    return _clone_with_metaclass

try:
    from threading import TIMEOUT_MAX as THREAD_TIMEOUT_MAX
except ImportError:
    THREAD_TIMEOUT_MAX = 1e10

if sys.version_info >= (2, 7):

    def format_d(i):
        """Format number."""
        return format(i, ',d')
else:

    def format_d(i):
        """Format number."""
        s = '%d' % i
        groups = []
        while s and s[-1].isdigit():
            groups.append(s[-3:])
            s = s[:-3]
        return s + ','.join(reversed(groups))

StringIO = io.StringIO
_SIO_write = StringIO.write
_SIO_init = StringIO.__init__

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 8/09/2018 - 4:23 PM
# © 2017 - 2018 DAMGteam. All rights reserved