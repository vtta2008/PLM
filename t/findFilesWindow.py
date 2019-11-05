# -*- coding: utf-8 -*-
"""

Script Name: findFilesWindow.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import sys
import csv, codecs
from PyQt5.QtCore import Qt, QDir, QFile, QFileInfo, QUrl, QStandardPaths
from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QCheckBox,
                             QApplication, QAction, QMessageBox, QPushButton,
                             QFileDialog, QHeaderView, QLineEdit, QAbstractItemView)
from PyQt5.QtGui import QIcon, QDesktopServices

###################################################################
myblue = "#fce94f"
home = QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0]
username = home.rpartition("/")[-1]
media = "/media/" + username

music = QStandardPaths.standardLocations(QStandardPaths.MusicLocation)[0]
videos = QStandardPaths.standardLocations(QStandardPaths.MoviesLocation)[0]
documents = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]
pictures = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)[0]
downloads = QStandardPaths.standardLocations(QStandardPaths.DownloadLocation)[0]
apps = QStandardPaths.standardLocations(QStandardPaths.ApplicationsLocation)[0]
temp = QStandardPaths.standardLocations(QStandardPaths.TempLocation)[0]
config = QStandardPaths.standardLocations(QStandardPaths.ConfigLocation)[0]
appdata = QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)[0]


class ListBox(QMainWindow):
    def __init__(self):
        super(ListBox, self).__init__()
        self.fileList = []
        self.folderlist = []
        self.allFolders = []
        self.dir = QDir.homePath()
        self.subdir = QDir.homePath()
        self.setGeometry(0, 0, 800, 450)
        self.setMinimumSize(500, 300)
        self.setContentsMargins(10, 10, 10, 0)
        self.setWindowIcon(QIcon.fromTheme('kfind'))
        self.setWindowTitle("Find Files")
        ##toolbar######################################################
        self.tb = self.addToolBar("Tools")
        self.tb.setMovable(False)
        self.tb.setContextMenuPolicy(Qt.PreventContextMenu)
        self.findEdit = QLineEdit("*")
        self.findAct = QAction(QIcon.fromTheme('edit-find'), "find", self,
                               statusTip="find Files",
                               triggered=self.findMyFiles)
        self.findEdit.addAction(self.findAct, QLineEdit.LeadingPosition)
        self.findEdit.setPlaceholderText("find")
        self.findEdit.setToolTip("for example: *word*")
        self.findEdit.setStatusTip("for example: *word*")
        self.tb.addWidget(self.findEdit)
        self.findEdit.returnPressed.connect(self.findMyFiles)

        self.tb.addSeparator()

        self.folderEdit = QLineEdit()
        self.folderAct = QAction(QIcon.fromTheme('document-open'), "change Folder", self,
                                 statusTip="change Folder",
                                 triggered=self.changeFolder)
        self.folderEdit.addAction(self.folderAct, QLineEdit.LeadingPosition)
        self.folderEdit.setPlaceholderText("insert folder path")
        self.folderEdit.setText(self.dir)
        #      self.folderEdit.textChanged.connect(self.setDir)
        self.folderEdit.returnPressed.connect(self.findMyFiles)
        self.tb.addWidget(self.folderEdit)

        self.tb.addSeparator()

        #      self.addToolBarBreak()
        self.noDot = QCheckBox("include hidden files")
        #      self.tb2 = self.addToolBar("hidden")
        #      self.tb2.addWidget(self.noDot)
        ##Listbox##########################################################
        self.lb = QTableWidget()
        self.lb.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.lb.setColumnCount(2)
        self.lb.setColumnWidth(0, 300)
        #      self.lb.setSelectionBehavior(self.lb.SelectRows)
        self.lb.setSelectionMode(self.lb.SingleSelection)
        self.lb.cellDoubleClicked.connect(self.doubleClicked)
        self.lb.itemClicked.connect(self.getItem)
        self.lb.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lb.horizontalHeader().setStretchLastSection(True)
        self.lb.setAlternatingRowColors(True)
        self.verticalHeader = QHeaderView(Qt.Vertical)
        self.lb.setVerticalHeader(self.verticalHeader)
        self.lb.horizontalHeader().setStretchLastSection(True)
        self.lb.setHorizontalHeaderItem(0, QTableWidgetItem("Filename"))
        self.lb.setHorizontalHeaderItem(1, QTableWidgetItem("Path"))
        self.verticalHeader.setDefaultSectionSize(24)
        self.lb.verticalHeader().hide()
        self.lb.setToolTip("double click first column to open file\nsecond column to open file parent folder")
        self.setCentralWidget(self.lb)
        self.findEdit.setFocus()
        self.statusBar().showMessage("Ready")
        print("Welcome\nPython Version: " + sys.version[:5])
        print("home is: " + home)
        self.setStyleSheet(stylesheet(self))

        self.copyBtn = QPushButton("copy filepath")
        self.copyBtn.clicked.connect(self.copyPath)
        self.copyBtn.setFlat(True)
        self.statusBar().addPermanentWidget(self.copyBtn)

        self.dir = self.folderEdit.text()

    #      self.show()
    ## def ####################################

    def removeAllRows(self):
        print("removing all rows")
        for row in range(0, self.lb.rowCount()):
            self.lb.removeRow(row)

    def removeDuplicates(self):
        for row in range(self.lb.rowCount()):
            if self.lb.item(row, 1) == self.lb.item(row + 1, 1):
                print("removing Row", str(row))
                self.lb.removeRow(row)

    def selectedRow(self):
        if self.lb.selectionModel().hasSelection():
            row = self.lb.selectionModel().selectedIndexes()[0].row()
            return int(row)

    def selectedColumn(self):
        column = self.lb.selectionModel().selectedIndexes()[0].column()
        return int(column)

    def getItem(self):
        row = self.selectedRow()
        column = self.selectedColumn()
        item = self.lb.item(row, column)
        if column == 1:
            myfile = item.text()
        else:
            myfile = self.lb.item(row, 1).text() + "/" + self.lb.item(row, 0).text()
        self.msg(myfile, 0)

    def copyPath(self):
        if self.lb.selectionModel().hasSelection():
            row = self.selectedRow()
            column = self.selectedColumn()
            myfile = self.lb.item(row, 1).text() + "/" + self.lb.item(row, 0).text()
            clip = QApplication.clipboard()
            clip.setText(myfile)
            self.msg("filepath copied!", 0)
        else:
            self.msg("nothing selected!", 0)

    def doubleClicked(self):
        row = self.selectedRow()
        column = self.selectedColumn()
        item = self.lb.item(row, column)
        if column == 1:
            myfile = item.text()
        else:
            myfile = self.lb.item(row, 1).text() + "/" + self.lb.item(row, 0).text()
        if QFile.exists(myfile):
            print("file exists: ", myfile)
            QDesktopServices.openUrl(QUrl("file://" + myfile))

    def setFolder(self):
        self.dir = ""
        self.folderEdit.setText(self.cmb.currentText())
        if not self.findEdit.text() == "*":
            self.setDir()
            self.findMyFiles()
        else:
            message = "please type a word to find"
            self.msg(message, 0)
            self.msgbox(message)

    def setDir(self):
        self.dir = self.folderEdit.text()

    def findMyFiles(self):
        self.folderlist = []
        self.allFolders = []
        self.lb.clearContents()
        self.dir = self.folderEdit.text()
        if not self.findEdit.text() == "*":
            self.lb.setRowCount(0)
            self.findFiles(self.dir)
            self.findFolders(self.dir)
            self.findSufolders()
            self.getFiles()
            self.removeDuplicates()
            if not self.lb.rowCount() == 0:
                self.msg("found " + str(self.lb.rowCount()) + " Files", 0)
            else:
                self.msg("nothing found", 0)
        else:
            message = "please type a word to find"
            self.msg(message, 0)
            self.msgbox(message)

    def findFolders(self, path):
        fileName = "*"
        currentDir = QDir(path)
        if self.noDot.isChecked():
            files = currentDir.entryList([fileName], QDir.AllDirs)
        else:
            files = currentDir.entryList([fileName], QDir.AllDirs | QDir.NoDotAndDotDot)
        for line in files:
            self.folderlist.append(path + "/" + line)

    def findSufolders(self):
        for folders in self.folderlist:
            self.allFolders.append(folders)
            self.findNewFolders(folders)

    def findNewFolders(self, path):
        fileName = "*"
        currentDir = QDir(path)
        files = currentDir.entryList([fileName], QDir.AllDirs | QDir.NoDotAndDotDot)
        for line in files:
            self.allFolders.append(path + "/" + line)
            self.findNewFolders(path + "/" + line)

    def findFiles(self, path):
        findName = self.findEdit.text()
        currentDir = QDir(path)
        self.msg("searching in " + currentDir.path(), 0)
        files = currentDir.entryList([findName], QDir.AllEntries | QDir.System | QDir.Drives)
        for line in files:
            self.lb.insertRow(0)
            self.lb.setItem(0, 0, QTableWidgetItem(line))
            self.lb.setItem(0, 1, QTableWidgetItem(path))  # + "/" + line))

    def getFiles(self):
        for mf in self.allFolders:
            self.findFiles(mf)

    def changeFolder(self):
        newfolder = QFileDialog.getExistingDirectory(self, "Find Files", self.dir)
        if newfolder:
            self.folderEdit.setText(newfolder)

    def closeEvent(self, event):
        print("goodbye")

    def msg(self, message, timeout):
        self.statusBar().showMessage(message, timeout)

    def msgbox(self, message):
        QMessageBox.warning(self, "'Find Files' Message", message, defaultButton=QMessageBox.Ok)


##stylesheet##########################################################
def stylesheet(self):
    return """
QTableWidget
{
background: #e9e9e9;
selection-color: white;
border: 1px solid lightgrey;
selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #729fcf, stop: 1  #204a87);
color: #202020;
outline: 0;
} 
QTableWidget::item::hover{
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);
}
QTableWidget::item::focus
{
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #729fcf, stop: 1  #204a87);
border: 0px;
}
QHeaderView 
{
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                         stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                         stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    border: 0px solid grey;
    font-size: 9pt;
    font-weight: bold;
    color: #2e3436;
}
QStatusBar
{
font-size: 8pt;
color: #403a3a;
}
QToolBar
{
border: 0px;
background-color: transparent;
}
QToolBar::Separator
{
background-color: transparent;
width: 20px;
}
QMainWindow
{
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                         stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                         stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}
QLineEdit
{
font-size: 9pt;
background: #eeeeec;
height: 20px;
}
"""
##main##########################################################
# if __name__ == "__main__":
#
#    app = QApplication(sys.argv)
#    main = ListBox()
#    main.show()
#    if len(sys.argv) > 1:
#        main.folderEdit.setText(sys.argv[1])
# sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:20 AM
# © 2017 - 2018 DAMGteam. All rights reserved