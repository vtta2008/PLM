# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    This is our source code directory, which should be named by your application or package you are working on.
    Inside we have the usual __init__.py file signifying that it's a Python package, next there is __main__.py
    which is used when we want to run our application directly with python -m blueprint. Last source file here
    is the app.py which is here really just for demonstration purposes. In real project instead of this app.py
    you would have few top level source files and more directories (internal packages). We will get to contents
    of these files a little later. Finally, we also have resources directory here, which is used for any static
    content your application might need, e.g. images, keystore, etc.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, subprocess, logging
from PLM.commons.Version import Version
from PLM.commons.Global import Global

# -------------------------------------------------------------------------------------------------------------
""" Metadatas """

__envKey__                          = "PLM"
__appName__                         = "Pipeline Manager (PLM)"
__name__                            = __appName__
__file__                            = __appName__
__version__                         = Version()
__apiVersion__                      = Version(0, 0, 1)


def __copyright__():
    return 'Copyright (C) DAMGTEAM.'


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

cwd                                 = os.path.abspath(os.getcwd()).replace('\\', '/')
dirname                             = os.path.basename(cwd)

if not dirname == __envKey__.lower():
    treeLst                         = cwd.split('/')
    index                           = treeLst.index(__envKey__) + 1
    ROOT_APP                        = '/'.join(treeLst[0:index])
else:
    ROOT_APP                        = cwd

ROOT                                = os.path.join(ROOT_APP, __envKey__)
globals                             = Global()

try:
    os.getenv(__envKey__)
except KeyError:
    subprocess.Popen('SetX {0} {1}'.format(__envKey__, ROOT), shell=True).wait()
else:
    if os.getenv(__envKey__)   != ROOT:
        subprocess.Popen('SetX {0} {1}'.format(__envKey__, ROOT), shell=True).wait()
finally:
    globals.cfgable = True

logger.info("{0} version {1} under api version {0}".format(__appName__, __version__, __apiVersion__))

if globals.qtBindingMode == 'PyQt5':

    try:
        import PyQt5
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(globals.qtBindingMode, globals.qtVersion), shell=True).wait()
    finally:
        from PyQt5.QtCore       import (QObject, QByteArray, QDate, QDateTime, QEventLoop, QFile, QFileInfo, QIODevice,
                                        QPoint, QProcess, QRect, QRectF, QRunnable, QSettings, QSize, QTextStream, QThread,
                                        QThreadPool, QTime, QTimer, QTimeZone, QUrl, )

        from PyQt5.QtGui        import (QBrush, QColor, QCursor, QFont, QFontMetrics, QIcon, QImage, QIntValidator,
                                        QKeySequence, QPaintDevice, QPainter, QPainterPath, QPalette, QPen, QPixmap,
                                        QPolygon, QTransform, )

        from PyQt5.QtNetwork    import (QNetworkAccessManager, QNetworkCookie, QNetworkCookieJar, QNetworkReply,
                                        QNetworkRequest, )

        from PyQt5.QtWidgets    import (QAction, QWidgetAction, QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
                                        QToolButton, QCheckBox, QComboBox, QDockWidget, QGraphicsItem, QGraphicsPathItem,
                                        QGraphicsObject, QGraphicsScene, QGraphicsView, QGridLayout, QGroupBox,
                                        QItemDelegate, QLabel, QLineEdit, QMainWindow, QMenu, QMenuBar, QMessageBox,
                                        QPlainTextEdit, QProgressBar, QRubberBand, QSplashScreen, QStatusBar,
                                        QSystemTrayIcon, QTabBar, QTabWidget, QTextEdit, QToolBar, QUndoCommand, QWidget)


        from PyQt5.QtCore       import pyqtSlot as Slot, pyqtSignal as Signal, pyqtProperty as Property


elif globals.qtBindingMode == 'PySide2':

    try:
        import PySide2
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(globals.qtBindingMode, globals.qtVersion), shell=True).wait()
    finally:
        from PySide2.QtCore     import (QObject, QByteArray, QDate, QDateTime, QEventLoop, QFile, QFileInfo, QIODevice,
                                        QPoint, QProcess, QRect, QRectF, QRunnable, QSettings, QSize, QTextStream, QThread,
                                        QThreadPool, QTime, QTimer, QTimeZone, QUrl, )

        from PySide2.QtGui      import (QBrush, QColor, QCursor, QFont, QFontMetrics, QIcon, QImage, QIntValidator,
                                        QKeySequence, QPaintDevice, QPainter, QPainterPath, QPalette, QPen, QPixmap,
                                        QPolygon, QTransform, )

        from PySide2.QtNetwork  import (QNetworkAccessManager, QNetworkCookie, QNetworkCookieJar, QNetworkReply,
                                        QNetworkRequest, )

        from PySide2.QtWidgets  import (QAction, QWidgetAction, QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
                                        QToolButton, QCheckBox, QComboBox, QDockWidget, QGraphicsItem, QGraphicsPathItem,
                                        QGraphicsObject, QGraphicsScene, QGraphicsView, QGridLayout, QGroupBox,
                                        QItemDelegate, QLabel, QLineEdit, QMainWindow, QMenu, QMenuBar, QMessageBox,
                                        QPlainTextEdit, QProgressBar, QRubberBand, QSplashScreen, QStatusBar,
                                        QSystemTrayIcon, QTabBar, QTabWidget, QTextEdit, QToolBar, QUndoCommand, QWidget)

        from PySide2.QtCore     import Slot, Signal, Property



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:15 AM
# © 2017 - 2019 DAMGteam. All rights reserved