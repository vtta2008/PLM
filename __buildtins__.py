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
import os, sys, subprocess, platform

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

if platform.system() == 'Windows':
    try:
        import winshell
    except ImportError:
        subprocess.Popen('python -m pip install winshell --user', shell=True).wait()

    try:
        import wmi
    except ImportError:
        subprocess.Popen('python -m pip install wmi --user', shell=True).wait()

    try:
        import helpdev
    except ImportError:
        subprocess.Popen('python -m pip install helpdev --user', shell=True).wait()

else:
    sys.exit()



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

    _recieveSignal                  = True
    _blockSignal                    = True
    _command                        = True
    _registLayout                   = True
    _jobsToDo                       = True
    _showLayoutError                = True
    _events                         = True

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

    _report                         = True
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
        self._report                = val

    @copyright.setter
    def copyright(self, val):
        self._copyright             = val

    @toBuildUis.setter
    def toBuildUis(self, val):
        self._toBuildUis            = val

    @toBuildCmds.setter
    def toBuildCmds(self, val):
        self._toBuildCmds           = val

    @ignoreIDs.setter
    def ignoreIDs(self, val):
        self._ignoreIDs             = val

class GlobalSetting(object):

    Type                            = 'DAMGPRESETING'
    key                             = 'PreSetting'
    _name                           = 'DAMG Pre Setting'

    cfgable                         = False
    recordLog                       = False
    printOutput                     = True

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

    @property
    def log(self):
        return self._log

    @property
    def data(self):
        return self._data

globalSetting = GlobalSetting()

# print(1)

try:
    os.getenv(__envKey__)
except KeyError:
    cmd = 'SetX {0} {1}'.format(__envKey__, ROOT)
    proc = subprocess.Popen(cmd, shell=True).wait()

    globalSetting.cfgable = True
else:
    if os.getenv(__envKey__)   != ROOT:
        cmd = 'SetX {0} {1}'.format(__envKey__, ROOT)
        proc = subprocess.Popen(cmd, shell=True).wait()
        globalSetting.cfgable = True
    else:
        globalSetting.cfgable = True

# print(4)

def __copyright__():
    _copyright = 'Pipeline Manager (PLM) Copyright (C) 2017 - 2020 by DAMGTEAM, contributed by Trinh Do & Duong Minh Duc.'
    if globalSetting.checks.copyright:
        print(_copyright)
    return _copyright

# print(5)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 6:55 AM
# © 2017 - 2018 DAMGteam. All rights reserved