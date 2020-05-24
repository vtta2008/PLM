# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
# Python
import os
from pyjavaproperties                   import Properties
from termcolor                          import cprint
from humanfriendly.text                 import concatenate, pluralize
from PLM.container                      import Iterator, Reserved
from PLM.types.baseType import BaseInfo


cwd                                     = os.path.abspath(os.getcwd())
par                                     = os.path.abspath(os.path.join(cwd, os.pardir))
bindir                                  = os.path.join(par, 'bin')
propFile                                = os.path.join(bindir, 'global.properties').replace('\\', '/')
p                                       = Properties()


if not os.path.exists(propFile) or not os.path.isfile(propFile):
    cprint("WARNING: Could not find property file")
    content                             = None
else:
    content                             = p.load(open(propFile))


propData_info                           = BaseInfo(content)
type_info                               = 'version: {0}'.format('.'.join(str(i) for i in propData_info))
str_info                                = '.'.join(str(i) for i in propData_info)


propData_construct_class                = dict(

    __version_info__                    = propData_info,
    __doc__                             = 'PLM documentations',
    __name__                            = 'version',
    __module__                          = 'PLM',
    __type__                            = type_info,
    __str__                             = str_info

)

class PropDataType(type):

    key                             = 'PropDataType'
    Type                            = 'DAMGPROPDATA'

    def __new__(cls, *args, **kwargs):
        newType = type.__new__(PropDataType, 'PropData', (PropDataType,), propData_construct_class)
        return newType

    def __init__(self):
        self.__new__()
        super(PropDataType, self).__init__(self, PropDataType)

    def __bases__(cls):
        return type.__new__(PropDataType, 'PropData', (PropDataType, ), propData_info)

    def __str__(self):
        return self.__str__

    def __repr__(self):
        return self.__str__

    def __call__(self):
        return isinstance(self, type)



class PropData(PropDataType):


    def __init__(self, **kwargs):
        """
        Initialize a :class:`PropertyManager` object.
        :param kwargs: Any keyword arguments are passed on to :func:`set_properties()`.
        """
        super(PropData, self).__init__(**kwargs)

        self.set_properties(**kwargs)
        missing_properties = self.missing_properties
        if missing_properties:
            msg = "missing %s" % pluralize(len(missing_properties), "required argument")
            raise TypeError("%s (%s)" % (msg, concatenate(missing_properties)))



    def clearProp(self):
        self._keys = []
        self._values = []
        self.update()

    def getProp(self, name):
        return self.__getitem__(name)

    def update(self):

        if len(self._keys) > 0:
            self._keys = [k for k in self._keys]
            self._values = [v for v in self._values]
        else:
            self._keys = []
            self._values = []

        return self

    def props(self):
        items = []
        if len(self._keys) > 0:
            for i in range(len(self._keys)):
                prop = (self._keys[i], self._values[i])
                items.append(prop)

        return items

    def removeProp(self, name):
        return self.__delitem__(name)

    def findProp(self, name):
        return self.__find__(name)



    def __delitem__(self, name):

        if self.findProp(name):
            index = self._keys.index(name)
            value = self._values[index]
            self._keys.remove(name)
            self._values.remove(value)

        self.update()



    def __getitem__(self, name):
        if self.findProp(name):
            return self._values[self._keys.index(name)]
        else:
            return KeyError("{0} does not exists".format(name))







    def __setitem__(self, name, value):

        if not self.findProp(name):
            self._keys.append(name)
            self._values.append(value)
        else:
            index = self._keys.index(name)
            self._values[index] = value

    def __sizeof__(self):
        pass





glbData = PropData()



class DamgProp(object):

    def __init__(self, getter=None, setter=None, deleter=None):

        if getter is not None and not isinstance(getter, classmethod):
            getter = classmethod(getter)

        if setter is not None and not isinstance(setter, classmethod):
            setter = classmethod(setter)

        if deleter is not None and not isinstance(deleter, classmethod):
            deleter = classmethod(deleter)

        self.__get = getter
        self.__set = setter
        self.__del = deleter

        info = getter.__get__(object)  # just need the info attrs.
        self.__doc__ = info.__doc__
        self.__name__ = info.__name__
        self.__module__ = info.__module__

        self.update()

    def __call__(self, *args, **kwargs):

        """ Make object callable """

        print('DamgProp called')

        if isinstance(self, object):
            return True
        else:
            return False

    def __get__(self, obj, type=None):

        if obj and type is None:
            type = obj.__class__

        self.value = self.__get.__get__(obj, type)()
        self.update()
        return self.value

    def __set__(self, obj, value):
        if obj is None:
            return self
        self.value = self.__set.__get__(obj)(value)
        self.update()
        return self.value

    def __delete__(self, obj):
        del obj

    def setter(self, setter):
        return self.__class__(self.__get, setter)

    def update(self):
        glbData[self.__name__] = self.value




# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved