# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM                        import glbSettings
from .baseConfigs               import Pys, Urls, Lgs, Fnts, Dirs, Pths, Ics, Apps, Sts, Fmts, Uis



class ConfigDirs(Dirs):


    key                             = 'ConfigDirs'


    def __init__(self):
        super(ConfigDirs, self).__init__()

        self.__dict__.update()

        if glbSettings.printCfgInfo:
            if glbSettings.printDirInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveDirInfo:
                self.save_data()



class ConfigPths(Pths):

    key                             = 'ConfigPths'

    def __init__(self):
        super(ConfigPths, self).__init__()

        self.__dict__.update()

        if glbSettings.printCfgInfo:
            if glbSettings.printPthInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.savePthInfo:
                self.save_data()



class ConfigIcons(Ics):

    key                                 = 'ConfigIcons'

    def __init__(self):
        super(ConfigIcons, self).__init__()

        if glbSettings.printCfgInfo:
            if glbSettings.printIconInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveIconInfo:
                self.save_data()



class ConfigApps(Apps):

    key                         = 'ConfigApps'

    def __init__(self):
        super(ConfigApps, self).__init__()

        if glbSettings.printCfgInfo:
            if glbSettings.printAppInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveAppInfo:
                self.save_data()



class ConfigPython(Pys):

    key                         = 'ConfigPython'

    def __init__(self):
        super(ConfigPython, self).__init__()


        if glbSettings.printCfgInfo:
            if glbSettings.printPythonInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.savePythonInfo:
                self.save_data()



class ConfigUrls(Urls):

    key                             = 'ConfigUrls'

    def __init__(self):
        super(ConfigUrls, self).__init__()

        if glbSettings.printCfgInfo:
            if glbSettings.printUrlInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveUrlInfo:
                self.save_data()



class ConfigLogos(Lgs):

    key                                 = 'ConfigLogos'

    def __init__(self):
        super(ConfigLogos, self).__init__()

        if glbSettings.printCfgInfo:
            if glbSettings.printAvatarInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveAvatarInfo:
                self.save_data()



class ConfigFonts(Fnts):

    key                                 = 'ConfigFonts'

    def __init__(self):
        super(ConfigFonts, self).__init__()

        if glbSettings.printCfgInfo:
            if glbSettings.printFontInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveFontInfo:
                self.save_data()



class ConfigSettings(Sts):

    key                                 = 'ConfigSettings'

    def __iter__(self):
        super(ConfigSettings, self).__iter__()

        if glbSettings.printCfgInfo:
            if glbSettings.printSettingInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveSettingInfo:
                self.save_data()



class ConfigFormats(Fmts):

    key                                 = 'ConfigFormats'

    def __iter__(self):
        super(ConfigFormats, self).__iter__()

        if glbSettings.printCfgInfo:
            if glbSettings.printFmtInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveFmtInfo:
                self.save_data()


class ConfigUiKeys(Uis):

    key                                 = 'ConfigUiKeys'

    def __iter__(self):
        super(ConfigUiKeys, self).__iter__()

        self.__dict__.update()

        if glbSettings.printCfgInfo:
            if glbSettings.printUiKeyInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveUiKeyInfo:
                self.save_data()

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved