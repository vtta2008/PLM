# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from bin.data.damg import DAMGDATETIME

class Alarm(DAMGDATETIME):

    Type = 'DAMGALARM'
    key = 'Alarm'
    _name = 'DAMG Alarm'

    def __init__(self, parent=None):
        super(Alarm, self).__init__(parent)

        self.parent = parent

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 16/11/2019 - 7:00 PM
# © 2017 - 2018 DAMGteam. All rights reserved