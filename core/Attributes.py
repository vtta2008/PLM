# -*- coding: utf-8 -*-
"""

Script Name: Attributes.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" import """

import json
import weakref

from docker import utils as util


class Attribute(object):

    attribute_type = 'generic'
    REQUIRED = ['name', 'attr_type', 'value', '_edges']

    def __init__(self, name, value, dagnode=None, user=True, **kwargs):

        # private attributes
        self._dag               = weakref.ref(dagnode) if dagnode else None
        self._type              = kwargs.get('attr_type', None)
        self._edges             = []

        self.name               = name
        self.label              = kwargs.get('label', "")
        self.default_value      = kwargs.get('default_value', "")
        self.value              = value

        self.doctstring         = kwargs.get('doctstring', '')
        self.desc               = kwargs.get('desc', '')

        # globals
        self.user               = user
        self.private            = kwargs.get('private', False)  # hidden
        self.hidden             = kwargs.get('hidden', False)
        self.connectable        = kwargs.get('connectable', False)
        self.locked             = kwargs.get('locked', False)
        self.required           = kwargs.get('required', False)

        # connection
        self.connection_type    = kwargs.get('connection_type', 'input')
        self.data_type          = kwargs.get('data_type', None)
        self.max_connections    = kwargs.get('max_connections', 1)  # 0 = infinite

        if self.connectable:
            pass

    def __str__(self):
        return json.dumps({self.name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self.name: self.data}, indent=4)

    def update(self, **kwargs):
        for name, value in kwargs.iteritems():
            if value not in [None, 'null']:
                if name not in ['_edges']:
                    if hasattr(self, name) and value != getattr(self, name):
                        print('# DEBUG: Attribute "%s" updating value: "%s": "%s" - "%s"' % (
                        self.name, name, value, getattr(self, name)))
                    setattr(self, name, value)

    @property
    def data(self):
        data = dict()
        for attr in ['label', 'value', 'desc', '_edges', 'attr_type', 'private',
                     'hidden', 'connectable', 'connection_type', 'locked', 'required', 'user']:
            if hasattr(self, attr):
                value = getattr(self, attr)
                if value or attr in self.REQUIRED:
                    data[attr] = value
        return data

    @property
    def dagnode(self):
        return self._dag()

    @property
    def attr_type(self):
        if self._type is not None:
            return self._type
        return util.attr_type(self.value)

    @attr_type.setter
    def attr_type(self, val):
        self._type = val

    @property
    def is_input(self):
        if not self.connectable:
            return False
        return self.connection_type == 'input'

    @property
    def is_output(self):
        if not self.connectable:
            return False
        return self.connection_type == 'output'

    def rename(self, name):
        old_name = self.name
        self.name = name

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 21/07/2018 - 11:09 PM
# © 2017 - 2018 DAMGteam. All rights reserved