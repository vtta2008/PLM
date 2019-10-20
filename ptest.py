import time
import sys
from PyQt5 import QtCore, QtWidgets

class countingWorker(QtCore.QObject):
    #explicit signal sent in the startCounting function
    set_box_signal = QtCore.pyqtSignal(int,str)

    #explicit slot that takes input from the start_counting_signal
    @QtCore.pyqtSlot(int,str)
    def startCounting(self,boxNumber,boxText):
        value = int(boxText)
        while True:
            value=1+value
            self.set_box_signal.emit(boxNumber,str(value))
            time.sleep(1)

class firstGui(QtWidgets.QDialog):
    #explicit signals from the start_counting_emitter function
    n = 7 # make this many counters
    start_counting_signal=QtCore.pyqtSignal(int, str)

    def __init__(self):
        super(firstGui, self).__init__()
        self.workers=[]
        self.threads=[]
        for j in range(self.n):
            self.workers.append(countingWorker())
            self.threads.append(QtCore.QThread())
            self.workers[j].moveToThread(self.threads[j])
        self.init_ui()

    def init_ui(self):
        self.boxes=[]
        self.starts=[]
        self.stops=[]
        for j in range(self.n):
            # Creating and naming the boxes
            self.boxes.append(QtWidgets.QLineEdit(self))
            self.boxes[j].setText('0')
            self.boxes[j].setObjectName('box'+str(j))
            # creating the start buttons
            self.starts.append(QtWidgets.QPushButton('Start', self))
            self.starts[j].setObjectName('start' + str(j))
            self.stops.append(QtWidgets.QPushButton('Stop', self))
            self.stops[j].setObjectName('stop' + str(j))

        # Creating a Horizontal Layout to add all the widgets
        self.hboxLayout = QtWidgets.QHBoxLayout(self)

        # Adding the widgets
        for j in range(self.n):
            self.hboxLayout.addWidget(self.boxes[j])
            self.hboxLayout.addWidget(self.starts[j])
            self.hboxLayout.addWidget(self.stops[j])

        # Setting the hBoxLayout as the main layout
        self.setLayout(self.hboxLayout)
        self.setWindowTitle('gui_4b')

        # making all of the connections
        for j in range(self.n):
            self.starts[j].clicked.connect(self.start_counting_emitter)
            self.stops[j].clicked.connect(self.stop_counting)
            self.workers[j].set_box_signal.connect(self.set_box_text)

        # show the GUI
        self.show()

    # this is an implicit slot for the startbuttons to connect to
    def start_counting_emitter(self):
        start_button_name=self.sender().objectName()
        start_number=int(start_button_name[5:])
        self.start_counting_signal.connect(self.workers[start_number].startCounting)
        if not self.threads[start_number].isRunning():
           self.threads[start_number].start()
           print('thread '+str(start_number)+' started')
           self.start_counting_signal.emit(start_number,self.boxes[start_number].text())
        self.start_counting_signal.disconnect(self.workers[start_number].startCounting)

    # implicit slot of the stop buttons
    def stop_counting(self):
        stop_button_name = self.sender().objectName()
        stop_number = int(stop_button_name[4:])
        if self.threads[stop_number].isRunning():
            self.threads[stop_number].terminate()
            print('thread '+str(stop_number)+' terminated')

    # explicit slot that takes input from the countingWorker and sets the text of the provided box
    @QtCore.pyqtSlot(int,str)
    def set_box_text(self,boxNumber,boxText):
        self.boxes[boxNumber].setText(boxText)

a = QtCore.QThreadPool()

b = a.activeThreadCount()

print(b)

def main():
    app = QtWidgets.QApplication(sys.argv)
    a = firstGui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()