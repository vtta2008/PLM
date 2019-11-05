# -*- coding: utf-8 -*-
"""

Script Name: QFilemanager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QSettings, QSize, Qt, QTextStream, QDir, QTranslator,
                          QLocale, QLibraryInfo, QTime, QTimer, QStandardPaths)
from PyQt5.QtGui import QIcon, QKeySequence, QTextCursor, QClipboard
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMessageBox, QTextEdit, QPushButton,
                             QLineEdit, QMenu, QInputDialog, QLCDNumber)
from PyQt5 import QtPrintSupport
import sys


class DigitalClock(QLCDNumber):

    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)
        self.setSegmentStyle(QLCDNumber.Flat)
        self.setDigitCount(8)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()
        self.resize(120, 40)

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm:ss')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:5] + ' ' + text[6:]
        self.display(text)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setStyleSheet(myStyleSheet(self))
        self.MaxRecentFiles = 5
        self.windowList = []
        self.recentFileActs = []
        self.curFile = ''
        self.setAcceptDrops(True)
        self.settings = QSettings("QTextEdit", "QTextEdit")
        self.myeditor = QTextEdit()
        # assert (self.locale().language() == QLocale.NewZealand)
        self.myeditor.setAcceptRichText(False)
        self.myeditor.setUndoRedoEnabled(True)
        self.myeditor.setStyleSheet(myStyleSheet(self))
        self.myeditor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.myeditor.customContextMenuRequested.connect(self.contextMenuRequested)

        self.createActions()
        self.createToolBars()
        self.createMenus()
        self.createStatusBar()

        self.setWindowIcon(QIcon.fromTheme("gnome-documents"))

        self.readSettings()
        self.myeditor.document().contentsChanged.connect(self.documentWasModified)
        self.setCurrentFile('')
        self.setCentralWidget(self.myeditor)
        self.myeditor.setFocus()

    def closeEvent(self, event):
        if self.maybeSave():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def newFile(self):
        if self.maybeSave():
            self.myeditor.clear()
            self.setCurrentFile('')

    def open(self):
        if self.maybeSave():
            documents = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]
            fileName, _ = QFileDialog.getOpenFileName(self, "open File", documents,
                                                      "Text Files (*.txt *.csv *.sh *.py) ;; all Files (*.*)")
            if fileName:
                self.loadFile(fileName)
            else:
                self.statusBar().showMessage("cancelled", 3000)

    def save(self):
        if not self.myeditor.toPlainText() == "":
            if self.myeditor.document().isModified():
                if self.curFile:
                    return self.saveFile(self.curFile)
                    self.setCurrentFile(fileName)
                else:
                    return self.saveAs()
            else:
                self.statusBar().showMessage("File '" + self.curFile + "' already saved", 3000)
        else:
            self.statusBar().showMessage("no Text")

    def saveAs(self):
        if not self.myeditor.toPlainText() == "":
            if self.curFile:
                fileName, _ = QFileDialog.getSaveFileName(self, "Save as...", self.curFile, "Text Files (*.txt)")
            else:
                documents = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]
                fileName, _ = QFileDialog.getSaveFileName(self, "Save as...", documents + "/newDocument.txt",
                                                          "Text Files (*.txt)")
            if fileName:
                return self.saveFile(fileName)

            return False
        else:
            self.statusBar().showMessage("no Text")

    def contextMenuRequested(self, point):
        cmenu = QMenu()
        cmenu = self.myeditor.createStandardContextMenu()
        if not self.myeditor.textCursor().selectedText() == "":
            cmenu.addSeparator()
            cmenu.addAction(QIcon.fromTheme("edit-find-and-replace"), "replace all occurrences", self.replaceThis)
        cmenu.exec_(self.myeditor.mapToGlobal(point))

    def replaceThis(self):
        if not self.myeditor.textCursor().selectedText() == "":
            rtext = self.myeditor.textCursor().selectedText()
            dlg = QInputDialog(self, Qt.Dialog)
            dlg.setOkButtonText("Replace")
            text = dlg.getText(self, "Replace", "replace '" + rtext + "' with:", QLineEdit.Normal, "")
            oldtext = self.myeditor.document().toPlainText()
            if not (text[0] == ""):
                newtext = oldtext.replace(rtext, text[0])
                self.myeditor.setPlainText(newtext)
                self.myeditor.document().setModified(True)

    def about(self):
        link = "<p><a title='Axel Schneider' href='http://goodoldsongs.jimdo.com' target='_blank'>Axel Schneider</a></p>"
        title = "über QTextEdit"
        message = (
                    "<span style='text-shadow: #2e3436 2px 2px 2px; color: #6169e1; font-size: 24pt;font-weight: bold;'><strong>QTextEdit 1.2</strong></span></p><br><br>created by<h2 >" + link + "</h2> with PyQt5"
                                                                                                                                                                                                   "<br><br>Copyright © 2018 The Qt Company Ltd and other contributors."
                                                                                                                                                                                                   "<br>Qt and the Qt logo are trademarks of The Qt Company Ltd.")
        msg = QMessageBox(QMessageBox.Information, title, message, QMessageBox.NoButton, self,
                          Qt.Dialog | Qt.NoDropShadowWindowHint).show()

    def documentWasModified(self):
        self.setWindowModified(self.myeditor.document().isModified())

    def createActions(self):
        self.newAct = QAction(QIcon.fromTheme('document-new'), "&Neu", self,
                              shortcut=QKeySequence.New, statusTip="new Document",
                              triggered=self.newFile)

        self.openAct = QAction(QIcon.fromTheme('document-open'), "open File",
                               self, shortcut=QKeySequence.Open,
                               statusTip="open File", triggered=self.open)

        self.saveAct = QAction(QIcon.fromTheme('document-save'), "Save", self,
                               shortcut=QKeySequence.Save,
                               statusTip="save Document", triggered=self.save)

        self.saveAsAct = QAction(QIcon.fromTheme('document-save-as'), "Save as...", self,
                                 shortcut=QKeySequence.SaveAs,
                                 statusTip="save Document to new filename",
                                 triggered=self.saveAs)

        self.exitAct = QAction(QIcon.fromTheme('application-exit'), "Exit", self, shortcut="Ctrl+Q",
                               statusTip="exit", triggered=self.close)

        self.cutAct = QAction(QIcon.fromTheme('edit-cut'), "Cut", self,
                              shortcut=QKeySequence.Cut,
                              statusTip="Cut",
                              triggered=self.myeditor.cut)

        self.copyAct = QAction(QIcon.fromTheme('edit-copy'), "Copy", self,
                               shortcut=QKeySequence.Copy,
                               statusTip="Copy",
                               triggered=self.myeditor.copy)

        self.pasteAct = QAction(QIcon.fromTheme('edit-paste'), "Paste",
                                self, shortcut=QKeySequence.Paste,
                                statusTip="Paste",
                                triggered=self.myeditor.paste)

        self.undoAct = QAction(QIcon.fromTheme('edit-undo'), "Undo",
                               self, shortcut=QKeySequence.Undo,
                               statusTip="Undo",
                               triggered=self.myeditor.undo)

        self.redoAct = QAction(QIcon.fromTheme('edit-redo'), "Redo",
                               self, shortcut=QKeySequence.Redo,
                               statusTip="Redo",
                               triggered=self.myeditor.redo)

        self.aboutAct = QAction(QIcon.fromTheme('help-about'), "Info", self,
                                statusTip="about QTextEdit",
                                triggered=self.about)

        self.aboutQtAct = QAction(QIcon.fromTheme('help-about'), "über Qt", self,
                                  statusTip="über Qt",
                                  triggered=QApplication.instance().aboutQt)

        self.repAllAct = QPushButton("replace all")
        self.repAllAct.setFixedWidth(100)
        self.repAllAct.setIcon(QIcon.fromTheme("edit-find-and-replace"))
        self.repAllAct.setStatusTip("replace all")
        self.repAllAct.clicked.connect(self.replaceAll)

        self.cutAct.setEnabled(False)
        self.copyAct.setEnabled(False)
        self.myeditor.copyAvailable.connect(self.cutAct.setEnabled)
        self.myeditor.copyAvailable.connect(self.copyAct.setEnabled)
        self.undoAct.setEnabled(False)
        self.redoAct.setEnabled(False)
        self.myeditor.undoAvailable.connect(self.undoAct.setEnabled)
        self.myeditor.redoAvailable.connect(self.redoAct.setEnabled)

        ### print preview
        self.printPreviewAct = QAction("Print Preview", self, shortcut=QKeySequence.Print, statusTip="Print Preview",
                                       triggered=self.handlePrintPreview)
        self.printPreviewAct.setIcon(QIcon.fromTheme("document-print-preview"))
        ### print
        self.printAct = QAction("print Document", self, shortcut=QKeySequence.Print, statusTip="print Document",
                                triggered=self.handlePrint)
        self.printAct.setIcon(QIcon.fromTheme("document-print"))

        for i in range(self.MaxRecentFiles):
            self.recentFileActs.append(
                QAction(self, visible=False,
                        triggered=self.openRecentFile))

    def findText(self):
        word = self.findfield.text()
        if self.myeditor.find(word):
            self.statusBar().showMessage("found '" + word + "'", 2000)
        else:
            self.myeditor.moveCursor(QTextCursor.Start)
            if self.myeditor.find(word):
                return
            else:
                self.statusBar().showMessage("found nothing", 3000)

    def replaceAll(self):
        oldtext = self.findfield.text()
        newtext = self.replacefield.text()
        if not oldtext == "":
            h = self.myeditor.toHtml().replace(oldtext, newtext)
            self.myeditor.setText(h)
            self.setModified(True)
            self.statusBar().showMessage("all replaced", 3000)
        else:
            self.statusBar().showMessage("nothing to replace", 3000)

    def replaceOne(self):
        oldtext = self.findfield.text()
        newtext = self.replacefield.text()
        if not oldtext == "":
            h = self.myeditor.toHtml().replace(oldtext, newtext, 1)
            self.myeditor.setText(h)
            self.setModified(True)
            self.statusBar().showMessage("1 replaced", 3000)
        else:
            self.statusBar().showMessage("nothing to replace", 3000)

    def openRecentFile(self):
        action = self.sender()
        if action:
            if (self.maybeSave()):
                self.loadFile(action.data())

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.separatorAct = self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        for i in range(self.MaxRecentFiles):
            self.fileMenu.addAction(self.recentFileActs[i])
        self.updateRecentFileActions()
        self.fileMenu.addSeparator()
        self.clearRecentAct = QAction("clear List", self, triggered=self.clearRecentFiles)
        self.clearRecentAct.setIcon(QIcon.fromTheme("edit-clear"))
        self.fileMenu.addAction(self.clearRecentAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)
        self.editMenu.addSeparator();
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.setIconSize(QSize(16, 16))
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)
        self.fileToolBar.addAction(self.saveAsAct)
        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.printPreviewAct)
        self.fileToolBar.addAction(self.printAct)
        self.fileToolBar.setStyleSheet("QToolBar { border: 0px }")
        self.fileToolBar.setMovable(False)
        self.setContextMenuPolicy(Qt.NoContextMenu)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.setIconSize(QSize(16, 16))
        self.editToolBar.addAction(self.undoAct)
        self.editToolBar.addAction(self.redoAct)
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)
        self.editToolBar.setMovable(False)
        self.editToolBar.setStyleSheet("QToolBar { border: 0px }")

        ### find / replace toolbar
        self.addToolBarBreak()
        self.findToolBar = self.addToolBar("Find")
        self.findToolBar.setIconSize(QSize(16, 16))
        self.findfield = QLineEdit()
        self.findfield.addAction(QIcon.fromTheme("edit-find"), 0)
        self.findfield.setClearButtonEnabled(True)
        self.findfield.setFixedWidth(200)
        self.findfield.setPlaceholderText("find")
        self.findfield.setStatusTip("press RETURN to find")
        self.findfield.setText("")
        self.findfield.returnPressed.connect(self.findText)
        self.findToolBar.addWidget(self.findfield)
        self.replacefield = QLineEdit()
        self.replacefield.addAction(QIcon.fromTheme("edit-find-replace"), 0)
        self.replacefield.setClearButtonEnabled(True)
        self.replacefield.setFixedWidth(200)
        self.replacefield.setPlaceholderText("replace with")
        self.replacefield.setStatusTip("press RETURN to replace first only")
        self.replacefield.returnPressed.connect(self.replaceOne)
        self.findToolBar.addSeparator()
        self.findToolBar.addWidget(self.replacefield)
        self.findToolBar.addSeparator()
        self.findToolBar.addWidget(self.repAllAct)
        self.findToolBar.setMovable(False)
        self.findToolBar.setStyleSheet("QToolBar { border: 0px }")

    def createStatusBar(self):
        self.statusBar().setStyleSheet(myStyleSheet(self))
        self.statusBar().showMessage("Welcome")
        self.DigitalClock = DigitalClock()
        self.DigitalClock.setStyleSheet(
            "QLCDNumber {padding: 2px, 2px 2px 2px; border: 0px solid #2e3436; color: #3465a4; background-color: transparent }")
        self.statusBar().addPermanentWidget(self.DigitalClock)

    def readSettings(self):
        pos = self.settings.value("pos", QPoint(200, 200))
        size = self.settings.value("size", QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("size", self.size())

    def maybeSave(self):
        if self.myeditor.document().isModified():
            ret = QMessageBox.warning(self, "QTextEdit Message",
                                      "Document was changed.\nSave changes?",
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                      defaultButton=QMessageBox.Save)
            if ret == QMessageBox.Save:
                return self.save()
            if ret == QMessageBox.Cancel:
                return False
        return True

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Message",
                                "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        infile = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.myeditor.setPlainText(infile.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File '" + fileName + "' loaded", 3000)

    def saveFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Message",
                                "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outfile = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outfile << self.myeditor.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName);
        self.statusBar().showMessage("File '" + fileName + "' saved", 3000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.myeditor.document().setModified(False)
        self.setWindowModified(False)

        if self.curFile:
            self.setWindowTitle(self.strippedName(self.curFile) + "[*]")
        else:
            self.setWindowTitle('New.txt' + "[*]")

        files = self.settings.value('recentFileList', [])
        if not files == "":
            try:
                files.remove(fileName)
            except ValueError:
                pass

            if fileName:
                files.insert(0, fileName)
                del files[self.MaxRecentFiles:]

                self.settings.setValue('recentFileList', files)
                self.updateRecentFileActions()

    def updateRecentFileActions(self):
        mytext = ""
        files = self.settings.value('recentFileList', [])
        numRecentFiles = min(len(files), self.MaxRecentFiles)
        #        if not files == "":
        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)
            self.recentFileActs[i].setIcon(QIcon.fromTheme("text-x-generic"))

        for j in range(numRecentFiles, self.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))

    def clearRecentFiles(self, fileName):
        self.settings.clear()
        self.updateRecentFileActions()

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()

    def msgbox(self, message):
        QMessageBox.warning(self, "Message", message)

    def handlePrint(self):
        if self.myeditor.toPlainText() == "":
            self.statusBar().showMessage("no Text to print")
            self.msgbox("kein Text zum Drucken")
        else:
            dialog = QtPrintSupport.QPrintDialog()
            if dialog.exec_() == QDialog.Accepted:
                self.handlePaintRequest(dialog.printer())
                self.statusBar().showMessage("Document printed")

    def handlePrintPreview(self):
        if self.myeditor.toPlainText() == "":
            self.statusBar().showMessage("no text to preview")
            self.msgbox("kein Text für Vorschau")
        else:
            dialog = QtPrintSupport.QPrintPreviewDialog()
            dialog.setGeometry(10, 0, self.width() - 60, self.height() - 60)
            dialog.paintRequested.connect(self.handlePaintRequest)
            dialog.exec_()
            self.statusBar().showMessage("Preview closed")

    def handlePaintRequest(self, printer):
        printer.setDocName(self.curFile)
        document = self.myeditor.document()
        document.print_(printer)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        f = str(event.mimeData().urls()[0].toLocalFile())
        self.loadFile(f)


def myStyleSheet(self):
    return """
QTextEdit
{
background: #eeeeec;
color: #202020;
}
QStatusBar
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #e5e5e5,
                                 stop: 0.5 #e9e9e9, stop: 1.0 #d2d2d2);
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
}
QLineEdit
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #e5e5e5,
                                 stop: 0.5 #e9e9e9, stop: 1.0 #d2d2d2);
}
QPushButton
{
background: #D8D8D8;
}
QLCDNumber
{
color: #204a87;
}
    """


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    #    assert(mainWin.locale().language() == QLocale.German)
    mainWin.show()
    if len(sys.argv) > 1:
        print(sys.argv[1])
        if not sys.argv[1] == "":
            mainWin.myeditor.setPlainText(sys.argv[1])
            mainWin.myeditor.document().setModified()
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:04 AM
# © 2017 - 2018 DAMGteam. All rights reserved