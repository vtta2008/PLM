#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""

# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# Plt
from toolkits.Widgets                       import (GroupBox, GridLayout, CheckBox, Label, Widget, VBoxLayout, AppIcon)
from utils                                  import str2bool
from bin                                    import DAMGDICT, DAMGLIST

# -------------------------------------------------------------------------------------------------------------
""" Preferences window """

class HeaderCheckBoxes(GridLayout):

    key                                     = 'HeaderCheckBoxes'
    la                                      = 0
    toolBarCBs                              = DAMGLIST()
    menuCBs                                 = DAMGLIST()
    connectCBs                              = DAMGLIST()
    checkboxes                              = DAMGDICT()
    def __init__(self, parent=None):
        super(HeaderCheckBoxes, self).__init__(parent)

        self.parent                         = parent
        self.buildHeaderCheckBoxes()

        cbs = [self.toolBarCBs, self.menuCBs, self.connectCBs, [self.headerCB]]

        for i in range(len(cbs)):
            if i == 0:
                prefix = 'ToolBar'
            elif i == 1:
                prefix = 'Menu'
            elif i == 2:
                prefix = 'Network'
            else:
                prefix = 'Header'

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
        self.headerCB = CheckBox('Header')
        self.headerCB.stateChanged.connect(self.headerStateChanged)

        mnl = self.la
        csl = mnl + 1
        tbl = csl + 1
        hdl = tbl + 1

        self.addWidget(Label({'txt': 'Menus'}), mnl, 0, 1, 1)
        i = 1
        for i in range(len(self.menuCBs)):
            self.addWidget(self.menuCBs[i], mnl, i-1, 1, 1)
            i += 1

        self.addWidget(Label({'txt': 'Tool Bar: '}), tbl, 0, 1, 1)
        i = 1
        for i in range(len(self.toolBarCBs)):
            self.addWidget(self.toolBarCBs[i], tbl, i-1, 1, 1)

        # self.addWidget(self.allToolBarCB, tbl, 1, 1, 1)
        # self.addWidget(self.tbTDCB, tbl, 2, 1, 1)
        # self.addWidget(self.tbVfxCB, tbl, 3, 1, 1)
        # self.addWidget(self.tbArtCB, tbl, 4, 1, 1)
        # self.addWidget(self.tbTexCB, tbl, 5, 1, 1)
        # self.addWidget(self.tbPostCB, tbl, 6, 1, 1)

        self.addWidget(Label({'txt': 'Connect Status'}), csl, 0, 1, 1)
        self.addWidget(self.allConnectCB, csl, 1, 1, 1)
        self.addWidget(self.serverCB, csl, 2, 1, 1)
        self.addWidget(self.onlineCB, csl, 3, 1, 1)
        self.addWidget(self.modeCB, csl, 4, 1, 1)

        self.addWidget(Label({'txt': 'Header'}), hdl, 0, 1, 1)
        self.addWidget(self.headerCB, hdl, 1, 1, 1)

    def buildServerStatusCheckBoxes(self):
        self.serverCB = CheckBox('Server')
        self.onlineCB = CheckBox('Internet')
        self.modeCB = CheckBox('Mode')
        self.allConnectCB = CheckBox("All: ")
        self.allConnectCB.stateChanged.connect(self.allConnectStateChanged)
        for cb in [self.serverCB, self.onlineCB, self.modeCB, self.allConnectCB]:
            self.connectCBs.append(cb)

    def buildMenuCheckBoxes(self):
        self.mnAppCB = CheckBox('&App')
        self.mnGoCB = CheckBox('&Go to')
        self.mnEditCB = CheckBox('&Edit')
        self.mnViewCB = CheckBox('&View')
        self.mnAppearanceCB = CheckBox('&Appearance')
        self.mnStylesheetCB = CheckBox('&Stylesheet')
        self.mnOfficeCB = CheckBox('&Office')
        self.mnToolsCB = CheckBox('&Tools')
        self.mnDevCB = CheckBox('&Dev')
        self.mnLibCB = CheckBox('&Lib')
        self.mnHelpCB = CheckBox('&Help')
        self.allMenuCB = CheckBox('All: ')
        self.allMenuCB.stateChanged.connect(self.allMenuStateChanged)

        for cb in [ self.allMenuCB, self.mnAppCB, self.mnGoCB, self.mnEditCB, self.mnViewCB, self.mnAppearanceCB,
                    self.mnStylesheetCB, self.mnOfficeCB, self.mnToolsCB, self.mnDevCB, self.mnLibCB, self.mnHelpCB, ]:
            self.menuCBs.append(cb)

    def buildToolBarCheckBoxes(self):
        self.tbTDCB = CheckBox("TD")
        self.tbVfxCB = CheckBox("VFX")
        self.tbArtCB = CheckBox("Art")
        self.tbTexCB = CheckBox("Tex")
        self.tbPostCB = CheckBox('Post')
        self.allToolBarCB = CheckBox("All: ")
        self.allToolBarCB.stateChanged.connect(self.allToolBarStateChanged)

        for cb in [self.allToolBarCB, self.tbTDCB, self.tbVfxCB, self.tbArtCB, self.tbTexCB, self.tbPostCB,]:
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

