# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
from pyjavaproperties               import Properties
from humanfriendly.text             import concatenate, pluralize

# PLM

from .objectType                    import PropDataType

cwd                                 = os.path.abspath(os.getcwd())
par                                 = os.path.abspath(os.path.join(cwd, os.pardir))
bindir                              = os.path.join(par, 'bin')
propFile                            = os.path.join(bindir, 'global.properties').replace('\\', '/')
p                                   = Properties()


class PropData(PropDataType):

    _keys                           = []
    _values                         = []
    _data                           = dict()

    def __init__(self, **kwargs):
        """
        Initialize a :class:`PropertyManager` object.
        :param kwargs: Any keyword arguments are passed on to :func:`set_properties()`.
        """
        super(PropData, self).__init__(**kwargs)

        self.set_properties(**kwargs)

        missing_properties          = self.missing_properties

        if missing_properties:
            msg                     = "missing %s" % pluralize(len(missing_properties), "required argument")
            raise TypeError("%s (%s)" % (msg, concatenate(missing_properties)))


    def clearProp(self):
        self._keys                  = []
        self._values                = []
        self.update()

    def getProp(self, name):
        return self.__getitem__(name)

    def update(self):

        if len(self._keys) > 0:
            self._keys              = [k for k in self._keys]
            self._values            = [v for v in self._values]
        else:
            self._keys              = []
            self._values            = []

        return self

    def propNames(self):
        return self.key_values

    def propValues(self):
        return self.key_properties

    def props(self):
        items = []
        if len(self._keys) > 0:
            for i in range(len(self._keys)):
                prop = (self._keys[i], self._values[i])
                items.append(prop)

        return items

    def removeProp(self, name):
        return self.__delitem__(name)

    @property
    def data(self):
        self.update()

        if len(self._keys) > 0:
            for k in self._keys:
                self._data[k] = self._values[self._keys.index(k)]

        return self._data

    def __contains__(self, item):
        return len(self._keys) > 0

    def __delitem__(self, name):

        if self.findProp(name):
            index = self._keys.index(name)
            value = self._values[index]
            self._keys.remove(name)
            self._values.remove(value)

        self.update()


glbData = PropData()

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved