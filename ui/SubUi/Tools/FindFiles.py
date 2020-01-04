#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Script Name: FindFile.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is a tool to find file name inside a specific directory

"""

# -------------------------------------------------------------------------------------------------------------

import sys

from PyQt5.QtCore           import (QDir, QIODevice, QFile, QFileInfo, Qt, QTextStream, QUrl)
from PyQt5.QtGui            import QDesktopServices
from PyQt5.QtWidgets        import (QAbstractItemView, QApplication, QComboBox, QFileDialog, QGridLayout, QHBoxLayout, QWidget,
                                    QHeaderView, QProgressDialog, QTableWidget, QTableWidgetItem, )

from appData                import SiPoExp, SiPoPre
from devkit.Widgets         import Widget, Button, Label
from devkit.Gui             import AppIcon

class FindFiles(Widget):

    key = 'FindFiles'

    def __init__(self, parent=None):
        super(FindFiles, self).__init__(parent)
        self.setWindowIcon(AppIcon(32, "FindFiles"))

        central_widget = QWidget(self)
        self.layout = QGridLayout(self)
        central_widget.setLayout(self.layout)

        self.buildUI()

    def buildUI(self):

        browseButton = Button({'txt': "&Browse...", 'cl': self.browse})
        findButton = Button({'txt': "&Find", 'cl': self.find})

        self.fileComboBox = self.createComboBox("*")
        self.textComboBox = self.createComboBox()
        self.directoryComboBox = self.createComboBox(QDir.currentPath())

        fileLabel = Label({'txt': "Named:"})
        textLabel = Label({'txt': "Containing text: "})
        directoryLabel = Label({'txt': "In directory: "})

        self.filesFoundLabel = Label()
        self.createFilesTable()

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(findButton)

        self.layout = QGridLayout()
        self.layout.addWidget(fileLabel, 0, 0)
        self.layout.addWidget(self.fileComboBox, 0, 1, 1, 2)
        self.layout.addWidget(textLabel, 1, 0)
        self.layout.addWidget(self.textComboBox, 1, 1, 1, 2)
        self.layout.addWidget(directoryLabel, 2, 0)
        self.layout.addWidget(self.directoryComboBox, 2, 1)
        self.layout.addWidget(browseButton, 2, 2)
        self.layout.addWidget(self.filesTable, 3, 0, 1, 3)
        self.layout.addWidget(self.filesFoundLabel, 4, 0)
        self.layout.addLayout(buttonsLayout, 5, 0, 1, 3)
        self.setLayout(self.layout)

        self.resize(700, 300)

    def browse(self):
        directory = QFileDialog.getExistingDirectory(self, "Find Files",
                                                     QDir.currentPath())

        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(self.directoryComboBox.findText(directory))

    @staticmethod
    def updateComboBox(comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    def find(self):
        self.filesTable.setRowCount(0)

        fileName = self.fileComboBox.currentText()
        text = self.textComboBox.currentText()
        path = self.directoryComboBox.currentText()

        self.updateComboBox(self.fileComboBox)
        self.updateComboBox(self.textComboBox)
        self.updateComboBox(self.directoryComboBox)

        self.currentDir = QDir(path)
        if not fileName:
            fileName = "*"
        files = self.currentDir.entryList([fileName],
                                          QDir.Files | QDir.NoSymLinks)

        if text:
            files = self.findFiles(files, text)
        self.showFiles(files)

    def findFiles(self, files, text):
        progressDialog = QProgressDialog(self)

        progressDialog.setCancelButtonText("&Cancel")
        progressDialog.setRange(0, files.count())
        progressDialog.setWindowTitle("Find Files")

        foundFiles = []

        for i in range(files.count()):
            progressDialog.setValue(i)
            progressDialog.setLabelText("Searching file number %d of %d..." % (i, files.count()))
            QApplication.processEvents()

            if progressDialog.wasCanceled():
                break

            inFile = QFile(self.currentDir.absoluteFilePath(files[i]))

            if inFile.open(QIODevice.ReadOnly):
                stream = QTextStream(inFile)
                while not stream.atEnd():
                    if progressDialog.wasCanceled():
                        break
                    line = stream.readLine()
                    if text in line:
                        foundFiles.append(files[i])
                        break

        progressDialog.close()

        return foundFiles

    def showFiles(self, files):
        for fn in files:
            file = QFile(self.currentDir.absoluteFilePath(fn))
            size = QFileInfo(file).size()

            fileNameItem = QTableWidgetItem(fn)
            fileNameItem.setFlags(fileNameItem.flags() ^ Qt.ItemIsEditable)
            sizeItem = QTableWidgetItem("%d KB" % (int((size + 1023) / 1024)))
            sizeItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            sizeItem.setFlags(sizeItem.flags() ^ Qt.ItemIsEditable)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, sizeItem)

        self.filesFoundLabel.setText("%d file(s) found (Double click on a file to open it)" % len(files))

    def createComboBox(self, text=""):
        comboBox = QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(SiPoExp, SiPoPre)
        return comboBox

    def createFilesTable(self):
        self.filesTable = QTableWidget(0, 2)
        self.filesTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.filesTable.setHorizontalHeaderLabels(("File Name", "Size"))
        self.filesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)

        self.filesTable.cellActivated.connect(self.openFileOfItem)

    def openFileOfItem(self, row, column):
        item = self.filesTable.item(row, 0)
        QDesktopServices.openUrl(QUrl(self.currentDir.absoluteFilePath(item.text())))

def main():
    app = QApplication(sys.argv)
    window = FindFiles()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()