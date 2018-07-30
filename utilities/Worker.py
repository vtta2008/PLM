# -*- coding: utf-8 -*-
"""

Script Name: Worker.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, time, traceback, unittest

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot,QRunnable, QObject, QThreadPool, QThread
from PyQt5.QtWidgets import QGridLayout, QWidget

# PLM
from ui.uikits.UiPreset import Label

# -------------------------------------------------------------------------------------------------------------
""" Signals """

class Signals(QObject):

    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

        - finished: No data
        - error: `tuple` (exctype, value, traceback.format_exc() )
        - result: `object` data returned from processing, anything

    '''

    workerFinished = pyqtSignal(int)
    workerReady = pyqtSignal(list, dict)
    dataReady = pyqtSignal(int, int)

    started = pyqtSignal()
    finished = pyqtSignal(int)
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

# -------------------------------------------------------------------------------------------------------------
""" Worker QRunnable """

class Worker(QRunnable):

    signals = Signals()
    workerFinished = signals.workerFinished
    workerReady = signals.workerReady
    dataReady = signals.dataReady

    def __init__(self, workerID=0, fn=None, *args, **kwargs):
        super(Worker, self).__init__()


        self.workerID = workerID
        self.fn = fn                            # Store constructor arguments (re-used for processing)
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):

        try:
            result = self.fn(*self.args, **self.kwargs, status = self.signals.status, progress = self.signals.progress)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)                                    # Return the result of the processing
        finally:
            self.signals.finished.emit(self.workerID)                                        # Done

# -------------------------------------------------------------------------------------------------------------
""" Thread """

class Thread(QThread):

    startSig = pyqtSignal(int)
    finishSig = pyqtSignal(int)

    def __init__(self, threadID, parent=None):
        super(Thread, self).__init__(parent)

        self.threadID = threadID

        self.startSig.connect(self.thread_start)
        self.finishSig.connect(self.thread_finish)

    @pyqtSlot()
    def thread_start(self):
        self.startSig.emit(self.threadID)

    @pyqtSlot()
    def thread_finish(self):
        self.finishSig.emit(self.threadID)

# -------------------------------------------------------------------------------------------------------------
""" Managing Thread """

class ThreadConsole(QWidget):

    def __init__(self, fn=print("Hello world"), parent=None):
        super(ThreadConsole, self).__init__(parent)

        self.setWindowTitle('Thread testing')

        self.numOfThread = QThreadPool().maxThreadCount()
        print("This pc can handle {0} threads optimally".format(self.numOfThread))

        self.fn = fn
        
        self.layout = QGridLayout(self)
        self.buildUI()
        self.setLayout(self.layout)
        self.setGeometry(300, 300, 300, 300)
        self.show()

        self.workers = {}
        self.threads = {}

        for i in range(self.numOfThread):
            self.setupThread(i)
            i += 1

        self.i = 0
        i = 0
        while i < self.numOfThread:
            self.startThread(i)

    def buildUI(self):

        self.labels = []

        for i in range(self.numOfThread):
            label = Label({'txt':'0'})
            self.labels.append(label)
            self.layout.addWidget(label, 0, i, 1, 1)
            i += 1

    def setupThread(self, i):

        self.workers[i] = Worker(workerID=i, fn=self.fn)

        self.threads[i] = Thread(i, self)
        self.threads[i].setObjectName("python thread{}"+str(i))
        self.threads[i].startSig.connect(self.threadStarted)
        self.threads[i].finishSig.connect(self.threadFinished)

        self.workers[i].workerFinished.connect(self.workerFinished)
        self.workers[i].workerFinished.connect(self.threads[i].quit)
        self.workers[i].dataReady.connect(self.workerResultReady)

        self.threads[i].started.connect(self.workers[i].run)

        self.destroyed.connect(self.threads[i].deleteLater)

    def startThread(self, i):
        self.threads[i].start()

    @pyqtSlot(int)
    def threadStarted(self, i):
        print('Thread {}  started'.format(i))
        print("Thread priority is {}".format(self.threads[i].priority()))

    @pyqtSlot(int)
    def threadFinished(self, i):
        print('Thread {} finished'.format(i))

    @pyqtSlot(int)
    def threadTerminated(self, i):
        print("Thread: {0} terminated".format(i))

    @pyqtSlot(int)
    def workerFinished(self, i):
        print('Worker {} finished'.format(i))

    @pyqtSlot(int, int)
    def workerResultReady(self, j, i):
        print("Worker {0} result returnhed".format(i))
        self.labels[i].setText("{}".format(j))

    def closeEvent(self, event):

        i=0
        while i < self.numOfThread:                 # Stop thread running
            self.threads[i].quit()
            i += 1

        i = 0
        while i < self.numOfThread:                 # Make sure window cannot be closed til all threads finish
            self.threads[i].wait()
            i += 1

        event.accept()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 14/06/2018 - 9:58 PM
# © 2017 - 2018 DAMGteam. All rights reserved