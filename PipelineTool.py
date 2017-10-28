# -*- coding: utf-8 -*-
"""
Script Name: appFuncs.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script will start some installation then call the main UI of the apps.
"""



import os, sys, logging, subprocess, json, shutil
from tk import appFuncs as func
from tk import autoUpdate as update

print 'it works here'

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

key = 'PIPELINE_TOOL'
toolName = 'Pipeline Tool'
scrInstall = os.getenv('PROGRAMDATA')

print 'it works here'

func.checkEnvKey(key, scrInstall, toolName)

packages = ['pywinauto', 'winshell', 'pandas']

for pkg in packages:
    func.checkPackageInstall(pkg)

update.createTempData()

userSetupScr = os.path.join(os.getcwd(), 'Maya_tk/userSetup.py')

userSetupDes = os.path.join(os.path.expanduser('~/Documents/maya/2017/prefs/scripts'), 'userSetup.py')

shutil.copy2(userSetupScr, userSetupDes)



#login UI
from ui import DesktopUI
reload(DesktopUI)
DesktopUI.initialize()