# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import os, sys, platform, win32api, requests, re, time, datetime, uuid

from PyQt5.QtCore import QSize, QRect, QRectF

from PLM.configs import KEYPACKAGE



def get_py_env_var(key, path):
    try:
        pth = os.getenv(key)
        if pth == None or pth == '':
            print('install showLayout_new environment variable')
            os.environ[key] = path
    except KeyError:
        print('install showLayout_new environment variable')
        os.environ[key] = path
    else:
        pass


def get_pointer_bounding_box(pointerPos, bbSize):
    point = pointerPos
    mbbPos = point
    point.setX(point.x() - bbSize / 2)
    point.setY(point.y() - bbSize / 2)
    size = QSize(bbSize, bbSize)
    bb = QRect(mbbPos, size)
    bb = QRectF(bb)
    return bb

def get_user_location():

    package = KEYPACKAGE
    pythonVersion = sys.version
    windowOS = platform.system()
    windowVersion = platform.version()

    sysOpts = package['sysOpts']
    cache = os.popen2("SYSTEMINFO")
    source = cache[1].read()

    sysInfo = {}

    sysInfo['python'] = pythonVersion
    sysInfo['os'] = windowOS + "|" + windowVersion
    sysInfo['pcUser'] = platform.node()
    sysInfo['operating system'] = platform.system() + "/" + platform.platform()
    sysInfo['python version'] = platform.python_version()

    values = {}

    for opt in sysOpts:
        values[opt] = [item.strip() for item in re.findall("%s:\w*(.*?)\n" % (opt), source, re.IGNORECASE)][0]
    for item in values:
        sysInfo[item] = values[item]

    return sysInfo

def get_screen_resolution():
    resW = win32api.GetSystemMetrics(0)
    resH = win32api.GetSystemMetrics(1)
    return resW, resH

def get_window_taskbar_size():
    resW, resH = get_screen_resolution()
    monitors = win32api.EnumDisplayMonitors()
    display1 = win32api.GetMonitorInfo(monitors[0][0])
    tbH = resH - display1['Work'][3]
    tbW = resW
    return tbW, tbH

def get_local_pc_info():
    r = requests.get('https://api.ipdata.co').json()
    info = dict()
    for key in r:
        k = (str(key))
        for c in ['ip', 'city', 'country_name']:
            if k == c:
                info[k] = str(r[key])
            else:
                info[k] = 'unknown'

    return info['ip'], info['city'], info['country_name']

def get_layout_size(layout):
    sizeW = layout.frameGeometry().width()
    sizeH = layout.frameGeometry().height()
    return sizeW, sizeH

# def get_text_size(text, painter=None):
#     if not painter:
#         metrics = QFontMetrics(QFont())
#     else:
#         metrics = painter.fontMetrics()
#     size = metrics.size(Qt.TextSingleLine, text)
#     return size

def get_datetime():
    datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
    return datetime_stamp

def getDate():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[0]

def getTime():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[1]

def getToken():
    return str(uuid.uuid4())

def getUnix():
    return (str(uuid.uuid4())).split('-')[-1]

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved