# -*- coding: utf-8 -*-
"""

Script Name: context.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    conftest.py is probably familiar to you if you ever used Pytest - it's a file used for specifying Pytest fixtures,
    hooks or loading external plugins.

"""
# -------------------------------------------------------------------------------------------------------------

from PySide2.QtCore    import QCoreApplication, QObject, QThread, Signal, Slot
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide2.QtWidgets import QPushButton, QComboBox

from time import sleep as tmSleep

class Task(QObject):

    sigOutput = Signal(int)

    # Initialization after Signals declared
    def __init__(self, CountBy):
        QObject.__init__(self)
        self.CntBy = CountBy
        self.Running = True
        self.Delay = 2

    def StartTask(self):
        CurCnt = 0
        while self.Running:  # Basically always True until ShutDown called
            CurCnt += 1 * self.CntBy
            self.sigOutput.emit(CurCnt)
            # If you do not give control to the Event Handler with a continuous
            # running process like this it does not matter if it is in its own
            # thread or not as due to rules of the GIL it will lock up the Event
            # Handler causing everything else to "Freeze" up especially in
            # regards to sending any signals into the Thread
            QCoreApplication.processEvents()
            # Using this to give time for things to occur in the GUI
            tmSleep(self.Delay)

    @Slot(int)
    def ReCountr(self, NewCntBy):
        self.CntBy = NewCntBy

    @Slot()
    def ShutDown(self):
        self.Running = False
        # All the Signals within a QThread must be disconnected from within
        # to prevent issues occuring on shutdown
        self.sigOutput.disconnect()
        # Make sure you pass control back to the Event Handler
        QCoreApplication.processEvents()


class Threader(QObject):
    sigNewCntBy = Signal(int)
    sigShutDwn = Signal()

    # Initialization after Signals declared
    def __init__(self, CntBy):
        QObject.__init__(self)
        self.CountBy = CntBy

        # Create the Listener
        self.Tasker = Task(self.CountBy)
        # Assign the Task Signals to Threader Slots
        self.Tasker.sigOutput.connect(self.ProcessOut)
        # Assign Threader Signals to the Task Slots
        self.sigNewCntBy.connect(self.Tasker.ReCountr)
        self.sigShutDwn.connect(self.Tasker.ShutDown)

        # Create the Thread
        self.Thred = QThread()
        # Move the Task Object into the Thread
        self.Tasker.moveToThread(self.Thred)
        # Assign the Task Starting Function to the Thread Call
        self.Thred.started.connect(self.Tasker.StartTask)
        # Start the Thread which launches Listener.Connect( )
        self.Thred.start()

    @Slot(int)
    def ProcessOut(self, Number):
        print('Current Count :', Number)

    @Slot(int)
    def NewCountBy(self, Number):
        self.sigNewCntBy.emit(Number)

    @Slot(int)
    def ShutDown(self):
        self.sigShutDwn.emit()
        self.Thred.quit()
        # All the Signals outside a QThread must be disconnected from
        # the outside to prevent issues occuring on shutdown
        self.sigNewCntBy.disconnect()
        self.sigShutDwn.disconnect()
        # This waits for the process within the Thread to stop were
        # upon it finalizes the Quit referenced above
        self.Thred.wait()


class Gui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.Started = False
        self.CountTask = QObject()

        self.btnStart = QPushButton('Click')
        self.btnStart.clicked.connect(self.DoTask)

        # Note if you use the X to close the window you
        # need to capture that event and direct it to do
        # self.ShutDown as well this is just a MUC
        self.btnQuit = QPushButton('Quit')
        self.btnQuit.clicked.connect(self.ShutDown)

        self.cbxNums = QComboBox()
        self.cbxNums.addItems(['1', '2', '3', '4', '5'])

        VBox = QVBoxLayout()
        VBox.addWidget(self.btnQuit)
        VBox.addWidget(self.btnStart)
        VBox.addWidget(self.cbxNums)

        self.setLayout(VBox)

    @Slot()
    def DoTask(self):
        Num = int(self.cbxNums.currentText())

        if self.Started:
            self.CountTask.NewCountBy(Num)
        else:
            self.Started = True
            self.CountTask = Threader(Num)

    @Slot()
    def ShutDown(self):
        self.CountTask.ShutDown()
        self.close()


if __name__ == '__main__':
    import sys
    MainEventThread = QApplication([])

    MainApp = Gui()
    MainApp.show()

    sys.exit(MainEventThread.exec_())


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:18 AM
# © 2017 - 2019 DAMGteam. All rights reserved