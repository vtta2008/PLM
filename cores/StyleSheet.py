# -*- coding: utf-8 -*-
"""

Script Name: StyleSheet.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
import platform

# PyQt5
from PyQt5.QtCore                   import QFile
from PyQt5.QtGui                    import QColor

# Plm
from bin                            import DAMG, DAMGDICT
from appData                        import DarkPalette
from cores.Loggers                  import Loggers
from appData                        import QSS_DIR
from toolkits.Core                  import TextStream
from plugins                        import Qt

qt_api = Qt.__binding__

class StyleSheet(DAMG):

    _filename                       = None
    _stylesheet                     = None
    filenames                       = DAMGDICT()

    def __init__(self, app=None):
        super(StyleSheet, self).__init__()

        self.logger = Loggers(__name__)
        self.app                    = app

    def getStyleSheet(self, fname):

        if qt_api == 'PyQt5':
            if self.app:
                palette = self.app.palette()
                palette.setColor(palette.Normal, palette.Link, QColor(DarkPalette.COLOR_BACKGROUND_LIGHT))
                self.app.setPalette(palette)

        self._filename              = self.getQssFile(fname)
        self._filename.open(QFile.ReadOnly | QFile.Text)
        ts                          = TextStream(self._filename)
        stylesheet                  = ts.readAll()
        stylesheet            = self.fixStyleSheet(stylesheet)
        return stylesheet

    def getQssFile(self, name):
        if name == 'dark':
            from scripts.rcs import darkstyle_rc
            filename = QFile(os.path.join(QSS_DIR, 'darkstyle.qss'))
        elif name == 'bright':
            from scripts.rcs import config_rc
            filename = QFile(os.path.join(QSS_DIR, 'brightstyle.qss'))
        elif name == 'chacoal':
            filename = QFile(os.path.join(QSS_DIR, 'chacoal.qss'))
        elif name == 'nuker':
            filename = QFile(os.path.join(QSS_DIR, 'nuker.qss'))
        else:
            if qt_api == 'PyQt5':
                from scripts.rcs import pyqt5_style_rc
            else:
                from scripts.rcs import pyside2_style_rc

            filename = QFile(os.path.join(QSS_DIR, 'style.qss'))

        return filename

    def fixStyleSheet(self, style):

        stylesheet                  = style

        if platform.system().lower() == 'darwin':
            mac_fix = '''
            QDockWidget::title
            {
                background-color: {0};
                text-align: center;
                height: 12px;
            }
            '''.format(DarkPalette.COLOR_BACKGROUND_NORMAL)
            stylesheet += mac_fix

        return stylesheet

    def removeStyleSheet(self):
        self._stylesheet                = None
        self.app.setStyleSheet(' ')
        return self._stylesheet

    def changeStyleSheet(self, key):
        self.removeStyleSheet()
        filename                        = self.getQssFile(key)
        self._stylesheet                      = self.getStyleSheet(filename)
        self.app.setStyleSheet(self._stylesheet)
        return self._stylesheet

    def set_style(self, key):
        fname = self.getQssFile(key)
        style = self.getStyleSheet(fname)
        self.changeStyleSheet(style)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, val):
        self._filename = val

    @property
    def stylesheet(self):
        return self._stylesheet

    @stylesheet.setter
    def stylesheet(self, val):
        self._stylesheet = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/06/2018 - 3:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved