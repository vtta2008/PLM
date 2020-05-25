# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from humanfriendly.text             import concatenate, pluralize






class DamgPropManager(object):

    _keys                           = []
    _values                         = []
    _data                           = dict()

    def __init__(self, **kwargs):

        super(DamgPropManager, self).__init__(**kwargs)

        self.set_properties(**kwargs)

        missing_properties          = self.missing_properties

        if missing_properties:
            msg                     = "missing {0}".format(pluralize(len(missing_properties)), "required argument")
            raise TypeError("{0} ({1})".format(msg, concatenate(missing_properties)))


    def set_properties(self, **kw):

        for name, value in kw.items():
            if self.have_property(name):
                setattr(self, name, value)
            else:
                raise TypeError("got an unexpected keyword argument {0}".format(name))

    @property
    def key_properties(self):
        return self.find_properties(key=True)

    @property
    def key_values(self):
        return tuple((name, getattr(self, name)) for name in self.key_properties)

    @property
    def missing_properties(self):
        names = sorted(set(self.required_properties) | set(self.key_properties))
        return [n for n in names if getattr(self, n, None) is None]

    @property
    def repr_properties(self):
        return self.key_properties or [name for name in self.find_properties(repr=True) if not hasattr(DamgPropManager, name)]

    @property
    def required_properties(self):
        return self.find_properties(required=True)

    def find_properties(self, **options):
        return [n for n in dir(self) if self.have_property(n, **options)]

    def have_property(self, name, **options):
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

    def clear_cached_properties(self):
        for name in self.find_properties(cached=True, resettable=True):
            delattr(self, name)

    def render_properties(self, *names):
        fields = []
        for name in names:
            value = getattr(self, name, None)
            if value is not None or name in self.key_properties:
                fields.append("{0}={1}".format(name, value))
        return "{0}({1})".format(self.__class__.__name__, ", ".join(fields))

    def __eq__(self, other):
        our_key = self.key_values
        return (our_key == other.key_values if our_key and isinstance(other, DamgPropManager) else NotImplemented)

    def __ne__(self, other):
        our_key = self.key_values
        return (our_key != other.key_values if our_key and isinstance(other, DamgPropManager) else NotImplemented)

    def __lt__(self, other):
        our_key = self.key_values
        return (our_key < other.key_values if our_key and isinstance(other, DamgPropManager) else NotImplemented)

    def __le__(self, other):
        our_key = self.key_values
        return (our_key <= other.key_values if our_key and isinstance(other, DamgPropManager) else NotImplemented)

    def __gt__(self, other):
        our_key = self.key_values
        return (our_key > other.key_values if our_key and isinstance(other, DamgPropManager) else NotImplemented)

    def __ge__(self, other):
        our_key = self.key_values
        return (our_key >= other.key_values if our_key and isinstance(other, DamgPropManager) else NotImplemented)

    def __hash__(self):
        return hash(DamgPropManager) ^ hash(self.key_values)

    def __repr__(self):
        return self.render_properties(*self.repr_properties)


glbData = DamgPropManager()

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved