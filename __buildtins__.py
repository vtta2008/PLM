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
import os, sys, subprocess, pathlib2, json

PIPE                                = subprocess.PIPE
STDOUT                              = subprocess.STDOUT
__envKey__                          = "DAMGTEAM"
ROOT                                = os.path.abspath(os.getcwd())

def asUtf8(s):
    if isinstance(s, pathlib2.Path):
        s = str(s)
    if type(s) in [str]:
        return s.encode(encoding='utf-8')
    else:
        return s

class PremiseController(object):

    Type                            = 'DAMGPRESETING'
    key                             = 'PreSetting'
    _name                           = 'DAMG Pre Setting'

    cfgable                         = False
    allowReport                     = True
    checkCopyright                  = False
    checkToBuildUis                 = False
    checkToBuildCmds                = False
    checkIgnoreIDs                  = False
    recordLog                       = False
    printOutput                     = False

    trackRecieveSignal              = False
    trackBlockSignal                = False
    trackCommand                    = False
    trackRegistLayout               = False
    trackJobsTodo                   = False
    trackShowLayoutError            = False
    trackEvents                     = False

    _data                           = dict()
    _log                            = dict()
    _cmds                           = dict()

    values = [cfgable, allowReport, checkCopyright, checkToBuildUis, checkToBuildCmds, checkIgnoreIDs,
              recordLog, printOutput, trackRecieveSignal, trackBlockSignal, trackCommand, trackRegistLayout,
              trackJobsTodo, trackShowLayoutError, trackEvents]

    keys = ['cfgable', 'allowReport', 'checkCopyright', 'checkToBuildUis', 'checkToBuildCmds', 'checkIgnoreIDs',
            'recordLog', 'printOutput', 'trackRecieveSignal', 'trackBlockSignal', 'trackCommand', 'trackRegistLayout',
            'trackJobsTodo', 'trackShowLayoutError', 'trackEvents']

    def __init__(self):
        super(PremiseController, self).__init__()

        if len(self.keys) == len(self.values):
            self.update()
        else:
            print('DataNotEqualError: {0} keys but {1} values'.format(len(self.keys), len(self.values)))

    def update(self):
        for k in self.keys:
            self._data[k] = self.values[self.keys.index(k)]

        with open(os.path.join(ROOT, 'appData/.tmp', '.cmds'), 'w+') as f:
            json.dump(self.cmds, f, indent=4)

    def edit(self, k, v):
        self._data[k] = v
        for key, value in self._data.items():
            if key == k:
                i = self.keys.index(key)
                self.values[i] = v
                self.update()
                return self.values[i]

    @property
    def name(self):
        return self._name

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        self._data = val

    @property
    def cmds(self):
        return self._cmds

    @cmds.setter
    def cmds(self, val):
        self._cmds = val

pres = PremiseController()

def run_command(cmd, printOutput=pres.printOutput):
    args = [arg for arg in cmd.split(' ')]
    # print( '%s %s' % (cmd, ' '.join( args )) )

    try:
        if sys.platform == 'win32':
            proc = subprocess.Popen(args=args, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False)
        else:
            proc = subprocess.Popen(args=args, close_fds=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

        output = proc.stdout.read()
        proc.wait()
    except EnvironmentError as e:
        output = 'ErrorRunning {0} {1}: {2}'.format(cmd, ' '.join(args), str(e))

    pres._cmds[cmd] = args
    pres._cmds.update()

    if printOutput:
        print(output.decode().replace('\\', '/'))

    return output

try:
    os.getenv(__envKey__)
except KeyError:
    cmd = 'SetX {0} {1}'.format(__envKey__, ROOT)
    run_command(cmd, pres.printOutput)
    pres.edit('cfgable', True)
    pres.cfgable = True
else:
    if os.getenv(__envKey__)   != ROOT:
        cmd = 'SetX {0} {1}'.format(__envKey__, ROOT)
        run_command(cmd, pres.printOutput)
        pres.edit('cfgable', True)
        pres.cfgable = True
    else:
        pres.edit('cfgable', True)
        pres.cfgable = True

try:
    import damg
except ImportError:
    cmd = 'python -m pip install --user --upgrade damg'
    run_command(cmd, pres.printOutput)

if pres.cfgable:
    from cores.ConfigManager import ConfigManager
    configManager = ConfigManager(__envKey__, ROOT)
    if not configManager.cfgs:
        if pres.allowReport:
            print("CONFIGERROR: configurations have not done yet.")
        sys.exit()
    else:
        if pres.allowReport:
            print('Configurations has been completed.')
else:
    if pres.allowReport:
        print('EnvironmentVariableError: {0} is not set to {1}, please try again.'.format(__envKey__, ROOT))
    sys.exit()

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

    if pres.checkIgnoreIDs:
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
    if pres.checkToBuildUis:
        print(toBuildUis)
    return toBuildUis

def __tobuildCmds__():
    import json
    tmpPth = __checkTmpPth__()
    toBuildCmdsFile = os.path.join(tmpPth, '.cmds')

    if os.path.exists(toBuildCmdsFile):
        with open(toBuildCmdsFile, 'r') as f:
            toBuildCmds = json.load(f)
    else:
        with open(toBuildCmdsFile, 'wb+') as f:
            toBuildCmds = json.dump(pres.cmds, f, indent=4)

    if pres.checkToBuildCmds:
        print(toBuildCmds)
    return toBuildCmds

def __copyright__():
    _copyright = 'Pipeline Manager (PLM) Copyright (C) 2017 - 2019 by DAMGTEAM, contributed by Trinh Do & Duong Minh Duc.'
    if pres.checkCopyright:
        print(_copyright)
    return _copyright

from PyQt5.QtWidgets import QApplication

class Application(QApplication):

    Type                            = 'DAMGAPPLICATION'
    key                             = 'Application'
    _name                           = 'DAMG Application'
    _envKey                         = __envKey__
    _root                           = ROOT

    _copyright                      = __copyright__()

    _login                          = False

    _trackRecieveSignal             = False
    _trackBlockSignal               = False
    _trackCommand                   = False
    _trackRegistLayout              = False
    _trackJobsTodo                  = False
    _trackShowLayoutError           = False
    _trackEvents                    = False

    timeReset                       = 5

    ignoreIDs                       = __ignoreIDs__()
    toBuildUis                      = __tobuildUis__()
    toBuildCmds                     = __tobuildCmds__()

    todoList                        = dict(toBuildUis = toBuildUis, toBuildCmds = toBuildCmds)

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

    def changeRecieveSignal(self, bool):
        self._trackRecieveSignal    = bool

    def changeBlockSignal(self, bool):
        self._trackBlockSignal      = bool

    def changeTrackCommand(self, bool):
        self._trackCommand          = bool

    def changeRegistLayout(self, bool):
        self._trackRegistLayout     = bool

    def changeJobsTodo(self, bool):
        self._trackJobsTodo         = bool

    def changeShowLayout(self, bool):
        self._trackShowLayoutError  = bool

    def changeTrackEvent(self, bool):
        self._trackEvents           = bool

    @property
    def login(self):
        return self._login

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @property
    def trackRecieveSignal(self):
        return self._trackRecieveSignal

    @property
    def trackBlockSignal(self):
        return self._trackBlockSignal

    @property
    def trackCommand(self):
        return self._trackCommand

    @property
    def trackRegistLayout(self):
        return self._trackRegistLayout

    @property
    def trackShowLayoutError(self):
        return self._trackShowLayoutError

    @property
    def trackEvents(self):
        return self._trackEvents

    @name.setter
    def name(self, val):
        self._name                  = val

    @login.setter
    def login(self, val):
        self._login                 = val

    @trackRecieveSignal.setter
    def trackRecieveSignal(self, val):
        self._trackRecieveSignal    = val

    @trackBlockSignal.setter
    def trackBlockSignal(self, val):
        self._trackBlockSignal      = val

    @trackCommand.setter
    def trackCommand(self, val):
        self._trackCommand          = val

    @trackRegistLayout.setter
    def trackRegistLayout(self, val):
        self._trackRegistLayout     = val

    @trackShowLayoutError.setter
    def trackShowLayoutError(self, val):
        self._trackShowLayoutError  = val

    @trackEvents.setter
    def trackEvents(self, val):
        self._trackEvents           = val

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 6:55 AM
# © 2017 - 2018 DAMGteam. All rights reserved