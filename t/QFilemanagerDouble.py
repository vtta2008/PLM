# -*- coding: utf-8 -*-
"""

Script Name: QFilemanagerDouble.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import sys
import os
import errno
import getpass
import socket
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence, QCursor, QDesktopServices

from t import findFilesWindow
from t import QTextEdit
from t import Qt5Player
from t import QAudioPlayer
from t import QImageViewer
from t import QWebViewer
from t import QTerminalFolder

from zipfile import ZipFile
import shutil
import subprocess
import stat
from send2trash import send2trash

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


class helpWindow(QMainWindow):
    def __init__(self):
        super(helpWindow, self).__init__()
        self.setStyleSheet(mystylesheet(myWindow()))
        self.helpText = """<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><!--StartFragment--><span style=" font-family:'Helvetica'; font-size:11pt; font-weight:600; text-decoration: underline; color:#2e3436;">Shortcuts:</span></p><br>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">rename File (F2)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">copy File(s) (Ctrl-C)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">paste File(s) (Ctrl-V)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">cut File(s) (Ctrl-X)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">open with TextEditor (F6)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">move File(s) to Trash(Del)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">delete File(s) (Shift+Del)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">find File(s) (Ctrl-F)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">play with vlc (F3)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">open folder in Terminal (F7)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">execute File in Terminal (F8)</span>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">go back (Backspace)</span></p>
<p style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Helvetica'; font-size:10pt; color:#2e3436;">refresh View (F5)</span></p>
<!--EndFragment--></p>
                                        """
        self.helpViewer = QLabel(self.helpText, self)
        self.helpViewer.setAlignment(Qt.AlignCenter)
        self.btnAbout = QPushButton("about")
        self.btnAbout.setFixedWidth(80)
        self.btnAbout.setIcon(QIcon.fromTheme("help-about"))
        self.btnAbout.clicked.connect(self.aboutApp)

        self.btnClose = QPushButton("Close")
        self.btnClose.setFixedWidth(80)
        self.btnClose.setIcon(QIcon.fromTheme("window-close"))
        self.btnClose.clicked.connect(self.close)

        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        layout.addWidget(self.helpViewer)
        layout.addStretch()
        layout.addWidget(self.btnAbout, alignment=Qt.AlignCenter)
        layout.addWidget(self.btnClose, alignment=Qt.AlignCenter)
        self.setCentralWidget(widget)

        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon.fromTheme("help-about"))

    def aboutApp(self):
        sysinfo = QSysInfo()
        myMachine = "currentCPU Architecture: " + sysinfo.currentCpuArchitecture() + "<br>" + sysinfo.prettyProductName() + "<br>" + sysinfo.kernelType() + " " + sysinfo.kernelVersion()
        title = "about QFileManager"
        message = """
                    <span style='color: #3465a4; font-size: 20pt;font-weight: bold;text-align: center;'
                    ></span></p><center><h3>QFileManager<br>1.0 Beta</h3></center>created by  
                    <a title='Axel Schneider' href='http://goodoldsongs.jimdo.com' target='_blank'>Axel Schneider</a> with PyQt5<br><br>
                    <span style='color: #555753; font-size: 9pt;'>©2019 Axel Schneider<br><br></strong></span></p>
                        """ + myMachine
        self.infobox(title, message)

    def infobox(self, title, message):
        QMessageBox(QMessageBox.Information, title, message, QMessageBox.NoButton, self,
                    Qt.Dialog | Qt.NoDropShadowWindowHint | Qt.FramelessWindowHint).show()


class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()

        self.setStyleSheet(mystylesheet(self))
        self.setWindowTitle("Filemanager")
        self.setWindowIcon(QIcon.fromTheme("system- file-manager"))
        self.process = QProcess()

        self.settings = QSettings("QFileManager", "QFileManager")
        self.clip = QApplication.clipboard()
        self.isInEditMode = False

        self.treeview = QTreeView()
        self.listview = QTreeView()

        self.cut = False
        self.folder_copied = ""

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.listview)

        hlay = QHBoxLayout()
        hlay.addWidget(self.splitter)

        wid = QWidget()
        wid.setLayout(hlay)
        self.createStatusBar()

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedHeight(18)
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setMaximum(100)
        self.statusBar().addPermanentWidget(self.progress_bar)

        self.setCentralWidget(wid)
        self.setGeometry(0, 26, 900, 500)

        path = QDir.rootPath()
        self.copyPath = ""
        self.copyList = []
        self.copyListNew = ""

        self.createActions()

        self.findfield = QLineEdit()
        self.findfield.returnPressed.connect(self.findFiles)
        self.findfield.addAction(QIcon.fromTheme("edit-find"), QLineEdit.LeadingPosition)
        self.findfield.setClearButtonEnabled(True)
        self.findfield.setFixedWidth(150)
        self.findfield.setPlaceholderText("find")
        self.findfield.setToolTip("press RETURN to find")
        self.findfield.setText("")

        self.tBar = self.addToolBar("Tools")
        self.tBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.tBar.setMovable(False)
        self.tBar.setIconSize(QSize(16, 16))
        self.tBar.addAction(self.createFolderAction)
        self.tBar.addAction(self.copyAction)
        self.tBar.addAction(self.cutAction)
        self.tBar.addAction(self.pasteAction)
        self.tBar.addSeparator()
        self.tBar.addAction(self.delActionTrash)
        self.tBar.addAction(self.delAction)
        self.tBar.addSeparator()
        self.tBar.addAction(self.terminalAction)
        self.tBar.addSeparator()
        self.tBar.addAction(self.helpAction)
        empty = QWidget()
        empty.setMinimumWidth(60)
        self.tBar.addWidget(empty)
        self.tBar.addAction(self.btnHome)
        self.tBar.addAction(self.btnDocuments)
        self.tBar.addAction(self.btnDownloads)
        self.tBar.addAction(self.btnMusic)
        self.tBar.addAction(self.btnVideo)
        empty = QWidget()
        empty.setMinimumWidth(20)
        self.tBar.addWidget(empty)
        self.tBar.addAction(self.btnBack)
        self.tBar.addAction(self.btnUp)
        empty = QWidget()
        empty.setMinimumWidth(20)
        self.tBar.addWidget(empty)
        self.cmb = QComboBox()
        self.cmb.activated.connect(self.setFolder)
        self.cmb.setFixedWidth(200)
        self.tBar.addWidget(self.cmb)
        empty = QWidget()
        empty.setMinimumWidth(30)
        self.tBar.addWidget(empty)
        self.tBar.addWidget(self.findfield)
        self.tBar.addAction(self.findFilesAction)

        self.dirModel = QFileSystemModel()
        self.dirModel.setReadOnly(False)
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.dirModel.setRootPath(QDir.rootPath())
        self.dirModel.setResolveSymlinks(True)

        self.fileModel = QFileSystemModel()
        self.fileModel.setReadOnly(False)
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.fileModel.setRootPath(QDir.rootPath())
        self.fileModel.setResolveSymlinks(True)

        self.listview.setRootIsDecorated(True)
        self.listview.setModel(self.fileModel)
        self.listview.header().resizeSection(0, 320)
        self.listview.header().resizeSection(1, 80)
        self.listview.header().resizeSection(2, 80)
        self.listview.setUniformRowHeights(True)
        self.listview.setExpandsOnDoubleClick(False)
        self.listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeview.setIndentation(12)
        self.listview.setSortingEnabled(True)
        self.listview.doubleClicked.connect(self.list_doubleClicked)
        self.listview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listview.setDragDropMode(QAbstractItemView.DragDrop)
        self.listview.setDragEnabled(True)
        self.listview.setAcceptDrops(True)
        self.listview.setDropIndicatorShown(True)
        self.listview.sortByColumn(0, Qt.AscendingOrder)

        self.treeview.setRootIsDecorated(True)
        self.treeview.setModel(self.dirModel)
        self.treeview.header().resizeSection(0, 320)
        self.treeview.header().resizeSection(1, 80)
        self.treeview.header().resizeSection(2, 80)
        self.treeview.setUniformRowHeights(True)
        self.treeview.setExpandsOnDoubleClick(False)
        self.treeview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeview.setIndentation(12)
        self.treeview.setSortingEnabled(True)
        self.treeview.doubleClicked.connect(self.list_doubleClicked)
        self.treeview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeview.setDragDropMode(QAbstractItemView.DragDrop)
        self.treeview.setDragEnabled(True)
        self.treeview.setAcceptDrops(True)
        self.treeview.setDropIndicatorShown(True)
        self.treeview.sortByColumn(0, Qt.AscendingOrder)

        docs = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]
        music = QStandardPaths.standardLocations(QStandardPaths.MusicLocation)[0]
        self.treeview.setRootIndex(self.dirModel.setRootPath(docs))
        self.listview.setRootIndex(self.fileModel.setRootPath(music))

        self.listview.clicked.connect(self.setNewWindowTitle)
        self.treeview.clicked.connect(self.setNewWindowTitle)
        self.treeview.setCurrentIndex(self.treeview.rootIndex())
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.setWindowTitle(path)

        self.fillCombo()

        self.splitter.setSizes([50, 50])

        print("Welcome to QFileManager")
        self.readSettings()
        self.enableHidden()
        self.treeview.setFocus()
        self.getRowCount()
        ind = self.cmb.findText(self.windowTitle())
        self.cmb.setCurrentIndex(ind)

    def fillCombo(self):
        self.cmb.addItem("/")
        ### media folder ###
        usb = QDir(media).entryList(["*"], QDir.Dirs | QDir.NoDot | QDir.NoDotDot)
        for disk in usb:
            self.cmb.addItem(media + "/" + disk)

        self.cmb.addItem(home)
        self.cmb.addItem(documents)
        self.cmb.addItem(pictures)
        self.cmb.addItem(music)
        self.cmb.addItem(videos)
        self.cmb.addItem(downloads)
        self.cmb.addItem(apps)
        self.cmb.addItem(appdata)
        self.cmb.addItem(config)
        self.cmb.addItem(home + "/.local")
        self.cmb.addItem("/bin")
        self.cmb.addItem(temp)
        #######################################################
        combolist = []
        for row in range(self.cmb.count()):
            combolist.append(self.cmb.itemText(row).rpartition("/")[2])
        #######################################################
        currentDir = QDir(home)
        disks = currentDir.entryList(["*"], QDir.Dirs | QDir.NoDot | QDir.NoDotDot)
        for disk in disks:
            if not disk in combolist:
                self.cmb.addItem(QDir.homePath() + "/" + disk)

    def setFolder(self):
        path = self.cmb.currentText()
        if self.listview.selectionModel().hasSelection():
            self.listview.setRootIndex(self.fileModel.setRootPath(path))
        if self.treeview.selectionModel().hasSelection():
            self.treeview.setRootIndex(self.dirModel.setRootPath(path))

    def setNewWindowTitle(self):
        if self.listview.hasFocus():
            self.treeview.clearSelection()
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).path()
            name = index.sibling(index.row(), 0).data()
            size = index.sibling(index.row(), 1).data()
            type = index.sibling(index.row(), 2).data()
            self.statusBar().showMessage("%s *** %s *** %s" % (name, type, size), 0)
        elif self.treeview.hasFocus():
            self.listview.clearSelection()
            index = self.treeview.selectionModel().currentIndex()
            path = self.dirModel.fileInfo(index).path()
            name = index.sibling(index.row(), 0).data()
            size = index.sibling(index.row(), 1).data()
            type = index.sibling(index.row(), 2).data()
            self.statusBar().showMessage("%s *** %s *** %s" % (name, type, size), 0)
        self.setWindowTitle(path)

    def getRowCount(self):
        count = 0
        if self.listview.hasFocus():
            index = self.listview.selectionModel().currentIndex()
            path = QDir(self.fileModel.fileInfo(index).absoluteFilePath())
            count = len(path.entryList(QDir.Files))
            self.statusBar().showMessage("%s %s" % (count, "Files"), 0)
        elif self.treeview.hasFocus():
            index = self.treeview.selectionModel().currentIndex()
            path = QDir(self.dirModel.fileInfo(index).absoluteFilePath())
            count = len(path.entryList(QDir.Files))
            self.statusBar().showMessage("%s %s" % (count, "Files"), 0)
        return count

    def closeEvent(self, e):
        print("writing settings ...\nGoodbye ...")
        self.writeSettings()

    def readSettings(self):
        print("reading settings ...")
        if self.settings.contains("pos"):
            pos = self.settings.value("pos", QPoint(200, 200))
            self.move(pos)
        else:
            self.move(0, 26)
        if self.settings.contains("size"):
            size = self.settings.value("size", QSize(800, 600))
            self.resize(size)
        else:
            self.resize(800, 600)
        if self.settings.contains("hiddenEnabled"):
            if self.settings.value("hiddenEnabled") == "false":
                self.hiddenEnabled = False
                self.enableHidden()
            else:
                self.hiddenEnabled = True
                self.enableHidden()

    def writeSettings(self):
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("size", self.size())
        self.settings.setValue("hiddenEnabled", self.hiddenEnabled, )

    def enableHidden(self):
        if self.hiddenEnabled == False:
            self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
            self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
            self.hiddenAction.setChecked(False)
            print("set hidden files to false")
        else:
            self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Hidden | QDir.AllDirs | QDir.Files)
            self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.Hidden | QDir.AllDirs | QDir.Files)
            self.hiddenAction.setChecked(True)
            print("set hidden files to true")

    def toggleHidden(self):
        if self.hiddenEnabled == False:
            self.hiddenEnabled = True
            self.enableHidden()
        else:
            self.hiddenEnabled = False
            self.enableHidden()

    def openOnOtherSide(self):
        if self.listview.hasFocus():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            self.treeview.setRootIndex(self.dirModel.setRootPath(path))
        if self.treeview.hasFocus():
            index = self.treeview.selectionModel().currentIndex()
            path = self.dirModel.fileInfo(index).absoluteFilePath()
            self.listview.setRootIndex(self.fileModel.setRootPath(path))

    ### actions
    def createActions(self):
        self.btnBack = QAction(QIcon.fromTheme("go-previous"), "go back", triggered=self.goBack)
        self.btnUp = QAction(QIcon.fromTheme("go-up"), "go up", triggered=self.goUp)
        self.btnHome = QAction(QIcon.fromTheme("go-home"), "home folder", triggered=self.goHome)
        self.btnMusic = QAction(QIcon.fromTheme("folder-music"), "music folder", triggered=self.goMusic)
        self.btnDocuments = QAction(QIcon.fromTheme("folder-documents"), "documents folder", triggered=self.goDocuments)
        self.btnDownloads = QAction(QIcon.fromTheme("folder-downloads"), "downloads folder", triggered=self.goDownloads)
        self.btnVideo = QAction(QIcon.fromTheme("folder-video"), "video folder", triggered=self.goVideo)
        self.openAction = QAction(QIcon.fromTheme("system-run"), "open File with default app", triggered=self.openFile)
        self.listview.addAction(self.openAction)
        self.treeview.addAction(self.openAction)

        self.newWinAction = QAction(QIcon.fromTheme("folder-showLayout_new"), "open in other side", triggered=self.openOnOtherSide)
        self.newWinAction.setShortcut(QKeySequence("Ctrl+n"))
        self.newWinAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.newWinAction)

        self.openActionText = QAction(QIcon.fromTheme("system-run"), "open File with built-in Texteditor",
                                      triggered=self.openFileText)
        self.openActionText.setShortcut(QKeySequence(Qt.Key_F6))
        self.openActionText.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.openActionText)

        self.openActionTextRoot = QAction(QIcon.fromTheme("applications-system"), "edit as root",
                                          triggered=self.openFileTextRoot)
        self.listview.addAction(self.openActionTextRoot)

        self.renameAction = QAction(QIcon.fromTheme("accessories-text-editor"), "rename File",
                                    triggered=self.renameFile)
        self.renameAction.setShortcut(QKeySequence(Qt.Key_F2))
        self.renameAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.renameAction)
        self.treeview.addAction(self.renameAction)

        self.renameFolderAction = QAction(QIcon.fromTheme("accessories-text-editor"), "rename Folder",
                                          triggered=self.renameFolder)
        self.treeview.addAction(self.renameFolderAction)

        self.copyAction = QAction(QIcon.fromTheme("edit-copy"), "copy File(s)", triggered=self.copyFile)
        self.copyAction.setShortcut(QKeySequence("Ctrl+c"))
        self.copyAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.copyAction)

        self.cutAction = QAction(QIcon.fromTheme("edit-cut"), "cut File(s)", triggered=self.cutFile)
        self.cutAction.setShortcut(QKeySequence("Ctrl+x"))
        self.cutAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.cutAction)

        self.pasteAction = QAction(QIcon.fromTheme("edit-paste"), "paste File(s) / Folder", triggered=self.pasteFile)
        self.pasteAction.setShortcut(QKeySequence("Ctrl+v"))
        self.pasteAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.pasteAction)

        self.delAction = QAction(QIcon.fromTheme("edit-delete"), "delete File(s)", triggered=self.deleteFile)
        self.delAction.setShortcut(QKeySequence("Shift+Del"))
        self.delAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.delAction)

        self.delFolderAction = QAction(QIcon.fromTheme("edit-delete"), "delete Folder", triggered=self.deleteFolder)
        self.treeview.addAction(self.delFolderAction)

        self.delActionTrash = QAction(QIcon.fromTheme("user-trash"), "move to trash", triggered=self.deleteFileTrash)
        self.delActionTrash.setShortcut(QKeySequence("Del"))
        self.delActionTrash.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.delActionTrash)

        self.imageAction = QAction(QIcon.fromTheme("image-x-generic"), "show Image", triggered=self.showImage)
        self.listview.addAction(self.imageAction)

        self.urlAction = QAction(QIcon.fromTheme("browser"), "preview Page", triggered=self.showURL)
        self.listview.addAction(self.urlAction)

        self.dbAction = QAction(QIcon.fromTheme("image-x-generic"), "show Database", triggered=self.showDB)
        self.listview.addAction(self.dbAction)

        self.py2Action = QAction(QIcon.fromTheme("python"), "run in python", triggered=self.runPy2)
        self.listview.addAction(self.py2Action)

        self.py3Action = QAction(QIcon.fromTheme("python3"), "run in python3", triggered=self.runPy3)
        self.listview.addAction(self.py3Action)

        self.findFilesAction = QAction(QIcon.fromTheme("edit-find"), "find in folder", triggered=self.findFiles)
        self.findFilesAction.setShortcut(QKeySequence("Ctrl+f"))
        self.findFilesAction.setShortcutVisibleInContextMenu(True)
        self.treeview.addAction(self.findFilesAction)

        self.zipAction = QAction(QIcon.fromTheme("zip"), "create zip from folder", triggered=self.createZipFromFolder)
        self.treeview.addAction(self.zipAction)

        self.zipFilesAction = QAction(QIcon.fromTheme("zip"), "create zip from selected files",
                                      triggered=self.createZipFromFiles)
        self.listview.addAction(self.zipFilesAction)

        self.unzipHereAction = QAction(QIcon.fromTheme("application-zip"), "extract here ...", triggered=self.unzipHere)
        self.listview.addAction(self.unzipHereAction)

        self.unzipToAction = QAction(QIcon.fromTheme("application-zip"), "extract to ...", triggered=self.unzipTo)
        self.listview.addAction(self.unzipToAction)

        self.playAction = QAction(QIcon.fromTheme("multimedia-player"), "play with Qt5Player",
                                  triggered=self.playInternal)
        self.playAction.setShortcut(QKeySequence(Qt.Key_F3))
        self.playAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.playAction)

        self.playInternalAction = QAction(QIcon.fromTheme("vlc"), "play with vlc", triggered=self.playMedia)
        self.listview.addAction(self.playInternalAction)

        self.mp3Action = QAction(QIcon.fromTheme("audio-x-generic"), "convert to mp3", triggered=self.makeMP3)
        self.listview.addAction(self.mp3Action)

        self.playlistAction = QAction(QIcon.fromTheme("audio-x-generic"), "make playlist from all mp3 files",
                                      triggered=self.makePlaylist)
        self.listview.addAction(self.playlistAction)

        self.playlistPlayerAction = QAction(QIcon.fromTheme("audio-x-generic"), "play Playlist",
                                            triggered=self.playPlaylist)
        self.listview.addAction(self.playlistPlayerAction)

        self.refreshAction = QAction(QIcon.fromTheme("view-refresh"), "refresh View", triggered=self.refreshList,
                                     shortcut="F5")
        self.refreshAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.refreshAction)

        self.hiddenAction = QAction("show hidden Files", triggered=self.toggleHidden)
        self.hiddenAction.setShortcut(QKeySequence("Ctrl+h"))
        self.hiddenAction.setShortcutVisibleInContextMenu(True)
        self.hiddenAction.setCheckable(True)
        self.listview.addAction(self.hiddenAction)

        self.goBackAction = QAction(QIcon.fromTheme("go-back"), "go back", triggered=self.goBack)
        self.goBackAction.setShortcut(QKeySequence(Qt.Key_Backspace))
        self.goBackAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.goBackAction)

        self.helpAction = QAction(QIcon.fromTheme("help"), "Help", triggered=self.showHelp)
        self.helpAction.setShortcut(QKeySequence(Qt.Key_F1))
        self.helpAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.helpAction)

        self.terminalAction = QAction(QIcon.fromTheme("terminal"), "open folder in Terminal",
                                      triggered=self.showInTerminal)
        self.terminalAction.setShortcut(QKeySequence(Qt.Key_F7))
        self.terminalAction.setShortcutVisibleInContextMenu(True)
        self.treeview.addAction(self.terminalAction)
        self.listview.addAction(self.terminalAction)

        self.terminalAction2 = QAction(QIcon.fromTheme("terminal"), "open folder in Terminal",
                                       triggered=self.showInTerminal2)

        self.startInTerminalAction = QAction(QIcon.fromTheme("terminal"), "execute in Terminal",
                                             triggered=self.startInTerminal)
        self.startInTerminalAction.setShortcut(QKeySequence(Qt.Key_F8))
        self.startInTerminalAction.setShortcutVisibleInContextMenu(True)
        self.listview.addAction(self.startInTerminalAction)

        self.executableAction = QAction(QIcon.fromTheme("applications-utilities"), "make executable",
                                        triggered=self.makeExecutable)
        self.listview.addAction(self.executableAction)

        self.createFolderAction = QAction(QIcon.fromTheme("folder-showLayout_new"), "create showLayout_new Folder",
                                          triggered=self.createNewFolder)
        self.createFolderAction.setShortcut(QKeySequence("Shift+Ctrl+n"))
        self.createFolderAction.setShortcutVisibleInContextMenu(True)
        self.treeview.addAction(self.createFolderAction)

    def playPlaylist(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                self.player = QAudioPlayer.Player('')
                self.player.setGeometry(100, 100, 500, 350)
                self.player.show()
                self.player.clearList()
                self.player.openOnStart(path)
                print("added Files to playlist")
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                self.player = QAudioPlayer.Player('')
                self.player.setGeometry(100, 100, 500, 350)
                self.player.show()
                self.player.clearList()
                self.player.openOnStart(path)
                print("added Files to playlist")

    def showImage(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                print("show image: ", path)
                self.win = QImageViewer.ImageViewer()
                self.win.show()
                self.win.filename = path
                self.win.loadFile(path)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                print("show image: ", path)
                self.win = QImageViewer.ImageViewer()
                self.win.show()
                self.win.filename = path
                self.win.loadFile(path)

    def showDB(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                import DBViewer
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                print("show image: ", path)
                self.db_win = DBViewer.MyWindow()
                self.db_win.show()
                self.db_win.fileOpenStartup(path)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                import DBViewer
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                print("show image: ", path)
                self.db_win = DBViewer.MyWindow()
                self.db_win.show()
                self.db_win.fileOpenStartup(path)

    def checkIsApplication(self, path):
        st = subprocess.check_output("file  --mime-type '" + path + "'", stderr=subprocess.STDOUT,
                                     universal_newlines=True, shell=True)
        if "application/x-executable" in st:
            print(path, "is an application")
            return True
        else:
            return False

    def makeExecutable(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                print("set", path, "executable")
                st = os.stat(path)
                os.chmod(path, st.st_mode | stat.S_IEXEC)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                print("set", path, "executable")
                st = os.stat(path)
                os.chmod(path, st.st_mode | stat.S_IEXEC)

    def showInTerminal(self):
        if self.treeview.hasFocus():
            index = self.treeview.selectionModel().currentIndex()
            path = self.dirModel.fileInfo(index).absoluteFilePath()
        elif self.listview.hasFocus():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
        self.terminal = QTerminalFolder.MainWindow()
        self.terminal.show()
        if self.terminal.isVisible():
            os.chdir(path)
            self.terminal.shellWin.startDir = path
            self.terminal.shellWin.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())
                                           + ":" + str(path) + "$ ")
            self.terminal.shellWin.appendPlainText(self.terminal.shellWin.name)

    def showInTerminal2(self):
        path = self.windowTitle()
        self.terminal = QTerminalFolder.MainWindow()
        self.terminal.show()
        if self.terminal.isVisible():
            os.chdir(path)
            self.terminal.shellWin.startDir = path
            self.terminal.shellWin.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())
                                           + ":" + str(path) + "$ ")
            self.terminal.shellWin.appendPlainText(self.terminal.shellWin.name)

    def startInTerminal(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                filename = self.fileModel.fileInfo(index).fileName()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                folderpath = self.fileModel.fileInfo(index).path()
                if not self.fileModel.fileInfo(index).isDir():
                    self.terminal = QTerminalFolder.MainWindow()
                    self.terminal.show()
                    if self.terminal.isVisible():
                        os.chdir(folderpath)
                        self.terminal.shellWin.startDir = folderpath
                        self.terminal.shellWin.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())
                                                       + ":" + str(folderpath) + "$ ")
                        self.terminal.shellWin.appendPlainText(self.terminal.shellWin.name)
                        self.terminal.shellWin.insertPlainText("./%s" % (filename))
                        self.terminal.shellWin.run(path)
                else:
                    self.terminal = QTerminalFolder.MainWindow()
                    self.terminal.show()
                    if self.terminal.isVisible():
                        os.chdir(path)
                        self.terminal.shellWin.startDir = path
                        self.terminal.shellWin.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())
                                                       + ":" + str(path) + "$ ")
                        self.terminal.shellWin.appendPlainText(self.terminal.shellWin.name)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                filename = self.dirModel.fileInfo(index).fileName()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                folderpath = self.dirModel.fileInfo(index).path()
                if not self.dirModel.fileInfo(index).isDir():
                    self.terminal = QTerminalFolder.MainWindow()
                    self.terminal.show()
                    if self.terminal.isVisible():
                        os.chdir(folderpath)
                        self.terminal.shellWin.startDir = folderpath
                        self.terminal.shellWin.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())
                                                       + ":" + str(folderpath) + "$ ")
                        self.terminal.shellWin.appendPlainText(self.terminal.shellWin.name)
                        self.terminal.shellWin.insertPlainText("./%s" % (filename))
                        self.terminal.shellWin.run(path)
                else:
                    self.terminal = QTerminalFolder.MainWindow()
                    self.terminal.show()
                    if self.terminal.isVisible():
                        os.chdir(path)
                        self.terminal.shellWin.startDir = path
                        self.terminal.shellWin.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())
                                                       + ":" + str(path) + "$ ")
                        self.terminal.shellWin.appendPlainText(self.terminal.shellWin.name)

    def createZipFromFolder(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).path()
                fname = self.fileModel.fileInfo(index).fileName()
                print("folder to zip:", path)
                self.copyFile()
                target, _ = QFileDialog.getSaveFileName(self, "Save as... (do not add .zip)", path + "/" + fname,
                                                        "zip files (*.zip)")
                if (target != ""):
                    shutil.make_archive(target, 'zip', path)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).path()
                fname = self.fileModel.fileInfo(index).fileName()
                print("folder to zip:", path)
                self.copyFile()
                target, _ = QFileDialog.getSaveFileName(self, "Save as... (do not add .zip)", path + "/" + fname,
                                                        "zip files (*.zip)")
                if (target != ""):
                    shutil.make_archive(target, 'zip', path)

    def createZipFromFiles(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).path()
                fname = self.fileModel.fileInfo(index).fileName()
                print("folder to zip:", path)
                self.copyFile()
                target, _ = QFileDialog.getSaveFileName(self, "Save as...", path + "/" + "archive.zip",
                                                        "zip files (*.zip)")
                if (target != ""):
                    zipText = ""
                    with ZipFile(target, 'w') as myzip:
                        for file in self.copyList:
                            fname = os.path.basename(file)
                            myzip.write(file, fname)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).path()
                fname = self.dirModel.fileInfo(index).fileName()
                print("folder to zip:", path)
                self.copyFile()
                target, _ = QFileDialog.getSaveFileName(self, "Save as...", path + "/" + "archive.zip",
                                                        "zip files (*.zip)")
                if (target != ""):
                    zipText = ""
                    with ZipFile(target, 'w') as myzip:
                        for file in self.copyList:
                            fname = os.path.basename(file)
                            myzip.write(file, fname)

    def unzipHere(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                file_index = self.listview.selectionModel().currentIndex()
                file_path = self.fileModel.fileInfo(file_index).filePath()
                ext = os.path.splitext(file_path)
                folder_path = self.windowTitle() + "/" + os.path.basename(file_path).replace(ext[1], "")
                print(file_path, folder_path)
                with ZipFile(file_path, 'r') as zipObj:
                    zipObj.extractall(folder_path)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                file_index = self.treeview.selectionModel().currentIndex()
                file_path = self.dirModel.fileInfo(file_index).filePath()
                ext = os.path.splitext(file_path)
                folder_path = self.windowTitle() + "/" + os.path.basename(file_path).replace(ext[1], "")
                with ZipFile(file_path, 'r') as zipObj:
                    zipObj.extractall(folder_path)

    def unzipTo(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                file_index = self.listview.selectionModel().currentIndex()
                file_path = self.fileModel.fileInfo(file_index).filePath()
                ext = os.path.splitext(file_path)
                dirpath = QFileDialog.getExistingDirectory(self, "selectFolder", QDir.homePath(),
                                                           QFileDialog.ShowDirsOnly)
                if dirpath:
                    with ZipFile(file_path, 'r') as zipObj:
                        zipObj.extractall(dirpath + "/" + os.path.basename(file_path).replace(ext[1], ""))
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                file_index = self.treeview.selectionModel().currentIndex()
                file_path = self.dirModel.fileInfo(file_index).filePath()
                ext = os.path.splitext(file_path)
                dirpath = QFileDialog.getExistingDirectory(self, "selectFolder", QDir.homePath(),
                                                           QFileDialog.ShowDirsOnly)
                if dirpath:
                    with ZipFile(file_path, 'r') as zipObj:
                        zipObj.extractall(dirpath + "/" + os.path.basename(file_path).replace(ext[1], ""))

    def findFiles(self):
        path = self.windowTitle()
        print("open findWindow")
        self.w = findFilesWindow.ListBox()
        self.w.show()
        self.w.folderEdit.setText(path)
        self.w.findEdit.setText("*" + self.findfield.text() + "*")
        if self.findfield.text() != "":
            self.w.findMyFiles()
        else:
            self.w.findEdit.setCursorPosition(1)

    def refreshList(self):
        print("refreshing view")
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).path()
        self.treeview.setCurrentIndex(self.fileModel.index(path))
        self.treeview.setFocus()

    def makeMP3(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).filePath()
                ext = self.fileModel.fileInfo(index).suffix()
                newpath = path.replace("." + ext, ".mp3")
                self.statusBar().showMessage("%s '%s'" % ("converting:", path))
                self.process.startDetached("ffmpeg", ["-i", path, newpath])
                print("%s '%s'" % ("converting", path))
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).filePath()
                ext = self.dirModel.fileInfo(index).suffix()
                newpath = path.replace("." + ext, ".mp3")
                print(ext)
                self.statusBar().showMessage("%s '%s'" % ("converting:", path))
                self.process.startDetached("ffmpeg", ["-i", path, newpath])
                print("%s '%s'" % ("converting", path))

    def makePlaylist(self):
        dirname = os.path.basename(self.windowTitle())
        path = os.path.join(self.windowTitle(), dirname + ".m3u")
        print(path)
        pl = QFile(path)
        pl.open(QIODevice.ReadWrite | QIODevice.Truncate)
        mp3List = []

        for name in os.listdir(self.windowTitle()):
            if os.path.isfile(os.path.join(self.windowTitle(), name)):
                if ".mp3" in name:
                    mp3List.append(self.windowTitle() + "/" + name)

        mp3List.sort(key=str.lower)
        print(path)

        with open(path, 'w') as playlist:
            playlist.write('\n'.join(mp3List))
            playlist.close()

    def showHelp(self):
        top = self.y() + 26
        left = self.width() / 2 - 100
        print(top)
        self.w = helpWindow()
        self.w.setWindowFlags(Qt.FramelessWindowHint)
        self.w.setWindowModality(Qt.ApplicationModal)
        self.w.setGeometry(left, top, 300, 360)
        self.w.show()

    def getFolderSize(self, path):
        size = sum(os.path.getsize(f) for f in os.listdir(folder) if os.path.isfile(f))
        return size

    def openFile(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                self.copyFile()
                for files in self.copyList:
                    print("%s '%s'" % ("open file", files))
                    if self.checkIsApplication(path) == True:
                        self.process.startDetached(files)
                    else:
                        QDesktopServices.openUrl(QUrl.fromLocalFile(files))
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                self.copyFile()
                for files in self.copyList:
                    print("%s '%s'" % ("open file", files))
                    if self.checkIsApplication(path) == True:
                        self.process.startDetached(files)
                    else:
                        QDesktopServices.openUrl(QUrl.fromLocalFile(files))

    def openFileText(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                self.texteditor = QTextEdit.MainWindow()
                self.texteditor.show()
                self.texteditor.loadFile(path)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                self.texteditor = QTextEdit.MainWindow()
                self.texteditor.show()
                self.texteditor.loadFile(path)

    def openFileTextRoot(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                file = sys.argv[0]
                mygksu = os.path.join(os.path.dirname(file), "mygksu")
                self.process.startDetached(mygksu, ["xed", path])
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                file = sys.argv[0]
                mygksu = os.path.join(os.path.dirname(file), "mygksu")
                self.process.startDetached(mygksu, ["xed", path])

    def playInternal(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).filePath()
                self.statusBar().showMessage("%s '%s'" % ("file:", path))
                self.player = Qt5Player.VideoPlayer('')
                self.player.show()
                self.player.loadFilm(path)
                print("%s '%s'" % ("playing", path))
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).filePath()
                self.statusBar().showMessage("%s '%s'" % ("file:", path))
                self.player = Qt5Player.VideoPlayer('')
                self.player.show()
                self.player.loadFilm(path)
                print("%s '%s'" % ("playing", path))

    def playMedia(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).filePath()
                self.statusBar().showMessage("%s '%s'" % ("file:", path))
                self.process.startDetached("cvlc", [path])
                print("%s '%s'" % ("playing with vlc:", path))
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).filePath()
                self.statusBar().showMessage("%s '%s'" % ("file:", path))
                self.process.startDetached("cvlc", [path])
                print("%s '%s'" % ("playing with vlc:", path))

    def showURL(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                self.webview = QWebViewer.MainWindow()
                self.webview.show()
                self.webview.load_url(path)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                self.webview = QWebViewer.MainWindow()
                self.webview.show()
                self.webview.load_url(path)

    def list_doubleClicked(self):
        if self.listview.hasFocus():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).absoluteFilePath()
            if not self.fileModel.fileInfo(index).isDir():
                if self.checkIsApplication(path) == True:
                    self.process.startDetached(path)
                else:
                    QDesktopServices.openUrl(QUrl.fromLocalFile(path))
            else:
                self.listview.setRootIndex(self.fileModel.setRootPath(path))
                self.setWindowTitle(path)
        elif self.treeview.hasFocus():
            index = self.treeview.selectionModel().currentIndex()
            path = self.dirModel.fileInfo(index).absoluteFilePath()
            if not self.dirModel.fileInfo(index).isDir():
                if self.checkIsApplication(path) == True:
                    self.process.startDetached(path)
                else:
                    QDesktopServices.openUrl(QUrl.fromLocalFile(path))
            else:
                self.treeview.setRootIndex(self.dirModel.setRootPath(path))
                self.setWindowTitle(path)
        self.getRowCount()

    def goBack(self):
        if self.treeview.hasFocus():
            index = self.treeview.selectionModel().currentIndex()
            path = self.dirModel.fileInfo(index).path()
            self.treeview.setRootIndex(self.dirModel.setRootPath(path))
            self.setWindowTitle(path)
        elif self.listview.hasFocus():
            index = self.listview.selectionModel().currentIndex()
            path = self.fileModel.fileInfo(index).path()
            self.listview.setRootIndex(self.fileModel.setRootPath(path))
            self.setWindowTitle(path)

    def goUp(self):
        if self.treeview.selectionModel().hasSelection():
            index = self.treeview.currentIndex()
            path = self.windowTitle()
            newpath = os.path.dirname(path)
            self.treeview.setCurrentIndex(self.dirModel.index(newpath))
            self.treeview.setRootIndex(self.dirModel.setRootPath(newpath))
            self.setWindowTitle(newpath)
            self.treeview.collapseAll()
        elif self.listview.selectionModel().hasSelection():
            index = self.listview.currentIndex()
            path = self.windowTitle()
            newpath = os.path.dirname(path)
            self.listview.setCurrentIndex(self.fileModel.index(newpath))
            self.listview.setRootIndex(self.fileModel.setRootPath(newpath))
            self.setWindowTitle(newpath)
            self.listview.collapseAll()

    def goHome(self):
        path = QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0]
        if self.treeview.hasFocus():
            self.treeview.setRootIndex(self.dirModel.setRootPath(path))
            self.setWindowTitle(path)
        elif self.listview.hasFocus():
            self.listview.setRootIndex(self.fileModel.setRootPath(path))
            self.setWindowTitle(path)

    def goMusic(self):
        path = QStandardPaths.standardLocations(QStandardPaths.MusicLocation)[0]
        if self.treeview.hasFocus():
            self.treeview.setRootIndex(self.dirModel.setRootPath(path))
            self.setWindowTitle(path)
        elif self.listview.hasFocus():
            self.listview.setRootIndex(self.fileModel.setRootPath(path))
            self.setWindowTitle(path)

    def goVideo(self):
        path = QStandardPaths.standardLocations(QStandardPaths.MoviesLocation)[0]
        if self.treeview.hasFocus():
            self.treeview.setRootIndex(self.dirModel.setRootPath(path))
            self.setWindowTitle(path)
        elif self.listview.hasFocus():
            self.listview.setRootIndex(self.fileModel.setRootPath(path))
            self.setWindowTitle(path)

    def goDocuments(self):
        path = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]
        if self.treeview.hasFocus():
            self.treeview.setRootIndex(self.dirModel.setRootPath(path))
            self.setWindowTitle(path)
        elif self.listview.hasFocus():
            self.listview.setRootIndex(self.fileModel.setRootPath(path))
            self.setWindowTitle(path)

    def goDownloads(self):
        path = QStandardPaths.standardLocations(QStandardPaths.DownloadLocation)[0]
        if self.treeview.hasFocus():
            self.treeview.setRootIndex(self.dirModel.setRootPath(path))
            self.setWindowTitle(path)
        elif self.listview.hasFocus():
            self.listview.setRootIndex(self.fileModel.setRootPath(path))
            self.setWindowTitle(path)

    def infobox(self, message):
        title = "QFilemager"
        QMessageBox(QMessageBox.Information, title, message, QMessageBox.NoButton, self,
                    Qt.Dialog | Qt.NoDropShadowWindowHint).show()

    def contextMenuEvent(self, event):
        if self.listview.hasFocus():
            self.menu = QMenu(self.listview)
            if not self.listview.selectionModel().hasSelection():
                self.menu.addAction(self.createFolderAction)
                self.menu.addAction(self.pasteAction)
                self.menu.addAction(self.terminalAction2)
                self.menu.popup(QCursor.pos())
            elif self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                self.menu.addAction(self.createFolderAction)
                self.menu.addAction(self.openAction)
                if not os.path.isdir(path):
                    self.menu.addAction(self.openActionText)
                    self.menu.addAction(self.openActionTextRoot)
                self.menu.addSeparator()
                if os.path.isdir(path):
                    self.menu.addAction(self.newWinAction)
                self.menu.addSeparator()
                self.menu.addAction(self.renameAction)
                self.menu.addSeparator()
                self.menu.addAction(self.copyAction)
                self.menu.addAction(self.cutAction)
                self.menu.addAction(self.terminalAction)
                self.menu.addAction(self.startInTerminalAction)
                self.menu.addAction(self.executableAction)
                ### database viewer
                db_extension = [".sql", "db", "sqlite", "sqlite3", ".SQL", "DB", "SQLITE", "SQLITE3"]
                for ext in db_extension:
                    if ext in path:
                        self.menu.addAction(self.dbAction)
                ### html viewer
                url_extension = [".htm", ".html"]
                for ext in url_extension:
                    if ext in path:
                        self.menu.addAction(self.urlAction)
                ### run in python
                if path.endswith(".py"):
                    self.menu.addAction(self.py2Action)
                    self.menu.addAction(self.py3Action)
                ### image viewer
                image_extension = [".png", "jpg", ".jpeg", ".bmp", "tif", ".tiff", ".pnm", ".svg",
                                   ".exif", ".gif"]
                for ext in image_extension:
                    if ext in path or ext.upper() in path:
                        self.menu.addAction(self.imageAction)
                self.menu.addSeparator()
                self.menu.addAction(self.delActionTrash)
                self.menu.addAction(self.delAction)
                self.menu.addSeparator()
                if ".m3u" in path:
                    self.menu.addAction(self.playlistPlayerAction)
                extensions = [".mp3", ".mp4", "mpg", ".m4a", ".mpeg", "avi", ".mkv", ".webm",
                              ".wav", ".ogg", ".flv ", ".vob", ".ogv", ".ts", ".m2v", "m4v", "3gp", ".f4v"]
                for ext in extensions:
                    if ext in path or ext.upper() in path:
                        self.menu.addSeparator()
                        self.menu.addAction(self.playAction)
                        self.menu.addAction(self.playInternalAction)
                        self.menu.addSeparator()
                extensions = [".mp4", "mpg", ".m4a", ".mpeg", "avi", ".mkv", ".webm",
                              ".wav", ".ogg", ".flv ", ".vob", ".ogv", ".ts", ".m2v", "m4v", "3gp", ".f4v"]
                for ext in extensions:
                    if ext in path or ext.upper() in path:
                        self.menu.addAction(self.mp3Action)
                        self.menu.addSeparator()
                if ".mp3" in path:
                    self.menu.addAction(self.playlistAction)
                self.menu.addAction(self.refreshAction)
                self.menu.addAction(self.hiddenAction)
                self.menu.addAction(self.zipFilesAction)
                zip_extension = [".zip", ".tar.gz", ".tgz", ".rar"]
                for ext in zip_extension:
                    if path.endswith(ext):
                        self.menu.addAction(self.unzipHereAction)
                        self.menu.addAction(self.unzipToAction)
                self.menu.popup(QCursor.pos())
        ######### treeview ############
        elif self.treeview.hasFocus():
            self.menu = QMenu(self.treeview)
            if not self.treeview.selectionModel().hasSelection():
                self.menu.addAction(self.createFolderAction)
                self.menu.addAction(self.pasteAction)
                self.menu.addAction(self.terminalAction2)
                self.menu.popup(QCursor.pos())
            elif self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                self.menu.addAction(self.createFolderAction)
                self.menu.addAction(self.openAction)
                if not os.path.isdir(path):
                    self.menu.addAction(self.openActionText)
                    self.menu.addAction(self.openActionTextRoot)
                self.menu.addSeparator()
                if os.path.isdir(path):
                    self.menu.addAction(self.newWinAction)
                self.menu.addSeparator()
                self.menu.addAction(self.renameAction)
                self.menu.addSeparator()
                self.menu.addAction(self.copyAction)
                self.menu.addAction(self.cutAction)
                self.menu.addAction(self.terminalAction)
                self.menu.addAction(self.startInTerminalAction)
                self.menu.addAction(self.executableAction)
                ### database viewer
                db_extension = [".sql", "db", "sqlite", "sqlite3", ".SQL", "DB", "SQLITE", "SQLITE3"]
                for ext in db_extension:
                    if ext in path:
                        self.menu.addAction(self.dbAction)
                ### html viewer
                url_extension = [".htm", ".html"]
                for ext in url_extension:
                    if ext in path:
                        self.menu.addAction(self.urlAction)
                ### run in python
                if path.endswith(".py"):
                    self.menu.addAction(self.py2Action)
                    self.menu.addAction(self.py3Action)
                ### image viewer
                image_extension = [".png", "jpg", ".jpeg", ".bmp", "tif", ".tiff", ".pnm", ".svg",
                                   ".exif", ".gif"]
                for ext in image_extension:
                    if ext in path or ext.upper() in path:
                        self.menu.addAction(self.imageAction)
                self.menu.addSeparator()
                self.menu.addAction(self.delActionTrash)
                self.menu.addAction(self.delAction)
                self.menu.addSeparator()
                if ".m3u" in path:
                    self.menu.addAction(self.playlistPlayerAction)
                extensions = [".mp3", ".mp4", "mpg", ".m4a", ".mpeg", "avi", ".mkv", ".webm",
                              ".wav", ".ogg", ".flv ", ".vob", ".ogv", ".ts", ".m2v", "m4v", "3gp", ".f4v"]
                for ext in extensions:
                    if ext in path or ext.upper() in path:
                        self.menu.addSeparator()
                        self.menu.addAction(self.playAction)
                        self.menu.addAction(self.playInternalAction)
                        self.menu.addSeparator()
                extensions = [".mp4", "mpg", ".m4a", ".mpeg", "avi", ".mkv", ".webm",
                              ".wav", ".ogg", ".flv ", ".vob", ".ogv", ".ts", ".m2v", "m4v", "3gp", ".f4v"]
                for ext in extensions:
                    if ext in path or ext.upper() in path:
                        self.menu.addAction(self.mp3Action)
                        self.menu.addSeparator()
                if ".mp3" in path:
                    self.menu.addAction(self.playlistAction)
                self.menu.addAction(self.refreshAction)
                self.menu.addAction(self.hiddenAction)
                self.menu.addAction(self.zipFilesAction)
                zip_extension = [".zip", ".tar.gz", ".tgz", ".rar"]
                for ext in zip_extension:
                    if path.endswith(ext):
                        self.menu.addAction(self.unzipHereAction)
                        self.menu.addAction(self.unzipToAction)
                self.menu.popup(QCursor.pos())

    def createNewFolder(self):
        path = self.windowTitle()
        dlg = QInputDialog(self)
        foldername, ok = dlg.getText(self, 'Folder Name', "Folder Name:", QLineEdit.Normal, "", Qt.Dialog)
        if ok:
            success = QDir(path).mkdir(foldername)

    def runPy2(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                self.process.startDetached("python", [path])
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                self.process.startDetached("python", [path])

    def runPy3(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                self.process.startDetached("python3", [path])
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                self.process.startDetached("python3", [path])

    def renameFile(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                basepath = self.fileModel.fileInfo(index).path()
                oldName = self.fileModel.fileInfo(index).fileName()
                dlg = QInputDialog()
                newName, ok = dlg.getText(self, 'showLayout_new Name:', path, QLineEdit.Normal, oldName, Qt.Dialog)
                if ok:
                    newpath = basepath + "/" + newName
                    QFile.rename(path, newpath)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                basepath = self.dirModel.fileInfo(index).path()
                oldName = self.dirModel.fileInfo(index).fileName()
                print("oldName:", oldName)
                dlg = QInputDialog()
                newName, ok = dlg.getText(self, 'showLayout_new Name:', path, QLineEdit.Normal, oldName, Qt.Dialog)
                if ok:
                    newpath = basepath + "/" + newName
                    QFile.rename(path, newpath)

    def renameFolder(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                basepath = self.fileModel.fileInfo(index).path()
                print("pasepath:", basepath)
                oldName = self.fileModel.fileInfo(index).fileName()
                dlg = QInputDialog()
                newName, ok = dlg.getText(self, 'showLayout_new Name:', path, QLineEdit.Normal, oldName, Qt.Dialog)
                if ok:
                    newpath = basepath + "/" + newName
                    print(newpath)
                    nd = QDir(path)
                    check = nd.rename(path, newpath)
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                path = self.dirModel.fileInfo(index).absoluteFilePath()
                basepath = self.dirModel.fileInfo(index).path()
                print("pasepath:", basepath)
                oldName = self.dirModel.fileInfo(index).fileName()
                dlg = QInputDialog()
                newName, ok = dlg.getText(self, 'showLayout_new Name:', path, QLineEdit.Normal, oldName, Qt.Dialog)
                if ok:
                    newpath = basepath + "/" + newName
                    print(newpath)
                    nd = QDir(path)
                    check = nd.rename(path, newpath)

    def copyFile(self):
        self.copyList = []
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                selected = self.listview.selectionModel().selectedRows()
                folderpath = self.fileModel.fileInfo(index).path()
                count = len(selected)
                for index in selected:
                    path = folderpath + "/" + self.fileModel.data(index, self.fileModel.FileNameRole)
                    print(path, "copied to clipboard")
                    self.copyList.append(path)
                    self.clip.setText('\n'.join(self.copyList))
                print("%s\n%s" % ("filepath(s) copied:", '\n'.join(self.copyList)))
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                selected = self.treeview.selectionModel().selectedRows()
                folderpath = self.dirModel.fileInfo(index).path()
                count = len(selected)
                for index in selected:
                    path = folderpath + "/" + self.dirModel.data(index, self.dirModel.FileNameRole)
                    print(path, "copied to clipboard")
                    self.copyList.append(path)
                    self.clip.setText('\n'.join(self.copyList))
                print("%s\n%s" % ("filepath(s) copied:", '\n'.join(self.copyList)))

    def pasteFile(self):
        if len(self.copyList) > 0:
            for target in self.copyList:
                print(target)
                destination = self.windowTitle() + "/" + QFileInfo(target).fileName()
                try:
                    shutil.copytree(target, destination)
                    if self.cut == True:
                        QFile.remove(target)
                        self.cut == False
                except OSError as e:
                    # If the error was caused because the source wasn't a directory
                    if e.errno == errno.ENOTDIR:
                        shutil.copy(target, destination)
                        if self.cut == True:
                            QFile.remove(target)
                            self.cut == False
                    else:
                        self.infobox('Directory not copied. Error: %s' % e)

    def cutFile(self):
        self.cut = True
        self.copyFile()

    def deleteFolder(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.lisview.selectionModel().currentIndex()
                delFolder = self.fileModel.fileInfo(index).absoluteFilePath()
                msg = QMessageBox.question(self, "Info", "Caution!\nReally delete this Folder?\n" + delFolder,
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if msg == QMessageBox.Yes:
                    print('Deletion confirmed.')
                    self.statusBar().showMessage("%s %s" % ("folder deleted", delFolder), 0)
                    self.fileModel.remove(index)
                    print("%s %s" % ("folder deleted", delFolder))
                else:
                    print('No clicked.')
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                delFolder = self.dirModel.fileInfo(index).absoluteFilePath()
                msg = QMessageBox.question(self, "Info", "Caution!\nReally delete this Folder?\n" + delFolder,
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if msg == QMessageBox.Yes:
                    print('Deletion confirmed.')
                    self.statusBar().showMessage("%s %s" % ("folder deleted", delFolder), 0)
                    self.dirModel.remove(index)
                    print("%s %s" % ("folder deleted", delFolder))
                else:
                    print('No clicked.')

    def deleteFile(self):
        self.copyFile()
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                msg = QMessageBox.question(self, "Info",
                                           "Caution!\nReally delete this Files?\n" + '\n'.join(self.copyList),
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if msg == QMessageBox.Yes:
                    print('Deletion confirmed.')
                    index = self.listview.selectionModel().currentIndex()
                    self.copyPath = self.fileModel.fileInfo(index).absoluteFilePath()
                    print("%s %s" % ("file deleted", self.copyPath))
                    self.statusBar().showMessage("%s %s" % ("file deleted", self.copyPath), 0)
                    for delFile in self.listview.selectionModel().selectedIndexes():
                        self.fileModel.remove(delFile)
                else:
                    print('No clicked.')
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                msg = QMessageBox.question(self, "Info",
                                           "Caution!\nReally delete this Files?\n" + '\n'.join(self.copyList),
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if msg == QMessageBox.Yes:
                    print('Deletion confirmed.')
                    index = self.treeview.selectionModel().currentIndex()
                    self.copyPath = self.dirModel.fileInfo(index).absoluteFilePath()
                    print("%s %s" % ("file deleted", self.copyPath))
                    self.statusBar().showMessage("%s %s" % ("file deleted", self.copyPath), 0)
                    for delFile in self.treeview.selectionModel().selectedIndexes():
                        self.dirModel.remove(delFile)
                else:
                    print('No clicked.')

    def deleteFileTrash(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                self.copyFile()
                msg = QMessageBox.question(self, "Info",
                                           "Caution!\nReally move this Files to Trash\n" + '\n'.join(self.copyList),
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if msg == QMessageBox.Yes:
                    print('Deletion confirmed.')
                    for delFile in self.copyList:
                        try:
                            send2trash(delFile)
                        except OSError as e:
                            self.infobox(str(e))
                        print("%s %s" % ("file moved to trash:", delFile))
                        self.statusBar().showMessage("%s %s" % ("file moved to trash:", delFile), 0)
                else:
                    print('No clicked.')
        elif self.treeview.hasFocus():
            if self.treeview.selectionModel().hasSelection():
                index = self.treeview.selectionModel().currentIndex()
                self.copyFile()
                msg = QMessageBox.question(self, "Info",
                                           "Caution!\nReally move this Files to Trash\n" + '\n'.join(self.copyList),
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if msg == QMessageBox.Yes:
                    print('Deletion confirmed.')
                    for delFile in self.copyList:
                        try:
                            send2trash(delFile)
                        except OSError as e:
                            self.infobox(str(e))
                        print("%s %s" % ("file moved to trash:", delFile))
                        self.statusBar().showMessage("%s %s" % ("file moved to trash:", delFile), 0)
                else:
                    print('No clicked.')

    def createStatusBar(self):
        sysinfo = QSysInfo()
        myMachine = "current CPU Architecture: " + sysinfo.currentCpuArchitecture() + " *** " + sysinfo.prettyProductName() + " *** " + sysinfo.kernelType() + " " + sysinfo.kernelVersion()
        self.statusBar().showMessage("%s: %s" % ("QFileManager", myMachine), 0)


def mystylesheet(self):
    return """
