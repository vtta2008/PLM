# coding=utf-8
"""
Script Name: databaseTools.py
Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script will find all the path of modules, icons, images ans store them to a file
"""

import os, sys, logging
import sqlite3 as lite
from tk import appFuncs as func

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

USERSQL = os.path.join(os.getcwd(), 'sql_tk\db\user.db')

def createNewAccount(username=None, password=None, avatar=None, aka=None, title=None, fullname=None, classAttr=None):
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(os.path.abspath(USERSQL))
    print db.open()

    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
                             "Unable to establish a database connection.py.\n"
                             "This example needs SQLite support. Please read the Qt SQL "
                             "driver documentation for information how to build it.\n\n"
                             "Click Cancel to exit.",
                             QMessageBox.Cancel)
        return False

    q = QSqlQuery()

    q.exec_("create table username(id int primary key, password varchar(20) , avatar varchar(20), "
            "a.k.a varchar(20), title varchar(20), class varchar(20), lastname varchar(20), firstname varchar(20))")

    q.exec_("INSERT INTO username VALUES(13, password, avatar, aka, title)")

    return True

def dynamic_username_entry()

def checkUserLogin(user_name, *args):

    usersql = os.path.join(os.getcwd(), 'sql_tk\db\user.db') #'D:\PipelineTool\sql_tk\db\user.db'

    userData = {}

    con = lite.connect(os.path.abspath(usersql))
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM user_profile")
        rows = cur.fetchall()
        for row in rows:
            if row[3] == user_name:
                userData[user_name] = rows[rows.index(row)]

    return userData

def checkPreUserLogin():

    con = lite.connect(USERSQL)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM current_login")
        rows = cur.fetchall()
        print rows

    return rows

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    createNewAccount('Trinh.Do', func.encoding('adsadsa'), 'TrinhDo', 'JimJim', 'PipelineTD', 'Trinh Do', 'Admin')