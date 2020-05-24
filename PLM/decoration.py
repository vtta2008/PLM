# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, pprint
from pyjavaproperties               import Properties
from termcolor                      import cprint
from humanfriendly.text             import concatenate, pluralize

# PLM
from PLM.container                     import Iterator, Reserved


class PropData(object):

    _keys                           = []
    _values                         = []
    _default                        = dict()

    def __init__(self, **kwargs):
        """
        Initialize a :class:`PropertyManager` object.
        :param kwargs: Any keyword arguments are passed on to :func:`set_properties()`.
        """

        pprint.pprint(self.default)


    @property
    def default(self):
        """
        A set of default property data under dict type. They are settings and values of global settings. All the default
        data is stored in a property file and would be updated in realtime.
        :return: A dict of default global setting, keys are setting name function and values are values had been set to.
        """

        cwd                         = os.path.abspath(os.getcwd())
        par                         = os.path.abspath(os.path.join(cwd, os.pardir))
        bindir                      = os.path.join(par, 'bin')
        propFile                    = os.path.join(bindir, 'global.properties').replace('\\', '/')
        p                           = Properties()

        if not os.path.exists(propFile) and os.path.isfile(propFile):
            cprint("WARNING: Could not find property file")
            self._default           = {}
        else:
            p.load(open(propFile))
            for k, v in p.items():
                self._default[k] = v

        return self._default

    def set_properties(self, **kwargs):
        """
        Set instance properties from keyword arguments.
        :param kw: Every keyword argument is used to assign a value to the instance property whose name matches the keyword argument.
        :raises: :exc:`~exceptions.TypeError` when a keyword argument doesn't match a :class:`property` on the given object.
        """
        for name, value in kwargs.items():
            if self.have_property(name):
                setattr(self, name, value)
            else:
                msg = "got an unexpected keyword argument %r"
                raise TypeError(msg % name)

    @property
    def key_properties(self):
        """A sorted list of strings with the names of any :attr:`~custom_property.key` properties."""
        return self.find_properties(key=True)

    @property
    def key_values(self):
        """A tuple of tuples with (name, value) pairs for each name in :attr:`key_properties`."""
        return tuple((name, getattr(self, name)) for name in self.key_properties)

    @property
    def missing_properties(self):
        """
        The names of key and/or required properties that are missing. This is a list of strings with the names of key
        and/or required properties that either haven't been set or are set to :data:`None`.
        """
        names = sorted(set(self.required_properties) | set(self.key_properties))
        return [n for n in names if getattr(self, n, None) is None]

    @property
    def repr_properties(self):
        """
        The names of the properties rendered by :func:`__repr__()` (a list of strings). When :attr:`key_properties` is
        nonempty the names of the key properties are returned, otherwise a more complex selection is made (of properties
        defined by subclasses of :class:`PropertyManager` whose :attr:`~custom_property.repr` is :data:`True`).
        """
        return self.key_properties or [name for name in self.find_properties(repr=True) if not hasattr(PropData, name)]

    @property
    def required_properties(self):
        """A sorted list of strings with the names of any :attr:`~custom_property.required` properties."""
        return self.find_properties(required=True)

    def find_properties(self, **options):
        """
        Find an object's properties (of a certain type).
        :param options: Passed on to :func:`have_property()` to enable filtering properties by the operations they support.
        :returns: A sorted list of strings with the names of properties.
        """
        # We don't explicitly sort our results here because the dir() function
        # is documented to sort its results alphabetically.
        return [n for n in dir(self) if self.have_property(n, **options)]

    def have_property(self, name, **options):
        """
        Check if the object has a property (of a certain type).
        :param name: The name of the property (a string).
        :param options: Any keyword arguments give the name of an option
                        (one of :attr:`~custom_property.writable`,
                        :attr:`~custom_property.resettable`,
                        :attr:`~custom_property.cached`,
                        :attr:`~custom_property.required`,
                        :attr:`~custom_property.key`,
                        :attr:`~custom_property.repr`) and an expected value
                        (:data:`True` or :data:`False`). Filtering on more than
                        one option is supported.
        :returns: :data:`True` if the object has a property with the expected
                  options enabled/disabled, :data:`False` otherwise.
        """
        property_type = getattr(self.__class__, name, None)
        if isinstance(property_type, property):
            if options:
                return all(getattr(property_type, n, None) == v or
                           n == 'repr' and v is True and getattr(property_type, n, None) is not False
                           for n, v in options.items())
            else:
                return True
        else:
            return False

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

    def findProp(self, name):
        return self.__find__(name)

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

    def __find__(self, name):
        return name in self._keys

    def __eq__(self, other):
        our_key = self.propNames()
        return (our_key == other.key_values if our_key and isinstance(other, PropData) else NotImplemented)

    # def __getattribute__(self, name):
    #     if hasattr(self, name):
    #         self.__getitem__(name)

    def __getitem__(self, name):
        if self.findProp(name):
           return self._values[self._keys.index(name)]
        else:
            return KeyError("{0} does not exists".format(name))

    def __ge__(self, other):
        our_key = self.key_values
        return (our_key >= other.key_values if our_key and isinstance(other, PropData) else NotImplemented)

    def __gt__(self, other):
        our_key = self.key_values
        return (our_key > other.key_values if our_key and isinstance(other, PropData) else NotImplemented)

    def __iter__(self):
        return Iterator(self)

    def __reversed__(self):
        return Reserved(self)

    def __len__(self):
        return len(self._keys)

    def __le__(self, other):
        our_key = self.key_values
        return (our_key <= other.key_values if our_key and isinstance(other, PropData) else NotImplemented)

    def __lt__(self, other):
        our_key = self.key_values
        return (our_key < other.key_values if our_key and isinstance(other, PropData) else NotImplemented)

    def __ne__(self, other):
        our_key = self.key_values
        return (our_key != other.key_values if our_key and isinstance(other, PropData) else NotImplemented)

    def __repr__(self):
        return self.render_properties(*self.repr_properties)

    def __setitem__(self, name, value):

        if not self.findProp(name):
            self._keys.append(name)
            self._values.append(value)
        else:
            index = self._keys.index(name)
            self._values[index] = value

    def __sizeof__(self):
        pass

    def __hash__(self):
        return hash(PropData) ^ hash(self.key_values)



glbData = PropData()



class DamgProp(object):

    def __init__(self, getter=None, setter=None, deleter=None):

        if getter is not None and not isinstance(getter, classmethod):
            getter                      = classmethod(getter)

        if setter is not None and not isinstance(setter, classmethod):
            setter                      = classmethod(setter)

        if deleter is not None and not isinstance(deleter, classmethod):
            deleter                     = classmethod(deleter)

        self.__get                      = getter
        self.__set                      = setter
        self.__del                      = deleter

        info                            = getter.__get__(object)  # just need the info attrs.
        self.__doc__                    = info.__doc__
        self.__name__                   = info.__name__
        self.__module__                 = info.__module__

    def __call__(self, *args, **kwargs):

        """ Make object callable """

        print('DamgProp called')

        if isinstance(self, object):
            return True
        else:
            return False

    def __get__(self, obj, type=None):

        if obj and type is None:
            type                        = obj.__class__

        self.value                      = self.__get.__get__(obj, type)()
        glbData[self.__name__]          = self.value
        return self.value

    def __set__(self, obj, value):
        if obj is None:
            return self
        self.value                      = self.__set.__get__(obj)(value)
        glbData[self.__name__]          = self.value
        return self.value

    def __delete__(self, obj):
        del obj

    def setter(self, setter):
        return self.__class__(self.__get, setter)





class TestProp(object):

    _x = 1

    def __init__(self):
        object.__init__(self)

    @DamgProp
    def x(self):
        return self._x

    @x.setter
    def x(self, v):
        self._x = v


t = TestProp()

print(t.x)

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved