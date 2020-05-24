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
from pyjavaproperties                   import Properties
from termcolor                          import cprint


# PLM
from PLM.types.baseType import BaseInfo, construct_class, Iterator, Reserved


infoDoc                             = 'PLM documentations'

# -------------------------------------------------------------------------------------------------------------
""" Type Version """

__majorVersion__                    = 13
__minorVersion__                    = 0
__microVersion__                    = 1

versionContent                      = (__majorVersion__, __minorVersion__, __microVersion__)
versionInfo                         = BaseInfo(versionContent)
versionInfo.key                     = 'VersionInfo'
versionInfo.Type                    = 'DAMGVERSIONINFO'
versionDataInfo                     = {'doc': infoDoc, 'name': 'Version', 'module': 'PLM'}
versionConstruct                    = construct_class(versionInfo, versionDataInfo)



class VersionType(type):

    key                             = 'VersionType'
    Type                            = 'DAMGVERSION'

    _step                           = 1
    _majo_step                      = 1
    _mino_step                      = 1
    _micro_step                     = 1

    def __new__(cls, *args, **kwargs):
        newType = type.__new__(VersionType, 'Version', (VersionType,), versionConstruct)
        return newType

    def __init__(self):
        self.__new__()
        super(VersionType, self).__init__(self, VersionType)

    def increase_majo_step(self):
        return self._majo_step + self._step

    def increase_mino_step(self):
        return self._mino_step + self._step

    def increase_micro_step(self):
        return self._micro_step + self._step

    def __bases__(cls):
        return type.__new__(VersionType, 'Version', (VersionType,), versionConstruct)

    def __str__(self):
        return self.__str__

    def __repr__(self):
        return self.__str__

    def __call__(self):
        return isinstance(self, type)

    @property
    def step(self):
        return self._step

    @property
    def majo_step(self):
        return self._majo_step

    @property
    def mino_step(self):
        return self._mino_step

    @property
    def micro_step(self):
        return self._micro_step

    @majo_step.setter
    def majo_step(self, val):
        self._majo_step                 = val

    @mino_step.setter
    def mino_step(self, val):
        self._mino_step                 = val

    @micro_step.setter
    def micro_step(self, val):
        self._micro_step                = val

    @step.setter
    def step(self, val):
        self._step                      = val


    __version__                         = '.'.join(str(i) for i in versionInfo)

    __qualname__                        = 'Version'



# -------------------------------------------------------------------------------------------------------------
""" Type PropertyData """


cwd                                  = os.path.abspath(os.getcwd())
par                                  = os.path.abspath(os.path.join(cwd, os.pardir))
bindir                               = os.path.join(par, 'bin')
propFile                             = os.path.join(bindir, 'global.properties').replace('\\', '/')
p                                    = Properties()

if not os.path.exists(propFile) or not os.path.isfile(propFile):
    cprint("WARNING: Could not find property file")
    propContent                      = None
    propDataContent                  = tuple()
else:
    propContent                      = p.load(open(propFile))
    propDataContent                  = (k for k in propContent.keys())

propDataInfo                         = BaseInfo(propDataContent)
propDataInfo.key                     = 'PropDataInfo'
propDataInfo.Type                    = 'DAMGPROPDATAINFO'
propDataDataInfo                     = {'doc': infoDoc, 'name': 'Version', 'module': 'PLM'}
propDataConstruct                    = construct_class(propDataInfo, propDataDataInfo)



class PropDataType(type):

    key                             = 'PropDataType'
    Type                            = 'DAMGPROPDATA'

    _default                        = dict()
    _missing                        = list()

    def __new__(cls, *args, **kwargs):
        newType = type.__new__(PropDataType, 'PropData', (PropDataType,), propDataConstruct)
        return newType

    def __init__(self):
        self.__new__()
        super(PropDataType, self).__init__(self, PropDataType)



    def __bases__(cls):
        return type.__new__(PropDataType, 'PropData', (PropDataType, ), propDataConstruct)

    def __str__(self):
        return self.__str__

    def __call__(self):
        return isinstance(self, type)

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

    def key_values(self):
        """A tuple of tuples with (name, value) pairs for each name in :attr:`key_properties`."""
        return tuple((name, getattr(self, name)) for name in self.find_properties)

    def key_properties(self):
        """A sorted list of strings with the names of any :attr:`~custom_property.key` properties."""
        return self.find_properties(key=True)

    def find_properties(self, **options):
        """
        Find an object's properties (of a certain type).
        :param options: Passed on to :func:`have_property()` to enable filtering properties by the operations they support.
        :returns: A sorted list of strings with the names of properties.
        """
        # We don't explicitly sort our results here because the dir() function
        # is documented to sort its results alphabetically.
        for k, v in self.default.items():
            if not self.have_property(k):
                self._missing.append(k)

        return [n for n in dir(self) if self.have_property(n, **options)]

    def repr_properties(self):
        """
        The names of the properties rendered by :func:`__repr__()` (a list of strings). When :attr:`key_properties` is
        nonempty the names of the key properties are returned, otherwise a more complex selection is made (of properties
        defined by subclasses of :class:`PropertyManager` whose :attr:`~custom_property.repr` is :data:`True`).
        """
        return self.key_properties or [name for name in self.find_properties(repr=True) if not hasattr(PropDataType, name)]

    def required_properties(self):
        """A sorted list of strings with the names of any :attr:`~custom_property.required` properties."""
        return self.find_properties(required=True)

    def render_properties(self, *names):
        """
        Render a human friendly string representation of an object with computed properties.
        :param names: Each positional argument gives the name of a property to include in the rendered object representation.
        :returns: The rendered object representation (a string). This method generates a user friendly textual representation for
        objects that use computed properties created using the
        :mod:`property_manager` module.
        """
        fields = []
        for name in names:
            value = getattr(self, name, None)
            if value is not None or name in self.key_properties:
                fields.append("{0}={1}".format(name, value))
        return "{0}({0})".format(self.__class__.__name__, ", ".join(fields))

    def missing_properties(self):
        """
        The names of key and/or required properties that are missing. This is a list of strings with the names of key
        and/or required properties that either haven't been set or are set to :data:`None`.
        """
        names = sorted(set(self.required_properties) | set(self.key_properties))
        return [n for n in names if getattr(self, n, None) is None]

    def have_property(self, name, **options):
        """
        Check if the object has a property (of a certain type).
        :param name: The name of the property (a string).
        :param options: Any keyword arguments give the name of an option
                        (one of :attr:`~custom_property.writable`, :attr:`~custom_property.resettable`,
                        :attr:`~custom_property.cached`, :attr:`~custom_property.required`, :attr:`~custom_property.key`,
                        :attr:`~custom_property.repr`) and an expected value (:data:`True` or :data:`False`).
                        Filtering on more than one option is supported.
        :returns: :data:`True` if the object has a property with the expected options enabled/disabled, :data:`False` otherwise.
        """
        if not options:
            return self.findProp(name)
        else:
            property_type = getattr(self.__class__, name, None)
            if isinstance(property_type, type(self)):
                return all(getattr(property_type, n, None) == v or
                           n == 'repr' and v is True and getattr(property_type, n, None) is not False
                           for n, v in options.items())
            else:
                return True

    def __contains__(self, item):
        return len(self._keys) > 0

    def __len__(self):
        return len(self._keys)

    def __iter__(self):
        return Iterator(self)

    def __reversed__(self):
        return Reserved(self)

    def __eq__(self, other):
        our_key = self.key_values()
        return (our_key == other.key_values if our_key and isinstance(other, PropDataType) else NotImplemented)

    def __ge__(self, other):
        our_key = self.key_values
        return (our_key >= other.key_values if our_key and isinstance(other, PropDataType) else NotImplemented)

    def __gt__(self, other):
        our_key = self.key_values
        return (our_key > other.key_values if our_key and isinstance(other, PropDataType) else NotImplemented)

    def __le__(self, other):
        our_key = self.key_values
        return (our_key <= other.key_values if our_key and isinstance(other, PropDataType) else NotImplemented)

    def __lt__(self, other):
        our_key = self.key_values
        return (our_key < other.key_values if our_key and isinstance(other, PropDataType) else NotImplemented)

    def __ne__(self, other):
        our_key = self.key_values
        return (our_key != other.key_values if our_key and isinstance(other, PropDataType) else NotImplemented)

    def __repr__(self):
        return self.render_properties(*self.repr_properties)

    def __hash__(self):
        return hash(PropDataType) ^ hash(self.key_values)


    @property
    def default(self):

        """
        A set of default property data under dict type. They are settings and values of global settings. All the default
        data is stored in a property file and would be updated in realtime.
        :return: A dict of default global setting, keys are setting name function and values are values had been set to.
        """

        if propContent:
            for k, v in propContent.items():
                self._default[k]                = v
        else:
            self._default                       = {}

        return self._default

    @property
    def missing(self):
        return self._missing

    @default.setter
    def default(self, val):
        self._default                           = val

    @missing.setter
    def missing(self, val):
        self._missing                           = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved