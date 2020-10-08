# -*- coding: utf-8 -*-
"""

Script Name: UndoCommand.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PySide2.QtWidgets                      import QUndoCommand


class UndoCommand(QUndoCommand):

    Type                    = 'DAMGCOMMAND'
    key                     = 'UndoCommand'
    _name                   = 'DAMG Undo Command'

    def __init__(self):
        QUndoCommand.__init__(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/12/2019 - 2:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved