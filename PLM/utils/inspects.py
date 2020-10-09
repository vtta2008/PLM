# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import os, sys, platform, sysconfig, win32api, requests, time, datetime, uuid, pkg_resources
from time                       import gmtime, strftime

from bin.Core                   import Size, Rect, RectF
from .converts                  import str2bool


installed_packages              = pkg_resources.working_set



def get_python_info():

    if (sys.executable == ""):
        executable = "NA"
    else:
        executable = sys.executable

    return {"timelog": strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
              "version": sysconfig.get_python_version(),
              'major': sys.version_info[0], 'minor': sys.version_info[1], 'micro': sys.version_info[2],
              "release level": sys.version_info[3], "serial": sys.version_info[5], 'executable': executable,
              "standard lib": sysconfig.get_path('stdlib')}


def get_system_info():

    return {"timelog": strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
            "os": [platform.system(), sys.platform],
            "pc name": platform.uname()[1],
            "architrecture": platform.architecture(),
            "processor": {'family': platform.processor(), 'number of cpu': os.cpu_count()},
            "pid": os.getpid(),
            "osVersion": platform.uname()[3],
            "hexVersion": sys.hexversion,
            "apiVersion": sys.api_version, }


def installed_pkgs():
    return sorted([str(pkg.key) for pkg in installed_packages])


def get_pkgs_info():
    info = {}
    for pkg in installed_packages:
        info[pkg.key]       = pkg.version
    return info


def get_pointer_bounding_box(pointerPos, bbSize):
    point                   = pointerPos
    mbbPos                  = point
    point.setX(point.x() - bbSize / 2)
    point.setY(point.y() - bbSize / 2)
    size                    = Size(bbSize, bbSize)
    bb                      = Rect(mbbPos, size)
    bb                      = RectF(bb)
    return bb


def get_all_path_from_dir(directory):
    """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    filePths = []   # List which will store all of the full file paths.
    dirPths = []    # List which will store all of the full folder paths.

    # Walk the tree.
    for root, directories, files in os.walk(directory, topdown=False):
        for filename in files:
            filePths.append(os.path.join(root, filename).replace('\\', '/'))  # Add to file list.
        for folder in directories:
            dirPths.append(os.path.join(root, folder).replace('\\', '/')) # Add to folder list.

    return [filePths, dirPths]


def get_file_path(directory):
    return get_all_path_from_dir(directory)[0]


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