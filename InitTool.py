# -*- coding: utf-8 -*-

import os, sys, logging, subprocess, json

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

key = 'PIPELINE_TOOL'
toolName = 'Pipeline Tool'
scrInstall = os.getenv('PROGRAMDATA')

def createKey(key, scrInstall, toolName):
    logger.debug('install new environment variable')
    toolPth = os.path.join(scrInstall, toolName)
    if not os.path.exists(toolPth):
        os.mkdir(toolPth)
    os.environ[key] = toolPth

try:
    pth = os.getenv(key)
    if pth == None:
        createKey(key, scrInstall, toolName)
except KeyError:
    createKey(key, scrInstall, toolName)
else:
    pass
finally:
    pass

from tk import defaultVariable as var
from tk import proc

def avatar(userName):
    img = userName + '.avatar.jpg'
    imgPth = os.path.join(os.getcwd(), 'imgs')
    avatarPth = os.path.join(imgPth, img)
    return avatarPth

try:
    import winshell
except ImportError:
    logger.debug('winshell is not installed')
    subprocess.Popen('pip install winshell')
else:
    pass

try:
    import pywinauto
except ImportError:
    logger.debug('installing pywinauto')
    subprocess.Popen('pip install pywinauto')
else:
    pass

TrinhPass = 'adsadsa'

userInfo = {}

userInfo['TrinhDo'] = [proc.endconding(TrinhPass), var.USER_CLASS[1], avatar('TrinhDo'),]

userDataPth = os.path.join(os.getenv(key), os.path.join(var.MAIN_NAMES['appdata'][1], var.MAIN_NAMES['login']))

with open(userDataPth, 'w+') as f:
    json.dump(userInfo, f, indent=4)

prodInfoFolder = os.path.join(os.getenv(key), os.path.join(var.MAIN_NAMES['appdata'][1], 'prodInfo'))
if not os.path.exists(prodInfoFolder):
    os.mkdir(prodInfoFolder)

deepSea = {}

deepSea['name'] = 'Deep Sea Production'
deepSea['path'] = 'E:/deep_sea'
deepSea['length'] = '60s'
deepSea['fps'] = '24fps'
deepSea['Admin'] = ['TrinhDo',]
deepSea['Supervisor'] = ['Luke',]
deepSea['Artist'] = ['Arjun', 'Annie', 'Magnus', 'Ananta', 'Kathrine']

with open(os.path.join(prodInfoFolder, 'deep_sea.prod'), 'w') as f:
    json.dump(deepSea, f, indent=4)

mwm = {}

mwm['name'] = 'Midea Washing Machine Project'
mwm['path'] = 'E:/mwm'
mwm['length'] = '45s'
mwm['fps'] = '24fps'
mwm['Admin'] = ['TrinhDo',]
mwm['Supervisor'] = ['Harry',]
mwm['Artist'] = ['Arjun', 'Annie', 'Jack', 'Tho']

with open(os.path.join(prodInfoFolder, 'mwm.prod'), 'w') as f:
    json.dump(mwm, f, indent=4)

#login UI
from ui import DesktopUI
reload(DesktopUI)
DesktopUI.initialize()