# -*- coding: utf-8 -*-
"""

Script Name: Attributes.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, json

# PyQt5
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication

# Plm
from appData import SPECS, REG_DIR
from utilities.utils import getUnix, get_datetime
from ui.lib.LayoutPreset import Button

# -------------------------------------------------------------------------------------------------------------
""" Attribute class """

class Specs(QObject):

    changeSetting = pyqtSignal(str, str, str)
    imported = pyqtSignal(bool)
    showed = pyqtSignal(bool)
    closed = pyqtSignal(bool)
    regInfo = {}

    def __init__(self, name=None, parent=None):
        super(Specs, self).__init__(parent)

        self._parent = parent
        self._data = SPECS[name]

        self._no       = self._data.get('ordinal')        # Ordinal Number
        self._id       = self._data.get('id')             # Object ID
        self._name     = self._data.get('objName')        # Object name
        self._unix     = self._data.get('unix')           # Unix id
        self._type     = self._data.get('type')           # Object type
        self._lvl      = self._data.get('lvl')            # Object level: represent hierarchy of plm
        self._title    = self._data.get('title')          # Title: if object is a layout, it is window title.
        self._tag      = self._data.get('tag')            # Tag
        self._flag     = self._data.get('flag')           # Flag
        self._cls      = self._data.get('cls')            # Original class
        self._datetime = self._data.get('datetime')       # Date time stamp
        self._import   = False                            # Check if the object is imported or not
        self._show     = False                            # Check if the object is showed or not (for layout object)

        self.regFile = os.path.join(REG_DIR, self.name() + ".r")
        self._register = os.path.exists(self.regFile)

        self.imported.connect(self.set_imported)
        self.showed.connect(self.set_showed)
        self.closed.connect(self.set_close)

        self.initialize()

    def initialize(self):
        self._parent.setObjectName(self.name())
        if self._title is not None:
            self._parent.setWindowTitle(self._title)

        self._parent.__setattr__('ordinal', self.ordinal())
        self._parent.__setattr__('id', self.id())
        self._parent.__setattr__('name', self.name())
        self._parent.__setattr__('unix', self.unix())
        self._parent.__setattr__('type', self.type())
        self._parent.__setattr__('level', self.level())
        self._parent.__setattr__('tag', self.tag())
        self._parent.__setattr__('cls', self.cls())
        self._parent.__setattr__('datetime', self.datetime())

        self.register()
        self.imported.emit(True)

    def register(self):

        self.regInfo['ordinal'] = self.ordinal()
        self.regInfo['name'] = self.name()
        self.regInfo['id'] = self.id()
        self.regInfo['unix'] = self.unix()
        self.regInfo['datetime'] = self.datetime()

        if not self._register:
            with open(self.regFile, 'w') as f:
                json.dump(self.regInfo, f, indent=4)
            self._register = True

        return self._register

    def deRegister(self):
        os.remove(self.regFile)
        self._register = False
        self.regInfo = {}

    def specs(self):
        return self._specs

    def datetime(self):
        if self._datetime is None:
            self._datetime = get_datetime()
        return self._datetime

    def unix(self):
        if not self._register:
            _unix = getUnix()
        else:
            with open(self.regFile, 'r') as f:
                data = json.load(f)
            _unix = data['unix']
        return _unix

    def isImported(self):
        return self._import

    def isShowed(self):
        return self._show

    def name(self):
        return self._name

    def ordinal(self):
        return self._no

    def id(self):
        return self._id

    def type(self):
        return self._type

    def level(self):
        return self._lvl

    def title(self):
        return self._title

    def tag(self):
        if self._tag is None:
            self._tag = 'NO_TAG'
        return self._tag

    def flag(self):
        if self._flag is None:
            self._flag = 'NO_FLAG'
        return self._flag

    def cls(self):
        return self._cls

    @pyqtSlot(bool)
    def set_imported(self, param):
        self._import = param
        # print('{0} has been imported'.format(self._parent.name))

    @pyqtSlot(bool)
    def set_showed(self, param):
        self._show = param
        if param:
            print('{0} has showed'.format(self._parent.name))
        else:
            print('{0} has hided'.format(self._parent.name))

    @pyqtSlot(bool)
    def set_close(self, param):
        if param:
            print('{0} has closed'.format(self._parent.name))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 8/07/2018 - 2:19 PM
# © 2017 - 2018 DAMGteam. All rights reserved