# -*- coding: utf-8 -*-
"""

Script Name: base.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

""" Import """

# Python
import os
from functools                          import partial

# PLM
from bin                                import DAMGDICT, DAMGLIST
from toolkits.Widgets                   import Action, Button
from utils                              import data_handler, is_string, is_action, is_button
from appData                            import (mainCfg, SHOWLAYOUT_KEY, START_FILE_KEY, EXECUTING_KEY, OPEN_BROWSER_KEY,
                                                CONFIG_DEV, CONFIG_TOOLS, CONFIG_OFFICE, CONFIG_TDS, CONFIG_ART, CONFIG_TEX,
                                                CONFIG_POST, CONFIG_VFX, CONFIG_EXTRA, CONFIG_SYSTRAY, RESTORE_KEY, SHOWMIN_KEY,
                                                SHOWMAX_KEY, EDIT_KEY, STYLESHEET_KEY, BTNTAGSIZE, TAGBTNSIZE, BTNICONSIZE, ICONBTNSIZE)

class KeyBase(DAMGDICT):

    key                                 = 'KeyBase'

    appInfo                             = data_handler(filePath=mainCfg)

    actionKeys                          = DAMGLIST()
    showLayoutKeys                      = DAMGLIST()
    showRestoreKeys                     = DAMGLIST()
    showMaximizeKeys                    = DAMGLIST()
    showMinimizeKeys                    = DAMGLIST()
    startFileKeys                       = DAMGLIST()
    openBrowserKeys                     = DAMGLIST()
    executingKeys                       = DAMGLIST()
    buttonKeys                          = DAMGLIST()
    tagKeys                             = DAMGLIST()

    # Actions
    orgActions                          = ['Organisation']
    teamActions                         = ['Team']
    prjActions                          = ['Project']
    taskActions                         = ['Task']
    stylesheetActions                   = STYLESHEET_KEY
    viewActions                         = ['Showall']
    appActions                          = ['SettingUI', 'Configuration', 'Preferences', 'Exit']
    goActions                           = ['ConfigFolder', 'IconFolder', 'SettingFolder', 'AppFolder']
    officeActions                       = ['TextEditor', 'NoteReminder'] + CONFIG_OFFICE
    toolsActions                        = CONFIG_TOOLS + ['CleanPyc', 'ReConfig', 'Debug']
    devActions                          = CONFIG_DEV
    libActions                          = ['Alpha', 'HDRI', 'Texture']
    helpActions                         = ['PLM wiki', 'About', 'CodeOfConduct', 'Contributing', 'Credit',
                                            'Reference', 'Version', 'Feedback', 'ContactUs', ]

    editActions                         = EDIT_KEY
    tdActions                           = CONFIG_TDS
    artActions                          = CONFIG_ART
    texActions                          = CONFIG_TEX
    postActions                         = CONFIG_POST
    vfxActions                          = CONFIG_VFX
    extraActions                        = CONFIG_EXTRA
    sysTrayActions                      = CONFIG_SYSTRAY

    tags                                = dict(
                                            pythonTag="https://docs.anaconda.com/anaconda/reference/release-notes/",
                                            licenceTag="https://github.com/vtta2008/damgteam/blob/master/LICENCE",
                                            versionTag="https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst"
                                                )

    tagButtons                          = ['pythonTag', 'licenceTag', 'versionTag']
    managerButtons                      = ['Organisation', 'Project', 'Team', 'Task']
    userButtons                         = ['UserSetting', 'SignUp', 'SwitchAccount', 'SignOut']

    checkedKeys                         = userButtons + tagButtons + managerButtons


    def __init__(self, parent=None):
        DAMGDICT.__init__(self)

        self._parent                    = parent

        self.showLayoutKeys.appendList(SHOWLAYOUT_KEY)
        self.startFileKeys.appendList(START_FILE_KEY)
        self.executingKeys.appendList(EXECUTING_KEY)
        self.openBrowserKeys.appendList(OPEN_BROWSER_KEY)
        self.showRestoreKeys.appendList(RESTORE_KEY)
        self.showMaximizeKeys.appendList(SHOWMAX_KEY)
        self.showMinimizeKeys.appendList(SHOWMIN_KEY)

        self.actionKeys = self.showLayoutKeys + self.startFileKeys + self.executingKeys + self.officeActions + \
                          self.showRestoreKeys + self.showMaximizeKeys + self.showMinimizeKeys

        self.showLayoutKeys.appendList(SHOWLAYOUT_KEY)
        self.startFileKeys.appendList(START_FILE_KEY)
        self.executingKeys.appendList(EXECUTING_KEY)
        self.openBrowserKeys.appendList(OPEN_BROWSER_KEY)
        self.showRestoreKeys.appendList(RESTORE_KEY)
        self.showMaximizeKeys.appendList(SHOWMAX_KEY)
        self.showMinimizeKeys.appendList(SHOWMIN_KEY)
        self.tagKeys.appendList(self.tagButtons)

        self.buttonKeys = self.showLayoutKeys + self.startFileKeys + self.executingKeys + self.showRestoreKeys + \
                          self.showMaximizeKeys + self.showMinimizeKeys + self.tagKeys

    def actionConfigError(self, key):
        return print('ActionKeyConfigError: This key is not registered: {0}'.format(key))

    def actionRegisterError(self, key):
        return print('ActionRegisterError: This action is already registered: {0}'.format(key))

    def buttonConfigError(self, key):
        return print('ButtonKeyConfigError: This key is not registered: {0}'.format(key))

    def buttonRegisterError(self, key):
        return print('ButtonRegisterError: This action is already registered: {0}'.format(key))

    def register(self, object):
        pass

    def createActions(self, keys, parent):
        actions = []
        for key in keys:
            if key in self.appInfo.keys():
                if is_string(key):
                    action = self.createAction(key, parent)
                    actions.append(action)
                elif is_action(key):
                    action = key
                    action.setParent(parent)
                    self.register(action)
                    actions.append(action)
                else:
                    print("DataTypeError: Could not add action: {0}".format(key))

        return actions

    def createAction(self, key, parent):
        if key in self.showLayoutKeys:
            # print('{0} is set to {1} action'.format(key, 'showlayout'))
            return self.showLayoutAction(key, parent)
        elif key in self.startFileKeys:
            # print('{0} is set to {1} action'.format(key, 'startfile'))
            return self.startFileAction(key, parent)
        elif key in self.executingKeys:
            # print('{0} is set to {1} action'.format(key, 'executing'))
            return self.executingAction(key, parent)
        elif key in self.openBrowserKeys:
            # print('{0} is set to {1} action'.format(key, 'openBrowser'))
            return self.openBrowserAction(key, parent)
        elif key in self.showMinimizeKeys:
            # print('{0} is set to {1} action'.format(key, 'showminimized'))
            return self.showMinAction(key, parent)
        elif key in self.showMaximizeKeys:
            # print('{0} is set to {1} action'.format(key, 'showmaximized'))
            return self.showMaxAction(key, parent)
        elif key in self.showRestoreKeys:
            # print('{0} is set to {1} action'.format(key, 'showrestore'))
            return self.showRestoreAction(key, parent)
        else:
            return self.actionConfigError(key)

    def showLayoutAction(self, key, parent):
        if key in self.appInfo.keys():
            action = Action({'icon': self.appInfo[key][1],
                             'txt': '&{0}'.format(key),
                             'stt': self.appInfo[key][0],
                             'trg': partial(parent.signals.emit, 'showLayout', key, 'show'), }, parent)
            action.key = '{0}_{1}_Action'.format(parent.key, key)
            action._name = action.key
            if action.key in self.actionKeys:
                return self[action.key]
            else:
                action._name = '{0} Action'.format(key)
                action.Type = 'DAMGShowLayoutAction'
                self.register(action)
                return action
        else:
            return self.actionConfigError(key)

    def showRestoreAction(self, key, parent):
        if key in self.appInfo.keys():
            action = Action({'icon': self.appInfo[key][1],
                             'txt': '&{0}'.format(key),
                             'stt': self.appInfo[key][0],
                             'trg': partial(parent.signals.emit, 'showLayout', self.appInfo[key][2], 'showRestore'), }, parent)
            action.key = '{0}_{1}_Action'.format(parent.key, key)
            action._name = action.key
            if action.key in self.actionKeys:
                return self[action.key]
            else:
                action._name = '{0} Action'.format(key)
                action.Type = 'DAMGShowNormalAction'
                self.register(action)
                return action
        else:
            return self.actionConfigError(key)

    def showMaxAction(self, key, parent):
        if key in self.appInfo.keys():
            action = Action({'icon': self.appInfo[key][1],
                             'txt': '&{0}'.format(key),
                             'stt': self.appInfo[key][0],
                             'trg': partial(parent.signals.emit, 'showLayout', self.appInfo[key][2], 'showMax'), }, parent)
            action.key = '{0}_{1}_Action'.format(parent.key, key)
            action._name = action.key
            if action.key in self.actionKeys:
                return self[action.key]
            else:
                action._name = '{0} Action'.format(key)
                action.Type = 'DAMGShowMaximizeAction'
                self.register(action)
                return action
        else:
            return self.actionConfigError(key)

    def showMinAction(self, key, parent):
        if key in self.appInfo.keys():
            action = Action({'icon': self.appInfo[key][1],
                             'txt': '&{0}'.format(key),
                             'stt': self.appInfo[key][0],
                             'trg': partial(parent.signals.emit, 'showLayout', self.appInfo[key][2], 'showMin'), }, parent)
            action.key = '{0}_{1}_Action'.format(parent.key, key)
            action._name = action.key
            if action.key in self.actionKeys:
                return self[action.key]
            else:
                action._name = '{0} Action'.format(key)
                action.Type = 'DAMGShowMinimizeAction'
                self.register(action)
                return action
        else:
            return self.actionConfigError(key)

    def startFileAction(self, key, parent):
        if key in self.appInfo.keys():
            # print('create start file action: {} {}'.format(key, self.appInfo[key][2]))
            action = Action({'icon': self.appInfo[key][1],
                             'txt': '&{0}'.format(key),
                             'stt': self.appInfo[key][0],
                             'trg': partial(os.startfile, self.appInfo[key][2])}, parent)
            action.key = '{0}_{1}_Action'.format(parent.key, key)
            action._name = action.key
            if action.key in self.actionKeys:
                return self[action.key]
            else:
                action._name = '{0} Action'.format(key)
                action.Type = 'DAMGStartFileAction'
                self.register(action)
                return action
        else:
            return self.actionConfigError(key)

    def executingAction(self, key, parent):
        if key in self.appInfo.keys():
            action = Action({'icon': self.appInfo[key][1],
                             'txt': '&{0}'.format(key),
                             'stt': self.appInfo[key][0],
                             'trg': partial(parent.signals.emit, 'executing', self.appInfo[key][2]), }, parent)
            action.key = '{0}_{1}_Action'.format(parent.key, key)
            action._name = '{0} Action'.format(key)
            if action.key in self.actionKeys:
                return self[action.key]
            else:
                action.Type = 'DAMGExecutingAction'
                self.register(action)
                return action
        else:
            return self.actionConfigError(key)

    def openBrowserAction(self, key, parent):
        if key in self.appInfo.keys():
            action = Action({'icon': self.appInfo[key][1],
                             'txt': '&{0}'.format(key),
                             'stt': self.appInfo[key][0],
                             'trg': partial(parent.signals.emit, 'openBrowser', self.appInfo[key][2]), }, parent)
            action.key = '{0}_{1}_Action'.format(parent.key, key)
            action._name = action.key
            if action.key in self.actionKeys:
                return self[action.key]
            else:
                action._name = '{0} Action'.format(key)
                action.Type = 'DAMGOpenBrowserAction'
                self.register(action)
                return action
        else:
            return self.actionConfigError(key)

    def createButtons(self, keys, parent):
        buttons = []
        for key in keys:
            if key in self.appInfo.keys():
                if not key in self.checkedKeys:
                    print('key: {0} is in appInfo: {1}'.format(key, self.appInfo[key]))
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
                print('key: {0} NOT in appInfo: {1}'.format(key, self.appInfo[key]))

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
        elif key in self.tagKeys:
            return self.tagOpenBrowserButton(key, parent)
        else:
            # print('key come here: {}'.format(key))
            return self.buttonConfigError(key)

    def showLayoutButton(self, key, parent):
        if key in self.appInfo.keys():
            if key in ['SignIn', 'SignOut', 'SignUp', 'SwitchAccount']:
                show = key
            else:
                show = 'show'

            button = Button({'txt': self.appInfo[key][0],
                             'stt': self.appInfo[key][2],
                             'cl': partial(parent.signals.emit, 'showLayout', key, show), })
            button.key = '{0}_{1}_Button'.format(parent.key, key)
            button._name = button.key
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
        if key in self.appInfo.keys():
            button = Button({'txt': self.appInfo[key][0],
                             'stt': self.appInfo[key][2],
                             'cl': partial(parent.signals.emit, 'showLayout', key, 'showRestore'), })
            button.key = '{0}_{1}_Button'.format(parent.key, key)
            button._name = button.key
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
        if key in self.appInfo.keys():
            button = Button({'txt': self.appInfo[key][0],
                             'stt': self.appInfo[key][2],
                             'cl': partial(parent.signals.emit, 'showLayout', key, 'showMaximized'), })
            button.key = '{0}_{1}_Button'.format(parent.key, key)
            button._name = button.key
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
        if key in self.appInfo.keys():
            button = Button({'txt': self.appInfo[key][0],
                             'stt': self.appInfo[key][2],
                             'cl': partial(parent.signals.emit, 'showLayout', key, 'showMinimized'), })
            button.key = '{0}_{1}_Button'.format(parent.key, key)
            button._name = button.key
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
        if key in self.appInfo.keys():
            button = Button({'txt': self.appInfo[key][0],
                             'stt': self.appInfo[key][2],
                             'cl': partial(os.startfile, key)})
            button.key = '{0}_{1}_Button'.format(parent.key, key)
            button._name = button.key
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
        if key in self.appInfo.keys():
            button = Button({'txt': self.appInfo[key][0],
                             'stt': self.appInfo[key][2],
                             'cl': partial(parent.signals.emit, 'executing', key), })
            button.key = '{0}_{1}_Button'.format(parent.key, key)
            button._name = button.key
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button.Type = 'DAMGExecutingButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(key)

    def openBrowserButton(self, key, parent):
        if key in self.appInfo.keys():
            button = Button({'txt': self.appInfo[key][0],
                             'stt': self.appInfo[key][2],
                             'cl': partial(parent.signals.emit, 'openBrowser', key), })
            button.key = '{0}_{1}_Button'.format(parent.key, key)
            button._name = button.key
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button._name = '{0} Button'.format(key)
                button.Type = 'DAMGOpenBrowserButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(key)

    def iconShowLayoutButton(self, key, parent):
        if key in self.appInfo.keys():
            button = Button({'icon': key,
                             'tt': self.appInfo[key][2],
                             'fix': BTNICONSIZE,
                             'ics': ICONBTNSIZE,
                             'cl': partial(parent.signals.emit, 'showLayout', key, 'show')})
            button.key = '{0}_{1}_Button'.format(parent.key, key)
            button._name = button.key
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button._name = '{0} Button'.format(key)
                button.Type = 'DAMGOpenBrowserButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(key)

    def tagOpenBrowserButton(self, tagName, parent):
        if tagName in self.tags.keys():
            button = Button({'tag': tagName,
                             'fix': BTNTAGSIZE,
                             'ics': TAGBTNSIZE,
                             'cl': partial(parent.signals.emit, 'openBrowser', self.tags[tagName])})
            button.key = '{0}_{1}_Button'.format(parent.key, tagName)
            button._name = button.key
            if button.key in self.buttonKeys:
                return self[button.key]
            else:
                button._name = '{0} Button'.format(tagName)
                button.Type = 'DAMGOpenBrowserButton'
                self.register(button)
                return button
        else:
            return self.buttonConfigError(tagName)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 7/12/2019 - 4:35 PM
# © 2017 - 2018 DAMGteam. All rights reserved