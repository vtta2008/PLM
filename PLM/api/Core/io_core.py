# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from PLM import globals
import subprocess

if globals.qtBindingMode == 'PyQt5':

    try:
        import PyQt5
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(globals.qtBindingMode, globals.qtVersion), shell=True).wait()
    finally:
        from PyQt5.QtCore       import (QObject, QByteArray, QDate, QDateTime, QEventLoop, QFile, QFileInfo, QIODevice,
                                        QPoint, QProcess, QRect, QRectF, QRunnable, QSettings, QSize, QTextStream, QThread,
                                        QThreadPool, QTime, QTimer, QTimeZone, QUrl, )
elif globals.qtBindingMode == 'PySide2':

    try:
        import PySide2
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(globals.qtBindingMode, globals.qtVersion), shell=True).wait()
    finally:
        from PySide2.QtCore     import (QObject, QByteArray, QDate, QDateTime, QEventLoop, QFile, QFileInfo, QIODevice,
                                        QPoint, QProcess, QRect, QRectF, QRunnable, QSettings, QSize, QTextStream, QThread,
                                        QThreadPool, QTime, QTimer, QTimeZone, QUrl, )


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved