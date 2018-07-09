# -*- coding: utf-8 -*-
"""

Script Name: StyleSheet.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, platform

# PyQt5
from PyQt5.QtCore import QObject, QFile, QTextStream

# Plm
from appData.scr._path import QSS_DIR
# from core.Loggers import SetLogger

class StyleSheets(QObject):

    def __init__(self, style=None, parent=None):
        super(StyleSheets, self).__init__(parent)
        self.logger = SetLogger(self)
        self.style = style
        if self.style == 'darkstyle':
            stylesheet = self.darkstyle()
        elif self.style == 'stylesheet':
            stylesheet = self.stylesheet()
        else:
            stylesheet = None

        self.changeStylesheet = stylesheet

    def darkstyle(self):
        f = QFile(os.path.join(QSS_DIR, 'darkstyle.qss'))
        stylesheet = self.load_stylesheet(f)
        return stylesheet

    def stylesheet(self):
        from plg_ins import pyqt5_style_rc
        f = QFile(os.path.join(QSS_DIR, 'stylesheet.qss'))
        stylesheet = self.load_stylesheet(f)
        return stylesheet

    def load_stylesheet(self, f):
        if not f.exists():
            self.logger.error('Unable to load stylesheet, file not found in resources')
            return ''
        else:
            f.open(QFile.ReadOnly | QFile.Text)
            ts = QTextStream(f)
            stylesheet = ts.readAll()
            if platform.system().lower() == 'darwin':  # see issue #12 on github
                mac_fix = '''
                QDockWidget::title
                {
                    background-color: #31363b;
                    text-align: center;
                    height: 12px;
                }
                '''
                stylesheet += mac_fix
            return stylesheet


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/06/2018 - 3:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved