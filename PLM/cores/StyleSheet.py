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
from PLM.options            import COLOR_BACKGROUND_NORMAL
from bin.damg               import DAMG, DAMGDICT
from bin.Core               import TextStream, File, QssFile
from bin.loggers import test_logger


class StyleSheet(DAMG):

    key                                 = 'StylesSheet'
    _filename                           = None
    _stylesheet                         = None
    filenames                           = DAMGDICT()

    def __init__(self, app=None):
        super(StyleSheet, self).__init__()

        self.logger                     = test_logger()
        self.app                        = app


    def getStyleSheet(self, style):
        if style == 'dark':
            # self.logger.info("Loading darkstyle_rc")
            pass
        elif style == 'PyQt5':
            # self.logger.info("Loading pyqt5_style_rc")
            pass
        elif style == 'PySide2':
            # self.logger.info("Loading pyside2_style_rc")
            pass
        elif style == 'pyqtgraph':
            # self.logger.info("Loading pyqtgraph_style_rc")
            pass
        else:
            style = None

        self._filename                  = QssFile(style)
        self._filename.open(File.ReadOnly | File.Text)
        ts                              = TextStream(self._filename)
        stylesheet                      = ts.readAll()
        self._stylesheet                = self.fixStyleSheet(stylesheet)

        return stylesheet

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
            '''.format(COLOR_BACKGROUND_NORMAL)
            stylesheet += mac_fix
        return stylesheet

    def removeStyleSheet(self):
        self._filename                  = ''
        self._stylesheet                = ''

    @classmethod
    def progressBar(self):
        qssPth                          = QssFile('progressBar')
        qssPth.open(File.ReadOnly | File.Text)
        ts                              = TextStream(qssPth)
        return ts.readAll()

    @property
    def filename(self):
        return self._filename

    @property
    def stylesheet(self):
        return self._stylesheet

    @filename.setter
    def filename(self, val):
        self._filename                  = val

    @stylesheet.setter
    def stylesheet(self, val):
        self._stylesheet                = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/06/2018 - 3:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved