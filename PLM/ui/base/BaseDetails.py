# -*- coding: utf-8 -*-
"""

Script Name: TaskDetails.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PLM.api.Widgets import GroupGrid, Label, CheckBox, PlainTextEdit
from PLM.utils import str2bool

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

        self.individualMode.stateChanged.connect(self.individual)
        self.groupMode.stateChanged.connect(self.group)
        self.departmentMode.stateChanged.connect(self.department)

        self.preProductionType      = CheckBox('PreProduction')
        self.productionType         = CheckBox('Production')
        self.postProductionType     = CheckBox('PostProduction')
        self.vfxType                = CheckBox('VFX')
        self.researchType           = CheckBox('Research')

        self.preProductionType.stateChanged.connect(self.preProduction)
        self.productionType.stateChanged.connect(self.production)
        self.postProductionType.stateChanged.connect(self.postProduction)
        self.vfxType.stateChanged.connect(self.vfx)
        self.researchType.stateChanged.connect(self.research)

        self.layout.addWidget(self.individualMode, 0, 1, 1, 1)
        self.layout.addWidget(self.groupMode, 0, 2, 1, 1)
        self.layout.addWidget(self.departmentMode, 0, 3, 1, 1)

        self.layout.addWidget(self.preProductionType, 1, 1, 1, 1)
        self.layout.addWidget(self.productionType, 1, 2, 1, 1)
        self.layout.addWidget(self.postProductionType, 1, 3, 1, 1)
        self.layout.addWidget(self.vfxType, 1, 4, 1, 1)
        self.layout.addWidget(self.researchType, 1, 5, 1, 1)

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

    def preProduction(self, bool):
        if str2bool(bool):
            self.productionType.setChecked(False)
            self.postProductionType.setChecked(False)
            self.vfxType.setChecked(False)
            self.researchType.setChecked(False)

            self._type = 'preProduction'

    def production(self, bool):
        if str2bool(bool):
            self.preProductionType.setChecked(False)
            self.postProductionType.setChecked(False)
            self.vfxType.setChecked(False)
            self.researchType.setChecked(False)

            self._type = 'Production'

    def postProduction(self, bool):
        if str2bool(bool):
            self.preProductionType.setChecked(False)
            self.productionType.setChecked(False)
            self.vfxType.setChecked(False)
            self.researchType.setChecked(False)

            self._type = 'PostProduction'

    def vfx(self, bool):
        if str2bool(bool):
            self.preProductionType.setChecked(False)
            self.productionType.setChecked(False)
            self.postProductionType.setChecked(False)
            self.researchType.setChecked(False)

            self._type = 'vfx'

    def research(self, bool):
        if str2bool(bool):
            self.preProductionType.setChecked(False)
            self.postProductionType.setChecked(False)
            self.vfxType.setChecked(False)
            self.researchType.setChecked(False)

            self._type = 'research'

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