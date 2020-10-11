
# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import time
import sys

from PySide2 import QtCore, QtWidgets, QtGui


class Worker(QtCore.QObject):
    """A worker that does something in a thread it's been moved to

    Args:
        QtCore ([type]): [description]
    """

    finished = QtCore.Signal()  # emitted after something is finished

    @QtCore.Slot()
    def do_something(self):
        """Do something that takes time
        """
        print("worker started")
        time.sleep(2)
        print("worker finished")
        self.finished.emit()


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # Setup worker on a different therad than main
        self.thread = QtCore.QThread()
        self.thread.start()

        # Create the worker and move it off the main thread
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        # Layout
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Widgets
        self.first_btn = QtWidgets.QPushButton("Worker Button")
        second_btn = QtWidgets.QPushButton("Another Button")
        for btn in [self.first_btn, second_btn]:
            btn.setFixedHeight(50)

        # Set layouts
        main_layout.addWidget(self.first_btn)
        main_layout.addWidget(second_btn)

        # Logic
        self.first_btn.clicked.connect(self.worker.do_something)
        self.first_btn.clicked.connect(self.set_waiting)
        second_btn.clicked.connect(self.do_something_else)
        self.worker.finished.connect(self.reset_btn)

    @QtCore.Slot()
    def do_something_else(self):
        """Another button doing something else. doesn't block the gui
        """
        print("doing something else")

    @QtCore.Slot()
    def set_waiting(self):
        """Set the button to say waiting
        """
        self.first_btn.setText("Waiting")

    @QtCore.Slot()
    def reset_btn(self):
        """Reset the button's text when the worker finished
        """
        self.first_btn.setText("Worker Button")

    def closeEvent(self, event):
        """Closes the thread before the GUI closes

        Args:
            event ([type]): [description]
        """
        print("closing")
        self.thread.quit()
        self.thread.wait()
        super(Main, self).closeEvent(event)


def start():
    app = QtWidgets.QApplication(sys.argv)

    gui = Main()
    gui.show()
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
