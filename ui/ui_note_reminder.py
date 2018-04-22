import sys

from PyQt5.QtCore import QFile, QRegExp, QTextCodec, QTextStream
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFileDialog, QGridLayout, QLabel, QMainWindow, QMenu,
                             QMessageBox, QTextEdit)

from utilities import utils as func


def codec_name(codec):
    try:
        # Python v3.
        name = str(codec.name(), encoding='ascii')
    except TypeError:
        # Python v2.
        name = str(codec.name())

    return name


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.textEdit = QTextEdit()
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.setCentralWidget(self.textEdit)

        self.codecs = []
        self.findCodecs()

        self.previewForm = PreviewForm(self)
        self.previewForm.setCodecList(self.codecs)

        self.saveAsActs = []
        self.createActions()
        self.createMenus()

        self.resize(500, 400)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            inFile = QFile(fileName)
            if not inFile.open(QFile.ReadOnly):
                QMessageBox.warning(self, "Codecs",
                                    "Cannot read file %s:\n%s" % (fileName, inFile.errorString()))
                return

            data = inFile.readAll()

            self.previewForm.setEncodedData(data)
            if self.previewForm.exec_():
                self.textEdit.setPlainText(self.previewForm.decodedString())

    def save(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            outFile = QFile(fileName)
            if not outFile.open(QFile.WriteOnly | QFile.Text):
                QMessageBox.warning(self, "Codecs",
                                    "Cannot write file %s:\n%s" % (fileName, outFile.errorString()))
                return

            action = self.sender()
            codecName = action.data()

            out = QTextStream(outFile)
            out.setCodec(codecName)
            out << self.textEdit.toPlainText()

    def about(self):
        QMessageBox.about(self, "About Codecs",
                          "The <b>Codecs</b> example demonstrates how to read and "
                          "write files using various encodings.")

    def aboutToShowSaveAsMenu(self):
        currentText = self.textEdit.toPlainText()

        for action in self.saveAsActs:
            codecName = action.data()
            codec = QTextCodec.codecForName(codecName)
            action.setVisible(codec and codec.canEncode(currentText))

    def findCodecs(self):
        codecMap = []
        iso8859RegExp = QRegExp('ISO[- ]8859-([0-9]+).*')

        for mib in QTextCodec.availableMibs():
            codec = QTextCodec.codecForMib(mib)
            sortKey = codec_name(codec).upper()
            rank = 0

            if sortKey.startswith('UTF-8'):
                rank = 1
            elif sortKey.startswith('UTF-16'):
                rank = 2
            elif iso8859RegExp.exactMatch(sortKey):
                if len(iso8859RegExp.cap(1)) == 1:
                    rank = 3
                else:
                    rank = 4
            else:
                rank = 5

            codecMap.append((str(rank) + sortKey, codec))

        codecMap.sort()
        self.codecs = [item[-1] for item in codecMap]

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O",
                               triggered=self.open)

        for codec in self.codecs:
            name = codec_name(codec)

            action = QAction(name + '...', self, triggered=self.save)
            action.setData(name)
            self.saveAsActs.append(action)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                               triggered=self.close)

        self.aboutAct = QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                                  triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.saveAsMenu = QMenu("&Save As", self)
        for action in self.saveAsActs:
            self.saveAsMenu.addAction(action)

        self.saveAsMenu.aboutToShow.connect(self.aboutToShowSaveAsMenu)

        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addMenu(self.saveAsMenu)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.helpMenu)

class PreviewForm(QDialog):
    def __init__(self, parent):
        super(PreviewForm, self).__init__(parent)

        self.encodingComboBox = QComboBox()
        encodingLabel = QLabel("&Encoding:")
        encodingLabel.setBuddy(self.encodingComboBox)

        self.textEdit = QTextEdit()
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.textEdit.setReadOnly(True)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.encodingComboBox.activated.connect(self.updateTextEdit)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QGridLayout()
        mainLayout.addWidget(encodingLabel, 0, 0)
        mainLayout.addWidget(self.encodingComboBox, 0, 1)
        mainLayout.addWidget(self.textEdit, 1, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Choose Encoding")
        self.resize(400, 300)

    def setCodecList(self, codecs):
        self.encodingComboBox.clear()
        for codec in codecs:
            self.encodingComboBox.addItem(codec_name(codec), codec.mibEnum())

    def setEncodedData(self, data):
        self.encodedData = data
        self.updateTextEdit()

    def decodedString(self):
        return self.decodedStr

    def updateTextEdit(self):
        mib = self.encodingComboBox.itemData(self.encodingComboBox.currentIndex())
        codec = QTextCodec.codecForMib(mib)

        data = QTextStream(self.encodedData)
        data.setAutoDetectUnicode(False)
        data.setCodec(codec)

        self.decodedStr = data.readAll()
        self.textEdit.setPlainText(self.decodedStr)

class WindowDialog(QDialog):

    def __init__(self, parent=None):
        super(WindowDialog, self).__init__(parent)

        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setWindowTitle('Note Reminder')
        self.mainMenu = MainWindow()
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.mainMenu, 0,0,1,1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = WindowDialog()
    mainWin.show()
    sys.exit(app.exec_())