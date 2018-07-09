# -*- coding: utf-8 -*-
"""

Script Name: localSQL.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys
import sqlite3 as lite

from appData import DB_PTH


# Plt
from utilities import utils as func

class QuerryDB(list):

    def query_table(self, tn="curUser"):
        conn = lite.connect(DB_PTH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM {0}".format(tn))
        data = list(cur.fetchall()[0])
        return data

class UpdateDB(object):

    conn = lite.connect(DB_PTH)
    cur = conn.cursor()

    def __init__(self, tn="curUser", data=list):
        super(UpdateDB, self).__init__()
        if tn == "curUser":
            self.update_curUser(data)

    def update_curUser(self, data):
        self.cur.execute("INSERT INTO curUser (username, token, cookie, remember) VALUES (?,?,?,?)", (data[0], data[1], data[2], data[3]))
        self.conn.commit()
        return True

class RemoveDB(object):

    conn = lite.connect(DB_PTH)
    cur = conn.cursor()

    def __init__(self, tn="curUser"):
        super(RemoveDB, self).__init__()

        self.remove_data(tn)

    def remove_data(self, tn):
        self.cur.execute("SELECT * FROM {0}".format(tn))
        self.cur.fetchall()
        self.cur.execute("DELETE FROM {0}".format(tn))
        self.conn.commit()

class TimeLog(object):

    conn = lite.connect(DB_PTH)
    cur = conn.cursor()

    def __init__(self, details=None):
        super(TimeLog, self).__init__()
        self.username, token, cookie, remember = QuerryDB().query_table("curUser")
        self.time = func.getTime()
        self.date = func.getDate()
        self.details = details
        self.cur.execute("INSERT INTO timelog (username, time, date, details) VALUES (?,?,?,?)", (self.username, self.time, self.date, self.details))
        self.conn.commit()

# -------------------------------------------------------------------------------------------------------------
"""

Created by panda on 3/06/2018 - 3:58 AM
Pipeline manager - DAMGteam

"""