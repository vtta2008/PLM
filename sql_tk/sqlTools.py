# coding=utf-8
"""
Script Name: databaseTools.py
Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script will find all the path of modules, icons, images ans store them to a file
"""

import os, sys, logging, time, datetime, json, yaml, subprocess
import sqlite3 as lite
from tk import appFuncs as func

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('D:\PipelineTool\sql_tk\db\user.db')

if not db.open():
    QMessageBox.critical(None, "Cannot open database",
                         "Unable to establish a database connection.py.\n"
                         "This example needs SQLite support. Please read the Qt SQL "
                         "driver documentation for information how to build it.\n\n"
                         "Click Cancel to exit.",
                         QMessageBox.Cancel)

    print 'False'

q = QSqlQuery()



def create_predatabase(id, username, password):
    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
                             "Unable to establish a database connection.py.\n"
                             "This example needs SQLite support. Please read the Qt SQL "
                             "driver documentation for information how to build it.\n\n"
                             "Click Cancel to exit.",
                             QMessageBox.Cancel)

        return False


    q.exec_("create table accountdb (id int primary key, username varchar(20), password varchar(20)")
    q.exec_("INSERT INTO acountdb VALUES (?, ?, ?,)",(id, username, password))

    return True

def create_first_profile_database(ids=99, cl='Tester', title='Tester', avatar='Tester', nickname='Tester', firstname='Tester', lastname='Tester'):

    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
                             "Unable to establish a database connection.py.\n"
                             "This example needs SQLite support. Please read the Qt SQL "
                             "driver documentation for information how to build it.\n\n"
                             "Click Cancel to exit.",
                             QMessageBox.Cancel)

        return False

    time_create = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d-%H:%M:%S'))

    q = QSqlQuery()

    q.exec_("create table profile (id int primary key, class varchar(20), title varchar(20), avatar varchar(20), nickname varchar(20), firsname varchar(20), lastname varchar(20), time_create varchar(20)")

    q.exec_("INSERT INTO profile (id, class, title, avatar, nickname, firstname, lastname, time_create) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(ids, cl, title, avatar, nickname, firstname, lastname, time_create))

    return True


create_predatabase(99, 'Testter', '313233343536')

create_first_profile_database()

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    # test_create_dbfile()

    # create_database_file()

