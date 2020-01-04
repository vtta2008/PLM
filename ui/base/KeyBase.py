# -*- coding: utf-8 -*-
"""

Script Name: KeyBase.py
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
from bin                                import DAMGDICT
from devkit.Widgets                     import Action, Button
from utils                              import is_string, is_action, is_button
from appData                            import (OPEN_URL_KEYS, CONFIG_DEV, CONFIG_TOOLS, CONFIG_OFFICE, CONFIG_TDS,
                                                CONFIG_ART, CONFIG_TEX, CONFIG_POST, CONFIG_VFX, CONFIG_PRE,
                                                CONFIG_EXTRA, CONFIG_SYSTRAY, SHORTCUT_KEYS, STYLESHEET_KEYS,
                                                BTNTAGSIZE, TAGBTNSIZE, plmInfo)

class KeyBase(DAMGDICT):

    key                                 = 'KeyBase'

    plmInfo                             = plmInfo

    # Actions
    stylesheetActions                   = STYLESHEET_KEYS
    viewActions                         = ['Showall']

    appActions                          = ['AppSetting', 'Configurations', 'Preferences', 'Organisation', 'Project', 'Team', 'Task', 'Exit']
    goActions                           = ['ConfigFolder', 'IconFolder', 'SettingFolder', 'AppDataFolder', 'PreferenceFolder', ]
    officeActions                       = ['TextEditor', 'NoteReminder'] + CONFIG_OFFICE
    toolsActions                        = CONFIG_TOOLS + ['CleanPyc', 'ReConfig', 'Debug']
    devActions                          = CONFIG_DEV
    libActions                          = ['Alpha', 'HDRI', 'Texture']
    helpActions                         = ['PLM wiki', 'About', 'CodeOfConduct', 'Contributing', 'Credit',
                                            'Reference', 'Version', 'Feedback', 'ContactUs', ]

    editActions                         = SHORTCUT_KEYS
    preActions                          = CONFIG_PRE
    tdActions                           = CONFIG_TDS
    artActions                          = CONFIG_ART
    texActions                          = CONFIG_TEX
    postActions                         = CONFIG_POST
    vfxActions                          = CONFIG_VFX
    extraActions                        = CONFIG_EXTRA
    sysTrayActions                      = CONFIG_SYSTRAY

    tagButtons                          = ['pythonTag', 'licenceTag', 'versionTag']
    managerButtons                      = ['Organisation', 'Project', 'Team', 'Task']
    userButtons                         = ['UserSetting', 'SignUp', 'SwitchAccount', 'SignOut']

    checkedKeys                         = [k for k in plmInfo.keys()]

    def __init__(self, parent=None):
        super(KeyBase, self).__init__(self)
        self.parent                     = parent

    def register(self, object):
        pass

    def keyConfigError(self, key):
        print('ActionKeyConfigError: Key is not in plmInfo: {0}'.format(key))

    def actionRegisterError(self, key):
        print('ActionRegisterError: This action is already registered: {0}'.format(key))

    def buttonRegisterError(self, key):
        print('ButtonRegisterError: This button is already registered: {0}'.format(key))

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
        action = Action({'icon': self.plmInfo[key].icon,
                         'txt': '&{0}'.format(key),
                         'stt': self.plmInfo[key].statusTip,
                         'tt': self.plmInfo[key].toolTip,
                         'trg': partial(self.parent.command, key), }, parent)
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
                         'stt': self.plmInfo[key].statusTip,
                         'tt': self.plmInfo[key].toolTip,
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
        button = Button({'icon': self.plmInfo[key].icon,
                         'stt': self.plmInfo[key].statusTip,
                         'tt': self.plmInfo[key].toolTip,
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