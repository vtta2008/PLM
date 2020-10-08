# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

from PySide2.QtGui    import QColor
from .utils         import generate_alternative_color
from .types         import is_string, is_bool, is_list, is_none, is_number

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return power_labels[n]+'bytes', size

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

def bytes2str(s):
    return str(s, 'utf-8')

def auto_convert(value):
    """
    Auto-convert a value to it's given type.
    """
    atype = attr_type(value)
    if atype == 'str':
        return str(value)

    if atype == 'bool':
        return bool(value)

    if atype == 'float':
        return float(value)

    if atype == 'int':
        return int(value)
    return value

def attr_type(value):
    """
    Determine the attribute type based on a value.
    Returns a string.
    For example:
        value = [2.1, 0.5]
        type = 'float2'
    :param value: attribute value.
    :returns: attribute type.
    :rtype: str
    """
    if is_none(value):
        return 'null'

    if is_list(value):
        return list_attr_types(value)

    else:
        if is_bool(value):
            return 'bool'

        if is_string(value):
            return 'str'

        if is_number(value):
            if type(value) is float:
                return 'float'

            if type(value) is int:
                return 'int'
    return 'unknown'

def list_attr_types(s):
    """
    Return a string type for the value.
    .. todo::
        - 'unknown' might need to be changed
        - we'll need a feature to convert valid int/str to floats
          ie:
            [eval(x) for x in s if type(x) in [str, unicode]]
    """
    if not is_list(s):
        return 'unknown'

    for typ in [str, int, float, bool]:
        if all(isinstance(n, typ) for n in s):
            return '%s%d' % (typ.__name__, len(s))

    if False not in list(set([is_number(x) for x in s])):
        return 'float%d' % len(s)
    return 'unknown'


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved