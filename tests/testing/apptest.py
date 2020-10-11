# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """



import functools, sys

from PySide2 import QtCore


def _handleProcFinished(process, exitCode):
    stdOut = process.readAllStandardOutput()
    stdErr = process.readAllStandardError()

    print("Standard Out: {0}".format(stdOut))
    print("Standard Error:: {0}".format(stdOut))

app = QtCore.QCoreApplication(sys.argv)

proc = QtCore.QProcess()
proc.finished.connect(functools.partial(_handleProcFinished, proc))
proc.start("ping", ["www.google.com", "-n", "5"])

sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
