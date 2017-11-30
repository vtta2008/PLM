# -*- coding: utf-8 -*-
"""
Script Name: englishDict.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    It is a very fun english dictionary.

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import os, sys, subprocess, json, logging

from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *

from sql_tk import connection

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

class SqlTable(QDialog):
    def __init__(self, tableName, parent=None):
        super(SqlTable, self).__init__(parent)

        self.setWindowTitle("Data Setting")

        self.model = QSqlTableModel(self)
        self.model.setTable(tableName)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()

        view = QTableView()
        view.setModel(self.model)

        submitButton = QPushButton("Submit")
        submitButton.setDefault(True)
        revertButton = QPushButton("&Revert")
        quitButton = QPushButton("Quit")

        buttonBox = QDialogButtonBox(Qt.Vertical)
        buttonBox.addButton(submitButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(revertButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QDialogButtonBox.RejectRole)

        submitButton.clicked.connect(self.submit)
        revertButton.clicked.connect(self.model.revertAll)
        quitButton.clicked.connect(self.close)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(view)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

    def submit(self):
        self.model.database().transaction()
        if self.model.submitAll():
            self.model.database().commit()
        else:
            self.model.database().rollback()
            QMessageBox.warning(self, "Cached Table",
                        "The database reported an error: %s" % self.model.lastError().text())

def initialize(tableName):
    app = QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)
    editor = SqlTable(tableName)
    editor.show()
    sys.exit(editor.exec_())

if __name__ == '__main__':
    initialize()

