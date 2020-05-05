# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import os
from .converter import str2bool

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