# -*- coding: utf-8 -*-
"""

Script Name: __buildins__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

""" Import """

# Python
import os, sys, subprocess, json

PIPE                                = subprocess.PIPE
STDOUT                              = subprocess.STDOUT
__envKey__                          = "DAMGTEAM"

def get_root():
    cwd                             = os.path.abspath(os.getcwd()).replace('\\', '/')
    dirname                         = os.path.basename(cwd)
    if not dirname == __envKey__.lower():
        treeLst                     = cwd.split('/')
        index                       = treeLst.index(__envKey__.lower()) + 1
        root                        = '/'.join(treeLst[0:index])
    else:
        root                        = cwd

    return root

ROOT                                = get_root()

class Modes(dict):
    key = 'Modes'

    _subprocess                     = True
    _config                         = 'Alpha'
    _login                          = 'Offline'
    _allowLocalMode                 = True

    def __init__(self):
        dict.__init__(self)

        self['subprocess']          = self.subprocess
        self['config']              = self.config
        self['login']               = self.login

    @property
    def subprocess(self):
        return self._subprocess

    @property
    def config(self):
        return self._config

    @property
    def login(self):
        return self._login

    @property
    def allowLocalMode(self):
        return self._allowLocalMode

    @subprocess.setter
    def subprocess(self, val):
        self._subprocess            = val

    @config.setter
    def config(self, val):
        self._config                = val

    @login.setter
    def login(self, val):
        self._login                 = val

    @allowLocalMode.setter
    def allowLocalMode(self, val):
        self._allowLocalMode        = val

class Tracks(dict):

    key = 'Tracks'

    _recieveSignal                  = False
    _blockSignal                    = False
    _command                        = False
    _registLayout                   = False
    _jobsToDo                       = False
    _showLayoutError                = False
    _events                         = False

    def __init__(self):
        dict.__init__(self)

        self['recieveSignal']       = self.recieveSignal
        self['blockSignal']         = self.blockSignal
        self['registLayout']        = self.registLayout
        self['jobjsTodo']           = self.jobsToDo
        self['showLayoutError']     = self.showLayoutError
        self['events']              = self.events

    @property
    def recieveSignal(self):
        return self._recieveSignal

    @property
    def blockSignal(self):
        return self._blockSignal

    @property
    def command(self):
        return self._command

    @property
    def registLayout(self):
        return self._registLayout

    @property
    def jobsToDo(self):
        return self._jobsToDo

    @property
    def showLayoutError(self):
        return self._showLayoutError

    @property
    def events(self):
        return self._events

    @recieveSignal.setter
    def recieveSignal(self, val):
        self._recieveSignal         = val

    @blockSignal.setter
    def blockSignal(self, val):
        self._blockSignal           = val

    @command.setter
    def command(self, val):
        self._command               = val

    @registLayout.setter
    def registLayout(self, val):
        self._registLayout          = val

    @jobsToDo.setter
    def jobsToDo(self, val):
        self._jobsToDo              = val

    @showLayoutError.setter
    def showLayoutError(self, val):
        self._showLayoutError       = val

    @events.setter
    def events(self, val):
        self._events                = val

class Checks(dict):

    key                             = 'Checks'

    _report                         = False
    _copyright                      = False
    _toBuildUis                     = False
    _toBuildCmds                    = False
    _ignoreIDs                      = False

    def __init__(self):
        dict.__init__(self)

        self['report']              = self.report
        self['copyright']           = self.copyright
        self['toBuildUis']          = self.toBuildUis
        self['toBUildCmds']         = self.toBuildCmds
        self['ignoreIDs']           = self.ignoreIDs

    @property
    def report(self):
        return self._report

    @property
    def copyright(self):
        return self._copyright

    @property
    def toBuildUis(self):
        return self._toBuildUis

    @property
    def toBuildCmds(self):
        return self._toBuildCmds

    @property
    def ignoreIDs(self):
        return self._ignoreIDs

    @report.setter
    def report(self, val):
        self._report = val

    @copyright.setter
    def copyright(self, val):
        self._copyright = val

    @toBuildUis.setter
    def toBuildUis(self, val):
        self._toBuildUis = val

    @toBuildCmds.setter
    def toBuildCmds(self, val):
        self._toBuildCmds = val

    @ignoreIDs.setter
    def ignoreIDs(self, val):
        self._ignoreIDs = val

class GlobalSetting(object):

    Type                            = 'DAMGPRESETING'
    key                             = 'PreSetting'
    _name                           = 'DAMG Pre Setting'

    cfgable                         = False
    recordLog                       = False
    printOutput                     = False

    _data                           = dict()
    _log                            = dict()
    _cmds                           = dict()

    def __init__(self):
        super(GlobalSetting, self).__init__()

        self.tracks                 = Tracks()
        self.checks                 = Checks()
        self.modes                  = Modes()

    @property
    def cmds(self):
        return self._cmds

glsetting = GlobalSetting()

# print(1)
try:
    os.getenv(__envKey__)
except KeyError:
    cmd = 'SetX {0} {1}'.format(__envKey__, ROOT)
    proc = subprocess.Popen(cmd, shell=True).wait()

    glsetting.cfgable = True
else:
    if os.getenv(__envKey__)   != ROOT:
        cmd = 'SetX {0} {1}'.format(__envKey__, ROOT)
        proc = subprocess.Popen(cmd, shell=True).wait()
        glsetting.cfgable = True
    else:
        glsetting.cfgable = True
# print(2)
if glsetting.cfgable:
    from appData import configs

    if not configs.cfgs:
        if glsetting.checks.report:
            print("CONFIGERROR: configurations have not done yet.")
        sys.exit()
    else:
        if glsetting.checks.report:
            print('Configurations has been completed.')
else:
    if glsetting.checks.report:
        print('EnvironmentVariableError: {0} is not set to {1}, please try again.'.format(__envKey__, ROOT))
    sys.exit()
# print(3)
def __checkTmpPth__():
    import platform
    tmpPth = os.path.join(ROOT, 'appData/.tmp')

    if not os.path.exists(tmpPth):
        os.mkdir(tmpPth)
        if platform.system() == "Windows":
            subprocess.call(["attrib", "+H", tmpPth])
        elif platform.system() == "Darwin":
            subprocess.call(["chflags", "hidden", tmpPth])

    return tmpPth
# print(4)
def __ignoreIDs__():
    tmpPth = __checkTmpPth__()
    ignoreIDsFile = os.path.join(tmpPth, '.ignoreIDs')

    if os.path.exists(ignoreIDsFile):
        with open(ignoreIDsFile, 'r') as f:
            ignoreIDs = json.load(f)
    else:
        ignoreIDs = [
                     'BotTab'       , 'ConnectStatus'      , 'ConnectStatusSection', 'Footer'                   ,
                     'GridLayout'   , 'MainMenuBar'        , 'MainMenuSection'     , 'MainMenuSectionSection'   ,
                     'MainStatusBar', 'MainToolBar'        , 'MainToolBarSection'  , 'MainToolBarSectionSection',
                     'Notification' , 'NotificationSection', 'TerminalLayout'      , 'TopTab'                   ,
                     'TopTab1'      , 'TopTab2'            , 'TopTab3'             ,
                    ]

        with open(ignoreIDsFile, 'w') as f:
            ignoreIDs = json.dump(ignoreIDs, f, indent=4)

    if glsetting.checks.ignoreIDs:
        print(ignoreIDs)
    return ignoreIDs
# print(5)
def __tobuildUis__():
    import json
    tmpPth = __checkTmpPth__()
    toBuildUIsFile = os.path.join(tmpPth, '.toBuildUis')

    if os.path.exists(toBuildUIsFile):
        with open(toBuildUIsFile, 'r') as f:
            toBuildUis = json.load(f)
    else:
        toBuildUis = [
                      'Alpha'           , 'ConfigOrganisation', 'ConfigProject'      , 'ConfigTask'         ,
                      'ConfigTeam'      , 'ContactUs'         , 'EditOrganisation'   , 'EditProject'        ,
                      'EditTask'        , 'EditTeam'          , 'Feedback'           , 'HDRI'               ,
                      'NewOrganisation' ,  'NewTask'          , 'NewTeam'            , 'OrganisationManager',
                      'ProjectManager'  , 'TaskManager'       , 'TeamManager'        , 'Texture'            ,
                      ]
        with open(toBuildUIsFile, 'w') as f:
            toBuildUis = json.dump(toBuildUis, f, indent=4)
    if glsetting.checks.toBuildUis:
        print(toBuildUis)
    return toBuildUis
# print(6)
def __tobuildCmds__():
    import json
    tmpPth = __checkTmpPth__()
    toBuildCmdsFile = os.path.join(tmpPth, '.cmds')

    if os.path.exists(toBuildCmdsFile):
        with open(toBuildCmdsFile, 'r') as f:
            try:
                toBuildCmds = json.load(f)
            except json.decoder.JSONDecodeError:
                toBuildCmds = glsetting.cmds
    else:
        with open(toBuildCmdsFile, 'wb+') as f:
            toBuildCmds = json.dump(glsetting.cmds, f, indent=4)

    if glsetting.checks.toBuildCmds:
        print(toBuildCmds)
    return toBuildCmds
# print(7)
def __copyright__():
    _copyright = 'Pipeline Manager (PLM) Copyright (C) 2017 - 2019 by DAMGTEAM, contributed by Trinh Do & Duong Minh Duc.'
    if glsetting.checks.copyright:
        print(_copyright)
    return _copyright
# print(8)
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 6:55 AM
# © 2017 - 2018 DAMGteam. All rights reserved