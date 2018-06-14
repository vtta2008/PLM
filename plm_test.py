import sys, time
from multiprocessing import Process
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtWidgets import QProgressBar, QDialogButtonBox, QVBoxLayout, QApplication, QDialog


class Compute(QObject):
    def __init__(self, win, parent=None):
        super(Compute, self).__init__(parent)

        self.win = win

    def calculate(self):
        for i in range(100):
            self.progressBar(i)
            time.sleep(0.05)

    def progressBar(self, value):
        self.win.updatePb.emit(value)


# -------------------------------------------------------------------------------
class Form(QDialog):

    updatePb = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        bbox = QDialogButtonBox()
        bbox.setOrientation(Qt.Horizontal)
        bbox.setStandardButtons(QDialogButtonBox.Ok)
        layout = QVBoxLayout(self)
        layout.addWidget(self.progressBar)
        layout.addWidget(bbox)
        bbox.clicked.connect(self.calculate)

        self.updatePb.connect(self.progressBar.setValue)

    def calculate(self):
        co = Compute(self)
        p = Process(target=co.calculate)
        p.start()
        p.join()


app = QApplication(sys.argv)
layout = Form()
layout.show()
app.exec_()