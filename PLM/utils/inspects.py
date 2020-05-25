# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import os, sys, platform, win32api, requests, re, time, datetime, uuid

from PLM.api.Core           import Size, Rect, RectF
from .converts              import str2bool


SYS_OPTS                                    = ["Host Name", "OS Name", "OS Version", "Product ID", "System Manufacturer",
                                                "System Model", "System type", "BIOS Version", "Domain", "Windows Directory",
                                                "Total Physical Memory", "Available Physical Memory", "Logon Server"]


def get_py_env_var(key, path):
    try:
        pth = os.getenv(key)
        if pth == None or pth == '':
            print('install showLayout_new environment variable')
            os.environ[key] = path
    except KeyError:
        print('install showLayout_new environment variable')
        os.environ[key]     = path
    else:
        pass


def get_pointer_bounding_box(pointerPos, bbSize):
    point                   = pointerPos
    mbbPos                  = point
    point.setX(point.x() - bbSize / 2)
    point.setY(point.y() - bbSize / 2)
    size                    = Size(bbSize, bbSize)
    bb                      = Rect(mbbPos, size)
    bb                      = RectF(bb)
    return bb

def get_user_location():

    pythonVersion           = sys.version
    windowOS                = platform.system()
    windowVersion           = platform.version()

    sysOpts                 = SYS_OPTS
    cache                   = os.popen2("SYSTEMINFO")
    source                  = cache[1].read()

    sysInfo                 = {}

    sysInfo['python']       = pythonVersion
    sysInfo['os']           = windowOS + "|" + windowVersion
    sysInfo['pcUser']       = platform.node()
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






def check_odd(num):
    return str2bool(num%2)

def check_preset(data):
    if data == {}:
        pass
    else:
        return True

def check_blank(data):
    if len(data) == 0 or data == "" or data is None:
        return False
    else:
        return True

def check_match(data1, data2):
    check = []
    if len(data1) == len(data2):
        for i in range(len(data1)):
            if data1[i] is data2[i]:
                continue
            else:
                check.append('False')
    else:
        check.append('False')

    if len(check) == 0:
        return True
    else:
        return False


def is_newer(file1, file2):
    """
    Returns true if file1 is newer than file2.

    :param str file1: first file to compare.
    :param str file2: second file to compare.

    :returns: file1 is newer.
    :rtype: bool
    """
    if not os.path.exists(file1) or not os.path.exists(file2):
        return False

    time1 = os.path.getmtime(file1)
    time2 = os.path.getmtime(file2)
    return time1 > time2


def get_all_odd(numLst):
    return [i for i in numLst if check_odd(i)]

def get_all_even(numLst):
    return [i for i in numLst if not check_odd(i)]


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved