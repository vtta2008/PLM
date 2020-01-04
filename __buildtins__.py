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
cmd                                 = 'SetX {0} {1}'.format(__envKey__, ROOT)

if platform.system() == 'Windows':

    try:
        import winshell
    except ImportError:
        subprocess.Popen('python -m pip install winshell --user', shell=True).wait()

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
        self['allowLocalMode']      = self.allowLocalMode

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
    _lineCode                       = True

    _emittable                      = False
    _emit                           = False
    _block                          = False
    _checkRepeat                    = False
    _getSignal                      = False
    _getSlot                        = False
    _checkState                     = False

    _missingIcon                    = False
    _missingUI                      = False

    _configInfo                     = True
    _deviceInfo                     = False
    _iconInfo                       = False
    _pythonInfo                     = False
    _directoryInfo                  = False
    _pthInfo                        = False
    _mayaInfo                       = False
    _urlInfo                        = False
    _appInfo                        = False
    _plmInfo                        = False

    def __init__(self):
        dict.__init__(self)

        self['recieveSignal']       = self.recieveSignal
        self['blockSignal']         = self.blockSignal
        self['registLayout']        = self.registLayout
        self['jobjsTodo']           = self.jobsToDo
        self['showLayoutError']     = self.showLayoutError
        self['events']              = self.events
        self['lineCode']            = self.lineCode

        self['emittable']           = self.emittable
        self['emit']                = self.emit
        self['block']               = self.block
        self['checkRepeat']         = self.checkRepeat
        self['getSignal']           = self.getSignal
        self['getSlot']             = self.getSlot
        self['checkState']          = self.checkState

        self['missingIcon']         = self.missingIcon
        self['missingUI']           = self.missingUI

        self['configInfo']          = self.configInfo
        self['deviceInfo']          = self.deviceInfo
        self['iconInfo']            = self.iconInfo
        self['pythonInfo']          = self.pythonInfo
        self['directoryInfo']       = self.directoryInfo
        self['pathInfo']            = self.pthInfo
        self['mayaInfo']            = self.mayaInfo
        self['urlInfo']             = self.urlInfo
        self['appInfo']             = self.appInfo
        self['plmInfo']             = self.plmInfo

    @property
    def configInfo(self):
        return self._configInfo

    @property
    def deviceInfo(self):
        return self._deviceInfo

    @property
    def iconInfo(self):
        return self._iconInfo

    @property
    def pythonInfo(self):
        return self._pythonInfo

    @property
    def directoryInfo(self):
        return self._directoryInfo

    @property
    def pthInfo(self):
        return self._pthInfo

    @property
    def mayaInfo(self):
        return self._pthInfo

    @property
    def urlInfo(self):
        return self._urlInfo

    @property
    def emittable(self):
        return self._emittable

    @property
    def emit(self):
        return self._emit

    @property
    def block(self):
        return self._block

    @property
    def checkRepeat(self):
        return self._checkRepeat

    @property
    def getSignal(self):
        return self._getSignal

    @property
    def checkState(self):
        return self._checkState

    @property
    def missingUI(self):
        return self._missingUI

    @property
    def missingIcon(self):
        return self._missingIcon

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
    def lineCode(self):
        return self._lineCode

    @property
    def events(self):
        return self._events

    @property
    def getSlot(self):
        return self._getSlot

    @property
    def appInfo(self):
        return self._appInfo

    @property
    def plmInfo(self):
        return self._plmInfo

    @getSlot.setter
    def getSlot(self, val):
        self._getSlot               = val

    @configInfo.setter
    def configInfo(self, val):
        self._configInfo            = val

    @deviceInfo.setter
    def deviceInfo(self, val):
        self._deviceInfo            = val

    @iconInfo.setter
    def iconInfo(self, val):
        self._iconInfo              = val

    @pythonInfo.setter
    def pythonInfo(self, val):
        self._pythonInfo            = val

    @directoryInfo.setter
    def directoryInfo(self, val):
        self._directoryInfo         = val

    @pthInfo.setter
    def pthInfo(self, val):
        self._pthInfo              = val

    @mayaInfo.setter
    def mayaInfo(self, val):
        self._pthInfo              = val

    @urlInfo.setter
    def urlInfo(self, val):
        self._urlInfo               = val

    @emittable.setter
    def emittable(self, val):
        self._emittable             = val

    @emit.setter
    def emit(self, val):
        self._emit                  = val

    @block.setter
    def block(self, val):
        self._block                 = val

    @checkRepeat.setter
    def checkRepeat(self, val):
        self._checkRepeat           = val

    @getSignal.setter
    def getSignal(self, val):
        self._getSignal             = val

    @checkState.setter
    def checkState(self, val):
        self._checkState            = val

    @missingUI.setter
    def missingUI(self, val):
        self._missingUI             = val

    @missingIcon.setter
    def missingIcon(self, val):
        self._missingIcon           = val

    @lineCode.setter
    def lineCode(self, val):
        self._lineCode              = val

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

    @appInfo.setter
    def appInfo(self, val):
        self._appInfo               = val

    @plmInfo.setter
    def plmInfo(self, val):
        self._plmInfo               = val


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


class DefaultSetting(dict):

    key                             = 'DefaultSetting'

    _auto_changeEmmitable           = True

    _save_configInfo                = True
    _save_deviceInfo                = False
    _save_iconInfo                  = False
    _save_pythonInfo                = False
    _save_directoryInfo             = False
    _save_pathInfo                  = False
    _save_mayaInfo                  = False
    _save_urlInfo                   = False
    _save_appInfo                   = False
    _save_plmInfo                   = False

    def __init__(self):
        dict.__init__(self)

        self['auto_changeEmmitable'] = self.auto_changeEmitable
        self['save_configInfo']     = self.save_configInfo
        self['save_deviceInfo']     = self.save_deviceInfo
        self['save_iconInfo']       = self.save_iconInfo
        self['save_pythonInfo']     = self.save_pythonInfo
        self['save_directoryInfo']  = self.save_directoryInfo
        self['save_pathInfo']       = self.save_pathInfo
        self['save_mayaInfo']       = self.save_mayaInfo
        self['save_urlInfo']        = self.save_urlInfo
        self['save_appInfo']        = self.save_appInfo
        self['save_plmInfo']        = self.save_plmInfo

    @property
    def auto_changeEmitable(self):
        return self._auto_changeEmmitable

    @property
    def save_configInfo(self):
        return self._save_configInfo

    @property
    def save_deviceInfo(self):
        return self._save_deviceInfo

    @property
    def save_iconInfo(self):
        return self._save_iconInfo

    @property
    def save_pythonInfo(self):
        return self._save_pythonInfo

    @property
    def save_directoryInfo(self):
        return self._save_directoryInfo

    @property
    def save_pathInfo(self):
        return self._save_pathInfo

    @property
    def save_mayaInfo(self):
        return self._save_pathInfo

    @property
    def save_urlInfo(self):
        return self._save_urlInfo

    @property
    def save_appInfo(self):
        return self._save_appInfo

    @property
    def save_plmInfo(self):
        return self._save_plmInfo

    @auto_changeEmitable.setter
    def auto_changeEmitable(self, val):
        self._auto_changeEmmitable  = val

    @save_configInfo.setter
    def save_configInfo(self, val):
        self._save_configInfo       = val

    @save_deviceInfo.setter
    def save_deviceInfo(self, val):
        self._save_deviceInfo       = val

    @save_iconInfo.setter
    def save_iconInfo(self, val):
        self._save_iconInfo         = val

    @save_pythonInfo.setter
    def save_pythonInfo(self, val):
        self._save_pythonInfo       = val

    @save_directoryInfo.setter
    def save_directoryInfo(self, val):
        self._save_directoryInfo    = val

    @save_pathInfo.setter
    def save_pathInfo(self, val):
        self._save_pathInfo         = val

    @save_mayaInfo.setter
    def save_mayaInfo(self, val):
        self._save_pathInfo         = val

    @save_urlInfo.setter
    def save_urlInfo(self, val):
        self._save_urlInfo          = val

    @save_appInfo.setter
    def save_apInfo(self, val):
        self._save_appInfo          = val

    @save_plmInfo.setter
    def save_plmInfo(self, val):
        self._save_plmInfo          = val

class GlobalSetting(object):

    Type                            = 'DAMGGLOBALSETTING'
    key                             = 'PreSetting'
    _name                           = 'DAMG Global Setting'

    cfgable                         = False
    recordLog                       = False
    printOutput                     = True

    def __init__(self):
        super(GlobalSetting, self).__init__()

        self.tracks                 = Tracks()
        self.checks                 = Checks()
        self.modes                  = Modes()
        self.defaults               = DefaultSetting()


globalSetting = GlobalSetting()

try:
    os.getenv(__envKey__)
except KeyError:
    proc = subprocess.Popen(cmd, shell=True).wait()
else:
    if os.getenv(__envKey__)   != ROOT:
        proc = subprocess.Popen(cmd, shell=True).wait()
finally:
    globalSetting.cfgable = True

def __copyright__():
    _copyright = 'Pipeline Manager (PLM) Copyright (C) 2017 - 2020 by DAMGTEAM, contributed by Trinh Do & Duong Minh Duc.'
    if globalSetting.checks.copyright:
        print(_copyright)
    return _copyright

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 6:55 AM
# © 2017 - 2018 DAMGteam. All rights reserved