class FooterCheckBoxes(GridLayout):

    key = 'FooterCheckBoxes'

class BodyCheckBoxes(GridLayout):

    key = 'BodyCheckBoxes'
    notificationCBs = DAMGLIST()
    checkboxes = DAMGDICT()

    def __init__(self, parent=None):
        super(BodyCheckBoxes, self).__init__(parent)
        self.parent = parent
        self.la = 0
        self.buildBodyCheckBoxes()

        cbs = [self.notificationCBs, [self.bodyCB]]

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
        self.bodyCB = CheckBox('Body')
        self.bodyCB.stateChanged.connect(self.bodyStateChanged)

        ntl = self.la
        bdl = ntl + 1

        self.addWidget(Label({'txt': 'Notification'}), ntl, 0, 1, 1)
        self.addWidget(self.allNotifiCB, ntl, 1, 1, 1)
        self.addWidget(self.cpuCB, ntl, 2, 1, 1)
        self.addWidget(self.ramCB, ntl, 3, 1, 1)
        self.addWidget(self.gpuCB, ntl, 4, 1, 1)
        self.addWidget(self.diskCB, ntl, 5, 1, 1)
        self.addWidget(self.timeCB, ntl, 6, 1, 1)
        self.addWidget(self.dateCB, ntl, 7, 1, 1)

        self.addWidget(Label({'txt': 'Body'}), bdl, 0, 1, 1)
        self.addWidget(self.bodyCB, bdl, 1, 1, 1)


        self.la = bdl + 1
        return self.la

    def buildNotificationCheckBoxes(self):
        self.cpuCB = CheckBox('cpu')
        self.ramCB = CheckBox('ram')
        self.gpuCB = CheckBox('gpu')
        self.diskCB = CheckBox('disk')
        self.timeCB = CheckBox('clock')
        self.dateCB = CheckBox('date')
        self.allNotifiCB = CheckBox("All: ")
        self.allNotifiCB.stateChanged.connect(self.allNotifiStateChanged)
        for cb in [self.cpuCB, self.ramCB, self.gpuCB, self.diskCB, self.timeCB, self.dateCB, self.allNotifiCB]:
            self.notificationCBs.append(cb)

    def allNotifiStateChanged(self, bool):
        for cb in self.notificationCBs:
            cb.setChecked(bool)

    def bodyStateChanged(self, bool):
        self.allNotifiStateChanged(bool)

class Preferences(Widget):

    key = 'Preferences'

    _msg_user_not_set = "Not configured yet, will be set with the first message received"

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        # self.resize(200, 100)
        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)
        # self.layout = GeneralSetting(self)
        self.layout = VBoxLayout()
        self.headerGrid = HeaderCheckBoxes(self)
        self.header = GroupBox('Header', parent=self)
        self.header.setLayout(self.headerGrid)

        self.bodyGrid = BodyCheckBoxes(self)
        self.body = GroupBox('Body', parent=self)
        self.body.setLayout(self.bodyGrid)

        self.footerGrid = FooterCheckBoxes(self)
        self.footer = GroupBox('Footer', parent=self)
        self.footer.setLayout(self.footerGrid)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.body)
        self.layout.addWidget(self.footer)

        self.setLayout(self.layout)

    def showEvent(self, event):
        self.resize(574, 252)
        self.resize(575, 252)

