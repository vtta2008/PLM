#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Initialise the QDarkGrayStyleSheet module when used with python.
    This modules provides a function to transparently load the stylesheets
    with the correct rc file.
"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """

import logging
import platform
from deprecated import deprecated

from PyQt5 import QtCore

from appPackages.qdarkgraystyle.qdarkgraystyle import compile_qrc, pyqt5_style_rc

__version__ = '1.0.2'

def _logger():
    return logging.getLogger('qdarkgraystyle')

def load_stylesheet():
    """
    Loads the stylesheet for use in a pyqt5 application.
    :return the stylesheet string
    """

    # Smart import of the rc file
    f = QtCore.QFile(':qdarkgraystyle/style.qss')
    if not f.exists():
        _logger().error('Unable to load stylesheet, file not found in '
                        'resources')
        return ''
    else:
        f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        ts = QtCore.QTextStream(f)
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

@deprecated(version='1.0.0', reason="You should use load_stylesheet")
def load_stylesheet_pyqt5():
    return load_stylesheet()
