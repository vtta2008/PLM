# -*- coding: utf-8 -*-
"""

Script Name: EventManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------



from PyQt5.QtGui                import QWheelEvent

from PLM.api.damg                import DAMGDICT, DAMG
from PLM.cores.base             import BaseStorage


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


class EventManager(BaseStorage):

    key = 'EventManager'

    def __init__(self, parent=None):
        DAMGDICT.__init__(self)

        self.parent         = parent
        self.wheelEvent     = WheelEvent()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 5:25 PM
# © 2017 - 2018 DAMGteam. All rights reserved