# -*- coding: utf-8 -*-
"""

Script Name: Signals.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

sender = ['senderID', 'numOfSections', ]

from PyQt5.QtCore import (pyqtSignal, QObject, Q_CLASSINFO)
from appData import appSetting
from appData.Loggers import SetLogger
logger = SetLogger()
from utilities.utils import get_unix

# -------------------------------------------------------------------------------------------------------------
""" Import """

class SignalManager(QObject):

    staticMetaObject = {

        Q_CLASSINFO("Name", "SIGNAL MANAGER"),
        Q_CLASSINFO("type", "Signal Object"),
        Q_CLASSINFO("unixID", "{0}".format(get_unix())),
        Q_CLASSINFO("ClassID", "HUB"),
        Q_CLASSINFO("Flag", "Contributing Setting")
    }

    def __init__(self, parent=None):
        super(SignalManager, self).__init__(parent)
        self.settings = appSetting


class Signals(SignalManager):

    set_style_sheet = pyqtSignal(str)
    load_style_sheet = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Signals, self).__init__(parent)






















# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 5:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved