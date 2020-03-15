# -*- coding: utf-8 -*-
"""

Script Name: StyleSheet.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import platform

# PLM
from PLM.commons                    import DAMG, DAMGDICT
from PLM.commons.Core               import TextStream, File, QssFile
from PLM.configs                    import DarkPalette
from PLM.cores                      import Loggers


class StyleSheet(DAMG):

    key                             = 'StylesSheet'
    _filename                       = None
    _stylesheet                     = None
    filenames                       = DAMGDICT()

    def __init__(self, app=None):
        super(StyleSheet, self).__init__()

        self.logger                 = Loggers(__name__)
        self.app                    = app

    def getStyleSheet(self, style):

        self._filename              = self.getQssFile(style)
        self._filename.open(File.ReadOnly | File.Text)
        ts                          = TextStream(self._filename)
        stylesheet                  = ts.readAll()
        self._stylesheet            = self.fixStyleSheet(stylesheet)

        return stylesheet

    def getQssFile(self, style):
        if style == 'dark':
            pass
        else:
            pass
        return QssFile(style)

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
        self._filename                  = ''
        self._stylesheet                = ''

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