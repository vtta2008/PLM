# -*- coding: utf-8 -*-
"""

Script Name: TaskDetails.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from toolkits.Widgets               import GroupGrid, Label, CheckBox, PlainTextEdit
from utils                          import str2bool

class BaseDetails(GroupGrid):

    key                             = 'BaseDetails'

    _mode                           = None
    _type                           = None

    def __init__(self, parent=None):
        super(BaseDetails, self).__init__()

        self.parent                 = parent
        self.setTitle('Details')

        self.layout.addWidget(Label({'txt': 'Mode: '}), 0, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Type'}), 1, 0, 1, 1)

        self.individualMode         = CheckBox('Individual')
        self.groupMode              = CheckBox('Group')
        self.departmentMode         = CheckBox('Department')

        self.researchType           = CheckBox('Research')
        self.readingType            = CheckBox('Reading')
        self.vfxType                = CheckBox('VFX')

        self.individualMode.stateChanged.connect(self.individual)
        self.groupMode.stateChanged.connect(self.group)
        self.departmentMode.stateChanged.connect(self.department)
        self.researchType.stateChanged.connect(self.research)
        self.readingType.stateChanged.connect(self.reading)
        self.vfxType.stateChanged.connect(self.vfx)

        self.layout.addWidget(self.individualMode, 0, 1, 1, 1)
        self.layout.addWidget(self.groupMode, 0, 2, 1, 1)
        self.layout.addWidget(self.departmentMode, 0, 3, 1, 1)
        self.layout.addWidget(self.researchType, 1, 1, 1, 1)
        self.layout.addWidget(self.readingType, 1, 2, 1, 1)
        self.layout.addWidget(self.vfxType, 1, 3, 1, 1)

        self.taskDetails = PlainTextEdit()
        self.layout.addWidget(self.taskDetails, 2, 0, 6, 6)

    def individual(self, bool):
        if str2bool(bool):
            self.groupMode.setChecked(False)
            self.departmentMode.setChecked(False)
            self._mode = 'individual'

    def group(self, bool):
        if str2bool(bool):
            self.individualMode.setChecked(False)
            self.departmentMode.setChecked(False)
            self._mode = 'group'

    def department(self, bool):
        if str2bool(bool):
            self.individualMode.setChecked(False)
            self.groupMode.setChecked(False)
            self._mode = 'department'

    def research(self, bool):
        if str2bool(bool):
            self.readingType.setChecked(False)
            self.vfxType.setChecked(False)
            self._type = 'research'

    def reading(self, bool):
        if str2bool(bool):
            self.researchType.setChecked(False)
            self.vfxType.setChecked(False)
            self._type = 'reading'

    def vfx(self, bool):
        if str2bool(bool):
            self.researchType.setChecked(False)
            self.readingType.setChecked(False)
            self._type = 'vfx'

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        self._type = val

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val):
        self._mode = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:55 AM
# © 2017 - 2018 DAMGteam. All rights reserved