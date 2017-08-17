# -*- coding: utf-8 -*-
"""
Script Name: appFuncs.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script will start some installation then call the main UI of the apps.
"""
import os, sys, logging, subprocess, json
from tk import appFuncs as func
from tk import autoUpdate as update

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

key = 'PIPELINE_TOOL'
toolName = 'Pipeline Tool'
scrInstall = os.getenv('PROGRAMDATA')

func.checkEnvKey(key, scrInstall, toolName)

packages = ['pywinauto', 'winshell']

for pkg in packages:
    func.checkPackageInstall(pkg)

update.createTempUser()

#login UI
from ui import DesktopUI
reload(DesktopUI)
DesktopUI.initialize()