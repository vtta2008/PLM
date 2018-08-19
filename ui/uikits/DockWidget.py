# -*- coding: utf-8 -*-
"""

Script Name: Widget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

# PyQt5
from PyQt5.QtGui import QTextTableFormat, QTextCharFormat
from PyQt5.QtWidgets import QTextEdit, QDockWidget

# PLM
from scr.appData import (right, SiPoMin, dockB, dockT, datetTimeStamp)

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

        cursor = self.textCursor()
        frame = cursor.currentFrame()
        frameFormat = frame.frameFormat()
        frameFormat.setPadding(1)
        frame.setFrameFormat(frameFormat)

        cursor.insertTable(1, 1, NoteStamp())
        cursor.insertText(datetTimeStamp, QTextCharFormat())

    def applySetting(self):
        self.resize(250, 100)
        self.setSizePolicy(SiPoMin, SiPoMin)

class DockWidget(QDockWidget):

    def __init__(self, name="Reminder", parent=None):
        super(DockWidget, self).__init__(parent)

        self.setWindowTitle = name
        self.setAllowedAreas(dockB | dockT)

        self.content = DockStamp(self)
        self.buildUI()
        self.setWidget(self.content)

    def buildUI(self):
        cursor = self.content.textCursor()
        cursor.insertBlock()
        cursor.insertText("Note info")

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 10:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved