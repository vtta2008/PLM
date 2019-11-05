# -*- coding: utf-8 -*-
"""

Script Name: DBViewer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5 import QtSql, QtPrintSupport
from PyQt5.QtGui import QTextDocument, QIcon, QTextCursor, QTextTableFormat
from PyQt5.QtCore import QFileInfo, Qt, QSettings, QSize, QFile, QTextStream, QItemSelectionModel, QVariant
from PyQt5.QtWidgets import (QMainWindow, QTableView, QDialog, QGridLayout, QPushButton, QAbstractItemView,
                             QLineEdit, QWidget, QFileDialog, QComboBox, QMessageBox, QApplication)
import sqlite3
import csv
import pandas

###################################
btnWidth = 110
btnHeight = 22


class MyWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.setObjectName("SqliteViewer")
        root = QFileInfo(__file__).absolutePath()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.settings = QSettings('Axel Schneider', self.objectName())
        self.viewer = QTableView()

        self.viewer.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.viewer.setSelectionMode(QAbstractItemView.SingleSelection | QItemSelectionModel.Select)

        self.viewer.verticalHeader().setSectionsMovable(True)
        self.viewer.verticalHeader().setDragEnabled(True)
        self.viewer.verticalHeader().setDragDropMode(QAbstractItemView.InternalMove)

        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.model = QtSql.QSqlTableModel()
        self.delrow = -1
        self.dbfile = ""
        self.tablename = ""
        self.headers = []
        self.results = ""
        self.mycolumn = 0
        self.viewer.verticalHeader().setVisible(False)
        self.setStyleSheet(stylesheet(self))
        self.viewer.setModel(self.model)
        #        self.viewer.clicked.connect(self.findrow)

        self.dlg = QDialog()
        self.layout = QGridLayout()
        self.layout.addWidget(self.viewer, 0, 0, 1, 4)

        self.myWidget = QWidget()
        self.myWidget.setLayout(self.layout)

        self.createToolbar()
        self.statusBar().showMessage("Ready")
        self.setCentralWidget(self.myWidget)
        self.setWindowIcon(QIcon.fromTheme("office-database"))
        self.setGeometry(0, 26, 800, 550)
        self.setWindowTitle("SqliteViewer")
        self.msg("Ready")
        self.viewer.setFocus()

    def createToolbar(self):
        #        self.actionOpen = QPushButton("Open DB")
        #        self.actionOpen.clicked.connect(self.fileOpen)
        #        icon = QIcon.fromTheme("document-open")
        #        self.actionOpen.setShortcut("Ctrl+O")
        #        self.actionOpen.setShortcutEnabled(True)
        #        self.actionOpen.setIcon(icon)
        #        self.actionOpen.setObjectName("actionOpen")
        #        self.actionOpen.setStatusTip("Open Database")
        #        self.actionOpen.setToolTip("Open Database")
        #
        #        self.actionImport = QPushButton("Import CSV")
        #        self.actionImport.clicked.connect(self.importCSV)
        #        icon = QIcon.fromTheme("document-open")
        #        self.actionImport.setShortcut("Shift+Ctrl+O")
        #        self.actionImport.setShortcutEnabled(True)
        #        self.actionImport.setIcon(icon)
        #        self.actionImport.setObjectName("actionImport")
        #        self.actionImport.setStatusTip("Import CSV & create Database")
        #        self.actionImport.setToolTip("Import CSV & create Database")

        self.actionSave_as = QPushButton("Export TSV")
        self.actionSave_as.clicked.connect(self.fileSaveTab)
        icon = QIcon.fromTheme("document-save")
        self.actionSave_as.setShortcut("Ctrl+S")
        self.actionSave_as.setShortcutEnabled(True)
        self.actionSave_as.setIcon(icon)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionSave_as.setStatusTip("save tab delimited Text")
        self.actionSave_as.setToolTip("save tab delimited Text")

        self.actionSave_comma = QPushButton("Export CSV")
        self.actionSave_comma.clicked.connect(self.fileSaveComma)
        icon = QIcon.fromTheme("document-save-as")
        self.actionSave_comma.setShortcut("Shift+Ctrl+S")
        self.actionSave_comma.setShortcutEnabled(True)
        self.actionSave_comma.setIcon(icon)
        self.actionSave_comma.setObjectName("actionSave_comma")
        self.actionSave_comma.setStatusTip("save comma delimited Text")
        self.actionSave_comma.setToolTip("save comma delimited Text")

        self.actionHide = QPushButton()
        self.actionHide.clicked.connect(self.toggleVerticalHeaders)
        icon = QIcon.fromTheme("go-first-symbolic")
        self.actionHide.setIcon(icon)
        self.actionHide.setToolTip("toggle vertical Headers")
        self.actionHide.setShortcut("F3")
        self.actionHide.setShortcutEnabled(True)
        self.actionHide.setStatusTip("toggle vertical Headers")

        ### first row as headers
        self.actionHeaders = QPushButton()
        icon = QIcon.fromTheme("ok")
        self.actionHeaders.setIcon(icon)
        self.actionHeaders.setToolTip("selected row to headers")
        self.actionHeaders.setShortcut("F5")
        self.actionHeaders.setShortcutEnabled(True)
        self.actionHeaders.setStatusTip("selected row to headers")

        self.actionPreview = QPushButton()
        self.actionPreview.clicked.connect(self.handlePreview)
        icon = QIcon.fromTheme("document-print-preview")
        self.actionPreview.setShortcut("Shift+Ctrl+P")
        self.actionPreview.setShortcutEnabled(True)
        self.actionPreview.setIcon(icon)
        self.actionPreview.setObjectName("actionPreview")
        self.actionPreview.setStatusTip("Print Preview")
        self.actionPreview.setToolTip("Print Preview")

        self.actionPrint = QPushButton()
        self.actionPrint.clicked.connect(self.handlePrint)
        icon = QIcon.fromTheme("document-print")
        self.actionPrint.setShortcut("Shift+Ctrl+P")
        self.actionPrint.setShortcutEnabled(True)
        self.actionPrint.setIcon(icon)
        self.actionPrint.setObjectName("actionPrint")
        self.actionPrint.setStatusTip("Print")
        self.actionPrint.setToolTip("Print")

        ###############################
        self.tb = self.addToolBar("ToolBar")
        self.tb.setIconSize(QSize(16, 16))
        self.tb.setMovable(False)
        #        self.tb.addWidget(self.actionOpen)
        #        self.tb.addWidget(self.actionImport)
        #        self.tb.addSeparator()
        self.tb.addWidget(self.actionSave_as)
        self.tb.addSeparator()
        self.tb.addWidget(self.actionSave_comma)
        self.tb.addSeparator()
        self.tb.addWidget(self.actionPreview)
        self.tb.addWidget(self.actionPrint)
        ### sep
        self.tb.addSeparator()
        self.tb.addSeparator()
        ### popupMenu
        self.pop = QComboBox()
        self.pop.setFixedWidth(200)
        self.pop.currentIndexChanged.connect(self.setTableName)
        self.tb.addWidget(self.pop)
        self.tb.addSeparator()
        self.tb.addWidget(self.actionHide)
        self.addToolBar(self.tb)

    def toggleVerticalHeaders(self):
        if self.viewer.verticalHeader().isVisible() == False:
            self.viewer.verticalHeader().setVisible(True)
            icon = QIcon.fromTheme("go-last-symbolic")
            self.actionHide.setIcon(icon)
        else:
            self.viewer.verticalHeader().setVisible(False)
            icon = QIcon.fromTheme("go-first-symbolic")
            self.actionHide.setIcon(icon)

    #    def fileOpen(self):
    #        tablelist = []
    #        fileName, _ = QFileDialog.getOpenFileName(None, "Open Database File", "/home/brian/Dokumente/DB", "DB (*.sqlite *.db *.sql3);; All Files (*.*)")
    #        if fileName:
    #            self.db.close()
    #            self.dbfile = fileName
    #            conn = sqlite3.connect(self.dbfile)
    #            cur = conn.cursor()
    #            res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #            for name in res:
    #                print (name[0])
    #                tablelist.append(name[0])
    #        self.db.setDatabaseName(self.dbfile)
    #        self.db.open()
    #        self.fillComboBox(tablelist)
    #        self.msg("please choose Table from the ComboBox")

    def fileOpenStartup(self, fileName):
        tablelist = []
        if fileName:
            self.dbfile = fileName
            self.db.setDatabaseName(self.dbfile)
            self.db.open()
            tablelist = self.db.tables()
            self.fillComboBox(tablelist)
            print(self.db.driverName())
            self.msg("please choose Table from the ComboBox")

    #    def importCSV(self):
    #        csvfile, _ = QFileDialog.getOpenFileName(None, "Open CSV File", "", "CSV (*.csv *.tsv *.txt)")
    #        if csvfile:
    #            filename = csvfile.rpartition("/")[2].replace(".csv", "")
    #            print(filename)
    #            sqlfile, _ = QFileDialog.getSaveFileName(None, "Save Database File", "/tmp/" + filename + ".sqlite", "SQLite (*.sqlite)")
    #            if sqlfile:
    #                if QFile.exists(sqlfile):
    #                    QFile.remove(sqlfile)
    #                con = sqlite3.connect(sqlfile)
    #                cur = con.cursor()
    #                file = QFile(csvfile)
    #                if not file.open(QFile.ReadOnly | QFile.Text):
    #                    QMessageBox.warning(self, "Meldung",
    #                            "Cannot read file %s:\n%s." % (fileName, file.errorString()))
    #                    return
    #                infile = QTextStream(file)
    #                mytext = infile.readLine()
    #
    #        ### ask for header
    #            ret = QMessageBox.question(self, "SQLiteViewer Message",
    #                    "use this line as header?\n\n" + mytext,
    #                    QMessageBox.Ok | QMessageBox.No, defaultButton = QMessageBox.Ok)
    #            if ret == QMessageBox.Ok:
    #                df = pandas.read_csv(csvfile, encoding = 'utf-8', delimiter = '\t')
    #            if ret == QMessageBox.No:
    #                df = pandas.read_csv(csvfile, encoding = 'utf-8', delimiter = '\t', header=None)
    #        df.to_sql(filename, con, if_exists='append', index=False)
    #        self.fileOpenStartup(sqlfile)
    #
    def fileSaveTab(self):
        if not self.model.rowCount() == 0:
            self.msg("exporting Table")
            conn = sqlite3.connect(self.dbfile)
            c = conn.cursor()
            data = c.execute("SELECT * FROM " + self.tablename)
            self.headers = [description[0] for description in c.description]
            fileName, _ = QFileDialog.getSaveFileName(None, "Export Table to CSV", self.tablename + ".tsv",
                                                      "CSV Files (*.csv *.tsv)")
            if fileName:
                with open(fileName, 'w') as f:
                    writer = csv.writer(f, delimiter='\t')
                    writer.writerow(self.headers)
                    writer.writerows(data)
        else:
            self.msg("nothing to export")

    def setAutoWidth(self):
        self.viewer.resizeColumnsToContents()

    def fillComboBox(self, tablelist):
        self.pop.clear()
        self.pop.insertItem(0, "choose Table ...")
        self.pop.setCurrentIndex(0)
        for row in tablelist:
            self.pop.insertItem(self.pop.count(), row)
        if self.pop.count() > 1:
            self.pop.setCurrentIndex(1)
            self.setTableName()

    def fileSaveComma(self):
        if not self.model.rowCount() == 0:
            self.msg("exporting Table")
            conn = sqlite3.connect(self.dbfile)
            c = conn.cursor()
            data = c.execute("SELECT * FROM " + self.tablename)
            headers = [description[0] for description in c.description]
            fileName, _ = QFileDialog.getSaveFileName(None, "Export Table to CSV", self.tablename + ".csv",
                                                      "CSV Files (*.csv)")
            if fileName:
                with open(fileName, 'w') as f:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow(headers)
                    writer.writerows(data)
        else:
            self.msg("nothing to export")

    def editCell(self):
        item = self.viewer.selectedIndexes()[0]
        row = self.selectedRow()
        column = self.selectedColumn()
        self.model.setData(item, self.editor.text())

    def setTableName(self):
        if not self.pop.currentText() == "choose Table ...":
            self.tablename = self.pop.currentText()
            print("DB is:", self.dbfile)
            self.msg("initialize")
            self.initializeModel()

    def initializeModel(self):
        print("Table selected:", self.tablename)
        self.model.setTable(self.tablename)
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.setAutoWidth()
        self.msg(self.tablename + " loaded *** " + str(self.model.rowCount()) + " records")

    #    def addrow(self):
    #        if self.viewer.selectionModel().hasSelection():
    #            row =  self.viewer.selectionModel().selectedIndexes()[0].row()
    #        else:
    #            row =  self.model.rowCount()
    #
    #        ret = self.model.insertRow(row)
    #        if ret:
    #            self.viewer.selectRow(row)
    #            item = self.viewer.selectedIndexes()[0]
    #            self.model.setData(item, str(""))
    #
    #    def findrow(self, i):
    #        self.delrow = i.row()

    def selectedRow(self):
        if self.viewer.selectionModel().hasSelection():
            row = self.viewer.selectionModel().selectedIndexes()[0].row()
            return int(row)

    def selectedColumn(self):
        column = self.viewer.selectionModel().selectedIndexes()[0].column()
        return int(column)

    def closeEvent(self, e):
        e.accept()

    #    def readSettings(self):
    #        print("reading settings")
    #        if self.settings.contains('geometry'):
    #            self.setGeometry(self.settings.value('geometry'))
    #
    #    def writeSettings(self):
    #        print("writing settings")
    #        self.settings.setValue('geometry', self.geometry())

    def msg(self, message):
        self.statusBar().showMessage(message)

    def handlePrint(self):
        if self.model.rowCount() == 0:
            self.msg("no rows")
        else:
            dialog = QtPrintSupport.QPrintDialog()
            if dialog.exec_() == QDialog.Accepted:
                self.handlePaintRequest(dialog.printer())
                self.msg("Document printed")

    def handlePreview(self):
        if self.model.rowCount() == 0:
            self.msg("no rows")
        else:
            dialog = QtPrintSupport.QPrintPreviewDialog()
            dialog.setFixedSize(1000, 700)
            dialog.paintRequested.connect(self.handlePaintRequest)
            dialog.exec_()
            self.msg("Print Preview closed")

    def handlePaintRequest(self, printer):
        printer.setDocName(self.tablename)
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.viewer.model()
        tableFormat = QTextTableFormat()
        tableFormat.setBorder(0.2)
        tableFormat.setBorderStyle(3)
        tableFormat.setCellSpacing(0);
        tableFormat.setTopMargin(0);
        tableFormat.setCellPadding(4)
        table = cursor.insertTable(model.rowCount() + 1, model.columnCount(), tableFormat)
        model = self.viewer.model()
        ### get headers
        myheaders = []
        for i in range(0, model.columnCount()):
            myheader = model.headerData(i, Qt.Horizontal)
            cursor.insertText(myheader)
            cursor.movePosition(QTextCursor.NextCell)
        #
        ## get cells
        for row in range(0, model.rowCount()):
            for col in range(0, model.columnCount()):
                index = model.index(row, col)
                cursor.insertText(str(index.data()))
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)


def stylesheet(self):
    return """
        QTableView
        {
            border: 1px solid grey;
            border-radius: 0px;
            font-size: 8pt;
            background-color: #e8eaf3;
            selection-color: #ffffff;
        }
        QTableView::item:hover
        {   
            color: black;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #729fcf, stop:1 #d3d7cf);           
        }

        QTableView::item:selected 
        {
            color: #F4F4F4;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6169e1, stop:1 #3465a4);
        } 
        QTableView::horizontalHeader
        {
            background-color:#d3d7cf;
            color: #2e3436; 
            border: 1px solid darkgray;
            font: bold
        }
        QTableView::verticalHeader
        {
            background-color:#d3d7cf;
            color: #2e3436; 
            border: 1px solid darkgray;
            font: bold; 
            padding-right: 4px;
            padding-top: 5px;
        }
        QStatusBar
        {
            font-size: 8pt;
            color: #57579e;
        }
        QPushButton
        {
            font-size: 8pt;
        }
        QPushButton:hover
        {   
            color: black;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #729fcf, stop:1 #d3d7cf);           
            border: 1px solid #b7b7b7 inset;
            border-radius: 3px;
        }
        QComboBox
        {
            font-size: 8pt;
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
padding-left: 10px;
padding-top: 0px;
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
    """
###################################
if __name__ == "__main__":
   import sys
   app = QApplication(sys.argv)
   app.setApplicationName('SQLViewer')
   main = MyWindow("")
   main.show()
   if len(sys.argv) > 1:
       print(sys.argv[1])
       main.fileOpenStartup(sys.argv[1])
#    else:
#        main.fileOpenStartup("/home/brian/Dokumente/DB/EddiesElectronics.sqlite")
   sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved