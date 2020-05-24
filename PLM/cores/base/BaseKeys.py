# -*- coding: utf-8 -*-
"""

Script Name: KeyBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from ... import globalSettings

""" Import """

# Python
import json
from functools                          import partial

# PLM
from .BaseStorage                       import BaseStorage
from PLM.api.Widgets import Action, Button
from PLM.utils                          import is_string, is_action, is_button
from PLM.cores.Errors                   import ActionKeyConfigError, ActionRegisterError, ButtonRegisterError
from PLM.configs                        import (BTNTAGSIZE, TAGBTNSIZE)


with open(plmCfg, 'r') as f:
    plmInfo = json.load(f)


class BaseKeys(BaseStorage):

    key                                 = 'KeyBase'

    # Actions
    appActions                          = ['AppSetting', 'Configurations', 'Preferences', 'Organisation', 'Project', 'Team', 'Task', 'Exit']
    goActions                           = ['ConfigFolder', 'IconFolder', 'SettingFolder', 'AppDataFolder', 'PreferenceFolder', ]
    editActions                         = SHORTCUT_KEYS
    viewActions                         = ['ShowAll']
    stylesheetActions                   = STYLESHEET_KEYS
    officeActions                       = ['TextEditor', 'NoteReminder'] + [k for k in CONFIG_OFFICE if k in plmInfo.keys()]

    devActions                          = [k for k in CONFIG_DEV if k in plmInfo.keys() and not k in ['QtDesigner']]
    toolsActions                        = [k for k in CONFIG_TOOLS if k in plmInfo.keys()] + ['CleanPyc', 'ReConfig', 'Debug', ] + devActions

    pluginActions                       = PLUGIN_UI_KEY
    formActions                         = FORM_KEY

    libActions                          = LIBRARY_UI_KEYS
    helpActions                         = ['PLM wiki', 'About', 'CodeOfConduct', 'Contributing', 'Credit', 'References',
                                           'Version', 'FeedBack', ] + formActions

    artActions                          = [k for k in CONFIG_ART if k in plmInfo.keys()]
    tdActions                           = [k for k in CONFIG_TDS if k in plmInfo.keys()]
    vfxActions                          = [k for k in CONFIG_VFX if k in plmInfo.keys()]
    texActions                          = [k for k in CONFIG_TEX if k in plmInfo.keys()]
    postActions                         = [k for k in CONFIG_POST if k in plmInfo.keys()]
    preActions                          = [k for k in CONFIG_PRE if k in plmInfo.keys()]
    extraActions                        = [k for k in CONFIG_EXTRA if k in plmInfo.keys()]

    sysTrayActions                      = ['Minimize', 'Restore', 'Maximize', 'Snipping Tool', 'ScreenShot', 'Exit', 'SignIn']

    # Buttons

    tagButtons                          = ['pythonTag', 'licenceTag', 'versionTag']
    managerButtons                      = ['Organisation', 'Project', 'Team', 'Task']
    userButtons                         = ['UserSetting', 'LogIn', 'SwitchAccount', 'LogOut']

    checkedKeys                         = [k for k in plmInfo.keys()]

    def __init__(self, parent=None):
        super(BaseKeys, self).__init__()
        self.parent                     = parent

    def keyConfigError(self, key):
        ActionKeyConfigError('Key is not in plmInfo: {0}'.format(key))

    def actionRegisterError(self, key):
        if globalSettings.actionRegisterError:
            ActionRegisterError('This action is already registered: {0}'.format(key))

    def buttonRegisterError(self, key):
        if globalSettings.checks.buttonRegisterError:
            ButtonRegisterError('This button is already registered: {0}'.format(key))

    def createActions(self, keys, parent):
        actions = []
        for key in keys:
            if key in self.checkedKeys:
                if is_string(key):
                    action = self.createAction(key, parent)
                    actions.append(action)
                elif is_action(key):
                    action = key
                    action.setParent(parent)
                    self.register(action)
                    actions.append(action)
                else:
                    self.actionRegisterError(key)
            else:
                self.keyConfigError(key)
        return actions

    def createButtons(self, keys, parent):
        buttons = []
        for key in keys:
            if key in self.checkedKeys:
                if is_string(key):
                    button = self.createButton(key, parent)
                    buttons.append(button)
                elif is_button(key):
                    button = key
                    button.setParent(parent)
                    self.register(Button)
                    buttons.append(Button)
                else:
                    self.actionRegisterError(key)
            else:
                self.keyConfigError(key)
        return buttons

    def createAction(self, key, parent):
        # if key in ['Organisation', 'Project', 'Team', 'Task']:
        #     key = '{0}Manager'.format(key)
        return self.action(key, parent)

    def createButton(self, key, parent):
        if key in OPEN_URL_KEYS:
            return self.openUrlButton(key, parent)
        else:
            return self.button(key, parent)

    def action(self, key, parent):
        action = Action({'icon': plmInfo[key]['icon'],
                         'txt': '&{0}'.format(key),
                         'stt': plmInfo[key]['statustip'],
                         'tt': plmInfo[key]['tooltip'],
                         'trg': partial(parent.command, key), }, parent)
        action.key = '{0}_{1}_Action'.format(parent.key, key)
        action._name = action.key
        if action.key in self.checkedKeys:
            return self[action.key]
        else:
            action._name = '{0} Action'.format(key)
            self.register(action)
            return action

    def button(self, key, parent):
        button = Button({'txt': '&{0}'.format(key),
                         'stt': plmInfo[key]['statustip'],
                         'tt': plmInfo[key]['tooltip'],
                         'cl': partial(self.parent.command, key), })
        button.key = '{0}_{1}_Button'.format(parent.key, key)
        button._name = button.key
        if button.key in self.checkedKeys:
            return self[button.key]
        else:
            button._name = '{0} Button'.format(key)
            self.register(button)
            return button

    def openUrlButton(self, key, parent):
        button = Button({'icon': plmInfo[key]['icon'],
                         'stt': plmInfo[key]['statustip'],
                         'tt': plmInfo[key]['tooltip'],
                         'fix': BTNTAGSIZE,
                         'ics': TAGBTNSIZE,
                         'cl': partial(self.parent.command, key)})
        button.key = '{0}_{1}_Button'.format(parent.key, key)
        button._name = button.key
        if button.key in self.checkedKeys:
            return self[button.key]
        else:
            button._name = '{0} Button'.format(key)
            button.Type = 'DAMGOpenBrowserButton'
            self.register(button)
            return button

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 7/12/2019 - 4:35 PM
# © 2017 - 2018 DAMGteam. All rights reserved