QTreeView
{
background: #e9e9e9;
selection-color: white;
border: 1px solid lightgrey;
selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #729fcf, stop: 1  #204a87);
color: #202020;
outline: 0;
font-size: 9pt;
} 
QTreeView::item::hover{
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);
}
QTreeView::item::focus
{
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #729fcf, stop: 1  #204a87);
border: 0px;
}
QTreeView::focus
{
border: 1px solid darkblue;
}
QMenu
{
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}
QMenu::item::selected
{
color: white;
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 lightblue, stop: 1  blue);
border: 0px;
}
QHeaderView
{
background: #d3d7cf;
color: #555753;
font-weight: bold;
border: 0px solid #555753;
}
QStatusBar
{
font-size: 8pt;
color: #555753;
}
QMenuBar
{
background: transparent;
border: 0px;
}
QToolBar
{
background: transparent;
border: 0px;
}
QMainWindow
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
font-size: 8pt;
}
QLabel
{
    font-size: 10pt;
    text-align: center;
     background: transparent;
    color:#204a87;
}
QMessageBox
{
    font-size: 10pt;
    text-align: center;
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    color:#204a87;
}
QPushButton{
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 grey);
border-style: solid;
border-color: darkgrey;
height: 26px;
width: 66px;
font-size: 8pt;
border-width: 1px;
border-radius: 6px;
}
QPushButton:hover:!pressed{
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 lightblue, stop: 1  blue);
border-style: solid;
border-color: darkgrey;
height: 26px;
width: 66px;
border-width: 1px;
border-radius: 6px;
}
QPushButton:hover{
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 lightgreen, stop: 1  green);
border-style: solid;
border-color: darkgrey;
border-width: 1px;
border-radius: 4px;
}
QToolButton
{
padding-left: 2px; padding-right: 2px;
}
QScrollBar::vertical
{
    width: 10px;
}
QScrollBar::horizontal
{
    height: 10px;
}   
    QSplitter::handle
{
    width: 8px;
    height: 8px;
}
    """


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myWindow()
    w.show()
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(path)
        w.listview.setRootIndex(w.fileModel.setRootPath(path))
        w.treeview.setRootIndex(w.dirModel.setRootPath(path))
        w.setWindowTitle(path)
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:09 AM
# © 2017 - 2018 DAMGteam. All rights reserved