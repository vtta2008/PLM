# -*- coding: utf-8 -*-
"""

Script Name: config.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import platform, subprocess

try:
    from importlib import reload
except ImportError:
    pass

PLATFORM = 'Windows'
API_MINIMUM = 0.64

from appData                        import metadatas as m
from appData.paths                  import *
from appData.text                   import *
from appData.keys                   import *
from appData.settingFormats         import *
from appData.settingOptions         import *

# -------------------------------------------------------------------------------------------------------------
""" Environment configKey """

__envKey__              = m.__envKey__
PLMAPPID                = m.PLMAPPID
VERSION                 = m.VERSION

# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__copyright__           = m.COPYRIGHT
__organization__        = m.__organization__
__groupname__           = m.__groupname__
__damgSlogan__          = m.__damgSlogan__
__website__             = m.__website__
__author1__             = m.__author1__
__author2__             = m.__author2__
__Founder__             = m.__author1__
__CoFonder1__           = m.__author2__
__email1__              = m.__email1__
__email2__              = m.__email2__

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__             = m.__project__
__appname__             = m.__appname__
__appShortcut__         = m.__appShortcut__
__version__             = m.__version__
__versionFull__         = m.VERSION
__cfgVersion__          = m.__cfgVersion__
__verType__             = m.__verType__
__reverType__           = m.__reverType__
__about__               = m.__about__
__homepage__            = m.__homepage__
__plmSlogan__           = m.__plmSlogan__
__plmWiki__             = m.__plmWiki__

# -------------------------------------------------------------------------------------------------------------
""" Server """

__globalServer__        = m.__globalServer__
__globalServerCheck__   = m.__globalServerCheck__
__globalServerAutho__   = m.__globalServerAutho__

__localPort__           = m.__localPort__
__localHost__           = m.__localHost__
__localServer           = m.__localServer__
__localServerCheck__    = m.__localServerCheck__
__localServerAutho__    = m.__localServerAutho__

__google__              = m.__google__
__googleVN__            = m.__googleVN__
__googleNZ__            = m.__googleNZ__

__email__               = m.__email__

__packages_dir__        = m.__packages_dir__
__classifiers__         = m.__classifiers__
__download__            = m.__download__
__description__         = m.__description__
__readme__              = m.__readme__
__modules__             = m.__modules__
__pkgsReq__             = m.__pkgsReq__

# -------------------------------------------------------------------------------------------------------------
""" Config directories """

allPths = [ROOT_DIR, CFG_DIR, CONFIG_DIR, CONFIG_LOCAL_DAMG_DIR, CONFIG_LOCAL_PLM_DIR, SETTING_DIR, LOG_DIR, CACHE_DIR,
           APP_DATA_DIR, BUILD_DIR, IMG_DIR, PLUGIN_DIR, UI_DIR, CACHE_DIR, TEST_DIR, DEPENDANCIES_DIR,
           BIN_DIR, APPS_DIR, DATA_DIR, DEPENDANCIES_DIR, SCRIPTS_DIR, QSS_DIR, DB_DIR, APPS_DIR, APP_ICON_DIR,
           WEB_ICON_DIR, AVATAR_DIR, LOGO_DIR, PIC_DIR,
           TAG_DIR, ICON_DIR_16, ICON_DIR_24, ICON_DIR_32, ICON_DIR_48, ICON_DIR_64, WEB_ICON_16, WEB_ICON_24,
           WEB_ICON_32, WEB_ICON_48, WEB_ICON_64, WEB_ICON_128, DAMG_LOGO_DIR, PLM_LOGO_DIR, DAMG_LOGO_32,
           PLM_LOGO_32, RAWS_DATA_DIR, DOCUMENTATION_DIR]

for p in allPths:
    if not os.path.exists(p):
        print('directory: "{0}" is not exists'.format(p))
        os.makedirs(p, exist_ok=True)

# Set config folder to invisible (hide)
if platform.system() == "Windows":
    subprocess.call(["attrib", "+H", CFG_DIR])
elif platform.system() == "Darwin":
    subprocess.call(["chflags", "hidden", CFG_DIR])

# -------------------------------------------------------------------------------------------------------------
""" Config file paths """

# appIconCfg          = p.appConfig
# webIconCfg          = p.webIconCfg
# logoIconCfg         = p.logoIconCfg
#
# pyEnvCfg            = p.pyEnvCfg
# appConfig           = p.appConfig
# mainConfig          = p.mainConfig
#
# DB_PTH              = p.DB_PTH
# LOG_PTH             = p.LOG_PTH
#
# APP_SETTING         = p.APP_SETTING
# USER_SETTING        = p.USER_SETTING
# FORMAT_SETTING      = p.FORMAT_SETTING
# UNIX_SETTING        = p.UNIX_SETTING

# -------------------------------------------------------------------------------------------------------------
""" Config data from text file """

def read_file(fileName):

    filePth = os.path.join(RAWS_DATA_DIR, fileName)

    if not os.path.exists(filePth):
        filePth = os.path.join(DOCUMENTATION_DIR, "{}.rst".format(fileName))

    if os.path.exists(filePth):
        with open(filePth, 'r') as f:
            data = f.read()
        return data

QUESTIONS = read_file('QUESTION')
ABOUT = read_file('ABOUT')
CREDIT = read_file('CREDIT')
CODECONDUCT = read_file('CODECONDUCT')
CONTRIBUTING = read_file('CONTRIBUTING')
REFERENCE = read_file('REFERENCE')
LICENCE_MIT = read_file('LICENCE_MIT')

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
