# -*- coding: utf-8 -*-
"""

Script Name: EventManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from bin                import DAMGDICT, DAMG

from PyQt5.QtGui        import QWheelEvent

class WheelEvent(DAMG):

    key                 = 'WheelEvent'
    Type                = 'DAMGEVENT'

    def eventFilter(self, object, event):
        if type(event) == QWheelEvent:
            if event.delta() > 0:
                print("wheel up")
            else:
                print("wheel down")
            event.accept()
            return True
        return False

class EventManager(DAMGDICT):

    key = 'EventManager'

    def __init__(self, parent=None):
        DAMGDICT.__init__(self)

        self.parent = parent
        self.wheelEvent = WheelEvent()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 5:25 PM
# © 2017 - 2018 DAMGteam. All rights reserved