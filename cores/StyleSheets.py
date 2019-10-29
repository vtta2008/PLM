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
from PyQt5.QtCore                    import QFile, QTextStream

# Plm
from cores.base                     import DAMG
from cores.Loggers                  import Loggers
from appData                        import QSS_DIR
from bin.resources.qss import darkstyle_rc, tooltips_rc

class StyleSheets(DAMG):

    key = 'styleSheets'

    def __init__(self, style=None, parent=None):
        super(StyleSheets, self).__init__(parent)

        self.logger = Loggers()

        self.style = style

        if self.style == 'dark':
            stylesheet = self.darkstyle()
        elif self.style == 'bright':
            stylesheet = self.brightstyle()
        else:
            stylesheet = None

        self.changeStylesheet = stylesheet

    def darkstyle(self):
        f = QFile(os.path.join(QSS_DIR, 'darkstyle.qss'))
        stylesheet = self.load_stylesheet(f)

        return stylesheet

    def brightstyle(self):
        f = QFile(os.path.join(QSS_DIR, 'brightstyle.qss'))
        stylesheet = self.load_stylesheet(f)

        return stylesheet

    def load_stylesheet(self, f):
        if not f.exists():
            self.logger.error('Unable to load stylesheet, file not found in resources')
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