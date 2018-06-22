# -*- coding: utf-8 -*-
"""

Script Name: util.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import winshell, os, json

from appData._meta import __plmWiki__, __envKey__
from appData._keys import KEYDETECT
from appData._keys import KEYPACKAGE, CONFIG_SYSTRAY, CONFIG_APPUI
from appData._path import DAMGLOGO, PLMLOGO, ICONDIR32, pyEnvCfg, mainConfig, appIconCfg, webIconCfg, appConfig

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

from sys import argv
from appData.Loggers import SetLogger
logger = SetLogger()

# -------------------------------------------------------------------------------------------------------------
""" Collecting all info. """

class LocalCfg(object):
    """
    Initialize the main class functions
    :param package: the package of many information stored from default variable
    :param names: the dictionary of names stored from default variable
    :returns: all installed app info, package app info, icon info, image info, pc info.

    """

    def __init__(self):

        super(LocalCfg, self).__init__()

        self.collect_env_variables()
        self.collect_icon_path()
        self.collect_all_app()
        self.collect_main_app()

    def collect_env_variables(self):
        envKeys = {}
        for key in os.environ.keys():
            envKeys[key] = os.getenv(key)
        self.create_config_file('envKeys', envKeys)

    def collect_icon_path(self):
        # Create dictionary for icon info
        self.iconInfo = {}
        self.iconInfo['Logo'] = PLMLOGO
        self.iconInfo['DAMG'] = DAMGLOGO
        # Custom some info to debug
        self.iconInfo['Sep'] = 'separato.png'
        self.iconInfo['File'] = 'file.png'
        # Get list of icons in imgage folder
        iconlst = [i for i in self.get_file_path(ICONDIR32) if i.endswith(".png")]

        for i in iconlst:
            self.iconInfo[os.path.basename(i).split('.icon')[0]] = i

        self.create_config_file('icon', self.iconInfo)

    def collect_all_app(self):
        """
        It will find and put all the info of installed apps to two list: appname and path
        return: self.appName, self.appPath
        """
        shortcuts = {}
        appName = []
        appPth = []

        all_programs = winshell.programs(common=1)

        for dirpath, dirnames, filenames in os.walk(all_programs):
            relpath = dirpath[1 + len(all_programs):]
            shortcuts.setdefault(relpath, []).extend([winshell.shortcut(os.path.join(dirpath, f)) for f in filenames])
        for relpath, lnks in sorted(shortcuts.items()):
            for lnk in lnks:
                name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
                appName.append(name)
                appPth.append(lnk.path)

        self.appInfo = {}

        for name in appName:
            self.appInfo[str(name)] = str(appPth[appName.index(name)])

        self.create_config_file("app", self.appInfo)

    def collect_main_app(self):

        self.mainInfo = {}

        delKeys = []
        for key in self.appInfo:
            for k in KEYDETECT:
                if k in key:
                    delKeys.append(key)

        for key in delKeys:
            self.del_key(key, self.appInfo)

        keepKeys = [k for k in KEYPACKAGE if k in self.appInfo and k in self.iconInfo]

        # Custom functions
        self.mainInfo['About'] = ['About PLM', self.iconInfo['About'], 'About']
        self.mainInfo['Exit'] = ['Exit Pipeline Tool', self.iconInfo['Exit'], 'Exit']
        self.mainInfo['CleanPyc'] = ['Clean ".pyc" files', self.iconInfo['CleanPyc'], 'CleanPyc']
        self.mainInfo['ClearData'] = ['Clean Config data', self.iconInfo['CleanConfig'], 'CleanConfigData']
        self.mainInfo['ReConfig'] = ['Re configuring data', self.iconInfo['Reconfig'], 'Re Config']
        self.mainInfo['Command Prompt'] = ['Open command prompt', self.iconInfo['Command Prompt'], 'open_cmd']
        self.mainInfo['PLM wiki'] = ['PLM wiki', self.iconInfo['PLM wiki'], "{key}".format(key=__plmWiki__)]
        self.mainInfo['PLMBrowser'] = ['PlmBrowser', self.iconInfo['PLMBrowser'], "PLMBrowser"]
        self.mainInfo['OpenConfig'] = ['Open config folder', self.iconInfo['OpenConfig'], '']

        for key in self.appInfo:
            if 'NukeX' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --nukex"
            elif 'Hiero' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --hiero"
            elif 'UVLayout' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " -launch"

        # Extra app come along with plm but not be installed in local.

        qtDesigner = os.path.join(os.getenv('PROGRAMDATA'), 'Anaconda3', 'Library', 'bin', 'designer.exe')

        davinciPth = os.path.join(os.getenv('PROGRAMFILES'), 'Blackmagic Design', 'DaVinci Resolve', 'resolve.exe')

        eVal = [qtDesigner, davinciPth]

        eKeys = ['QtDesigner', 'Davinci Resolve 14']

        for key in eKeys:
            if os.path.exists(eVal[eKeys.index(key)]):
                self.mainInfo[key] = [key, self.getAppIcon(32, key), "{key}".format(key=eVal[eKeys.index(key)])]

        for key in keepKeys:
            self.mainInfo[key] = [key, self.getAppIcon(32, key), "{key}".format(key=self.appInfo[key])]

        for key in CONFIG_APPUI:
            self.mainInfo[key] = [key, self.getAppIcon(32, key), "{key}".format(key=key)]

        for key in CONFIG_SYSTRAY:
            self.mainInfo[key] = [key, self.getAppIcon(32, key), "{key}".format(key=key)]

        self.create_config_file('main', self.mainInfo)

    def getAppIcon(self, size=32, iconName="AboutPlm"):
        iconPth = os.path.join(os.getenv(__envKey__), 'imgs', 'icons', "x" + str(size))
        return os.path.join(iconPth, iconName + ".icon.png")

    def get_all_path_from_dir(self, dir):
        """
            This function will generate the file names in a directory
            tree by walking the tree either top-down or bottom-up. For each
            directory in the tree rooted at directory top (including top itself),
            it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        filePths = []  # List which will store all of the full file paths.
        dirPths = []  # List which will store all of the full folder paths.

        # Walk the tree.
        for root, directories, files in os.walk(dir, topdown=False):
            for filename in files:
                filePths.append(os.path.join(root, filename))  # Add to file list.
            for folder in directories:
                dirPths.append(os.path.join(root, folder))  # Add to folder list.
        return [filePths, dirPths]

    def get_file_path(self, dir):
        self.handle_path_error(dir)
        return self.get_all_path_from_dir(dir)[0]

    def del_key(self, key, dict={}):
        try:
            del dict[key]
            # logger.debug("key deleted: {key}".format(key=key))
        except KeyError:
            dict.pop(key, None)
            # logger.debug("key poped: {key}".format(key=key))

    def create_config_file(self, name, data):
        if name == 'envKeys':
            filePth = pyEnvCfg
        elif name == "main":
            filePth = mainConfig
        elif name == 'icon':
            filePth = appIconCfg
        elif name == 'app':
            filePth = appConfig
        else:
            filePth = webIconCfg

        with open(filePth, 'w') as f:
            json.dump(data, f, indent=4)

    def handle_path_error(self, dir=None):
        if not os.path.exists(dir) or dir is None:
            try:
                raise IsADirectoryError("Path is not exists: {0}".format(dir))
            except IsADirectoryError as error:
                pass
                # logger.debug('Caught error: ' + repr(error))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/06/2018 - 12:34 AM
# © 2017 - 2018 DAMGteam. All rights reserved