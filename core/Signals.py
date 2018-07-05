# -*- coding: utf-8 -*-
"""

Script Name: Signals.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

sender = ['senderID', 'numOfSections', ]

from PyQt5.QtCore import (pyqtSignal, QObject)

# -------------------------------------------------------------------------------------------------------------
""" Import """

class Signals(QObject):

    saveSetting = pyqtSignal(str, str)
    loadSetting = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Signals, self).__init__(parent)






















# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 5:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved