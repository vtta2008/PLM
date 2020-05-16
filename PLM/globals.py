# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """


class ObjectGlb(object):

    key                                 = 'GlobalSetting'
    Type                                = 'DAMG Global Setting'
    _name                               = 'DAMG Global Setting'
    _copyright                          = 'Copyright (C) DAMGTEAM.'

    _cfgable = False
    _cfgAll = False

    def __init__(self):
        object.__init__(self)

    @property
    def name(self):
        return self._name

    @property
    def copyright(self):
        return self._copyright

    @property
    def cfgable(self):
        return self._cfgable

    @property
    def cfgAll(self):
        return self._cfgAll

    @cfgAll.setter
    def cfgAll(self, val):
        self._cfgAll                    = val

    @cfgable.setter
    def cfgable(self, val):
        self._cfgable                   = val


# -------------------------------------------------------------------------------------------------------------
""" Config global """


class reportGlb(ObjectGlb):

    _printCfgInfo                       = True
    _printPthInfo                       = False
    _printPythonInfo                    = False
    _printAppInfo                       = False
    _printDirInfo                       = False
    _printAvatarInfo                    = False
    _printLogoInfo                      = False
    _printImgInfo                       = False
    _printIconInfo                      = False
    _printServerInfo                    = False
    _printEnvInfo                       = False
    _printUrlInfo                       = False
    _printTypeInfo                      = False
    _printFmtInfo                       = False
    _printPlmInfo                       = False
    _printPcInfo                        = False
    _printSettingInfo                   = False
    _printSignalReceive                 = False
    _printFontInfo                      = False

    def __init__(self):
        ObjectGlb.__init__(self)

    @property
    def printCfgInfo(self):
        return self._printCfgInfo

    @property
    def printPthInfo(self):
        return self._printPthInfo

    @property
    def printPythonInfo(self):
        return self._printPythonInfo

    @property
    def printAppInfo(self):
        return self._printAppInfo

    @property
    def printDirInfo(self):
        return self._printDirInfo

    @property
    def printAvatarInfo(self):
        return self._printAvatarInfo

    @property
    def printLogoInfo(self):
        return self._printLogoInfo

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
    def printUrlInfo(self):
        return self._printUrlInfo

    @property
    def printTypeInfo(self):
        return self._printTypeInfo

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
    def printPcInfo(self):
        return self._printPcInfo

    @property
    def printSettingInfo(self):
        return self._printSettingInfo

    @property
    def printSignalReceive(self):
        return self._printSignalReceive

    @property
    def printFontInfo(self):
        return self._printFontInfo

    @printFontInfo.setter
    def printFontInfo(self, val):
        self._printFontInfo = val

    @printSignalReceive.setter
    def printSignalReceive(self, val):
        self._printSignalReceive        = val

    @printSettingInfo.setter
    def printSettingInfo(self, val):
        self._printSettingInfo          = val

    @printPcInfo.setter
    def printPcInfo(self, val):
        self._printPcInfo               = val

    @printPlmInfo.setter
    def printPlmInfo(self, val):
        self._printPlmInfo              = val

    @saveFmtInfo.setter
    def saveFmtInfo(self, val):
        self._saveFmtInfo               = val

    @printFmtInfo.setter
    def printFmtInfo(self, val):
        self._printFmtInfo              = val

    @printTypeInfo.setter
    def printTypeInfo(self, val):
        self._printTypeInfo             = val

    @printUrlInfo.setter
    def printUrlInfo(self, val):
        self._printUrlInfo              = val

    @printServerInfo.setter
    def printServerInfo(self, val):
        self._printServerInfo           = val

    @saveEnvInfo.setter
    def saveEnvInfo(self, val):
        self._saveEnvInfo               = val

    @printEnvInfo.setter
    def printEnvInfo(self, val):
        self._printEnvInfo              = val

    @printIconInfo.setter
    def printIconInfo(self, val):
        self._printIconInfo             = val

    @saveImgInfo.setter
    def saveImgInfo(self, val):
        self._saveImgInfo               = val

    @printImgInfo.setter
    def printImgInfo(self, val):
        self._printImgInfo              = val

    @printLogoInfo.setter
    def printLogoInfo(self, val):
        self._printLogoInfo             = val

    @printAvatarInfo.setter
    def printAvatarInfo(self, val):
        self._printAvatarInfo           = val

    @printDirInfo.setter
    def printDirInfo(self, val):
        self._printDirInfo              = val

    @printAppInfo.setter
    def printAppInfo(self, val):
        self.printAppInfo               = val

    @printPythonInfo.setter
    def printPythonInfo(self, val):
        self._printPythonInfo           = val

    @printPthInfo.setter
    def printPthInfo(self, val):
        self._printPthInfo              = val

    @printCfgInfo.setter
    def printCfgInfo(self, val):
        self._printCfgInfo              = val


class RecordGlb(reportGlb):

    _saveFontInfo                       = True
    _saveCfgInfo                        = True
    _savePthInfo                        = True
    _savePythonInfo                     = True
    _saveAppInfo                        = True
    _saveDirInfo                        = True
    _saveAvatarInfo                     = True
    _saveLogoInfo                       = True
    _saveImgInfo                        = True
    _saveIconInfo                       = True
    _saveServerInfo                     = True
    _saveEnvInfo                        = True
    _saveUrlInfo                        = True
    _saveTypeInfo                       = True
    _saveFmtInfo                        = True
    _savePlmInfo                        = True
    _savePcInfo                         = True

    def __init__(self):
        reportGlb.__init__(self)

    @property
    def saveServerInfo(self):
        return self._saveServerInfo

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
    def saveAppInfo(self):
        return self._saveAppInfo

    @property
    def saveDirInfo(self):
        return self._saveDirInfo

    @property
    def saveAvatarInfo(self):
        return self._saveAvatarInfo

    @property
    def saveLogoInfo(self):
        return self._saveLogoInfo

    @property
    def saveUrlInfo(self):
        return self._saveUrlInfo

    @property
    def saveTypeInfo(self):
        return self._saveTypeInfo

    @property
    def savePlmInfo(self):
        return self._savePlmInfo

    @property
    def savePcInfo(self):
        return self._savePcInfo

    @property
    def saveIconInfo(self):
        return self._saveIconInfo

    @property
    def saveFontInfo(self):
        return self._saveFontInfo

    @saveFontInfo.setter
    def saveFontInfo(self, val):
        self._saveFontInfo              = val

    @saveLogoInfo.setter
    def saveLogoInfo(self, val):
        self._saveLogoInfo              = val

    @saveAvatarInfo.setter
    def saveAvatarInfo(self, val):
        self._saveAvatarInfo            = val

    @saveDirInfo.setter
    def saveDirInfo(self, val):
        self._saveDirInfo               = val

    @saveAppInfo.setter
    def saveAppInfo(self, val):
        self._saveAppInfo               = val

    @saveIconInfo.setter
    def saveIconInfo(self, val):
        self._saveIconInfo              = val

    @savePcInfo.setter
    def savePcInfo(self, val):
        self._savePcInfo                = val

    @savePlmInfo.setter
    def savePlmInfo(self, val):
        self._savePlmInfo               = val

    @saveTypeInfo.setter
    def saveTypeInfo(self, val):
        self._saveTypeInfo              = val

    @saveUrlInfo.setter
    def saveUrlInfo(self, val):
        self._saveUrlInfo               = val

    @saveServerInfo.setter
    def saveServerInfo(self, val):
        self._saveServerInfo            = val

    @savePythonInfo.setter
    def savePythonInfo(self, val):
        self._savePythonInfo            = val

    @savePthInfo.setter
    def savePthInfo(self, val):
        self._savePthInfo               = val

    @saveCfgInfo.setter
    def saveCfgInfo(self, val):
        self._saveCfgInfo               = val


# -------------------------------------------------------------------------------------------------------------
""" Mode global """


class ModesGlb(RecordGlb):

    _qtBindingMode                      = 'PyQt5'
    _qtVersion                          = '5.14.1'
    _dataTypeSaving                     = 'json'

    loading_options                     = ['loading', 'progress']
    binding_options                     = ['PyQt5', 'PySide2']
    saving_options                      = ['json', 'yaml']

    def __init__(self):
        RecordGlb.__init__(self)

    @property
    def qtBindingMode(self):
        return self._qtBindingMode

    @property
    def dataTypeSaving(self):
        return self._dataTypeSaving

    @property
    def qtVersion(self):
        return self._qtVersion

    @qtVersion.setter
    def qtVersion(self, val):
        self._qtVersion                 = val

    @dataTypeSaving.setter
    def dataTypeSaving(self, val):
        if val in self.saving_options:
            self._dataTypeSaving        = val

    @qtBindingMode.setter
    def qtBindingMode(self, val):
        if val in self.qtBindingMode:
            self._qtBindingMode         = val


# -------------------------------------------------------------------------------------------------------------
""" Error global """


class ErrorsGlb(ModesGlb):

    _allowAllErrors = True
    _actionRegisterError = True

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
        self._actionRegisterError       = val

    @allowAllErrors.setter
    def allowAllErrors(self, val):
        self._allowAllErrors            = val


# -------------------------------------------------------------------------------------------------------------
""" Signal global """


class SignalGlb(ErrorsGlb):

    _emittable = False
    _autoChangeEmittable = True
    _trackRecieveSignal = False
    _trackBlockSignal = False
    _trackCommand = False
    _trackRegistLayout = False

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
        self._trackRegistLayout = val

    @trackCommand.setter
    def trackCommand(self, val):
        self._trackCommand = val

    @trackBlockSignal.setter
    def trackBlockSignal(self, val):
        self._trackBlockSignal = val

    @trackRecieveSignal.setter
    def trackRecieveSignal(self, val):
        self._trackRecieveSignal = val

    @autoChangeEmittable.setter
    def autoChangeEmittable(self, val):
        self._autoChangeEmittable = val

    @emittable.setter
    def emittable(self, val):
        self._emittable = val


# -------------------------------------------------------------------------------------------------------------
""" Setting global """


class GlobalBase(SignalGlb):

    def __init__(self):
        SignalGlb.__init__(self)

    def setCfgAll(self, val):
        self._cfgAll = val


# -------------------------------------------------------------------------------------------------------------


class Global(GlobalBase):

    def __init__(self):
        GlobalBase.__init__(self)


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved