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


# -------------------------------------------------------------------------------------------------------------
""" Base Object """


class ObjectGlb(object):

    key                             = 'GlobalSetting'
    Type                            = 'DAMG Global Setting'
    _name                           = 'DAMG Global Setting'
    _copyright                      = __copyright__()

    def __init__(self):
        object.__init__(self)

    @property
    def name(self):
        return self._name

    @property
    def copyright(self):
        return self._copyright


# -------------------------------------------------------------------------------------------------------------
""" Config global """


class ConfigGlb(ObjectGlb):

    _cfgable                        = False

    _printCfgInfo                   = True
    _printPthInfo                   = False
    _printPythonInfo                = False
    _printAppInfo                   = False
    _printDirInfo                   = False
    _printAvatarInfo                = False
    _printLogoInfo                  = False
    _printImgInfo                   = False
    _printIconInfo                  = False
    _printServerInfo                = False
    _printEnvInfo                   = False
    _printUrlInfo                   = False
    _printTypeInfo                  = False
    _printFmtInfo                   = False
    _printPlmInfo                   = False
    _printPcInfo                    = False
    _printSettingInfo               = False
    _printSignalReceive             = False

    _saveCfgInfo                    = True
    _savePthInfo                    = True
    _savePythonInfo                 = True
    _saveAppInfo                    = True
    _saveDirInfo                    = True
    _saveAvatarInfo                 = True
    _saveLogoInfo                   = True
    _saveImgInfo                    = True
    _saveIconInfo                   = True
    _saveServerInfo                 = True
    _saveEnvInfo                    = True
    _saveUrlInfo                    = True
    _saveTypeInfo                   = True
    _saveFmtInfo                    = True
    _savePlmInfo                    = True
    _savePcInfo                     = True

    def __init__(self):
        ObjectGlb.__init__(self)


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

    @property
    def printLogoInfo(self):
        return self._printLogoInfo

    @property
    def saveLogoInfo(self):
        return self._saveLogoInfo

    @property
    def printImgInfo(self):
        return self._printImgInfo

    @property
    def saveImgInfo(self):
        return self._saveImgInfo

    @property
    def printIconInfo(self):
        return self._printIconInfo

    @property
    def printEnvInfo(self):
        return self._printEnvInfo

    @property
    def saveEnvInfo(self):
        return self._saveEnvInfo

    @property
    def printServerInfo(self):
        return self._printServerInfo

    @property
    def saveServerInfo(self):
        return self._saveServerInfo

    @property
    def printUrlInfo(self):
        return self._printUrlInfo

    @property
    def saveUrlInfo(self):
        return self._saveUrlInfo

    @property
    def printTypeInfo(self):
        return self._printTypeInfo

    @property
    def saveTypeInfo(self):
        return self._saveTypeInfo

    @property
    def printFmtInfo(self):
        return self._printFmtInfo

    @property
    def saveFmtInfo(self):
        return self._saveFmtInfo

    @property
    def printPlmInfo(self):
        return self._printPlmInfo

    @property
    def savePlmInfo(self):
        return self._savePlmInfo

    @property
    def printPcInfo(self):
        return self._printPcInfo

    @property
    def savePcInfo(self):
        return self._savePcInfo

    @property
    def saveIconInfo(self):
        return self._saveIconInfo

    @property
    def printSettingInfo(self):
        return self._printSettingInfo

    @property
    def printSignalReceive(self):
        return self._printSignalReceive

    @printSignalReceive.setter
    def printSignalReceive(self, val):
        self._printSignalReceive    = val
    
    @printSettingInfo.setter
    def printSettingInfo(self, val):
        self._printSettingInfo      = val

    @saveIconInfo.setter
    def saveIconInfo(self, val):
        self._saveIconInfo          = val

    @savePcInfo.setter
    def savePcInfo(self, val):
        self._savePcInfo            = val

    @printPcInfo.setter
    def printPcInfo(self, val):
        self._printPcInfo           = val

    @savePlmInfo.setter
    def savePlmInfo(self, val):
        self._savePlmInfo           = val

    @printPlmInfo.setter
    def printPlmInfo(self, val):
        self._printPlmInfo          = val

    @saveFmtInfo.setter
    def saveFmtInfo(self, val):
        self._saveFmtInfo           = val

    @printFmtInfo.setter
    def printFmtInfo(self, val):
        self._printFmtInfo          = val

    @saveTypeInfo.setter
    def saveTypeInfo(self, val):
        self._saveTypeInfo          = val

    @printTypeInfo.setter
    def printTypeInfo(self, val):
        self._printTypeInfo         = val

    @saveUrlInfo.setter
    def saveUrlInfo(self, val):
        self._saveUrlInfo           = val

    @printUrlInfo.setter
    def printUrlInfo(self, val):
        self._printUrlInfo          = val

    @saveServerInfo.setter
    def saveServerInfo(self, val):
        self._saveServerInfo        = val

    @printServerInfo.setter
    def printServerInfo(self, val):
        self._printServerInfo       = val

    @saveEnvInfo.setter
    def saveEnvInfo(self, val):
        self._saveEnvInfo           = val

    @printEnvInfo.setter
    def printEnvInfo(self, val):
        self._printEnvInfo          = val

    @printIconInfo.setter
    def printIconInfo(self, val):
        self._printIconInfo         = val

    @saveImgInfo.setter
    def saveImgInfo(self, val):
        self._saveImgInfo           = val

    @printImgInfo.setter
    def printImgInfo(self, val):
        self._printImgInfo          = val

    @saveLogoInfo.setter
    def saveLogoInfo(self, val):
        self._saveLogoInfo          = val

    @printLogoInfo.setter
    def printLogoInfo(self, val):
        self._printLogoInfo         = val

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


# -------------------------------------------------------------------------------------------------------------
""" Mode global """


class ModesGlb(ConfigGlb):

    _allowLocalMode                 = False

    def __init__(self):
        ConfigGlb.__init__(self)

    @property
    def allowLocalMode(self):
        return self._allowLocalMode

    @allowLocalMode.setter
    def allowLocalMode(self, val):
        self._allowLocalMode        = val


# -------------------------------------------------------------------------------------------------------------
""" Error global """


class ErrorsGlb(ModesGlb):

    _allowAllErrors                 = True
    _actionRegisterError            = True

    def __init__(self):
        ModesGlb.__init__(self)


    @property
    def allowAllErrors(self):
        return self._allowAllErrors

    @property
    def actionRegisterError(self):
        return self._actionRegisterError

    @actionRegisterError.setter
    def actionRegisterError(self, val):
        self._actionRegisterError   = val

    @allowAllErrors.setter
    def allowAllErrors(self, val):
        self._allowAllErrors        = val


# -------------------------------------------------------------------------------------------------------------
""" Signal global """


class SignalGlb(ErrorsGlb):

    _emittable                      = False
    _autoChangeEmittable            = True

    def __init__(self):
        ErrorsGlb.__init__(self)

    @property
    def emittable(self):
        return self._emittable

    @property
    def autoChangeEmittable(self):
        return self._autoChangeEmittable

    @autoChangeEmittable.setter
    def autoChangeEmittable(self, val):
        self._autoChangeEmittable   = val

    @emittable.setter
    def emittable(self, val):
        self._emittable             = val


# -------------------------------------------------------------------------------------------------------------
""" Setting global """


class GlobalBase(SignalGlb):

    def __init__(self):
        SignalGlb.__init__(self)


# -------------------------------------------------------------------------------------------------------------


class GlobalSetting(GlobalBase):

    def __init__(self):
        GlobalBase.__init__(self)


globalSetting                       = GlobalSetting()
ROOT_APP                            = get_root()
ROOT                                = os.path.join(ROOT_APP, __envKey__)
cmd                                 = 'SetX {0} {1}'.format(__envKey__, ROOT)


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