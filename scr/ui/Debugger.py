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
import sys, types, doctest, pprint
from io import StringIO
from code import InteractiveConsole

# PyQt5
from PyQt5.QtWidgets import QTextEdit, QApplication, QGridLayout
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import (qDebug, qInstallMessageHandler, QtInfoMsg, QtWarningMsg, QtCriticalMsg, QtFatalMsg)

# PLM
from scr.core.paths import SiPoMin

# -------------------------------------------------------------------------------------------------------------
""" Processing User Input """

class Console(InteractiveConsole):

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

class pDetector(QTextEdit):              # A simple QTextEdit, with a few pre-set attributes and a file-like interface.
    def __init__(self, parent=None):
        super(pDetector, self).__init__(parent)

        self._buffer = StringIO()
        self.setReadOnly(True)

    def write(self, msg):                   # Add msg to the console's output, on a new line.
        self._buffer.write(msg)
        self.insertPlainText(msg)
        self.moveCursor(QTextCursor.End)    # Autoscroll


    def __getattr__(self, attr):
        return getattr(self._buffer, attr)  # Fall back to the buffer object if an attribute can't be found.

# -------------------------------------------------------------------------------------------------------------
""" Bug detector """

class pDeBug(pDetector):

    def __init__(self, mode, context, message, parent=None):
        super(pDeBug, self).__init__(parent)

        self.mode = mode
        self.context = context
        self.message = message

        self.detector = pDetector()
        self.seeking()

        qInstallMessageHandler(self.message_handler)

    def seeking(self):

        self.detector.seek(0)
        self.detector.seek(0)
        self.detector.read()
        self.detector.seek(0)

        s = self.detector.read(4)
        print(len(s))
        assert (len(s) == 0)
        self.detector.write(s)

    def message_handler(self):
        if self.mode == QtInfoMsg:
            self.mode = 'INFO'
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

        line = self.context.line
        funct = self.context.function
        file = self.context.file

        qDebug('message_handler: line: {0}, func: {1}(), file: {2}'.format(line, funct, file))
        qDebug('  %s: %s\n' % (self.mode, self.message))

        print(self.mode, self.message)

class pDebugger(QGridLayout):

    def __init__(self, parent=None):
        super(pDebugger, self).__init__(parent)

        doctest.testmod(verbose=True)
        self.console = Console()
        self.buildUI()

    def buildUI(self):
        self.textEdit = pDeBug(QtFatalMsg, self.console, None)
        self.addWidget(self.textEdit)
        self.applySetting()

    def applySetting(self):
        self.textEdit.setSizePolicy(SiPoMin, SiPoMin)
        self.textEdit.setMaximumHeight(100)

    def debug_trace(self):
        """Set a tracepoint in the Python debugger that works with Qt."""
        from PyQt5.QtCore import pyqtRemoveInputHook

        from pdb import set_trace
        pyqtRemoveInputHook()
        set_trace()

def main():

    debug = QApplication(sys.argv)
    layout = pDebugger()
    layout.show()
    debug.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 20/07/2018 - 9:19 PM
# © 2017 - 2018 DAMGteam. All rights reserved