# -*- coding: utf-8 -*-
"""

Script Name: HeaderCheckBoxes.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from bin.Widgets import GroupGrid, CheckBox, Label
from bin.damg import DAMGLIST, DAMGDICT
from PLM.utils import str2bool

class HeaderCheckBoxes(GroupGrid):

    key                         = 'HeaderCheckBoxes'
    toolBarCBs                  = DAMGLIST()
    menuCBs                     = DAMGLIST()
    connectCBs                  = DAMGLIST()
    checkboxes                  = DAMGDICT()

    def __init__(self, title, parent=None):
        super(HeaderCheckBoxes, self).__init__(title, parent)

        self.parent = parent
        self.buildHeaderCheckBoxes()

        cbs = [self.toolBarCBs, self.menuCBs, self.connectCBs, [self.headerCB]]

        for i in range(len(cbs)):
            if i == 0:
                prefix          = 'ToolBar'
            elif i == 1:
                prefix          = 'Menu'
            elif i == 2:
                prefix          = 'Network'
            else:
                prefix          = 'Header'

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

    def buildHeaderCheckBoxes(self):
        self.buildToolBarCheckBoxes()
        self.buildMenuCheckBoxes()
        self.buildServerStatusCheckBoxes()
        self.headerCB           = CheckBox('Header')
        self.headerCB.stateChanged.connect(self.headerStateChanged)

        mnl                     = 0
        csl                     = mnl + 1
        tbl                     = csl + 1
        hdl                     = tbl + 1

        self.layout.addWidget(Label({'txt': 'Menus'}), mnl, 0, 1, 1)

        for i in range(len(self.menuCBs)):
            self.layout.addWidget(self.menuCBs[i], mnl, i+1, 1, 1)
            i += 1

        self.layout.addWidget(Label({'txt': 'Connect Status'}), csl, 0, 1, 1)
        for i in range(len(self.connectCBs)):
            self.layout.addWidget(self.connectCBs[i], csl, i+1, 1, 1)

        self.layout.addWidget(Label({'txt': 'Tool Bar: '}), tbl, 0, 1, 1)
        for i in range(len(self.toolBarCBs)):
            self.layout.addWidget(self.toolBarCBs[i], tbl, i+1, 1, 1)
            i += 1

        self.layout.addWidget(Label({'txt': 'Header'}), hdl, 0, 1, 1)
        self.layout.addWidget(self.headerCB, hdl, 1, 1, 1)

    def buildServerStatusCheckBoxes(self):
        self.serverCB           = CheckBox('Server')
        self.onlineCB           = CheckBox('Internet')
        self.modeCB             = CheckBox('Mode')
        self.allConnectCB       = CheckBox("All: ")
        self.allConnectCB.stateChanged.connect(self.allConnectStateChanged)
        for cb in [self.allConnectCB, self.serverCB, self.onlineCB, self.modeCB]:
            self.connectCBs.append(cb)

    def buildMenuCheckBoxes(self):
        self.mnAppCB            = CheckBox('&App')
        self.mnGoCB             = CheckBox('&Go to')
        self.mnEditCB           = CheckBox('&Edit')
        self.mnViewCB           = CheckBox('&View')
        self.mnOfficeCB         = CheckBox('&Office')
        self.mnToolsCB          = CheckBox('&Tools')
        self.mnPluginCB         = CheckBox('&Plug-ins')
        self.mnLibCB            = CheckBox('&Lib')
        self.mnWinCB            = CheckBox('&Window')
        self.mnHelpCB           = CheckBox('&Help')
        self.allMenuCB          = CheckBox('All: ')
        self.allMenuCB.stateChanged.connect(self.allMenuStateChanged)

        for cb in [self.allMenuCB, self.mnAppCB, self.mnGoCB, self.mnEditCB, self.mnViewCB,
                   self.mnOfficeCB, self.mnToolsCB, self.mnPluginCB, self.mnLibCB, self.mnWinCB, self.mnHelpCB, ]:
            self.menuCBs.append(cb)

    def buildToolBarCheckBoxes(self):

        self.tbTDCB             = CheckBox("TD")
        self.tbVfxCB            = CheckBox("VFX")
        self.tbArtCB            = CheckBox("Art")
        self.tbTexCB            = CheckBox("Tex")
        self.tbPreCB            = CheckBox('Pre')
        self.tbPostCB           = CheckBox('Post')
        self.tbOfficeCB         = CheckBox('Office')
        self.tbDevCB            = CheckBox('Dev')
        self.tbToolCB           = CheckBox('Tool')
        self.tbExtraCB          = CheckBox('Extra')
        self.tbSysTrayCB        = CheckBox('SysTray')
        self.allToolBarCB       = CheckBox("All: ")
        self.allToolBarCB.stateChanged.connect(self.allToolBarStateChanged)

        for cb in [self.allToolBarCB, self.tbTDCB, self.tbVfxCB, self.tbArtCB, self.tbTexCB, self.tbPreCB,
                   self.tbPostCB, self.tbOfficeCB, self.tbDevCB, self.tbToolCB, self.tbExtraCB, self.tbSysTrayCB, ]:

            self.toolBarCBs.append(cb)

    def allToolBarStateChanged(self, bool):
        for cb in self.toolBarCBs:
            cb.setChecked(bool)

    def allMenuStateChanged(self, bool):
        for cb in self.menuCBs:
            cb.setChecked(bool)

    def allConnectStateChanged(self, bool):
        for cb in self.connectCBs:
            cb.setChecked(bool)

    def headerStateChanged(self, bool):
        self.allToolBarCB.setChecked(bool)
        self.allMenuCB.setChecked(bool)
        self.allConnectCB.setChecked(bool)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 7:09 AM
# © 2017 - 2018 DAMGteam. All rights reserved