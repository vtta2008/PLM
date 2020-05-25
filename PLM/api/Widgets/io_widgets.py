# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from PLM import qtBinding

if qtBinding == 'PyQt5':
    from PyQt5.QtWidgets    import (QApplication, QAction, QShortcut, QWidgetAction, QVBoxLayout, QHBoxLayout,
                                    QPushButton, QToolButton, QCheckBox, QComboBox, QDockWidget, QGraphicsItem,
                                    QGraphicsObject, QGraphicsPathItem, QGraphicsScene, QGraphicsView, QGridLayout,
                                    QGroupBox, QItemDelegate, QLabel, QTextEdit, QLCDNumber, QLineEdit, QMainWindow,
                                    QMenu, QMenuBar, QMessageBox, QPlainTextEdit, QProgressBar, QRubberBand,
                                    QSplashScreen, QStatusBar, QSystemTrayIcon, QTabBar, QTabWidget, QTableWidget,
                                    QToolBar, QUndoCommand, QWidget, QSizePolicy, )
elif qtBinding == 'PySide2':
    from PySide2.QtWidgets import (QApplication, QAction, QShortcut, QWidgetAction, QVBoxLayout, QHBoxLayout,
                                    QPushButton, QToolButton, QCheckBox, QComboBox, QDockWidget, QGraphicsItem,
                                    QGraphicsObject, QGraphicsPathItem, QGraphicsScene, QGraphicsView, QGridLayout,
                                    QGroupBox, QItemDelegate, QLabel, QTextEdit, QLCDNumber, QLineEdit, QMainWindow,
                                    QMenu, QMenuBar, QMessageBox, QPlainTextEdit, QProgressBar, QRubberBand,
                                    QSplashScreen, QStatusBar, QSystemTrayIcon, QTabBar, QTabWidget, QTableWidget,
                                    QToolBar, QUndoCommand, QWidget, QSizePolicy, )

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved