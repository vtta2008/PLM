#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: baseSQL.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QTextBrowser, QTableWidget,
                             QTableWidgetItem, QApplication, QTabWidget, QGridLayout)
from PyQt5.QtGui import QIcon

from utilities import sqlManager
import appData as app

from ui import uirc as rc

tableNames = ["userTokenLogin", "timeLog", "curUser", "security_questions", ]

class Tab1(QWidget):
    def __init__(self, parent=None):
        super(Tab1, self).__init__(parent=parent)
        layout = QFormLayout()
        layout.setVerticalSpacing(20)

        h_l = QHBoxLayout()
        h_l.setSpacing(10)
        search_line = QLineEdit()
        search_btn = QPushButton()
        search_btn.setText('Search')
        h_l.addWidget(search_line)
        h_l.addWidget(search_btn)
        layout.addItem(h_l)

        layout.addRow("ID", QTextBrowser())
        layout.addRow("username", QTextBrowser())
        layout.addRow("token", QTextBrowser())
        layout.addRow("cookie", QTextBrowser())
        layout.addRow("checkbox", QTextBrowser())
        layout.addRow("dateCreate", QTextBrowser())

        self.setLayout(layout)


class Tab2(QWidget):
    def __init__(self, parent=None):
        super(Tab2, self).__init__(parent=parent)
        layout = QFormLayout()

        self.d_view = QTableWidget(self)

        self.d_view.resizeColumnsToContents()
        self.d_view.resizeRowsToContents()

        self.id1 = QLineEdit()
        self.username = QLineEdit()
        self.token = QLineEdit()
        self.cookie = QLineEdit()
        self.checkbox = QLineEdit()
        self.dateCreate = QLineEdit()

        self.add_btn = QPushButton("Add New")
        self.add_btn.setFixedSize(100, 50)
        edit_btn = QPushButton("Edit Current")
        edit_btn.setFixedSize(100, 50)
        del_btn = QPushButton("Delete Current")
        del_btn.setFixedSize(100, 50)

        end_less = QLineEdit()
        end_greater = QLineEdit()
        term_less = QLineEdit()
        term_greater = QLineEdit()
        updateBtn = QPushButton()
        updateBtn.setText("Filter")
        updateBtn.setFixedSize(50, 30)

        h_l = QGridLayout()
        h_l.setSpacing(10)
        h_l.addWidget(rc.Label('ID'), 0, 0)
        h_l.addWidget(self.id1, 0, 1)
        h_l.addWidget(rc.Label('username'), 0, 2)
        h_l.addWidget(self.username, 0, 3)
        h_l.addWidget(rc.Label('token'), 0, 4)
        h_l.addWidget(self.token, 0, 5)

        h_l_2 = QGridLayout()
        h_l_2.setSpacing(10)
        h_l_2.addWidget(rc.Label('cookie'), 1, 0)
        h_l_2.addWidget(self.cookie, 1, 1)
        h_l_2.addWidget(rc.Label('checkbox'), 1, 2)
        h_l_2.addWidget(self.checkbox, 1, 3)
        h_l_2.addWidget(rc.Label('dateCreate'), 1, 4)
        h_l_2.addWidget(self.dateCreate, 1, 5)

        h_l_3 = QHBoxLayout()
        h_l_3.setSpacing(10)
        h_l_3.addStretch()
        h_l_3.addWidget(self.add_btn)
        h_l_3.addWidget(edit_btn)
        h_l_3.addWidget(del_btn)
        h_l_3.addStretch()

        h_l_4 = QHBoxLayout()
        h_l_4.setSpacing(10)
        h_l_4.addWidget(rc.Label('*'))
        h_l_4.addWidget(term_less)
        h_l_4.addWidget(rc.Label('*'))
        h_l_4.addWidget(term_greater)
        h_l_4.addWidget(rc.Label('*'))
        h_l_4.addWidget(end_less)
        h_l_4.addWidget(rc.Label('*'))
        h_l_4.addWidget(end_greater)
        h_l_4.addWidget(updateBtn)

        layout.addWidget(self.d_view)
        layout.addItem(h_l)
        layout.addItem(h_l_2)
        layout.addItem(h_l_3)
        layout.addItem(h_l_4)
        self.setLayout(layout)

    def setData(self, headers, datas):
        self.d_view.setColumnCount(len(headers))
        self.d_view.setRowCount(len(datas))

        self.d_view.setHorizontalHeaderLabels(headers)

        for j, data in enumerate(datas):
            for i, d in enumerate(data):
                newitem = QTableWidgetItem("{}".format(d))
                self.d_view.setItem(j, i, newitem)

    def readData(self):
        username = self.username.text()
        token = self.token.text()
        cookie = self.cookie.text()
        checkbox = self.checkbox.text()
        dateCreate = self.dateCreate.text()

        data = (username, token, cookie, checkbox, dateCreate)

        if any(elem is "" for elem in data):
            return
        return data


class DataBrowser(QTabWidget):
    def __init__(self, parent=None):
        super(DataBrowser, self).__init__(parent)

        for tableName in tableNames:
            sqlManager.DatabaseManager(app.DB_PTH, tableName)

        self.dbu = sqlManager.DatabaseManager(app.DB_PTH, "userTokenLogin")

        self.tab1 = Tab1(self)
        self.tab2 = Tab2(self)

        self.addTab(self.tab1, "Data View")
        self.addTab(self.tab2, "Data Edit")

        self.setWindowTitle("database viewer")
        # self.setFixedSize(800, 400)
        self.setWindowIcon(QIcon('icon.png'))

        self.tab2.add_btn.clicked.connect(self.add)
        self.updateData()

    def add(self):
        data = self.tab2.readData()
        if data:
            self.dbu1.addentry(data)
            self.updateData()

    def updateData(self):
        headers = self.dbu.getcols()
        datas = self.dbu.gettable()
        self.tab2.setData(headers=headers, datas=datas)


if __name__ == '__main__':
    sqlApp = QApplication(sys.argv)
    ex = DataBrowser()
    ex.show()
    sqlApp.exec_()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/06/2018 - 12:45 AM