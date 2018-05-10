#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A simple example of use.

Load an ui made in QtDesigner and apply the DarkStyleSheet.

Requirements:
    - Python 3
    - PyQt5

.. note.. :: qdarkgraystyle does not have to be installed to run
    the example

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """

import logging
import unittest
import sys
import os

from PyQt5 import QtWidgets, QtCore

import qdarkgraystyle
from appPackages.qdarkgraystyle.example.ui import example_pyqt5_ui as example_ui


class TestPyQt5(unittest.TestCase):

    def setUp(self):
        super(TestPyQt5, self).setUp()

    def test_create_main_window(self):
        """
        Application entry point
        """
        logging.basicConfig(level=logging.DEBUG)
        # create the application and the main window
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()

        # setup ui
        ui = example_ui.Ui_MainWindow()
        ui.setupUi(window)

        # setup stylesheet
        app.setStyleSheet(qdarkgraystyle.load_stylesheet())

        # auto quit after 2s when testing on travis-ci
        QtCore.QTimer.singleShot(2000, app.exit)

        # run
        window.show()
        app.exec_()
