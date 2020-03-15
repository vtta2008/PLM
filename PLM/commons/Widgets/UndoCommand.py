# -*- coding: utf-8 -*-
"""

Script Name: UndoCommand.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__


from PyQt5.QtWidgets        import QUndoCommand
from PLM.cores import Loggers
from PLM.cores import SettingManager
from PLM.cores import SignalManager

class UndoCommand(QUndoCommand):

    Type                    = 'DAMGCOMMAND'
    key                     = 'UndoCommand'
    _name                   = 'DAMG Undo Command'
    _copyright              = __copyright__()

    def __init__(self):
        QUndoCommand.__init__(self)

        self.logger         = Loggers(self.key)
        self.SignalManager  = SignalManager(self)
        self.Settings       = SettingManager(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/12/2019 - 2:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved