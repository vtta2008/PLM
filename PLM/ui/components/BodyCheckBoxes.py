# -*- coding: utf-8 -*-
"""

Script Name: BodyCheckBoxes.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PLM.commons.Widgets import GroupGrid, CheckBox, Label
from bin                                    import DAMGLIST, DAMGDICT
from PLM.utils import str2bool

class BodyCheckBoxes(GroupGrid):

    key                                     = 'BodyCheckBoxes'
    notificationCBs                         = DAMGLIST()
    checkboxes                              = DAMGDICT()

    def __init__(self, title, parent=None):
        super(BodyCheckBoxes, self).__init__(title, parent)
        self.parent                         = parent
        self.buildBodyCheckBoxes()

        cbs                                 = [self.notificationCBs, [self.bodyCB]]
        for i in range(len(cbs)):
            if i == 0:
                prefix = 'Notification'
            else:
                prefix = 'Body'

            for cb in cbs[i]:
                cb.key = '{0}_{1}_CheckBox_{2}'.format(self.parent.key, prefix, cb.text())
                cb._name = '{0} {1} Check Box: {2}'.format(self.parent.key, prefix, cb.text())

                cb.settings._settingEnable = True
                state = cb.getValue('checkState')
                if state is None:
                    state = True
                cb.setValue('checkState', state)
                cb.setChecked(str2bool(state))
                self.checkboxes.add(cb.key, cb)

    def buildBodyCheckBoxes(self):
        self.buildNotificationCheckBoxes()
        self.bodyCB                         = CheckBox('Body')
        self.bodyCB.stateChanged.connect(self.bodyStateChanged)

        ntl = 0
        bdl = ntl + 1

        self.layout.addWidget(Label({'txt': 'Notification'}), ntl, 0, 1, 1)
        for i in range(len(self.notificationCBs)):
            self.layout.addWidget(self.notificationCBs[i], ntl, i+1, 1, 1)
            i += 1

        self.layout.addWidget(Label({'txt': 'Body'}), bdl, 0, 1, 1)
        self.layout.addWidget(self.bodyCB, bdl, 1, 1, 1)

    def buildNotificationCheckBoxes(self):
        self.cpuCB                          = CheckBox('cpu')
        self.ramCB                          = CheckBox('ram')
        self.gpuCB                          = CheckBox('gpu')
        self.diskCB                         = CheckBox('disk')
        self.weekCB                         = CheckBox('week')
        self.timeCB                         = CheckBox('clock')
        self.dateCB                         = CheckBox('date')
        self.allNotifiCB                    = CheckBox("All: ")
        self.allNotifiCB.stateChanged.connect(self.allNotifiStateChanged)

        for cb in [self.allNotifiCB, self.cpuCB, self.ramCB, self.gpuCB, self.diskCB, self.weekCB, self.timeCB, self.dateCB]:
            self.notificationCBs.append(cb)

    def allNotifiStateChanged(self, bool):
        for cb in self.notificationCBs:
            cb.setChecked(bool)

    def bodyStateChanged(self, bool):
        self.allNotifiStateChanged(bool)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 7:11 AM
# © 2017 - 2018 DAMGteam. All rights reserved