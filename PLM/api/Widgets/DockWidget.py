# -*- coding: utf-8 -*-
"""

Script Name: Widget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from .io_widgets                            import QTextEdit, QDockWidget
from PLM.api.Gui.io_gui                     import QTextTableFormat, QTextCharFormat
from PLM.api.qtOption                       import right, datetTimeStamp
from PLM.cores.SignalManager                import SignalManager
from PLM.settings                           import AppSettings

# -------------------------------------------------------------------------------------------------------------
""" Dock widget """

class NoteStamp(QTextTableFormat):
    def __init__(self):
        super(NoteStamp, self).__init__()
        self.setBorder(1)
        self.setCellPadding(4)
        self.setAlignment(right)


class DockStamp(QTextEdit):

    def __init__(self, parent=None):
        super(DockStamp, self).__init__(parent)

        self.buildStamp()

    def buildStamp(self):

        cursor                          = self.textCursor()
        frame                           = cursor.currentFrame()
        frameFormat                     = frame.frameFormat()
        frameFormat.setPadding(1)
        frame.setFrameFormat(frameFormat)

        cursor.insertTable(1, 1, NoteStamp())
        cursor.insertText(datetTimeStamp, QTextCharFormat())
        self.resize(250, 100)

class DockWidget(QDockWidget):

    Type                                    = 'DAMGUI'
    key                                     = 'DockWidget'
    _name                                   = 'DAMG Dock Widget'

    def __init__(self, parent=None):
        QDockWidget.__init__(self)

        self.parent                         = parent
        self.settings                       = AppSettings(self)
        self.signals                        = SignalManager(self)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 10:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved