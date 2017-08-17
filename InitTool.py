# -*- coding: utf-8 -*-

import os, sys, logging, subprocess, json
from tk import appFuncs as func

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

packages = ['pywinauto', 'winshell']

key = 'PIPELINE_TOOL'
toolName = 'Pipeline Tool'
scrInstall = os.getenv('PROGRAMDATA')

func.checkEnvKey(key, scrInstall, toolName)

func.checkPlugin('winshell')

#login UI
from ui import DesktopUI
reload(DesktopUI)
DesktopUI.initialize()