# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

class Base:

    key                         = 'Base'
    Type                        = 'DAMGBASE'
    _name                       = None

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

    def update(self):
        self.__dict__.update()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name              = val



class BaseTuple(tuple):

    Type                                = 'DAMGTUPLE'
    key                                 = 'BaseTuple'
    _name                               = 'DAMG Base Tuple'

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
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                      = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved