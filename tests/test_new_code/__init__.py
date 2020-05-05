# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import globalSetting

import inspect

def isprop(v):
    return isinstance(v, property)

propnames = [name for (name, value) in inspect.getmembers(globalSetting, isprop)]

print(globalSetting.__dict__)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:17 AM
# © 2017 - 2019 DAMGteam. All rights reserved