# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    This is our source code directory, which should be named by your application or package you are working on.
    Inside we have the usual __init__.py file signifying that it's a Python package, next there is __main__.py
    which is used when we want to run our application directly with python -m blueprint. Last source file here
    is the app.py which is here really just for demonstration purposes. In real project instead of this app.py
    you would have few top level source files and more directories (internal packages). We will get to contents
    of these files a little later. Finally, we also have resources directory here, which is used for any static
    content your application might need, e.g. images, keystore, etc.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, subprocess, platform, pkg_resources, json

__envKey__                          = "PLM"

def get_root():
    cwd                             = os.path.abspath(os.getcwd()).replace('\\', '/')
    dirname                         = os.path.basename(cwd)
    if not dirname == __envKey__.lower():
        treeLst                     = cwd.split('/')
        index                       = treeLst.index(__envKey__) + 1
        root                        = '/'.join(treeLst[0:index])
    else:
        root                        = cwd

    return root


def save_data(filePth, data):
    if os.path.exists(filePth):
        os.remove(filePth)
    with open(filePth, 'w+') as f:
        json.dump(data, f, indent=4)
    return True


def install_py_packages(name):
    """
    Install python package via command prompt
    :param name: name of component
    :return:
    """
    # print('Using pip to install %s' % name)
    if os.path.exists(name):
        subprocess.Popen('python %s install' % name)
    else:
        subprocess.Popen('python -m pip install %s --user --upgrade' % name, shell=True).wait()


def __copyright__():
    _copyright = 'Pipeline Manager (PLM) Copyright (C) 2017 - 2020 by DAMGTEAM, contributed by Trinh Do & Duong Minh Duc.'
    if globalSetting.checks.copyright:
        print(_copyright)
    return _copyright


def check_platform():
    if platform.system() == 'Windows':
        return True
    else:
        return False


def check_pkgRequired_win():

    pkgRequired = {

        'pytest'                : '5.3.2',
        'pytest-cov'            : '2.8.1',
        'msgpack'               : '0.6.2',
        'pip'                   : '19.3.1',
        'PyQt5'                 : '5.14.1',
        'PyQtWebEngine'         : '5.14.0',
        'PyQt5-sip'             : '12.7.0',
        'winshell'              : '0.6.0',
        'helpdev'               : '0.6.10',
        'deprecate'             : '1.0.5',
        'argparse'              : '1.4.0',
        'green'                 : '3.1.0',
        'GPUtil'                : '1.4.0',
        'playsound'             : '1.2.2',
        'python-resize-image'   : '1.1.19',
        'WMI'                   : '1.4.9',

    }

    names = [pkg.project_name for pkg in pkg_resources.working_set]
    versions = [pkg.version for pkg in pkg_resources.working_set]
    for pkg, ver in pkgRequired.items():
        pkg_installed           = False
        ver_installed           = False

        for i in range(len(names)):
            name                = names[i]
            if pkg == name:
                pkg_installed   = True
                version         = versions[i]
                if len(version.split('.')) == 2:
                    major       = int(version.split('.')[0])
                    minor       = int(version.split('.')[1])
                    micro       = 0
                else:
                    major       = int(version.split('.')[0])
                    minor       = int(version.split('.')[1])
                    micro       = int(version.split('.')[2])

                v1, v2, v3      = ver.split('.')

                if not major < int(v1) and not minor < int(v2) and not micro < int(v3):
                    ver_installed = True

                break

        if not pkg_installed or not ver_installed:
            install_py_packages(pkg)


class Modes(object):

    key = 'Modes'

    _subprocess                     = True
    _config                         = 'Alpha'
    _login                          = 'Offline'
    _allowOfflineMode               = False

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
        return self._allowOfflineMode

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
        self._allowOfflineMode        = val


class Tracks(object):

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

    _setting                        = False
    _fixKey                         = False
    _deleteKey                      = False

    _configInfo                     = True
    _formatInfo                     = False
    _deviceInfo                     = False
    _iconInfo                       = False
    _pythonInfo                     = False
    _directoryInfo                  = False
    _pthInfo                        = False
    _mayaInfo                       = False
    _urlInfo                        = False
    _appInfo                        = False
    _plmInfo                        = False
    _envInfo                        = False

    @property
    def configInfo(self):
        return self._configInfo

    @property
    def envInfo(self):
        return self._envInfo

    @property
    def formatInfo(self):
        return self._formatInfo

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
    def setting(self):
        return self._setting

    @property
    def fixKey(self):
        return self._fixKey

    @property
    def deleteKey(self):
        return self._deleteKey

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

    @envInfo.setter
    def envInfo(self, val):
        self._envInfo               = val

    @formatInfo.setter
    def formatInfo(self, val):
        self._formatInfo            = val

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
        self._pthInfo               = val

    @mayaInfo.setter
    def mayaInfo(self, val):
        self._pthInfo               = val

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

    @setting.setter
    def setting(self, val):
        self._setting               = val

    @fixKey.setter
    def fixKey(self, val):
        self._fixKey                = val

    @deleteKey.setter
    def deleteKey(self, val):
        self._deleteKey             = val

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
    _actionRegisterError            = False

    def __init__(self):
        dict.__init__(self)

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

    @property
    def actionRegisterError(self):
        return self._actionRegisterError

    @actionRegisterError.setter
    def actionRegisterError(self, val):
        self._actionRegisterError   = val

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
    _save_envInfo                   = True
    _save_formatInfo                = True
    _save_deviceInfo                = True
    _save_iconInfo                  = True
    _save_pythonInfo                = True
    _save_directoryInfo             = True
    _save_pathInfo                  = True
    _save_mayaInfo                  = True
    _save_urlInfo                   = True
    _save_appInfo                   = True
    _save_plmInfo                   = True

    def __init__(self):
        dict.__init__(self)

    @property
    def auto_changeEmitable(self):
        return self._auto_changeEmmitable

    @property
    def save_configInfo(self):
        return self._save_configInfo

    @property
    def save_envInfo(self):
        return self._save_envInfo

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

    @property
    def save_formatInfo(self):
        return self._save_formatInfo

    @auto_changeEmitable.setter
    def auto_changeEmitable(self, val):
        self._auto_changeEmmitable  = val

    @save_configInfo.setter
    def save_configInfo(self, val):
        self._save_configInfo       = val

    @save_envInfo.setter
    def save_envInfo(self, val):
        self._save_envInfo          = val

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
    def save_appInfo(self, val):
        self._save_appInfo          = val

    @save_plmInfo.setter
    def save_plmInfo(self, val):
        self._save_plmInfo          = val

    @save_formatInfo.setter
    def save_formatInfo(self, val):
        self._save_formatInfo       = val


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


globalSetting                       = GlobalSetting()
ROOT                                = get_root()
ROOT_APP                            = os.path.dirname(ROOT)
cmd                                 = 'SetX {0} {1}'.format(__envKey__, ROOT)

if check_platform():
    try:
        os.getenv(__envKey__)
    except KeyError:
        proc = subprocess.Popen(cmd, shell=True).wait()
    else:
        if os.getenv(__envKey__)   != ROOT:
            proc = subprocess.Popen(cmd, shell=True).wait()
    finally:
        globalSetting.cfgable = True
        check_pkgRequired_win()
else:
    print('Sorry, we only work with windows for now.')
    sys.exit()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:15 AM
# © 2017 - 2019 DAMGteam. All rights reserved