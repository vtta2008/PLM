# coding=utf-8
"""
Script Name: autoUpdate.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script will find take the duty of updating all new data everytime user using this tool, the update
    will be released out from admins.
"""

import os, sys, json, logging
from tk import proc
from tk import defaultVariable as var
from tk import appFuncs as func

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

key = 'PIPELINE_TOOL'
toolName = 'Pipeline Tool'
scrInstall = os.getenv('PROGRAMDATA')

def createTempUser():

    userInfo = {}

    userInfo['TrinhDo'] = [proc.endconding('adsadsa'), var.USER_CLASS[1], func.avatar('TrinhDo'),]
    userInfo['DucDM'] = [proc.endconding('ducdudao'), var.USER_CLASS[1], func.avatar('DucDM'),]
    userInfo['Arjun'] = [proc.endconding('123456'), var.USER_CLASS[3], func.avatar('Arjun'),]
    userInfo['Annie'] = [proc.endconding('123123'), var.USER_CLASS[3], func.avatar('Annie'),]

    userDataPth = os.path.join(os.getenv(key), os.path.join(var.MAIN_NAMES['appdata'][1], var.MAIN_NAMES['login']))

    with open(userDataPth, 'w+') as f:
        json.dump(userInfo, f, indent=4)


def createTempProduction():

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

def createTempData():
    createTempUser()
    createTempProduction()

if __name__=='__main__':
    createTempData()