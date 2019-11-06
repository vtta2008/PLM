# -*- coding: utf-8 -*-
"""

Script Name: ButtonManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from __future__ import absolute_import, unicode_literals

import os
from damg import DAMGDICT, DAMGLIST
from functools import partial

from ui.uikits.Button import Button
from utils import data_handler, is_button, is_string
from appData import (mainConfig, SHOWLAYOUT_KEY, START_FILE_KEY, EXECUTING_KEY, OPEN_BROWSER_KEY, CONFIG_DEV, CONFIG_TOOLS,
                     CONFIG_OFFICE, CONFIG_TDS, CONFIG_ART, CONFIG_TEX, CONFIG_POST, CONFIG_VFX, CONFIG_EXTRA,
                     CONFIG_SYSTRAY, RESTORE_KEY, SHOWMIN_KEY, SHOWMAX_KEY)

class ButtonManager(DAMGDICT):

    key             = 'ButtonManager'
    _name           = 'ButtonManager'

    mainInfo         = data_handler(filePath=mainConfig)

    buttonKeys      = DAMGLIST()
    showLayoutKeys  = DAMGLIST()
    showRestoreKeys = DAMGLIST()
    showMaximizeKeys = DAMGLIST()
    showMinimizeKeys = DAMGLIST()
    startFileKeys   = DAMGLIST()
    openBrowserKeys = DAMGLIST()
    executingKeys   = DAMGLIST()

    orgButtons      = ['NewOrganisation', 'EditOrganisation', 'ConfigOrganisation', 'OrganisationManager']

    teamButtons     = ['NewTeam', 'EditTeam', 'ConfigTeam', 'TeamManager']
    prjButtons      = ['NewProject', 'EditProject', 'ConfigProject', 'ProjectManager']
    userButtons     = ['UserSetting', 'SignUp', 'SwitchAccount', 'SignOut']

    checkedKeys = teamButtons + prjButtons + userButtons

    def __init__(self, parent=None):
        super(ButtonManager, self).__init__(self)

        self.parent = parent
        self.showLayoutKeys.appendList(SHOWLAYOUT_KEY)
        self.startFileKeys.appendList(START_FILE_KEY)
        self.executingKeys.appendList(EXECUTING_KEY)
        self.openBrowserKeys.appendList(OPEN_BROWSER_KEY)
        self.showRestoreKeys.appendList(RESTORE_KEY)
        self.showMaximizeKeys.appendList(SHOWMAX_KEY)
        self.showMinimizeKeys.appendList(SHOWMIN_KEY)

        self.buttonKeys = self.showLayoutKeys + self.startFileKeys + self.executingKeys + self.showRestoreKeys + self.showMaximizeKeys + self.showMinimizeKeys

    def buttonConfigError(self, key):
        return print('ButtonKeyConfigError: This key is not registered: {0}'.format(key))

    def buttonRegisterError(self, key):
        return print('ButtonRegisterError: This action is already registered: {0}'.format(key))

    def projectButtonsGroupBox(self, parent):
        return self.createButtons(self.prjButtons, parent)

    def teamButtonsGroupBox(self, parent):
        return self.createButtons(self.teamButtons, parent)

    def userButtonGroupBox(self, parent):
        return self.createButtons(self.userButtons, parent)

    def createButtons(self, keys, parent):
        buttons = []
        for key in keys:
            if key in self.mainInfo.keys():
                if not key in self.checkedKeys:
                    print('key: {0} is in mainInfo: {1}'.format(key, self.mainInfo[key]))
                if is_string(key):
                    button = self.createButton(key, parent)
                    buttons.append(button)
                elif is_button(key):
                    button = key
                    button.setParent(parent)
                    self.register(Button)
                    buttons.append(Button)
                else:
                    print("DataTypeError: Could not add Button: {0}".format(key))
            else:
                print('key: {0} NOT in mainInfo: {1}'.format(key, self.mainInfo[key]))

        return buttons

    def createButton(self, key, parent):
        if key in self.showLayoutKeys:
            return self.showLayoutButton(key, parent)
        elif key in self.startFileKeys:
            return self.showLayoutButton(key, parent)
        elif key in self.executingKeys:
            return self.executingButton(key, parent)
        elif key in self.openBrowserKeys:
            return self.openBrowserButton(key, parent)
        elif key in self.showMinimizeKeys:
            return self.showMinButton(key, parent)
        elif key in self.showMaximizeKeys:
            return self.showMaxButton(key, parent)
        elif key in self.showRestoreKeys:
            return self.showRestoreButton(key, parent)
        else:
            # print('key come here: {}'.format(key))
            return self.buttonConfigError(key)

    def showLayoutButton(self, key, parent):
        if key in self.mainInfo.keys():
            button = Button({'txt': self.mainInfo[key][0],
                             'stt': self.mainInfo[key][2],
                             'cl': partial(parent.signals.emit, 'showLayout',  key, 'show'), })
            button.key = '{0}Button'.format(key)
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button._name = '{0} Button'.format(key)
                button.Type = 'DAMGShowLayoutButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(key)

    def showRestoreButton(self, key, parent):
        if key in self.mainInfo.keys():
            button = Button({'txt': self.mainInfo[key][0],
                             'stt': self.mainInfo[key][2],
                             'cl': partial(parent.signals.emit, 'showLayout',  key, 'showRestore'), })
            button.key = '{0}Button'.format(key)
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button._name = '{0} Button'.format(key)
                button.Type = 'DAMGShowNormalButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(key)

    def showMaxButton(self, key, parent):
        if key in self.mainInfo.keys():
            button = Button({'txt': self.mainInfo[key][0],
                             'stt': self.mainInfo[key][2],
                             'cl': partial(parent.signals.emit, 'showLayout',  key, 'showMax'), })
            button.key = '{0}Button'.format(key)
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button._name = '{0} Button'.format(key)
                button.Type = 'DAMGShowMaximizeButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(key)

    def showMinButton(self, key, parent):
        if key in self.mainInfo.keys():
            button = Button({'txt': self.mainInfo[key][0],
                             'stt': self.mainInfo[key][2],
                             'cl': partial(parent.signals.emit, 'showLayout',  key, 'showMin'), })
            button.key = '{0}Button'.format(key)
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button._name = '{0} Button'.format(key)
                button.Type = 'DAMGShowMinimizeButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(key)

    def startFileButton(self, key, parent):
        if key in self.mainInfo.keys():
            button = Button({'txt': self.mainInfo[key][0],
                             'stt': self.mainInfo[key][2],
                             'cl': partial(os.startfile, key)})
            button.key = '{0}Button'.format(key)
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button._name = '{0} Button'.format(key)
                button.Type = 'DAMGStartFileButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(key)

    def executingButton(self, key, parent):
        if key in self.mainInfo.keys():
            button = Button({'txt': self.mainInfo[key][0],
                             'stt': self.mainInfo[key][2],
                             'cl': partial(parent.signals.emit, 'executing', key), })
            button.key = '{0}Button'.format(key)
            button._name = '{0} Button'.format(key)
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button.Type = 'DAMGExecutingButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(key)

    def openBrowserButton(self, key, parent):
        if key in self.mainInfo.keys():
            button = Button({'txt': self.mainInfo[key][0],
                             'stt': self.mainInfo[key][2],
                             'cl': partial(parent.signals.emit, 'openBrowser', key), })
            button.key = '{0}{1}Button'.format(parent.key, key)
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button._name = '{0} Button'.format(key)
                button.Type = 'DAMGOpenBrowserButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(key)

    def register(self, button):
        if not button.key in self.buttonKeys:
            self.buttonKeys.append(button.key)
            self[button.key] = button
        else:
            return self.buttonRegisterError(button.key)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 10:22 AM
# © 2017 - 2018 DAMGteam. All rights reserved