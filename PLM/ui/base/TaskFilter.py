# -*- coding: utf-8 -*-
"""

Script Name: TaskFilter.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


from PLM.commons                                        import DAMGDICT, DAMGLIST
from PLM.commons.Widgets import GroupGrid, CheckBox, Label
from PLM.utils import str2bool


class TaskFilter(GroupGrid):

    key                                         = 'TaskFilter'
    cbs                                         = DAMGLIST()
    checkboxes                                  = DAMGDICT()

    def __init__(self):
        super(TaskFilter, self).__init__()

        self.setTitle('Fillter')

        self.overduedCB                         = CheckBox()
        self.urgentCB                           = CheckBox()
        self.safetyCB                           = CheckBox()
        self.allTabCheckBox                     = CheckBox()
        self.allTabCheckBox.stateChanged.connect(self.allTabCheckBoxStateChanged)

        texts = ['Overdued', 'Urgent', 'Others', 'All']
        cbs = [self.overduedCB, self.urgentCB, self.safetyCB, self.allTabCheckBox]

        for cb in cbs:
            cb.key = 'task_{0}_CheckBox_{1}'.format(self.key, texts[cbs.index(cb)])
            cb._name = cb.key.replace('_', ' ')
            cb.settings._settingEnable = True
            state = cb.getValue('checkState')
            if state is None:
                state = True
            cb.setValue('checkState', state)
            cb.setChecked(str2bool(state))
            self.checkboxes.add(cb.key, cb)
            self.cbs.append(cb)

        odl = 0
        ugl = odl + 1
        stl = ugl + 1
        al = stl + 1

        self.layout.addWidget(Label({'txt': 'Overdued', 'sss': 'color: red'}), odl, 0, 1, 2)
        self.layout.addWidget(self.overduedCB, odl, 2, 1, 1)
        self.layout.addWidget(Label({'txt': 'Urgent', 'sss': 'color: orange'}), ugl, 0, 1, 2)
        self.layout.addWidget(self.urgentCB, ugl, 2, 1, 1)
        self.layout.addWidget(Label({'txt': 'Others', 'sss': 'color: green'}), stl, 0, 1, 2)
        self.layout.addWidget(self.safetyCB, stl, 2, 1, 1)
        self.layout.addWidget(Label({'txt': 'All'}), al, 0, 1, 2)
        self.layout.addWidget(self.allTabCheckBox, al, 2, 1, 1)

    def allTabCheckBoxStateChanged(self, bool):
        self.overduedCB.setChecked(bool)
        self.urgentCB.setChecked(bool)
        self.safetyCB.setChecked(bool)

    def showEvent(self, event):
        self.resize(76, 3)
        self.resize(158, 138)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:52 PM
# © 2017 - 2018 DAMGteam. All rights reserved