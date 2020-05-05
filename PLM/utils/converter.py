# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

from PyQt5.QtGui    import QColor
from .utils         import generate_alternative_color


def tuple2Qcolor(data=None, alternate=False, av=20):
    if len(data) == 3:
        color = QColor(data[0], data[1], data[2])
        if alternate:
            mult = generate_alternative_color(color, av)
            color = QColor(max(0, data[0]-(av*mult)), max(0, data[1]-(av*mult)), max(0, data[2]-(av*mult)))
        return color
    elif len(data) == 4:
        color = QColor(data[0], data[1], data[2], data[3])
        if alternate:
            mult = generate_alternative_color(color, av)
            color = QColor(max(0, data[0]-(av*mult)), max(0, data[1]-(av*mult)), max(0, data[2]-(av*mult)), data[3])
        return color
    else:
        print('ColorNotRecognize: Can only be [R, G, B] or [R, G, B, A], Using default color !', data)
        color = QColor(120, 120, 120)
        if alternate:
            color = QColor(120-av, 120-av, 120-av)
        return color


def text_to_utf8(input):
    return input.encode('utf-8')

def text_to_hex(text):
    return ''.join(["%02X" % ord(x) for x in str(text)])

def hex_to_text(hex):
    bytes = []
    hexStr = ''.join(str(hex).split(" "))
    for i in range(0, len(hexStr), 2):
        bytes.append(chr(int(hexStr[i:i + 2], 16)))
    outPut = ''.join(bytes)
    return outPut

def str2bool(arg):
    return str(arg).lower() in ['true', 1, '1', 'ok', '2']

def bool2str(arg):
    if arg:
        return "True"
    else:
        return "False"

def byte2mb(byte):
    return round(byte/1048576)

def byte2gb(byte):
    return round(byte/1073741824)

def mb2gb(mb):
    return round(mb/1024)


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved