#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility scripts to compile the qrc file. The script will
attempt to compile the qrc file using the following tools:
    - pyrcc5

Delete the compiled files that you don't want to use 
manually after running this script.
"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def compile_all():
    """
    Compile style.qrc  pyrcc5
    """
    logger.info('Compiling for PyQt5: style.qrc -> pyqt5_style_rc.py')
    os.system('pyrcc5 style.qrc -o pyqt5_style_rc.py')


if __name__ == '__main__':
    compile_all()
