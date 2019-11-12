# -*- coding: utf-8 -*-
"""

Script Name: test.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtCore import QProcess, QObject
from PyQt5 import QtWidgets
import subprocess, pathlib, os, sys, logging

def __run_command( app, cmd, all_args, working_dir ):
    all_args = [str(arg) for arg in all_args]
    app.log.info( '%s %s' % (cmd, ' '.join( all_args ) ) )
    proc = QProcess()
    proc.setStandardInputFile( proc.nullDevice() )
    proc.setStandardOutputFile( proc.nullDevice() )
    proc.setStandardErrorFile( proc.nullDevice() )
    proc.startDetached( cmd, all_args, str( working_dir ) )

def asUtf8( s ):
    if isinstance( s, pathlib.Path ):
        s = str( s )

    if type( s ) == str:
        return s.encode( 'utf-8' )
    else:
        return s

def __run_command_with_output( app, cmd, args ):
    app.log.info( '%s %s' % (cmd, ' '.join( args )) )

    try:
        cmd = asUtf8( cmd )
        args = [asUtf8( arg ) for arg in args]
        proc = subprocess.Popen(
                    [cmd]+args,
                    close_fds=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                    )

        output = proc.stdout.read()
        proc.wait()

    except EnvironmentError as e:
        return 'error running %s %s: %s' % (cmd, ' '.join( args ), str(e))

    return output

# Uncomment below for terminal log messages
# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(QTextEditLogger, self).__init__(parent)
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class MyDialog(QtWidgets.QDialog, QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        logTextBox = QTextEditLogger(self)
        # You can format what is printed to text box
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)

        self._button = QtWidgets.QPushButton(self)
        self._button.setText('Test Me')

        layout = QtWidgets.QVBoxLayout()
        # Add the showLayout_new logging box widget to the layout
        layout.addWidget(logTextBox.widget)
        layout.addWidget(self._button)
        self.setLayout(layout)

        # Connect signal to slot
        self._button.clicked.connect(self.test)

    def test(self):
        logging.debug('damn, a bug')
        logging.info('something to remember')
        logging.warning('that\'s not right')
        logging.error('foobar')

app = QtWidgets.QApplication(sys.argv)
dlg = MyDialog()
dlg.show()
dlg.raise_()
sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:38 AM
# © 2017 - 2018 DAMGteam. All rights reserved