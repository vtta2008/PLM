import sys

from PyQt5.QtCore import pyqtSignal, QObject, QSize, Qt, QUrl
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebPage


def cout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def cerr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


class FrameCapture(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super(FrameCapture, self).__init__()

        self._percent = 0
        self._page = QWebPage()
        self._page.mainFrame().setScrollBarPolicy(Qt.Vertical,
                                                  Qt.ScrollBarAlwaysOff)
        self._page.mainFrame().setScrollBarPolicy(Qt.Horizontal,
                                                  Qt.ScrollBarAlwaysOff)
        self._page.loadProgress.connect(self.printProgress)
        self._page.loadFinished.connect(self.saveResult)

    def load(self, url, outputFileName):
        cout("Loading %s\n" % url.toString())
        self._percent = 0
        index = outputFileName.rfind('.')
        self._fileName = index == -1 and outputFileName + ".png" or outputFileName
        self._page.mainFrame().load(url)
        self._page.setViewportSize(QSize(1024, 768))

    def printProgress(self, percent):
        if self._percent >= percent:
            return
        self._percent += 1
        while self._percent < percent:
            self._percent += 1
            cout("#")

    def saveResult(self, ok):
        cout("\n")
        # Crude error-checking.
        if not ok:
            cerr("Failed loading %s\n" % self._page.mainFrame().url().toString())
            self.finished.emit()
            return

        # Save each frame in different image files.
        self._frameCounter = 0
        self.saveFrame(self._page.mainFrame())
        self.finished.emit()

    def saveFrame(self, frame):
        fileName = self._fileName
        if self._frameCounter:
            index = fileName.rfind('.')
            fileName = "%s_frame%s%s" % (fileName[:index], self._frameCounter, fileName[index:])
        image = QImage(frame.contentsSize(), QImage.Format_ARGB32_Premultiplied)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        frame.documentElement().render(painter)
        painter.end()
        image.save(fileName)
        self._frameCounter += 1
        for childFrame in frame.childFrames():
            self.saveFrame(childFrame)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        cerr("www.damgteam.com")
        sys.exit(1)

    url = QUrl.fromUserInput(sys.argv[1])
    fileName = sys.argv[2]

    app = QApplication(sys.argv)

    capture = FrameCapture()
    capture.finished.connect(app.quit)
    capture.load(url, fileName)

    app.exec_()