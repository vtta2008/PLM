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
import os
import subprocess
import json
import yaml
import pprint

# -------------------------------------------------------------------------------------------------------------
""" Metadatas """


__envKey__                          = "PLM"
__appName__                         = "Pipeline Manager (PLM)"
__name__                            = __appName__
__file__                            = __appName__

__majorVersion__                    = "13"
__minorVersion__                    = "0"
__microVersion__                    = "1"


# -------------------------------------------------------------------------------------------------------------
""" Global functions """


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


def __copyright__():
    return 'Pipeline Manager (PLM) Copyright (C) 2017 - 2020 by DAMGTEAM, contributed by Trinh Do & Duong Minh Duc.'


# -------------------------------------------------------------------------------------------------------------
""" Build Version """


class BaseTuple(tuple):

    Type                                = 'DAMGTUPLE'
    key                                 = 'BaseTuple'
    _name                               = 'DAMG Base Tuple'
    _copyright                          = __copyright__()

    def __new__(cls, *args):
        cls.args = args

        return tuple.__new__(BaseTuple, tuple(cls.args))

    def __bases__(self):
        return tuple(BaseTuple, tuple(self.args))

    def __call__(self):

        """ Make object callable """

        if isinstance(self, object):
            return True
        else:
            return False

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName



class VersionTuple(BaseTuple):

    key                                 = 'VersionTuple'

    def __init__(self, *args, **kwargs):
        BaseTuple.__new__(self)

        self.metadata                   = kwargs
        self.args                       = args



class VersionInfo(VersionTuple):


    Type                            = 'DAMGVERSIONINFO'
    key                             = '__version_info__'


    def __new__(self):

        self._MAJOR                 = __majorVersion__
        self._MINOR                 = __minorVersion__
        self._MICRO                 = __microVersion__

        return tuple.__new__(VersionInfo, (self._MAJOR, self._MINOR, self._MICRO))

    def __bases__(self):
        return tuple(VersionInfo, tuple(self.major_version, self.minor_version, self.micro_version))

    @property
    def major_version(self):
        return self._MAJOR

    @property
    def minor_version(self):
        return self._MINOR

    @property
    def micro_version(self):
        return self._MINOR

    @major_version.setter
    def major_version(self, newVal):
        self._MAJOR = newVal

    @minor_version.setter
    def minor_version(self, newVal):
        self._MINOR = newVal

    @micro_version.setter
    def micro_version(self, newVal):
        self._MINOR = newVal



version_info = VersionInfo()



version_construct_class = dict(

    __version_info__                = version_info,
    __doc__                         = 'PLM documentations',
    __name__                        = 'version',
    __module__                      = 'PLM',
    __type__                        = 'version: {0}'.format('.'.join(str(i) for i in version_info)),
    __str__                         = '.'.join(str(i) for i in version_info)

)



class VersionType(type):

    key                             = 'VersionType'
    Type                            = 'DamgVersion'

    _step                           = 1
    _majo_step                      = 1
    _mino_step                      = 1
    _micro_step                     = 1

    def __new__(cls, *args, **kwargs):
        newType = type.__new__(VersionType, 'version', (VersionType,), version_construct_class)
        return newType

    def __init__(self):
        self.__new__()
        super(VersionType, self).__init__(self, VersionType)

    def increase_majo_step(self):
        return self._majo_step + self._step

    def increase_mino_step(self):
        return self._mino_step + self._step

    def increase_micro_step(self):
        return self._micro_step + self._step

    def __bases__(cls):
        return type.__new__(VersionType, 'version', (VersionType,), version_construct_class)

    def __str__(self):
        return self.__str__

    def __repr__(self):
        return self.__str__

    def __call__(self):
        return isinstance(self, type)

    @property
    def step(self):
        return self._step

    @property
    def majo_step(self):
        return self._majo_step

    @property
    def mino_step(self):
        return self._mino_step

    @property
    def micro_step(self):
        return self._micro_step

    @majo_step.setter
    def majo_step(self, val):
        self._majo_step             = val

    @mino_step.setter
    def mino_step(self, val):
        self._mino_step             = val

    @micro_step.setter
    def micro_step(self, val):
        self._micro_step            = val

    @step.setter
    def step(self, val):
        self._step                  = val


    __version__                 = '.'.join(str(i) for i in version_info)

    __qualname__                = 'version'



class Version(VersionType):

    key                         = 'version'

    def __init__(self, major, minor, micro):
        super(Version, self).__init__()

        assert(isinstance(major, int))
        assert(isinstance(minor, int))
        assert(isinstance(micro, int))

        self._major             = major
        self._minor             = minor
        self._micro             = micro

    @staticmethod
    def fromString(string):
        major, minor, micro     = string.split('.')
        return Version(int(major), int(minor), int(micro))

    def __str__(self):
        return '{0}.{1}.{2}'.format(self.major, self.minor, self.micro)

    def __eq__(self, other):
        return all([self.major == other.major,
                    self.minor == other.minor,
                    self.micro == other.micro])

    def __ge__(self, other):
        lhs = int("".join([str(self.major), str(self.minor), str(self.micro)]))
        rhs = int("".join([str(other.major), str(other.minor), str(other.micro)]))
        return lhs >= rhs

    def __gt__(self, other):
        lhs = int("".join([str(self.major), str(self.minor), str(self.micro)]))
        rhs = int("".join([str(other.major), str(other.minor), str(other.micro)]))
        return lhs >= rhs

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def micro(self):
        return self._micro



__version__ = Version(__majorVersion__, __minorVersion__, __microVersion__)


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
    _cfgAll                         = False

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
    _printFontInfo                  = False

    _saveFontInfo                   = True
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

    @property
    def printFontInfo(self):
        return self._printFontInfo

    @property
    def saveFontInfo(self):
        return self._saveFontInfo

    @property
    def cfgAll(self):
        return self._cfgAll

    @cfgAll.setter
    def cfgAll(self, val):
        self._cfgAll                = val

    @saveFontInfo.setter
    def saveFontInfo(self, val):
        self._saveFontInfo          = val

    @printFontInfo.setter
    def printFontInfo(self, val):
        self._printFontInfo         = val

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

    _allModeSwitchAble                          = True
    _switchQtBindingMode                        = False
    _switchLoginMode                            = False
    _switchDataTypeSavingMode                   = False
    _switchSplashLoadingMode                    = False

    _allowLocalMode                             = False

    _qtBindingMode                              = 'PyQt5'
    _dataTypeSaving                             = 'json'
    _splashLoadingMode                          = 'progress'

    loadingMode                                 = ['loading', 'progress']
    bindingMode                                 = ['PyQt5', 'PySide2']
    savingMode                                  = ['json', 'yaml']

    def __init__(self):
        ConfigGlb.__init__(self)

    @property
    def allowLocalMode(self):
        return self._allowLocalMode

    @property
    def qtBindingMode(self):
        return self._qtBindingMode

    @property
    def switchQtBindingMode(self):
        return self._switchQtBindingMode

    @property
    def switchLoginMode(self):
        return self._switchLoginMode

    @property
    def switchDataTypeSavingMode(self):
        return self._switchDataTypeSavingMode

    @property
    def dataTypeSaving(self):
        return self._dataTypeSaving

    @property
    def splashLoadingMode(self):
        return self._splashLoadingMode

    @property
    def switchSplashLoadingMode(self):
        return self._switchSplashLoadingMode

    @property
    def allModeSwitchAble(self):
        return self._allModeSwitchAble

    @allModeSwitchAble.setter
    def allModeSwitchAble(self, val):
        self._allModeSwitchAble                 = val

    @switchSplashLoadingMode.setter
    def switchSplashLoadingMode(self, val):
        self._switchSplashLoadingMode           = val

    @splashLoadingMode.setter
    def splashLoadingMode(self, val):
        if self.allModeSwitchAble and self.switchSplashLoadingMode:
            if val in self.loadingMode:
                self._splashLoadingMode         = val

    @dataTypeSaving.setter
    def dataTypeSaving(self, val):
        if self.allModeSwitchAble and self.switchDataTypeSavingMode:
            if val in self.savingMode:
                self._dataTypeSaving        = val

    @switchDataTypeSavingMode.setter
    def switchDataTypeSavingMode(self, val):
        self._switchDataTypeSavingMode          = val

    @switchLoginMode.setter
    def switchLoginMode(self, val):
        self._switchLoginMode                   = val

    @switchQtBindingMode.setter
    def switchQtBindingMode(self, val):
        self._switchQtBindingMode               = val

    @qtBindingMode.setter
    def qtBindingMode(self, val):
        if self.allModeSwitchAble and self.switchQtBindingMode:
            if val in self.bindingMode:
                self._qtBindingMode             = val

    @allowLocalMode.setter
    def allowLocalMode(self, val):
        if self.allModeSwitchAble and self.switchLoginMode:
            self._allowLocalMode                = val


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
    _trackRecieveSignal             = False
    _trackBlockSignal               = False
    _trackCommand                   = False
    _trackRegistLayout              = False

    def __init__(self):
        ErrorsGlb.__init__(self)

    @property
    def emittable(self):
        return self._emittable

    @property
    def autoChangeEmittable(self):
        return self._autoChangeEmittable

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

    @trackRegistLayout.setter
    def trackRegistLayout(self, val):
        self._trackRegistLayout     = val

    @trackCommand.setter
    def trackCommand(self, val):
        self._trackCommand          = val

    @trackBlockSignal.setter
    def trackBlockSignal(self, val):
        self._trackBlockSignal      = val

    @trackRecieveSignal.setter
    def trackRecieveSignal(self, val):
        self._trackRecieveSignal    = val

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

    def setCfgAll(self, val):
        self._cfgAll                = val


# -------------------------------------------------------------------------------------------------------------


class GlobalSetting(GlobalBase):

    def __init__(self):
        GlobalBase.__init__(self)


globalSetting                       = GlobalSetting()
ROOT_APP                            = get_root()
ROOT                                = os.path.join(ROOT_APP, __envKey__)
cmd                                 = 'SetX {0} {1}'.format(__envKey__, ROOT)


class Cfg(dict):

    key                             = 'ConfigBase'
    _filePath                       = None

    def __init__(self):
        dict.__init__(self)

        self.update()

    def save_data(self):
        if not self.filePath:
            return

        if os.path.exists(self.filePath):
            os.remove(self.filePath)
        with open(self.filePath, 'w+') as f:
            if globalSetting.dataTypeSaving == 'json':
                json.dump(self, f, indent=4)
            elif globalSetting.dataTypeSaving == 'yaml':
                yaml.dump(self, f, default_flow_style=False)
            else:
                # will update more data type library later if need
                pass
        return True

    def pprint(self):
        return pprint.pprint(self)

    def add(self, key, value):
        self[key]                   = value

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, val):
        self._filePath              = val

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