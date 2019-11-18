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

from PyQt5.QtWidgets import QApplication
import sys
app = QApplication(sys.argv)
a = app.desktop()
print(a)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:38 AM
# © 2017 - 2018 DAMGteam. All rights reserved