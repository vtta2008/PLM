# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import validators, re
from collections            import OrderedDict
from PLM.commons            import DAMGDICT, DAMGLIST
from PLM.configs            import actionTypes, buttonTypes, urlTypes


from PyQt5.QtWidgets        import QPushButton, QToolButton, QWidgetAction, QAction, QActionGroup
from PyQt5.QtCore           import QUrl, QUrlQuery


def detect_url(s):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s)


def url_valid(s):
    if validators.url(s):
        return True
    else:
        return False


def is_url(s):
    if is_string(s):
        return url_valid(s)
    else:
        if type(s) in [QUrl, QUrlQuery]:
            return True
        elif s.Type in urlTypes:
            return True
        else:
            return False


def is_button(s):
    if type(s) in [QPushButton, QToolButton, ]:
        return True
    elif s.Type in buttonTypes:
        return True
    else:
        return False


def is_action(s):
    if type(s) in [QWidgetAction, QAction, QActionGroup]:
        return True
    elif s.Type in actionTypes:
        return True
    else:
        return False


def is_none(s):
    return type(s).__name__ == 'NoneType'


def is_string(s):
    return type(s) in [str]


def is_number(s):
    """ Check if a string is a int/float """
    if is_bool(s):
        return False
    return isinstance(s, int) or isinstance(s, float)


def is_bool(s):
    """ Returns true if the object is a boolean value. """
    return isinstance(s, bool) or str(s).lower() in ['true', 'false']


def is_list(s):
    """ Returns true if the object is a list type. """
    return type(s) in [list, tuple, DAMGLIST]


def is_dict(s):
    """ Returns true if the object is a dict type. """
    return type(s) in [dict, OrderedDict, DAMGDICT]


def list_attr_types_obj(obj):
    """ return a list of attribute types """
    return [type(getattr(obj, name)).__name__ for name in dir(obj) if name[:2]!= '__' and name[-2:] != '__']

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved