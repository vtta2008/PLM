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
""" Metadatas """

__organization__                    = "DAMGTEAM"
__organizationID__                  = "DAMG"
__organizationName__                = 'DAMGTEAM'
__organizationDomain__              = "www.damgteam.com"
__slogan__                          = "Comprehensive Solution"

__envKey__                          = "PLM"
__productID__                       = __envKey__
__appName__                         = "Pipeline Manager (PLM)"
__appSlogan__                       = ""
__appDescription__                  = ""
__homepage__                        = "https://pipeline.damgteam.com"
__plmWiki__                         = "https://github.com/vtta2008/PipelineTool/wiki"

__localPort__                       = "20987"
__localHost__                       = "http://localhost:"
__localServer__                     = "{0}{1}".format(__localHost__, __localPort__)
__localServerCheck__                = "{0}/check".format(__localServer__)
__localServerAutho__                = "{0}/auth".format(__localServer__)

from .version import plmVersion

__version__                         = plmVersion.version_string
__license__                         = "Apache"
__title__                           = "PLM"

# -------------------------------------------------------------------------------------------------------------
""" Import """
# Python
import os, sys
from termcolor                      import cprint
from subprocess                     import PIPE, Popen

TRADE_MARK                          = '™'

def path_exists(path):
    return os.path.exists(path)

def create_path(*args):
    path                            = os.path.abspath(os.path.join(*args)).replace('\\', '/')
    path_exists(path)
    return path

def current_directory():
    path                            = os.path.abspath(os.getcwd()).replace('\\', '/')
    path_exists(path)
    return path

def parent_dir(path):
    path                            = os.path.abspath(os.path.join(path, os.pardir)).replace('\\', '/')
    path_exists(path)
    return path

def directory_name(path):
    return os.path.basename(path)


# setting up environment variable

cprint("{0} v{1}".format(__appName__, __version__), 'cyan')
cwd                                 = current_directory()
cfgable                             = False

if not directory_name(cwd) == __envKey__:
    cprint("Wrong root path. Current directory: {0}".format(cwd), 'red', attrs=['underline', 'blink'])
    sys.exit()
else:
    if directory_name(parent_dir(cwd)) == __envKey__:
        ROOT_APP                = parent_dir(cwd)
        ROOT                    = cwd
    else:
        ROOT_APP                = cwd
        ROOT                    = create_path(cwd, __envKey__)

import PySide2
qtPluginDir = create_path(parent_dir(PySide2.__file__), 'plugins/platforms')
os.environ['QT_PLUGIN_PATH'] = qtPluginDir

if __envKey__ not in os.environ:
    p = Popen('SetX {0} {1}'.format(__envKey__, ROOT), stdout=PIPE)
    txt = p.communicate()[0].decode('utf8')

else:
    if os.getenv(__envKey__).replace('\\', '/') != ROOT:
        p = Popen('SetX {0} {1}'.format(__envKey__, ROOT), stdout=PIPE)
        txt = p.communicate()[0].decode('utf8')
        print(txt)


from pyPLM.settings import GlobalSettings
glbSettings                             = GlobalSettings()

textProp                                = create_path(ROOT_APP, 'bin', 'text.properties')
glbProp                                 = create_path(ROOT_APP, 'bin', 'global.properties')

# Directory

SOUND_DIR                               = create_path(ROOT_APP, 'bin', 'data', 'sound')

LOCALAPPDATA                            = os.getenv('LOCALAPPDATA')

APPDATA_DAMG                            = create_path(LOCALAPPDATA, __organization__)
APPDATA_PLM                             = create_path(APPDATA_DAMG, __appName__)

CFG_DIR                                 = create_path(APPDATA_PLM, '.configs')
TMP_DIR                                 = create_path(APPDATA_PLM, '.tmp')
CACHE_DIR                               = create_path(APPDATA_PLM, '.cache')
PREF_DIR                                = create_path(APPDATA_PLM, 'preferences')
SETTING_DIR                             = create_path(CFG_DIR, 'settings')
DB_DIR                                  = APPDATA_PLM
LOG_DIR                                 = CFG_DIR
TASK_DIR                                = create_path(CFG_DIR, 'task')
TEAM_DIR                                = create_path(CFG_DIR, 'team')
PRJ_DIR                                 = create_path(CFG_DIR, 'project')
ORG_DIR                                 = create_path(CFG_DIR, 'organisation')
USER_LOCAL_DATA                         = create_path(CFG_DIR, 'userLocal')
USER_DIR                                = parent_dir(os.getenv('HOME'))
LIBRARY_DIR                             = create_path(APPDATA_DAMG, 'libraries')

# Filepath

APP_SETTING                             = create_path(SETTING_DIR, 'PLM.ini')
USER_SETTING                            = create_path(SETTING_DIR, 'user.ini')
FORMAT_SETTING                          = create_path(SETTING_DIR, 'fmt.ini')
UNIX_SETTING                            = create_path(SETTING_DIR, 'unix.ini')

APP_LOG                                 = create_path(LOG_DIR, 'PLM.log')
USER_LOG                                = create_path(LOG_DIR, 'user.log')
SERVER_LOG                              = create_path(LOG_DIR, 'server.log')
VERSION_LOG                             = create_path(LOG_DIR, 'version.log')
UNIX_LOG                                = create_path(LOG_DIR, 'unix.log')

LOCAL_DB                                = create_path(DB_DIR, 'local.db')
METADATA                                = create_path(ROOT, 'configs/metadatas.py')



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:15 AM
# © 2017 - 2019 DAMGteam. All rights reserved