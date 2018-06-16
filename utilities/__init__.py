#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os, re, parse


__all__ = ['attr_type', 'auto_convert', 'camel_case_to_lower_case_underscore', 'camel_case_to_title', 'clean_name',
           'is_bool', 'is_dict', 'is_list', 'is_none', 'is_number', 'is_string', 'list_attr_types',
           'lower_case_underscore_to_camel_case', 'is_newer', 'test_func']

def clean_name(text):
    return re.sub(r'[^a-zA-Z0-9\n\.]', '_', text)

def camel_case_to_lower_case_underscore(text):
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(text):
        if char.isupper() and from_char_position < text:
            words.append(s[from_char_position:current_char_position].lower())
            from_char_position = current_char_position
    words.append(text[from_char_position:].lower())
    return '_'.join(words)


def camel_case_to_title(text):
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(text):
        if char.isupper() and from_char_position < current_char_position:
            words.append(text[from_char_position:current_char_position].title())
            from_char_position = current_char_position
    words.append(text[from_char_position:].title())
    return ' '.join(words)


def lower_case_underscore_to_camel_case(text):
    split_string = text.split('_')
    # use string's class to work on the string to keep its type
    class_ = text.__class__
    return split_string[0] + class_.join('', map(class_.capitalize, split_string[1:]))

def auto_convert(value):
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

    if not is_list(s):
        return 'unknown'

    for typ in [str, int, float, bool]:
        if all(isinstance(n, typ) for n in s):
            return '%s%d' % (typ.__name__, len(s))

    if False not in list(set([is_number(x) for x in s])):
        return 'float%d' % len(s)
    return 'unknown'

def is_none(s):
    return type(s).__name__ == 'NoneType'

def is_string(s):
    return type(s) in ['str', 'unicode']

def is_number(s):
    if is_bool(s):
        return False
    return isinstance(s, int) or isinstance(s, float)

def is_bool(s):
    return isinstance(s, bool) or str(s).lower() in ['true', 'false']

def is_list(s):
    return type(s) in [list, tuple]

def is_dict(s):
    from collections import OrderedDict
    return type(s) in [dict, OrderedDict]

def is_newer(file1, file2):
    if not os.path.exists(file1) or not os.path.exists(file2):
        return False

    time1 = os.path.getmtime(file1)
    time2 = os.path.getmtime(file2)
    return time1 > time2


# - Testing -----
def test_func(w, h):
    print('# width: %.2f, height: %.2f' % (float(w), float(h)))

def nodeParse(node):
    t = node[u"type"]

    if t == u"Program":
        body = [parse(block) for block in node[u"body"]]
        return Program(body)

    elif t == u"VariableDeclaration":
        kind = node[u"kind"]
        declarations = [parse(declaration) for declaration in node[u"declarations"]]
        return VariableDeclaration(kind, declarations)

    elif t == u"VariableDeclarator":
        id = parse(node[u"id"])
        init = parse(node[u"init"])
        return VariableDeclarator(id, init)

    elif t == u"Identifier":
        return Identifier(node[u"name"])

    elif t == u"Literal":
        return Literal(node[u"value"])

    elif t == u"BinaryExpression":
        operator = node[u"operator"]
        left = parse(node[u"left"])
        right = parse(node[u"right"])
        return BinaryExpression(operator, left, right)
    else:
        raise ValueError("Invalid data structure.")