# -*- coding: utf-8 -*-
"""

Script Name: UndoCommand.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__


from PyQt5.QtWidgets        import QUndoCommand
from cores.Loggers          import Loggers
from cores.Settings         import Settings
from cores.SignalManager    import SignalManager

class UndoCommand(QUndoCommand):

    Type                    = 'DAMGCOMMAND'
    key                     = 'UndoCommand'
    _name                   = 'DAMG Undo Command'
    _copyright              = __copyright__()

    def __init__(self):
        QUndoCommand.__init__(self)

        self.logger         = Loggers(self.key)
        self.SignalManager  = SignalManager(self)
        self.Settings       = Settings(self)

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