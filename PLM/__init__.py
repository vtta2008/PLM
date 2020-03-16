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
import os, subprocess, json

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

def __copyright__():
    return 'Pipeline Manager (PLM) Copyright (C) 2017 - 2020 by DAMGTEAM, contributed by Trinh Do & Duong Minh Duc.'

ROOT_APP                            = get_root()
ROOT                                = os.path.join(ROOT_APP, __envKey__)
cmd                                 = 'SetX {0} {1}'.format(__envKey__, ROOT)


class SettingsRequired(object):

    _cfgable                        = False

    _printCfgInfo                   = True
    _printPthInfo                   = False
    _printPythonInfo                = False
    _printAppInfo                   = False
    _printDirInfo                   = False
    _printAvatarInfo                = False

    _saveCfgInfo                    = True
    _savePthInfo                    = False
    _savePythonInfo                 = False
    _saveAppInfo                    = False
    _saveDirInfo                    = False
    _saveAvatarInfo                 = False

    def __init__(self):
        object.__init__(self)


    @property
    def printCfgInfo(self):
        return self._printCfgInfo

    @property
    def cfgable(self):
        return self._cfgable

    @property
    def printPthInfo(self):
        return self._printPthInfo

    @property
    def printPythonInfo(self):
        return self._printPythonInfo

    @property
    def saveCfgInfo(self):
        return self._saveCfgInfo

    @property
    def savePthInfo(self):
        return self._savePthInfo

    @property
    def savePythonInfo(self):
        return self._savePythonInfo

    @property
    def printAppInfo(self):
        return self._printAppInfo

    @property
    def saveAppInfo(self):
        return self._saveAppInfo

    @property
    def printDirInfo(self):
        return self._printDirInfo

    @property
    def saveDirInfo(self):
        return self._saveDirInfo

    @property
    def printAvatarInfo(self):
        return self._printAvatarInfo

    @property
    def saveAvatarInfo(self):
        return self._saveAvatarInfo

    @saveAvatarInfo.setter
    def saveAvatarInfo(self, val):
        self._saveAvatarInfo        = val


    @printAvatarInfo.setter
    def printAvatarInfo(self, val):
        self._printAvatarInfo       = val

    @saveDirInfo.setter
    def saveDirInfo(self, val):
        self._saveDirInfo           = val

    @printDirInfo.setter
    def printDirInfo(self, val):
        self._printDirInfo          = val

    @saveAppInfo.setter
    def saveAppInfo(self, val):
        self._saveAppInfo           = val

    @printAppInfo.setter
    def printAppInfo(self, val):
        self.printAppInfo           = val

    @savePythonInfo.setter
    def savePythonInfo(self, val):
        self._savePythonInfo        = val

    @savePthInfo.setter
    def savePthInfo(self, val):
        self._savePthInfo           = val

    @saveCfgInfo.setter
    def saveCfgInfo(self, val):
        self._saveCfgInfo           = val

    @printPythonInfo.setter
    def printPythonInfo(self, val):
        self._printPythonInfo       = val

    @printPthInfo.setter
    def printPthInfo(self, val):
        self._printPthInfo          = val

    @printCfgInfo.setter
    def printCfgInfo(self, val):
        self._printCfgInfo          = val

    @cfgable.setter
    def cfgable(self, val):
        self._cfgable               = val


class GlobalBase(SettingsRequired):

    key                             = 'GlobalSetting'
    Type                            = 'DAMG Global Setting'
    _name                           = 'DAMG Global Setting'
    _copyright                      = __copyright__()

    def __init__(self):
        super(GlobalBase, self).__init__()

    @property
    def name(self):
        return self._name

    @property
    def copyright(self):
        return self._copyright



class GlobalSetting(GlobalBase):

    def __init__(self):
        super(GlobalSetting, self).__init__()


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



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:15 AM
# © 2017 - 2019 DAMGteam. All rights reserved