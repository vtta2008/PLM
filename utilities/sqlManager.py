#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: resourceDB.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import sqlite3 as lite
from appData import DB_PTH

class DatabaseManager(object):

    def __init__(self, database, table):
        self.db = database
        self.table = table

        self.con = lite.connect(DB_PTH)
        self.cursor = self.con.cursor()

        if self.table == "userTokenLogin":
            self.cursor.execute("CREATE TABLE IF NOT EXISTS`{0}`(`s_id` INTEGER PRIMARY KEY AUTOINCREMENT,`username` TEXT NOT NULL, `token` TEXT, `cookie` TEXT,`checkbox` BOOL,`dateCreate` TEXT)".format(self.table),)
        elif self.table == "curUser":
            self.cursor.execute("CREATE TABLE IF NOT EXISTS` {0}`(username TEXT, auto_login TEXT)".format(self.table),)
        elif self.table == "timeLog":
            self.cursor.execute("CREATE TABLE IF NOT EXISTS` {0}`(dateTime TEXT , username TEXT, eventlog TEXT)".format(self.table),)
        elif self.table == "security_questions":
            self.cursor.execute("CREATE TABLE IF NOT EXISTS ` {0}`(questions TEXT, timeLog TEXT, uploadBy TEXT, source TEXT)".format(self.table),)

        self.con.commit()

    def gettable(self):
        self.cursor.execute("SELECT * FROM {}".format(self.table))
        return self.cursor.fetchall()

    def getcols(self):
        self.cursor.execute("SELECT * FROM {}".format(self.table))
        return [description[0] for description in self.cursor.description]

    def addentry(self, message):
        name, mid, lec, res, term, final, end = message
        cmd = "INSERT INTO {} (name, username, token, cookie, checkbox, dateCreate, end) VALUES((?), (?), (?), (?), (?), (?), (?));".format(
            self.table)
        self.cursor.execute(cmd, (name, mid, lec, res, term, final, end))
        self.con.commit()

    def __del__(self):
        self.con.commit()
        self.cursor.close()
        self.con.close()


if __name__ == '__main__':
    dbu = DatabaseManager(app.DBPTH, 'userTokenLogin')
    dbu.addentry(('nn', 10, 11, 12, 13, 14, 15))
    print(dbu.gettable())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/06/2018 - 12:48 AM