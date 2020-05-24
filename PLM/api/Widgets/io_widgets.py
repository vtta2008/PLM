# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from PLM import GLobalSetting
import subprocess

if GLobalSetting.qtBinding == 'PyQt5':
    from PyQt5.QtWidgets    import (QAction, QWidgetAction, QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
                                    QToolButton, QCheckBox, QComboBox, QDockWidget, QGraphicsItem, QGraphicsPathItem,
                                    QGraphicsObject, QGraphicsScene, QGraphicsView, QGridLayout, QGroupBox, QItemDelegate,
                                    QLabel, QLCDNumber, QLineEdit, QMainWindow, QMenu, QMenuBar, QMessageBox,
                                    QPlainTextEdit, QProgressBar, QRubberBand, QSplashScreen, QStatusBar, QSystemTrayIcon,
                                    QTabBar, QTabWidget, QTextEdit, QToolBar, QUndoCommand, QWidget, QTableWidget, )
elif GLobalSetting.qtBinding == 'PySide2':
    from PySide2.QtWidgets  import (QAction, QWidgetAction, QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
                                    QToolButton, QCheckBox, QComboBox, QDockWidget, QGraphicsItem, QGraphicsPathItem,
                                    QGraphicsObject, QGraphicsScene, QGraphicsView, QGridLayout, QGroupBox, QItemDelegate,
                                    QLabel, QLCDNumber, QLineEdit, QMainWindow, QMenu, QMenuBar, QMessageBox,
                                    QPlainTextEdit, QProgressBar, QRubberBand, QSplashScreen, QStatusBar, QSystemTrayIcon,
                                    QTabBar, QTabWidget, QTextEdit, QToolBar, QUndoCommand, QWidget, QTableWidget, )

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved