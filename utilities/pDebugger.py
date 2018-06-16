#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

Script Name: PyQtDebuging.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
import types
import doctest
from io import StringIO
from code import InteractiveConsole

# PyQt5
from PyQt5.QtWidgets import QTextEdit, QApplication, QWidget, QHBoxLayout
from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtCore import (qDebug, qInstallMessageHandler, QtInfoMsg, QtWarningMsg, QtCriticalMsg, QtFatalMsg)

# Plt
import appData as app
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.logger

# -------------------------------------------------------------------------------------------------------------
""" Processing User Input """

class Console(InteractiveConsole):

    def __init__(self, names=None):

        names = names or {}
        names['console'] = self
        InteractiveConsole.__init__(self, names)
        self.superspace = types.ModuleType('superspace')

    def enter(self, source):
        source = self.preprocess(source)
        self.runcode(source)

    @staticmethod
    def preprocess(source):
        return source

# -------------------------------------------------------------------------------------------------------------
""" Bug detector """

class pDetector(QTextEdit):
    '''
    A simple QTextEdit, with a few pre-set attributes and a file-like
    interface.
    '''
    def __init__(self, parent=None):
        super(pDetector, self).__init__(parent)

        self._buffer = StringIO()
        self.setReadOnly(True)

    def write(self, msg):
        '''Add msg to the console's output, on a new line.'''
        self.insertPlainText(msg)
        # Autoscroll
        self.moveCursor(QTextCursor.End)
        self._buffer.write(msg)

    def __getattr__(self, attr):
        '''
        Fall back to the buffer object if an attribute can't be found.
        '''
        return getattr(self._buffer, attr)

# -------------------------------------------------------------------------------------------------------------
""" Bug detector """

class pDeBug(pDetector):

    """
    It's main use case is to serve as an output console, for debugging or
    other purposes.

    It provides a file-like interface for ease of integration with other
    python features such as the logging module, on top of a slightly
    pre-set QTextEdit widget.

    Since it inherits QTextEdit directly, all of the widget's methods are
    available directly for further customization or GUI integration.
    """

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
        assert (len(s) == 4)
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

class pDebugger(QWidget):

    def __init__(self, parent=None):
        super(pDebugger, self).__init__(parent)

        doctest.testmod(verbose=True)

        self.setWindowIcon(QIcon(func.getAppIcon(32, 'DeBug')))
        self.setWindowTitle('Pipeline debug')

        self.layout = QHBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.textEdit = pDeBug()
        self.layout.addWidget(self.textEdit)

        self.applySetting()

    def applySetting(self):
        pass

def main():

    debug = QApplication(sys.argv)
    layout = pDebugger()
    layout.show()
    debug.exec_()

if __name__ == '__main__':
    main()

