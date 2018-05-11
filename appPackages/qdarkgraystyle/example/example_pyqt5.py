#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A simple example of use.
Load an ui made in QtDesigner and apply the DarkStyleSheet.

Requirements:
    - Python 3
    - PyQt5

.. note.. :: qdarkgraystyle does not have to be installed to run the example
"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os, sys, logging

from PyQt5 import QtWidgets, QtCore
# make the example runnable without the need to install
abspath = os.path.abspath
dirname = os.path.dirname

sys.path.insert(0, abspath(dirname(abspath(__file__)) + '/..'))

from appPackages import qdarkgraystyle
from appPackages.qdarkgraystyle.example.ui import example_pyqt5_ui as example_ui

def main():
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
    ui.bt_delay_popup.addActions([
        ui.actionAction,
        ui.actionAction_C
    ])
    ui.bt_instant_popup.addActions([
        ui.actionAction,
        ui.actionAction_C
    ])
    ui.bt_menu_button_popup.addActions([
        ui.actionAction,
        ui.actionAction_C
    ])
    window.setWindowTitle('QDarkGrayStyle example')

    # tabify dock widgets to show bug #6
    window.tabifyDockWidget(ui.dockWidget1, ui.dockWidget2)

    # setup stylesheet
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    # auto quit after 2s when testing on travis-ci
    if '--travis' in sys.argv:
        QtCore.QTimer.singleShot(2000, app.exit)

    # run
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
