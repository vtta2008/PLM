# -*- coding: utf-8 -*-
"""

Script Name: ConfigManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
# """ Import """
#
# # Python
# import os, sys, subprocess, shutil, winshell, pkg_resources, json
# from platform                           import system
#
# # PyQt5
# from PyQt5                              import __file__ as pyqt_path
# from PyQt5.QtCore                       import QProcess
#
# # DAMG
# from bin                                import DAMG, DAMGDICT, DAMGLIST
#
# __groupname__                           = "DAMGTEAM"
# __appName__                             = "Pipeline Manager (PLM)"
#
# __pkgsReq__                             = ['PyQt5', 'pip', 'urllib3', 'chardet', 'appdirs', 'deprecate', 'msgpack',
#                                            'winshell', 'pyqtwebengine', 'pandas', 'wheel', 'argparse', 'green']
#
# KEYPACKAGE                              = ['Adobe Photoshop CC 2017', 'Adobe Photoshop CC 2018',
#                                            'Adobe Photoshop CC 2019', 'Adobe Illustrator CC 2017',
#                                            'Adobe Illustrator CC 2018', 'Adobe Illustrator CC 2019',
#                                            'Adobe Audition CC 2017', 'Adobe Audition CC 2018', 'Adobe Audition CC 2019',
#                                            'Adobe After Effects CC 2017', 'Adobe After Effects CC 2018',
#                                            'Adobe After Effects CC 2019', 'Adobe Premiere Pro CC 2017',
#                                            'Adobe Premiere Pro CC 2018', 'Adobe Premiere Pro CC 2019',
#                                            'Adobe Media Encoder CC 2017', 'Adobe Media Encoder CC 2018',
#                                            'Adobe Media Encoder CC 2019', 'Autodesk Maya 2017', 'Autodesk Maya 2018',
#                                            'Autodesk Maya 2019', 'Autodesk Maya 2020', 'Autodesk MudBox 2017',
#                                            'Autodesk MudBox 2018', 'Autodesk MudBox 2019', 'Autodesk MudBox 2020',
#                                            'Autodesk 3ds Max 2017', 'Autodesk 3ds Max 2018', 'Autodesk 3ds Max 2019',
#                                            'Autodesk 3ds Max 2020', 'Autodesk AutoCAD 2017', 'Autodesk AutoCAD 2018',
#                                            'Autodesk AutoCAD 2019', 'Autodesk AutoCAD 2020', 'Substance Painter',
#                                            'Substance Designer', 'Hiero11.1v1', 'Hiero11.2v1', 'Hiero4.0v1',
#                                            'Hiero4.1v1', 'Hiero2.6v3', 'HieroPlayer11.1v1', 'HieroPlayer11.2v1',
#                                            'HieroPlayer4.0v1', 'HieroPlayer4.1v1', 'HieroPlayer2.6v3', 'Mari 11.1v1',
#                                            'Mari 11.2v1', 'Mari 4.0v1', 'Mari 4.1v1', 'Mari 2.6v3', 'NukeX11.1v1',
#                                            'NukeX11.2v1', 'NukeX4.0v1', 'NukeX4.1v1', 'NukeX2.6v3', 'Katana 11.1v1',
#                                            'Katana 11.2v1', 'Katana 4.0v1', 'Katana 4.1v1', 'Katana 2.6v3',
#                                            'ZBrush 4R6', 'ZBrush 4R7', 'ZBrush 4R8', 'Houdini FX 16.5.439',
#                                            'Houdini FX 16.5.496', 'Word 2013', 'Word 2015', 'Word 2016', 'Word 2017',
#                                            'Word 2018', 'Word 2019', 'Word 2020', 'Excel 2013', 'Excel 2015',
#                                            'Excel 2016', 'Excel 2017', 'Excel 2018', 'Excel 2019', 'Excel 2020',
#                                            'PowerPoint 2013', 'PowerPoint 2015', 'PowerPoint 2016', 'PowerPoint 2017',
#                                            'PowerPoint 2018', 'PowerPoint 2019', 'PowerPoint 2020', 'Wordpad 2013',
#                                            'Wordpad 2015', 'Wordpad 2016', 'Wordpad 2017', 'Wordpad 2018',
#                                            'Wordpad 2019', 'Wordpad 2020', 'JetBrains PyCharm 2017.3.3',
#                                            'JetBrains PyCharm 2018.1', 'Storyboarder', 'Krita (x64)', 'Sublime Text 2',
#                                            'Sublime Text 3', 'Wordpad', 'Headus UVLayout', 'Snipping Tool', 'Spyder',
#                                            'QtDesigner', 'Git Bash', 'About', 'Calculator', 'Calendar', 'Credit',
#                                            'EnglishDictionary', 'FindFiles', 'ForgotPassword', 'ImageViewer',
#                                            'Preferences', 'ScreenShot', 'UserSetting', 'PLMBrowser',
#                                            'NoteReminder', 'TextEditor', 'NodeGraph', 'Word', 'Excel', 'PowerPoint',
#                                            'ReConfig', 'CleanPyc', 'Debug']
#
# PROGRAM86                               = os.getenv('PROGRAMFILES(X86)')
# PROGRAM64                               = os.getenv('PROGRAMW6432')
# LOCALAPPDATA                            = os.getenv('LOCALAPPDATA')
# PROGRAMDATA                             = os.getenv('PROGRAMDATA')
# DESKTOP_DIR                             = os.path.join(os.environ["HOMEPATH"], "desktop")           # Desktop path
#
# autodeskVer                             = [ "2017", "2018", "2019", "2020"]
# autodeskApp                             = [ "Autodesk Maya", "Autodesk MudBox", "Autodesk 3ds Max", "Autodesk AutoCAD"]
# userMayaDir                             = os.path.expanduser(r"~/Documents/maya")
#
# KEYDETECT                               = [ "Non-commercial", "Uninstall", "Verbose", "License", "Skype", ".url"]
#
# __plmWiki__                             = "https://github.com/vtta2008/PipelineTool/wiki"
#
# CONFIG_APPUI                            = [ 'About', 'Calculator', 'Calendar', 'Credit', 'EnglishDictionary',
#                                             'FindFiles', 'ForgotPassword', 'ImageViewer', 'NewProject', 'Preferences',
#                                             'ScreenShot', 'UserSetting', 'PLMBrowser', 'NoteReminder', 'TextEditor',
#                                             'NodeGraph', 'Messenger', 'InviteFriend', 'SignIn', 'SignUp', 'SignOut',
#                                             'SwitchAccount']
#
# CONFIG_SYSTRAY                          = ['ScreenShot', 'Snipping Tool']
#
# FIX_KEY                                 = { 'ScreenShot': 'ScreenShot', 'Snipping Tool': 'SnippingTool'}
#
# PIPE                                    = subprocess.PIPE
# STDOUT                                  = subprocess.STDOUT

# class ConfigManager(DAMG):
#
#     key                                 = 'Configurations'
#
#     checkList                           = DAMGDICT()
#     cfgInfo                             = DAMGDICT()
#     cfgError                            = DAMGDICT()
#     install_packages                    = DAMGDICT()
#
#     packages                            = DAMGLIST()
#     versions                            = DAMGLIST()
#
#     printOutput                         = False
#
#     def __init__(self, appKey, rootDir, mode):
#         super(ConfigManager, self).__init__(self)
#
#         self.appKey                     = appKey
#         self.rootDir                    = rootDir
#         self.mode                       = mode
#
#         if self.mode.subprocess:
#             self.process = subprocess.Popen
#         else:
#             self.process = QProcess
#
#         self.cfgs                       = True
#         self._pthInfo                   = False
#         self._iconInfo                  = False
#         self._mainPkgs                  = False
#         self._appInfo                   = False
#
#         self.checkList['platform']      = self.cfg_platform()
#         self.checkList['root']          = self.cfg_envVariable(self.appKey, self.rootDir)
#         self.checkList['paths']         = self.cfg_cfgDir()
#         self.checkList['localDB']       = self.cfg_localDB()
#         self.checkList['pyqt']          = self.cfg_pyqt_env()
#         self.checkList['version']       = self.cfg_pyVersion()
#         self.checkList['path']          = self.cfg_pyPath(self.get_pyPth())
#         self.checkList['pip']           = self.cfg_pip()
#         self.checkList['deepFreeze']    = self.cfg_cx_Freeze()
#         self.checkList['requirement']   = self.cfg_requirements()
#         self.checkList['maya']          = self.cfg_maya()
#         self.checkList['envKeys']       = self.cfg_envVars()
#         self.checkList['iconPths']      = self.cfg_iconPth()
#         self.checkList['apps']          = self.get_app_installed()
#         self.checkList['mainPkg']       = self.cfg_mainPkgs()
#
#         for key in self.checkList.keys():
#
#             if self.checkList[key]:
#                 continue
#             else:
#                 self.cfgs = False
#                 break
#
#         self.folder_settings(self.pthInfo['config'], 'h')
#         pths, fns = self.get_all_paths(self.pthInfo['config'])
#         listObj = pths + fns
#         self.batch_folder_settings(listObj, 'h')
#
#     def cfg_platform(self):
#         self.cfgInfo['platform'] = system()
#         if system() == 'Windows':
#             return True
#         else:
#             return False
#
#     def cfg_envVariable(self, key, value):
#
#         envKeys = [k for k in os.environ.keys()]
#
#         if not key in envKeys:
#             os.environ[key] = value
#         else:
#             if os.getenv(key) != value:
#                 os.environ[key] = value
#
#         return True
#
#     def cfg_cfgDir(self, cfgFileName='paths.cfg', **dirPth):
#
#         dirPth['root']                 = self.rootDir
#
#         dirPth['appData']              = self.set_dir('appData')
#         dirPth['config']               = self.set_dir('appData/.config')
#         dirPth['setting']              = self.set_dir('appData/.config')
#         dirPth['log']                  = self.set_dir('appData/.config')
#
#         dirPth['tmp']                  = self.set_dir('appData/.tmp')
#         dirPth['task']                 = self.set_dir('appData/.config/task')
#         dirPth['project']              = self.set_dir('appData/.config/project')
#         dirPth['organisation']         = self.set_dir('appData/.config/organisation')
#         dirPth['team']                 = self.set_dir('appData/.config/team')
#         dirPth['user']                 = self.set_dir('appData/.config')
#         dirPth['userPref']             = self.set_dir('appData/.config')
#         dirPth['nodegraph']            = self.set_dir('appData/.config')
#         dirPth['cache']                = self.set_dir('appData/.config/.cache')
#
#         dirPth['docs']            = self.set_dir('appData/documentations')
#         dirPth['source']               = self.set_dir('appData/raws')
#
#         dirPth['bin']                  = self.set_dir('bin')
#         dirPth['resource']             = self.set_dir('bin/rcs')
#
#         dirPth['cores']                = self.set_dir('cores')
#
#         dirPth['hooks']              = self.set_dir('hooks')
#         dirPth['Houdini']              = self.set_dir('hooks/Houdini')
#         dirPth['Mari']                 = self.set_dir('hooks/Mari')
#         dirPth['Maya']                 = self.set_dir('hooks/Maya')
#         dirPth['Nuke']                 = self.set_dir('hooks/Nuke')
#         dirPth['Zbrush']               = self.set_dir('hooks/ZBrush')
#         dirPth['DaVinci']              = self.set_dir('hooks/DaVinci')
#         dirPth['Substances']           = self.set_dir('hooks/Substances')
#         dirPth['Photoshop']            = self.set_dir('hooks/Photoshop')
#         dirPth['Illustration']         = self.set_dir('hooks/Illustration')
#
#         dirPth['img']                  = self.set_dir('imgs')
#         dirPth['avatar']               = self.set_dir('imgs/avatar')
#         dirPth['icon']                 = self.set_dir('imgs/icons')
#         dirPth['icon12']               = self.set_dir('imgs/icons/x12')
#         dirPth['icon16']               = self.set_dir('imgs/icons/x16')
#         dirPth['icon24']               = self.set_dir('imgs/icons/x24')
#         dirPth['icon32']               = self.set_dir('imgs/icons/x32')
#         dirPth['icon48']               = self.set_dir('imgs/icons/x48')
#         dirPth['icon64']               = self.set_dir('imgs/icons/x64')
#
#         dirPth['logo']                 = self.set_dir('imgs/logo')
#         dirPth['DAMGTEAM']             = self.set_dir('imgs/logo/DAMGTEAM')
#         dirPth['PLM']                  = self.set_dir('imgs/logo/PLM')
#         dirPth['Maya']                 = self.set_dir('imgs/maya')
#         dirPth['nodes']                = self.set_dir('imgs/nodes')
#         dirPth['Picture']              = self.set_dir('imgs/pics')
#         dirPth['styles']               = self.set_dir('imgs/styles')
#
#         dirPth['Tagicon']              = self.set_dir('imgs/tags')
#         dirPth['WebIcon']              = self.set_dir('imgs/web')
#         dirPth['WebIcon12']            = self.set_dir('imgs/web/x12')
#         dirPth['WebIcon16']            = self.set_dir('imgs/web/x16')
#         dirPth['WebIcon24']            = self.set_dir('imgs/web/x24')
#         dirPth['WebIcon32']            = self.set_dir('imgs/web/x32')
#         dirPth['WebIcon48']            = self.set_dir('imgs/web/x48')
#         dirPth['WebIcon64']            = self.set_dir('imgs/web/x64')
#         dirPth['WebIcon128']           = self.set_dir('imgs/web/x128')
#
#         dirPth['plugin']               = self.set_dir('plugins')
#         dirPth['NodeGraph']             = self.set_dir('plugins/NodeGraph')
#
#         dirPth['Scripts']              = self.set_dir('scripts')
#         dirPth['json']                 = self.set_dir('scripts/json')
#         dirPth['qss']                  = self.set_dir('scripts/qss')
#         dirPth['rcs']                  = self.set_dir('scripts/rcs')
#
#         dirPth['test']                 = self.set_dir('test')
#
#         dirPth['devkit']             = self.set_dir('devkit')
#         dirPth['Core']                 = self.set_dir('devkit/Core')
#         dirPth['Gui']                  = self.set_dir('devkit/Gui')
#         dirPth['Widgets']              = self.set_dir('devkit/Widgets')
#
#         dirPth['ui']                   = self.set_dir('ui')
#         dirPth['base']                 = self.set_dir('ui/base')
#         dirPth['Body']                 = self.set_dir('ui/Body')
#         dirPth['Tabs']                 = self.set_dir('ui/Body/Tabs')
#         dirPth['Footer']               = self.set_dir('ui/Footer')
#         dirPth['Header']               = self.set_dir('ui/Header')
#         dirPth['Menus']                = self.set_dir('ui/Header/Menus')
#         dirPth['Network']              = self.set_dir('ui/Header/Network')
#         dirPth['Toolbars']             = self.set_dir('ui/Header/Toolbars')
#         dirPth['SubUi']                = self.set_dir('ui/SubUi')
#         dirPth['Funcs']                = self.set_dir('ui/SubUi/Funcs')
#         dirPth['Info']                 = self.set_dir('ui/SubUi/Info')
#         dirPth['Projects']             = self.set_dir('ui/SubUi/Projects')
#         dirPth['Settings']             = self.set_dir('ui/SubUi/Settings')
#         dirPth['Tools']                = self.set_dir('ui/SubUi/Tools')
#
#         dirPth['utils']                = self.set_dir('utils')
#
#         for pth in dirPth.values():
#             self.create_folder(pth)
#             if not os.path.exists(pth):
#                 self.cfgError['paths error'] = pth
#
#         self.pthInfo = dirPth
#         self._pthInfo = True
#
#         pth = os.path.join(dirPth['config'], cfgFileName)
#         self.compare_data(pth, dirPth)
#         return True
#
#     def cfg_localDB(self):
#         if self._pthInfo:
#             self.pthInfo['localDB'] = os.path.join(self.pthInfo['appData'], 'local.db')
#             if not os.path.exists(self.pthInfo['localDB']):
#                 from cores.SQLS import SQLS
#                 SQLS(self.pthInfo['localDB'])
#
#         return self._pthInfo
#
#     def cfg_pyqt_env(self):
#         if self.checkList['platform']:
#             pyqt = os.path.dirname(pyqt_path)
#             key = 'QT_QPA_PLATFORM_PLUGIN_PATH'
#             value = os.path.join(pyqt, "plugins")
#             print(value)
#             check = self.cfg_envVariable(key, value)
#         else:
#             check = False
#         return check
#
#     def cfg_pyVersion(self):
#         self.pyVersion = float(sys.version[:3])
#         self.cfgInfo['version'] = sys.version
#
#         return True
#
#     def cfg_pyPath(self, pyPth):
#         sysPths = self.get_system_path()
#         addPyPath = False
#         for pth in sysPths:
#             if pth == pyPth:
#                 continue
#             else:
#                 addPyPath = True
#         if not addPyPath:
#             os.environ['PATH'] = os.getenv('PATH') + pyPth
#             addPyPath = True
#
#         return addPyPath
#
#     def cfg_pip(self):
#         pipVer = self.get_pkg_version('pip')
#         cmd = 'python -m pip install --user --upgrade pip'
#         if pipVer is None:
#             self.run_command(cmd, self.printOutput)
#         else:
#             if pipVer < 18.0:
#                 self.run_command(cmd, self.printOutput)
#             else:
#                 self.run_command(cmd, self.printOutput)
#         return True
#
#     def cfg_cx_Freeze(self):
#         try:
#             import cx_Freeze
#         except ImportError:
#             cmd = 'python -m pip install --user --upgrade cx_Freeze'
#             self.run_command(cmd, self.printOutput)
#         return True
#
#     def cfg_requirements(self):
#         for pkg in __pkgsReq__:
#             check = self.check_pyPkg(pkg)
#             if not check:
#                 cmd = 'python -m pip install --user --upgrade {0}'.format(pkg)
#                 self.run_command(cmd, self.printOutput)
#         return True
#
#     def cfg_maya(self):
#         tk = os.path.join(os.getenv(self.appKey), 'hooks', 'maya')
#         tanker = dict(modules=['anim', 'lib', 'modeling', 'rendering', 'simulating', 'surfacing', ], )
#
#         pVal = ""
#         pyList = [os.path.join(tk, k) for k in tanker] + [os.path.join(tk, "modules", p) for p in tanker["modules"]]
#
#         for p in pyList:
#             pVal += p + ';'
#         os.environ['PYTHONPATH'] = pVal
#
#         usScr = os.path.join(os.getenv(self.appKey), 'packages', 'maya', 'userSetup.py')
#         if os.path.exists(usScr):
#             mayaVers = [os.path.join(tk, v) for v in autodeskVer if os.path.exists(os.path.join(tk, v))] or []
#             if not len(mayaVers) == 0 or not mayaVers == []:
#                 for usDes in mayaVers:
#                     shutil.copy(usScr, usDes)
#
#         return True
#
#     def cfg_envVars(self, fileName='envKey.cfg', **envKeys):
#         for key in os.environ.keys():
#             envKeys[key] = os.getenv(key)
#         pth = os.path.join(self.pthInfo['config'], fileName)
#         self.compare_data(pth, envKeys)
#         return True
#
#     def cfg_iconPth(self, fileName='appIcon.cfg', **iconInfo):
#
#         iconInfo['Logo'] = os.path.join(os.getenv(self.appKey), 'imgs/logo/PLM', '32x32.png')
#         iconInfo['DAMG'] = os.path.join(os.getenv(self.appKey), 'imgs/logo/DAMGTEAM', '32x32.png')
#         iconInfo['Sep'] = 'separato.png'                                           # Custom some info to debug
#         iconInfo['File'] = 'file.png'
#
#         iconlst = [i for i in self.get_file_path(os.path.join(os.getenv(self.appKey), 'imgs/icons/x32')) if '.icon' in i]    # Get list of icons in imgage folder
#
#         for i in iconlst:
#             iconInfo[os.path.basename(i).split('.icon')[0]] = i
#
#         self.iconInfo = iconInfo
#         self._iconInfo = True
#
#         pth = os.path.join(self.pthInfo['config'], fileName)
#         self.compare_data(pth, self.iconInfo)
#
#         return True
#
#     def cfg_mainPkgs(self, fileName='main.cfg', **mainInfo):
#
#         self.mainInfo = mainInfo
#
#         delKeys = []
#         for key in self.appInfo:
#             for k in KEYDETECT:
#                 if k in key:
#                     delKeys.append(key)
#                     # print("KEY DETECTED: {0}. Append to list to be deleted later".format(configKey))
#
#         for key in delKeys:
#             self.del_key(key, self.appInfo)
#
#         keepKeys = [k for k in KEYPACKAGE if k in self.appInfo and k in self.iconInfo]
#
#         # Custom functions
#
#         # show layout
#         self.mainInfo['About']                  = ['About PLM', self.iconInfo['About'], 'About']
#         self.mainInfo['CodeOfConduct']          = ['Code of Conduct', self.iconInfo['CodeOfConduct'], 'CodeOfConduct']
#         self.mainInfo['Contributing']           = ['Contributing', self.iconInfo['Contributing'], 'Contributing']
#         self.mainInfo['ReConfig']               = ['Re configuring qssPths', self.iconInfo['ReConfig'], 'ReConfig']
#         self.mainInfo['Reference']              = ['Reference', self.iconInfo['Reference'], 'Reference']
#         self.mainInfo['PLM wiki']               = ['PLM wiki', self.iconInfo['PLM wiki'], "{key}".format(key=__plmWiki__)]
#         self.mainInfo['Browser']                = ['Browser', self.iconInfo['Browser'], "Browser"]
#         self.mainInfo['OpenConfig']             = ['Open config folder', self.iconInfo['OpenConfig'], '']
#         self.mainInfo['Version']                = ['Version Info', 'Version', 'Version']
#         self.mainInfo['Licence']                = ['Licence Info', 'Licence', 'Licence Info']
#
#         self.mainInfo['Organisation']           = ['Organisation', 'OrganisationManager', 'Organisation']
#         self.mainInfo['Team']                   = ['Team', 'TeamManager', 'Team']
#         self.mainInfo['Project']                = ['Project', 'ProjectManager', 'Project']
#         self.mainInfo['Task']                   = ['Task', 'TaskManager', 'Task']
#
#         self.mainInfo['SettingUI']              = ['PLM Settings', 'Settings', 'SettingUI']
#         self.mainInfo['Configuration']          = ['PLM Configuration', 'Configuration', 'Configuration']
#         self.mainInfo['Showall']                = ['showall', 'ShowAll', 'showall']
#
#         self.mainInfo['Alpha']                  = ['Open Alpha Map Library', 'AlphaLibrary', 'AlphaLibrary']
#         self.mainInfo['HDRI']                   = ['Open HDRI Map Library', 'HDRILibrary', 'HDRILibrary']
#         self.mainInfo['Texture']                = ['Open Texture Map Library', 'TextureLibrary', 'TextureLibrary']
#
#         self.mainInfo['Feedback']               = ['Feedback', 'Feedback', 'Feedback']
#         self.mainInfo['ContactUs']              = ['Contact Us', 'ContactUs', 'ContactUs']
#
#         self.mainInfo['Restore']                = ['Restore', 'Restore', 'PipelineManager']
#         self.mainInfo['Maximize']               = ['Maximize', 'Maximize', 'PipelineManager']
#         self.mainInfo['Minimize']               = ['Minimize', 'Minimize', 'PipelineManager']
#
#         self.mainInfo['Apperance']              = ['Appearance', 'Appearance', 'Appearance']
#
#         # Executing
#         self.mainInfo['CleanPyc']               = ['Clean ".pyc" files', self.iconInfo['CleanPyc'], 'CleanPyc']
#         self.mainInfo['Debug']                  = ['Run PLM Debugger', self.iconInfo['Debug'], 'Debug']
#         self.mainInfo['Exit']                   = ['Exit PLM', self.iconInfo['Exit'], 'Exit']
#         self.mainInfo['ConfigFolder']           = ['Go To Config Folder', 'ConfigFolder', self.pthInfo['config']]
#         self.mainInfo['IconFolder']             = ['Go To Icon Folder', 'IconFolder', self.pthInfo['icon']]
#         self.mainInfo['SettingFolder']          = ['Go To Setting Folder', 'SettingFolder', self.pthInfo['setting']]
#         self.mainInfo['AppFolder']              = ['Go To PLM Folder', 'AppFolder', self.pthInfo['root']]
#         self.mainInfo['Command Prompt']         = ['Open command prompt', self.iconInfo['Command Prompt'], 'open_cmd']
#
#         self.mainInfo['Cut']                    = ['Cut', 'Cut', 'Cut']
#         self.mainInfo['Copy']                   = ['Copy', 'Copy', 'Copy']
#         self.mainInfo['Paste']                  = ['Paste', 'Paste', 'Paste']
#
#         self.mainInfo['bright']                 = ['bright', 'bright', 'bright']
#         self.mainInfo['dark']                   = ['dark', 'dark', 'dark']
#         self.mainInfo['chacoal']                = ['chacoal', 'chacoal', 'chacoal']
#         self.mainInfo['nuker']                  = ['nuker', 'nuker', 'nuker']
#
#         # Update link
#         self.mainInfo['pythonTag']              = ['pythonLink', 'pythonTagIcon', 'https://docs.anaconda.com/anaconda/reference/release-notes/']
#         self.mainInfo['licenceTag']             = ['licenceLink', 'licenceTagIcon', 'https://github.com/vtta2008/damgteam/blob/master/LICENCE']
#         self.mainInfo['versionTag']             = ['versionLink', 'versionTagIcon', 'https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst']
#
#         for key in self.appInfo:
#             if 'NukeX' in key:
#                 self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --nukex"
#             elif 'Hiero' in key:
#                 self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --hiero"
#             elif 'UVLayout' in key:
#                 self.appInfo[key] = '"' + self.appInfo[key] + '"' + " -launch"
#
#         qtDesigner = os.path.join(os.getenv('PROGRAMDATA'), 'Anaconda3', 'Library', 'bin', 'designer.exe')
#         davinciPth = os.path.join(os.getenv('PROGRAMFILES'), 'Blackmagic Design', 'DaVinci Resolve', 'resolve.exe')
#
#         eVal = [qtDesigner, davinciPth]
#         eKeys = ['QtDesigner', 'Davinci Resolve 14']
#
#         for key in eKeys:
#             if os.path.exists(eVal[eKeys.index(key)]):
#                 self.mainInfo[key] = [key, self.getAppIcon(32, key), "{0}".format(eVal[eKeys.index(key)])]
#
#         for key in keepKeys:
#             self.mainInfo[key] = [key, self.getAppIcon(32, key), "{0}".format(self.appInfo[key])]
#
#         for key in CONFIG_APPUI:
#             if key == 'UserSetting':
#                 self.mainInfo[key] = ['Profile', self.getAppIcon(32, key), 'User Profile']
#             elif key == 'SignIn':
#                 self.mainInfo[key] = ['Sign In', self.getAppIcon(32, key), 'SignIn']
#             elif key == 'SignUp':
#                 self.mainInfo[key] = ['New Account', self.getAppIcon(32, key), 'Create new account']
#             elif key == 'SwtichAccount':
#                 self.mainInfo[key] = ['Change Account', self.getAppIcon(32, key), 'Change other account']
#             elif key == 'SignOut':
#                 self.mainInfo[key] = ['Sign Out', self.getAppIcon(32, key), 'Log Out']
#             else:
#                 self.mainInfo[key] = [key, self.getAppIcon(32, key), "{0}".format(key)]
#
#         for key in CONFIG_SYSTRAY:
#             if key in self.appInfo:
#                 self.mainInfo[key] = [key, self.getAppIcon(32, key), self.appInfo[key]]
#             else:
#                 self.mainInfo[key] = [key, self.getAppIcon(32, key), FIX_KEY[key]]
#
#         pth = os.path.join(self.pthInfo['config'], fileName)
#         self.save_data(pth, self.mainInfo)
#         return True
#
#     def getAppIcon(self, size=32, iconName="AboutPlm"):
#         iconPth = os.path.join(os.getenv(self.appKey), 'imgs', 'icons', "x" + str(size))
#         return os.path.join(iconPth, iconName + ".icon.png")
#
#     def get_app_installed(self, fileName='main.cfg', **appInfo):
#         shortcuts = {}
#         appName = []
#         appPth = []
#
#         all_programs = winshell.programs(common=1)
#
#         for dirpath, dirnames, filenames in os.walk(all_programs):
#             relpath = dirpath[1 + len(all_programs):]
#             shortcuts.setdefault(relpath, []).extend([winshell.shortcut(os.path.join(dirpath, f)) for f in filenames])
#         for relpath, lnks in sorted(shortcuts.items()):
#             for lnk in lnks:
#                 name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
#                 appName.append(name)
#                 appPth.append(lnk.path)
#
#         for name in appName:
#             appInfo[str(name)] = str(appPth[appName.index(name)])
#
#         self.appInfo = appInfo
#         self._appInfo = True
#
#         pth = os.path.join(self.pthInfo['config'], fileName)
#         self.compare_data(pth, self.appInfo)
#         return True
#
#     def get_pkg_version(self, pkg):
#         check = self.check_pyPkg(pkg)
#         if check:
#             return float(self.versions[self.packages.index(pkg)][:4])
#         else:
#             return None
#
#     def get_system_path(self):
#         return os.getenv('PATH').split(';')[0:-1]
#
#     def get_pkgs(self):
#         return [(d.project_name, d.version) for d in pkg_resources.working_set]
#
#     def get_pyPth(self):
#
#         if 'Anaconda' in sys.version:
#             pyDirName = [f for f in os.listdir(PROGRAMDATA) if 'Anaconda' in f]
#             pyPth = os.path.join(PROGRAMDATA, pyDirName[0])
#         else:
#             pyDirName = [f for f in (os.listdir(PROGRAM86) + os.listdir(PROGRAM64) + os.listdir(LOCALAPPDATA)) if 'python' in f]
#             if os.path.exists(os.path.join(PROGRAM86, pyDirName[0])):
#                 pyPth = os.path.join(PROGRAM86, pyDirName[0])
#             elif os.path.exists(os.path.join(PROGRAM64, pyDirName[0])):
#                 pyPth = os.path.join(PROGRAM64, pyDirName[0])
#             else:
#                 pyPth = os.path.join(LOCALAPPDATA, pyDirName[0])
#
#         if not os.path.exists(os.path.join(pyPth, 'python.exe')):
#             for root, directories, files in os.walk(pyPth, topdown=False):
#                 for filename in files:
#                     if filename == 'python.exe':
#                         pyPth = os.path.dirname(filename)
#                         break
#
#         pths = [f for f in os.getenv('PATH').split(';') if not f == '']
#
#         if not pyPth in pths:
#             pth = ""
#             for p in pths:
#                 pth = pth + p + "; "
#             pth = pth + pyPth + "; "
#             os.environ['PATH'] = pth
#
#         return pyPth
#
#     def get_all_paths(self, directory):
#         filePths = []                                                       # List which will store all file paths.
#         dirPths = []                                                        # List which will store all folder paths.
#         for root, directories, files in os.walk(directory, topdown=False):  # Walk the tree.
#             for filename in files:
#                 filePths.append(os.path.join(root, filename))               # Add to file list.
#             for folder in directories:
#                 dirPths.append(os.path.join(root, folder))                  # Add to folder list.
#         return [filePths, dirPths]
#
#     def get_dir_path(self, directory):
#         return self.get_all_paths(directory)[1]
#
#     def get_file_path(self, directory):
#         return self.get_all_paths(directory)[0]
#
#     def set_dir(self, folName, subRoot=None):
#         if self.mode.config in ['Alpha', 'alpha', 'dev', 'test']:
#             if subRoot is not None:
#                 root = self.check_dir(self.rootDir, subRoot)
#             else:
#                 root = self.rootDir
#         else:
#             localAppData = self.check_dir(os.path.join(self.rootDir, 'appData/.config'))
#             cfgCompany = self.check_dir(localAppData, __groupname__)
#             root = self.check_dir(cfgCompany, __appName__)
#
#         pth = self.check_dir(root, folName)
#         # print("Set directory: {}".format(pth))
#         return pth
#
#     def check_dir(self, root, folName=None):
#         if folName is None:
#             pth = root
#         else:
#             pth = os.path.join(root, folName).replace('\\', '/')
#         return pth
#
#     def check_pyPkg(self, pkg):
#         self.install_packages = self.get_pkgs()
#         self.packages = [p[0] for p in self.install_packages]
#         self.versions = [v[1] for v in self.install_packages]
#         if pkg in self.packages:
#             return True
#         else:
#             return False
#
#     def compare_data(self, pth, newData={}):
#         if os.path.exists(pth):
#             with open(pth, 'r') as f:
#                 oldData = json.load(f)
#             if type(oldData) != type(newData):
#                 return self.save_data(pth, newData)
#             else:
#                 for key, value in oldData.items():
#                     if key in newData.keys() and newData[key] == value:
#                         continue
#                     else:
#                         return self.save_data(pth, newData)
#         else:
#             return self.save_data(pth, newData)
#
#     def save_data(self, filePth, data):
#         if os.path.exists(filePth):
#             os.remove(filePth)
#
#         with open(filePth, 'w') as f:
#             json.dump(data, f, indent=4)
#         return True
#
#     def del_key(self, key, data):
#         try:
#             del data[key]
#         except KeyError:
#             dict.pop(key, None)
#
#     def folder_settings(self, directory, mode):
#         if system() == "Windows" or system() == "Darwin":
#             if mode == "h":
#                 if system() == "Windows":
#                     subprocess.call(["attrib", "+H", directory])
#                 elif system() == "Darwin":
#                     subprocess.call(["chflags", "hidden", directory])
#             elif mode == "s":
#                 if system() == "Windows":
#                     subprocess.call(["attrib", "-H", directory])
#                 elif system() == "Darwin":
#                     subprocess.call(["chflags", "nohidden", directory])
#             else:
#                 raise (
#                     "CommandIncorrectError: Expected command 'HIDE' and 'UNHIDE' (both are not case sensitive)")
#         else:
#             raise ("PlatformCompatibleError: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")
#
#     def batch_folder_settings(self, listObj, mode):
#         for obj in listObj:
#             if os.path.exists(obj):
#                 self.folder_settings(obj, mode)
#             else:
#                 print('{0}: PathError: Could not find the specific path: {1}'.format(self.__class__.__name__, obj))
#
#     def create_folder(self, pth, mode=0o770):
#         if os.path.exists(pth):
#             return []
#
#         (head, tail) = os.path.split(pth)
#         res = self.create_folder(head, mode)
#         try:
#             original_umask = os.umask(0)
#             os.makedirs(pth, mode)
#         finally:
#             os.umask(original_umask)
#
#         os.chmod(pth, mode)
#
#         res += [pth]
#         return res
#
#     def run_command(self, cmd, printOutput=False):
#         args = [arg for arg in cmd.split(' ')]
#         # print( '%s %s' % (cmd, ' '.join( args )) )
#         t = " ".join(args)
#         if self.mode.subprocess:
#             try:
#                 if sys.platform == 'win32':
#                     proc = self.process(args=args, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False)
#                 else:
#                     proc = self.process(args=args, close_fds=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
#                 output = proc.stdout.read()
#                 proc.wait()
#             except EnvironmentError as e:
#                 output = 'ErrorRunning {0} {1}: {2}'.format(cmd, t, str(e))
#         else:
#             proc = self.process()
#             proc.setStandardInputFile(proc.nullDevice())
#             proc.setStandardOutputFile(proc.nullDevice())
#             proc.setStandardErrorFile(proc.nullDevice())
#
#             if proc.state() != 2:
#                 proc.waitForStarted()
#                 proc.waitForFinished()
#                 if "|" in t or ">" in t or "<" in t:
#                     proc.start('sh -c "' + cmd + ' ' + t + '"')
#                 else:
#                     proc.start(cmd + " " + t)
#
#             try:
#                 output = str(proc.readAll(), encoding='utf8').rstrip()
#             except TypeError:
#                 output = str(proc.readAll()).rstrip()
#
#         if printOutput:
#             print(output.decode().replace('\\', '/'))
#
#         return output

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/10/2019 - 12:22 PM
# © 2017 - 2018 DAMGteam. All rights reserved