# -*- coding: utf-8 -*-
"""

Script Name: MetaDatas.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, re, json

# PyQt5
from PyQt5.QtCore import QObject, QMetaObject, QMetaClassInfo, QMetaProperty, QMetaMethod, QMetaType

# Plm
from appData import SPECS, REGEX
from core.Loggers import SetLogger

class MetaDatas(QObject):

    def __init__(self, filename=None, parent=None, **kwargs):
        super(MetaDatas, self).__init__(parent)
        self.logger = SetLogger(self)
        self._template = filename
        self._data = {}
        self._preset = None
        self._initialize = False
        self._parent = parent

        if filename:
            self._data = None

    @property
    def data(self):
        return json.dumps(self._data, indent=4)

    def parse(self, filename):
        if self._initialize:
            self.initialize()

        self.logger.debug('Reading metadata file: {0}'.format(filename))
        data = {}
        if filename is not None:
            if os.path.exists(filename):
                parent = data
                attrName = None
                for line in open(filename, 'r'):
                    line = line.rstrip('\n')
                    rline = line.lstrip(' ')
                    rline = line.rstrip()

                    if not rline.startswith("#") and not rline.startswith(';') and rline.strip() != "":
                        if re.match(REGEX.get("section"), rline):
                            sectionObj = re.search(REGEX.get("section_value"), rline)
                            if sectionObj:
                                sectionType = sectionObj.group('attr')
                                sectionValue = sectionObj.group('value')
                                if sectionType == 'group':
                                    if sectionValue not in parent:
                                        parent = data
                                        groupData = {}
                                        parent[sectionValue] = groupData
                                        parent = parent[sectionValue]

                                    if sectionType == 'attr':
                                        attrData = {}
                                        parent[sectionValue] = attrData
                                        attrName = sectionValue

                                    if sectionType in ['input', 'output']:
                                        connData = {}
                                        connData.update(connectable = True)
                                        connData.update(connection_type = sectionType)
                                        parent[sectionValue] = connData
                                        attrName = sectionValue

                        else:
                            propObj = re.search(REGEX.get("properties"), rline)
                            if propObj:
                                pname = propObj.group('name')
                                ptype = propObj.group('type')
                                pvalue = propObj.group('value')

                                value = pvalue
                                if ptype in ['BOOL', 'INPUT', 'OUTPUT']:
                                    if ptype == 'BOOL':
                                        value = True if pvalue == 'true' else False

                                    if ptype in ['INPUT', 'OUTPUT']:
                                        value = pvalue.lower()
                            else:
                                try:
                                    value = eval(pvalue)
                                except:
                                    self.logger.warning("cannot parse default value of {0}.{1}: {2}, {3}".format(attrName, pname, pvalue, filename))
                            properties = {pname: {'type': ptype, 'value': value}}
                            parent[attrName].update(properties)
                    else:
                        if rline:
                            self.logger.debug("skipping: {0}".format(rline))
        return data

    def initialize(self):
        self._template = None
        self._data = {}

    def query(self, key):
        """Read the value of a variable from the package without importing."""
        module_path = os.path.join('appData', '__init__.py')
        with open(module_path) as module:
            for line in module:
                parts = line.strip().split(' ')
                if parts and parts[0] == key:
                    return parts[-1].strip("'")
        assert 0, "'{0}' not found in '{1}'".format(key, module_path)

    def getInfo(self, key):
       return SPECS[key]


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 6:15 AM
# © 2017 - 2018 DAMGteam. All rights reserved