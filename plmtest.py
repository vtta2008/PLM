# -*- coding: utf-8 -*-
"""

Script Name: Plm.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Manager

"""
import random
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QVBoxLayout, QPushButton, QWidget, QLineEdit
from PyQt5.QtGui import QIntValidator

import appData as app
logger = app.logger

class WorkThread(QThread):
    ''' Streaming task in its window.
    Signals and Slots are used for communication between objects. '''

    # Declare a signal, with an argument (int) for transmission in the connected slots
    threadSignal = pyqtSignal(int)

    def __init__(self, startParm):
        super(WorkThread, self).__init__()
        self.startParm = startParm         # Initialize the parameters passed to the task

    def run(self, *args, **kwargs):
        c = self.startParm
        while True:
            QThread.msleep(200)
            c += 1
            self.threadSignal.emit(c)      # We disable the signal and pass arguments to the connected slot


class WorkThreadMain(QThread):
    ''' Streaming Main task '''

    threadSignalMain = pyqtSignal(int)
    def __init__(self, startParm):
        super(WorkThreadMain, self).__init__()
        self.startParm = startParm

    def run(self, *args, **kwargs):
        c = self.startParm
        while True:
            QThread.msleep(1000)
            c += 1
            self.threadSignalMain.emit(c)


class MsgBox(QDialog):
    """ Window initialization class for visualizing an additional stream
         and a button to close the stream window if the thread is stopped! """

    def __init__(self):
        super().__init__()

        layout     = QVBoxLayout(self)
        self.label = QLabel("")
        layout.addWidget(self.label)

        close_btn  = QPushButton("Close thread")
        layout.addWidget(close_btn)

        close_btn.clicked.connect(self.close)

        self.setGeometry(900, 65, 400, 80)
        self.setWindowTitle('MsgBox for WorkThread')


class MainWindow(QWidget):
    ''' Main Window '''

    def __init__(self):
        super(MainWindow, self).__init__()

        layout     = QVBoxLayout(self)
        self.labelMain = QLabel("The result of the Main task: ")
        layout.addWidget(self.labelMain)
        self.labelThread = QLabel("The result of the Thread task: ")
        layout.addWidget(self.labelThread)
        validator = QIntValidator(1, 999, self)
        validator.setBottom(1)
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Enter the initial parameter for the stream task")
        self.lineEdit.setValidator(validator)    # self.lineEdit will only take integers from 1 to 999
        layout.addWidget(self.lineEdit)

        self.btn = QPushButton("Start thread!")
        layout.addWidget(self.btn)
        self.btnMain = QPushButton("Start Main!")
        layout.addWidget(self.btnMain)
        self.setGeometry(550, 65, 300, 200)
        self.setWindowTitle('MainWindow')

        self.btn.clicked.connect(self.on_btn)
        self.btnMain.clicked.connect(self.on_btnMain)

        self.msg = MsgBox()
        self.thread     = None
        self.threadMain = None

    def on_btn(self):
        ''' Starting or Stopping an Additional Stream-WorkThread from the main window '''

        # Input parameters for transfer to the stream, if not specified, we pass default `0`
        startParm = int(self.lineEdit.text()) if self.lineEdit.text()!="" else 0
        if self.thread is None:
            self.thread = WorkThread(startParm)

            self.thread.threadSignal.connect(self.on_threadSignal)
            self.thread.start()

            self.btn.setText("Stop thread")
            self.lineEdit.hide()
        else:
            self.thread.terminate()
            self.thread = None
            self.btn.setText("Start thread")
            self.lineEdit.show()

    def on_threadSignal(self, value):
        ''' Visualization of streaming data-WorkThread. '''

        self.msg.label.setText(str(value))
        self.labelThread.setText("The result of the Thread task: " + str(value)) # We show also in the main window

        # We restore the rendering of the stream window if it was closed. The flow is working.
        if not self.msg.isVisible():
            self.msg.show()


    def on_btnMain(self):
        ''' Starting or Stopping the Main Thread-WorkThreadMain '''

        cM = random.randrange(1, 100)
        if self.threadMain is None:
            self.threadMain = WorkThreadMain(cM)
            self.threadMain.threadSignalMain.connect(self.on_threadSignalMain)
            self.threadMain.start()
            self.btnMain.setText("Stop Main")
        else:
            self.threadMain.terminate()
            self.threadMain = None
            self.btnMain.setText("Start Main")

    def on_threadSignalMain(self, value):
        ''' Visualization of streaming data WorkThreadMain '''

        self.labelMain.setText("The result of the Main task: " + str(value))


if __name__ == '__main__':
    app = QApplication([])
    mw  = MainWindow()
    mw.show()
    app.exec()

# ----------------------------------------------------------------------------