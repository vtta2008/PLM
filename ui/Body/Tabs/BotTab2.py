# -*- coding: utf-8 -*-
"""

Script Name: debugger.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    It's main use case is to serve as an output console, for debugging or
    other purposes.

    It provides a file-like interface for ease of integration with other
    python features such as the logging module, on top of a slightly
    pre-set QTextEdit widget.

    Since it inherits QTextEdit directly, all of the widget's methods are
    available directly for further customization or GUI integration.

"""
# -------------------------------------------------------------------------------------------------------------
import doctest
import types
from io import StringIO

# PyQt5
from PyQt5.QtCore               import (qDebug, qInstallMessageHandler, QtInfoMsg, QtWarningMsg, QtCriticalMsg, QtFatalMsg)
from PyQt5.QtGui                import QTextCursor

# PLM
from appData                    import SiPoMin
from toolkits.Widgets           import GridLayout, Detector, Widget

# -------------------------------------------------------------------------------------------------------------
""" Processing User Input """

class Console(GridLayout):

    key                         = 'Console'

    def __init__(self, names=None):
        super(Console, self).__init__(names)
        self.names = names
        if self.names is None:
            self.names = dict()
            self.names['console'] = self

        self.superspace = types.ModuleType('superspace')

    def enter(self, source):
        source = self.preprocess(source)
        self.runcode(source)

    @staticmethod
    def preprocess(source):
        return source

# -------------------------------------------------------------------------------------------------------------
""" Bug detector """

class pDetector(Detector):              # A simple QTextEdit, with a few pre-set attributes and a file-like interface.

    key                         = 'pDetector'

    def __init__(self, parent=None):
        super(pDetector, self).__init__(parent)

        self._buffer            = StringIO()
        self.parent             = parent
        self.setReadOnly(True)

    def write(self, msg):                   # Add msg to the console's output, on a showLayout_new line.
        self._buffer.write(msg)
        self.insertPlainText(msg)
        self.moveCursor(QTextCursor.End)    # Autoscroll

    def __getattr__(self, attr):
        return getattr(self._buffer, attr)  # Fall back to the buffer object if an attribute can't be found.

class BotTab2(Widget):

    Type                        = 'DAMGDEBUG'
    key                         = 'BotTab2'
    _name                       = 'DAMG Debugger'


    def __init__(self, parent=None):
        super(BotTab2, self).__init__(parent)

        self.parent = parent
        self.mode = QtInfoMsg
        self.console = Console()
        self.buildUI()
        qInstallMessageHandler(self.message_handler)
        self.setLayout(self.console)

    def buildUI(self):

        self.textEdit = pDetector()
        self.console.addWidget(self.textEdit)
        self.textEdit.setSizePolicy(SiPoMin, SiPoMin)
        self.textEdit.setMaximumHeight(100)

    def debug_trace(self):
        """Set a tracepoint in the Python debugger that works with Qt."""

        from PyQt5.QtCore import pyqtRemoveInputHook
        from pdb import set_trace
        pyqtRemoveInputHook()
        set_trace()

    def message_handler(self, line, funct, file):

        if self.mode == QtInfoMsg:
            self.mode = 'INFO'
        elif self.mode == QtWarningMsg:
            self.mode = 'WARNING'
        elif self.mode == QtCriticalMsg:
            self.mode = 'CRITICAL'
        elif self.mode == QtFatalMsg:
            self.mode = 'FATAL'
        else:
            self.mode = 'DEBUG'

        message = 'message_handler: line: {0}, func: {1}(), file: {2}'.format(line, funct, file)
        self.textEdit.appendPlainText(message)
        # mess = self.seeking()
        # print(mess)
        qDebug(message)

    def seeking(self):

        s = self.textEdit.read(4)
        print(len(s))
        assert (len(s) == 0)
        self.textEdit.write(s)
        return s

    def test(self):
        return doctest.testmod(verbose=True)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 20/07/2018 - 9:19 PM
# © 2017 - 2018 DAMGteam. All rights reserved