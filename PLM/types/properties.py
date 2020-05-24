# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from .objectType                    import PropertyType
from .propData                      import glbData



class DamgProperty(PropertyType):


    key                                 = 'DamgProperty'


    def __init__(self, getter=None, setter=None, deleter=None):
        super(DamgProperty, self).__init__(getter, setter, deleter)

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

        print('DamgProperty called')

        if isinstance(self, object):
            return True
        else:
            return False

    def __get__(self, obj, type=None):

        if obj and type is None:
            type                        = obj.__class__

        self.value                      = self.__get.__get__(obj, type)()
        # glbData[self.__name__]          = self.value
        return self.value

    def __set__(self, obj, value):
        if obj is None:
            return self
        self.value                      = self.__set.__get__(obj)(value)
        # glbData[self.__name__]          = self.value
        return self.value

    def __delete__(self, obj):
        del obj

    def setter(self, setter):
        return self.__class__(self.__get, setter)



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved