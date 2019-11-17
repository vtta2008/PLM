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
import os, sys, subprocess

__envKey__                      = "DAMGTEAM"
ROOT                            = os.path.abspath(os.getcwd())

cfgable                         = False
allowReport                     = False
checkCopyright                  = False
checkToBuildUis                 = False
checkToBuildCmds                = False
checkIgnoreIDs                  = False

try:
    os.getenv(__envKey__)
except KeyError:
    subprocess.Popen('SetX {0} {1}'.format(__envKey__, ROOT), shell=True).wait()
    cfgable = True
else:
    if os.getenv(__envKey__)   != ROOT:
        subprocess.Popen('SetX {0} {1}'.format(__envKey__, ROOT), shell=True).wait()
        cfgable                 = True
    else:
        cfgable                 = True
finally:
    if cfgable:
        from cores.ConfigManager import ConfigManager
        configManager = ConfigManager(__envKey__, ROOT)
        if not configManager.cfgs:
            if allowReport:
                print("CONFIGERROR: configurations have not done yet.")
            sys.exit()
        else:
            if allowReport:
                print('Configurations has been completed.')
    else:
        if allowReport:
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
    import json
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

    if checkIgnoreIDs:
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
    if checkToBuildUis:
        print(toBuildUis)
    return toBuildUis

def __tobuildCmds__():
    import json
    tmpPth = __checkTmpPth__()
    toBuildCmdsFile = os.path.join(tmpPth, '.toBuildCmds')

    if os.path.exists(toBuildCmdsFile):
        with open(toBuildCmdsFile, 'r') as f:
            toBuildCmds = json.load(f)
    else:
        toBuildCmds = [

                      ]
        with open(toBuildCmdsFile, 'w') as f:
            toBuildCmds = json.dump(toBuildCmds, f, indent=4)

    if checkToBuildCmds:
        print(toBuildCmds)
    return toBuildCmds

def copyright():
    copyright = 'Pipeline Manager (PLM) Copyright (C) 2017 - 2019 by DAMGTEAM, contributed by Trinh Do & Duong Minh Duc.'
    if checkCopyright:
        print(copyright)
    return copyright

from PyQt5.QtWidgets import QApplication

class Application(QApplication):

    Type                            = 'DAMGAPPLICATION'
    key                             = 'Application'
    _name                           = 'DAMG Application'
    _envKey                         = __envKey__
    _root                           = ROOT

    _copyright                      = copyright()
    _login                          = False
    _trackRecieveSignal             = False
    _trackBlockSignal               = False
    _trackCommand                   = False
    _trackRegistLayout              = False
    _trackJobsTodo                  = False
    _trackShowLayoutError           = False
    _trackEvents                    = False

    ignoreIDs                       = __ignoreIDs__()
    toBuildUis                      = __tobuildUis__()
    toBuildCmds                     = __tobuildCmds__()

    todoList = dict(toBuildUis = toBuildUis, toBuildCmds = toBuildCmds)

    def __call__(self, *args, **kwargs):
        print('Application has been called from: {0}'.format(__name__))

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

    def exitEvent(self):
        if self._trackJobsTodo:
            from pprint import pprint
            pprint(self.todoList)
        self.exit()

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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 6:55 AM
# © 2017 - 2018 DAMGteam. All rights reserved