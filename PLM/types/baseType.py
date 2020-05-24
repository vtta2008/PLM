# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """


class Iterator(object):

    """ Make object Iterable """

    def __init__(self, sorted_dict):

        self._dict                      = sorted_dict
        self._keys                      = sorted(self._dict.keys())
        self._nr_items                  = len(self._keys)
        self._idx                       = 0

    def __iter__(self):
        return self

    def next(self):
        if self._idx >= self._nr_items:
            raise StopIteration

        key                             = self._keys[self._idx]
        value                           = self._dict[key]
        self._idx += 1

        return key, value

    __next__                            = next


class Reserved(object):

    """ Make object Reservable """

    def __init__(self, sorted_dict):

        self._dict                      = sorted_dict
        self._keys                      = sorted(self._dict.keys())
        self._nr_items                  = len(self._keys)
        self._idx                       = 0

    def __iter__(self):
        return self

    def next(self):
        if self._idx >= self._nr_items:
            raise StopIteration

        key                             = self._keys[self._idx]
        value                           = self._dict[key]
        self._idx -= 1

        return key, value

    __next__                            = next


class BaseTuple(tuple):

    Type                                = 'DAMGTUPLE'
    key                                 = 'BaseTuple'
    _name                               = 'DAMG Base Tuple'
    _copyright                          = 'Copyright (C) 2017 - 2020 by DAMGTEAM.'

    def __new__(cls, *args):
        cls.args                        = args
        return tuple.__new__(BaseTuple, tuple(cls.args))

    def __bases__(self):
        return tuple(BaseTuple, tuple(self.args))

    def __call__(self):

        """ Make object callable """

        if isinstance(self, object):
            return True
        else:
            return False

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName




class TypeTuple(BaseTuple):

    key                                 = 'TypeTuple'

    def __init__(self, *args, **kwargs):
        BaseTuple.__new__(self)

        self.kwargs                     = kwargs
        self.args                       = args


class BaseInfo(TypeTuple):

    Type                                = 'DAMGTYPEINFO'
    key                                 = 'TypeInfo'

    def __new__(self, content=tuple()):
        self.content                    = content
        return tuple.__new__(BaseInfo, self.content)

    def __bases__(self):
        if self.content:
            return tuple(BaseInfo, self.content)
        else:
            return tuple(BaseInfo, tuple())



def construct_class(infoObj, infoData, **info):

    obj                                 = infoObj
    doc_info                            = infoData['doc']
    name_info                           = infoData['name']
    module_info                         = infoData['module']
    str_info                            = '.'.join(str(i) for i in obj)
    type_info                           = '{0}: {1}'.format(name_info, str_info)
    infoKey                             = '__{0}__info__'.format(name_info.lower())

    info[infoKey]                       = obj
    info['__doc__']                     = doc_info
    info['__name__']                    = name_info
    info['__module__']                  = module_info
    info['__type__']                    = type_info
    info['__str__']                     = str_info

    return info


def set_property(obj, name, value):
    """
    Set or override the value of a property.
    :param obj: The object that owns the property.
    :param name: The name of the property (a string).
    :param value: The new value for the property.
    This function directly modifies the :attr:`~object.__dict__` of the given
    object and as such it avoids any interaction with object properties. This
    is intentional: :func:`set_property()` is meant to be used by extensions of
    the `property-manager` project and by user defined setter methods.
    """
    obj.__dict__[name] = value


def clear_property(obj, name):
    """
    Clear the assigned or cached value of a property.
    :param obj: The object that owns the property.
    :param name: The name of the property (a string).
    This function directly modifies the :attr:`~object.__dict__` of the given
    object and as such it avoids any interaction with object properties. This
    is intentional: :func:`clear_property()` is meant to be used by extensions
    of the `property-manager` project and by user defined deleter methods.
    """
    obj.__dict__.pop(name, None)


def format_property(obj, name):
    """
    Format an object property's dotted name.
    :param obj: The object that owns the property.
    :param name: The name of the property (a string).
    :returns: The dotted path (a string).
    """
    return "%s.%s" % (obj.__class__.__name__, name)





# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved