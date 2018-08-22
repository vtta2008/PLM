# -*- coding: utf-8 -*-
"""

Script Name: Storage.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import os, json
from __rc__.element import DObj, DDict, DMtd


class Paths(DObj):

    _name       = 'Paths'
    _objname    = 'DAMG paths'
    _data       = DDict()

    def __init__(self, parent=None):
        super(Paths, self).__init__()

        self._root      = os.getenv('ROOT')
        self._parent    = parent

        if self._parent is not None:
            self.setID(self._parent.__id__() + '.' + self._name)

        self._data.add_item('root', self.root())
        self._data.add_item('plugins', self.plugins())
        self._data.add_item('resource', self.resource())
        self._data.add_item('imgs', self.imgs())
        self._data.add_item('avatar', self.avatar())
        self._data.add_item('icons', self.icons())
        self._data.add_item('logo', self.icons())
        self._data.add_item('maya', self.maya())
        self._data.add_item('pics', self.pics())
        self._data.add_item('tags', self.tags())
        self._data.add_item('web', self.web())
        self._data.add_item('api', self.api())
        self._data.add_item('docker', self.docker())
        self._data.add_item('container', self.containers())
        self._data.add_item('config', self.config())
        self._data.add_item('core', self.core())
        self._data.add_item('utils', self.core())

    @property
    def data(self):
        return self._data

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def setID(self, id):
        self._id = id

    def root(self):
        return self._root

    def plugins(self):
        return os.path.join(self._root, '__plugins__')

    def resource(self):
        return os.path.join(self._root, '__rc__')

    def imgs(self):
        return os.path.join(self.resource(), 'imgs')

    def avatar(self):
        return os.path.join(self.imgs(), 'avatar')

    def icons(self):
        return os.path.join(self.imgs(), 'icons')

    def logo(self):
        return os.path.join(self.imgs(), 'logo')

    def maya(self):
        return os.path.join(self.imgs(), 'maya')

    def pics(self):
        return os.path.join(self.imgs(), 'pics')

    def tags(self):
        return os.path.join(self.imgs(), 'tags')

    def web(self):
        return os.path.join(self.imgs(), 'web')

    def qss(self):
        return os.path.join(self.resource(), 'qss')

    def api(self):
        return os.path.join(self.root(), 'api')

    def containers(self):
        return os.path.join(self.root(), 'docker_storages')

    def config(self):
        return os.path.join(self.containers(), '.config')

    def log(self):
        return os.path.join(self.containers(), '.logs')

    def core(self):
        return os.path.join(self.root(), 'core')

    def utils(self):
        return os.path.join(self.root(), 'utils')

    def docker(self):
        return os.path.join(self.root(), 'docker')


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/07/2018 - 9:48 PM
# © 2017 - 2018 DAMGteam. All rights reserved