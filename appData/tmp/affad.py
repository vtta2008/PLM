
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utilities import utils as func


class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self._pixmapHandle = None
        self.aspectRatioMode = Qt.KeepAspectRatio
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.zoomStack = []
        # self.canZoom = True
        # self.canPan = True


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.buildUI()

    def buildUI(self):

        picLayout = QHBoxLayout()
        pth = func.get_avatar('TrinhDo')
        label = QImageReader()
        label.graphicsItem(pth)
        change = QPushButton('change')
        change.clicked.connect(self.changeIt)


        self.layout.addWidget(picLayout)
        self.layout.addWidget(change)
        self.setLayout(self.layout)

    def changeIt(self):
        pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    window.createSample()
    sys.exit(app.exec_())