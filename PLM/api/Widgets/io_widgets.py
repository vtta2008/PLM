# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from PLM import globals
import subprocess

if globals.qtBindingMode == 'PyQt5':

    try:
        import PyQt5
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(globals.qtBindingMode, globals.qtVersion), shell=True).wait()
    finally:
        from PyQt5.QtWidgets    import (QAction, QWidgetAction, QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
                                        QToolButton, QCheckBox, QComboBox, QDockWidget, QGraphicsItem, QGraphicsPathItem,
                                        QGraphicsObject, QGraphicsScene, QGraphicsView, QGridLayout,
                                        QGroupBox, QItemDelegate, QLabel, QLCDNumber, QLineEdit, QMainWindow, QMenu,
                                        QMenuBar, QMessageBox, QPlainTextEdit, QProgressBar, QRubberBand, QSplashScreen,
                                        QStatusBar, QSystemTrayIcon, QTabBar, QTabWidget, QTextEdit, QToolBar, QUndoCommand, QWidget)
elif globals.qtBindingMode == 'PySide2':
    try:
        import PySide2
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(globals.qtBindingMode, globals.qtVersion), shell=True).wait()
    finally:
        from PySide2.QtWidgets  import (QAction, QWidgetAction, QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
                                        QToolButton, QCheckBox, QComboBox, QDockWidget, QGraphicsItem, QGraphicsPathItem,
                                        QGraphicsObject, QGraphicsScene, QGraphicsView, QGridLayout,
                                        QGroupBox, QItemDelegate, QLabel, QLCDNumber, QLineEdit, QMainWindow, QMenu,
                                        QMenuBar, QMessageBox, QPlainTextEdit, QProgressBar, QRubberBand, QSplashScreen,
                                        QStatusBar, QSystemTrayIcon, QTabBar, QTabWidget, QTextEdit, QToolBar, QUndoCommand, QWidget)

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved