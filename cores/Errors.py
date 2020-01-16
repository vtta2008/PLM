# -*- coding: utf-8 -*-
"""

Script Name: Errors.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

class NodePropertyError(Exception):
    pass


class NodeWidgetError(Exception):
    pass


class NodeRegistrationError(Exception):
    pass


class PortRegistrationError(Exception):
    pass


class NodeMenuError(Exception):
    pass

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 1:22 AM
# © 2017 - 2018 DAMGteam. All rights reserved