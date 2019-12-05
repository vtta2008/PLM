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
from PyQt5.QtWidgets import QApplication

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

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class Modes(dict):
    key = 'Modes'

    _subprocess                     = True
    _config                         = 'Alpha'

    def __init__(self):
        dict.__init__(self)

        self['subprocess']          = self.subprocess
        self['config']              = self.config

    @property
    def subprocess(self):
        return self._subprocess

    @property
    def config(self):
        return self._config

    @subprocess.setter
    def subprocess(self, val):
        self._subprocess            = val

    @config.setter
    def config(self, val):
        self._config                = val

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

class PreSettings(object):

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
        super(PreSettings, self).__init__()

        self.tracks                 = Tracks()
        self.checks                 = Checks()
        self.modes                  = Modes

    @property
    def cmds(self):
        return self._cmds

preSetting = PreSettings()

# print(1)
try:
    os.getenv(__envKey__)
except KeyError:
    cmd = 'SetX {0} {1}'.format(__envKey__, ROOT)
    subprocess.Popen(cmd, shell=True).wait()
    preSetting.cfgable = True
else:
    if os.getenv(__envKey__)   != ROOT:
        cmd = 'SetX {0} {1}'.format(__envKey__, ROOT)
        subprocess.Popen(cmd, shell=True).wait()
        preSetting.cfgable = True
    else:
        preSetting.cfgable = True

if preSetting.cfgable:
    from cores.ConfigManager import ConfigManager
    configManager = ConfigManager(__envKey__, ROOT, Modes())
    if not configManager.cfgs:
        if preSetting.checks.report:
            print("CONFIGERROR: configurations have not done yet.")
        sys.exit()
    else:
        if preSetting.checks.report:
            print('Configurations has been completed.')
else:
    if preSetting.checks.report:
        print('EnvironmentVariableError: {0} is not set to {1}, please try again.'.format(__envKey__, ROOT))
    sys.exit()
# print(2)

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

    if preSetting.checks.ignoreIDs:
        print(ignoreIDs)
    return ignoreIDs

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
    if preSetting.checks.toBuildUis:
        print(toBuildUis)
    return toBuildUis

def __tobuildCmds__():
    import json
    tmpPth = __checkTmpPth__()
    toBuildCmdsFile = os.path.join(tmpPth, '.cmds')

    if os.path.exists(toBuildCmdsFile):
        with open(toBuildCmdsFile, 'r') as f:
            try:
                toBuildCmds = json.load(f)
            except json.decoder.JSONDecodeError:
                toBuildCmds = preSetting.cmds
    else:
        with open(toBuildCmdsFile, 'wb+') as f:
            toBuildCmds = json.dump(preSetting.cmds, f, indent=4)

    if preSetting.checks.toBuildCmds:
        print(toBuildCmds)
    return toBuildCmds

def __copyright__():
    _copyright = 'Pipeline Manager (PLM) Copyright (C) 2017 - 2019 by DAMGTEAM, contributed by Trinh Do & Duong Minh Duc.'
    if preSetting.checks.copyright:
        print(_copyright)
    return _copyright

# print(3)

class Application(QApplication):

    Type                            = 'DAMGAPPLICATION'
    key                             = 'Application'
    _name                           = 'DAMG Application'
    _envKey                         = __envKey__
    _root                           = ROOT

    _copyright                      = __copyright__()

    _login                          = False

    trackRecieveSignal             = preSetting.tracks.recieveSignal
    trackBlockSignal               = preSetting.tracks.blockSignal
    trackCommand                   = preSetting.tracks.command
    trackRegistLayout              = preSetting.tracks.registLayout
    trackJobsTodo                  = preSetting.tracks.jobsToDo
    trackShowLayoutError           = preSetting.tracks.showLayoutError
    trackEvents                    = preSetting.tracks.events

    timeReset                       = 5

    ignoreIDs                       = __ignoreIDs__()
    toBuildUis                      = __tobuildUis__()
    toBuildCmds                     = __tobuildCmds__()

    TODO                            = dict(toBuildUis = toBuildUis, toBuildCmds = toBuildCmds)

    showLayout_old                  = []
    executing_old                   = []
    setSetting_old                  = []
    openBrowser_old                 = []
    sysNotify_old                   = []

    _styleSheet                     = None

    _allowLocalMode                 = True


    def checkSignalRepeat(self, old, data):
        new = [i for i in data]

        if len(new) == 0:
            repeat = False
        elif len(new) == len(old):
            repeat = True
            for i in range(len(new)):
                if not new[i] == old[i]:
                    repeat = False
                    break
        else:
            repeat = False

        old = new
        return old, repeat

    def runEvent(self):
        return sys.exit(self.exec_())

    def setRecieveSignal(self, bool):
        preSetting.tracks.recieveSignal = bool
        self.trackRecieveSignal = bool

    def setBlockSignal(self, bool):
        preSetting.tracks.blockSignal = bool
        self.trackBlockSignal = bool

    def setTrackCommand(self, bool):
        preSetting.tracks.command = bool
        self.trackCommand = bool

    def setRegistLayout(self, bool):
        preSetting.tracks.registLayout = bool
        self.trackRegistLayout = bool

    def setJobsTodo(self, bool):
        preSetting.tracks.jobsToDo = bool
        self.trackJobsTodo = bool

    def setShowLayout(self, bool):
        preSetting.tracks.showLayoutError = bool
        self.trackShowLayoutError = bool

    def setTrackEvent(self, bool):
        preSetting.tracks.events = bool
        self.trackEvents = bool

    def countDownReset(self, limit):
        self.count += 1
        if self.count == limit:
            self.showLayout_old     = []
            self.executing_old      = []
            self.setSetting_old     = []
            self.openBrowser_old    = []
            self.sysNotify_old      = []

    @property
    def login(self):
        return self._login

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                  = val

    @login.setter
    def login(self, val):
        self._login                 = val

# print(4)
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 6:55 AM
# © 2017 - 2018 DAMGteam. All rights reserved