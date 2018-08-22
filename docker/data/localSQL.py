# -*- coding: utf-8 -*-
"""

Script Name: localSQL.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

""" Import """

# Python
import sqlite3 as lite
from core.paths             import DB_PTH
from docker.Storage import PObj

# Plt
from docker import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Resource database """

TN  = ['curUser'   , 'userTokenLogin', 'timelog' , 'tmpConfig', ]                               # Table name

IDN = ['id'        , 'userid'        , 'tokenid' , 'pcid'     , ]                               # ID name
CTN = ['username'  , 'token'         , 'cookie'  , 'remember' , 'details', ]                    # Common name
TCN = ['date'      , 'time'          , 'datetime', ]                                            # Time column name
CCN = ['lastConfig', 'curSettingPth' , ]                                                        # Config column name

IDA = ['INTEGER PRIMARY KEY AUTOINCREMENT, ', 'INT PRIMARY KEY, ', ]                            # ID attribute
CTA = ['TEXT NOT NULL, '                    , 'TEXT, '           , 'BOOL, ', ]                  # Common attribute
STA = ['VACHAR(20,) '                       , 'VARCHAR, '        , ]                            # String attribute

CC = "CREATE TABLE IF NOT EXISTS "                                                              # Create table

# Attribute preset
ATD = dict( id            = IDA[0], userid = IDA[1], tokenid  = IDA[0], pcid     = IDA[0], username   = CTA[0],
            token         = CTA[1], cookie = CTA[1], remember = CTA[2], details  = CTA[1], lastConfig = STA[1],
            curSettingPth = CTA[1], date   = CTA[1], time     = CTA[1], datetime = CTA[1], )

# Local table details
LTD = dict(
            curUser         = [CTN[0], CTN[1], CTN[2], CTN[3], ],
            userTokenLogin  = [IDN[2], CTN[0], CTN[1], TCN[2], ],
            timelog         = [CTN[0], TCN[1], TCN[0], CTN[4], ],
            tmpConfig       = [CCN[0], CCN[1], ],
)

# -------------------------------------------------------------------------------------------------------------
""" Create database """

class SQLS(PObj):

    key = "Resource DB"

    def __init__(self, filename, parent=None):
        super(SQLS, self).__init__(parent)

        self.fn = filename
        self.conn = lite.connect(self.fn)
        self.cur = self.conn.cursor()

        for tn in TN:
            self.create_table(tn)

    def generate_command(self, tn = TN[0]):
        cl = LTD[tn]
        cmd = ""
        for i in range(len(cl)):
            cmd += cl[i] + " " + ATD[cl[i]]
        cmd = cmd[:-2]
        return cmd

    def create_table(self, tn = TN[0]):
        cmd = self.generate_command(tn)
        self.cur.execute("CREATE TABLE IF NOT EXISTS `{0}` ({1})".format(tn, cmd))
        self.conn.commit()


class QuerryDB(list):

    key = 'query db'

    def __init__(self):
        self.reg = PObj(self)

    def query_table(self, tn="curUser"):
        conn = lite.connect(DB_PTH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM {0}".format(tn))

        if len(cur.fetchall()) == 0:
            return []
        else:
            return list(cur.fetchall()[0])

class UpdateDB(PObj):

    key = 'update db'
    conn = lite.connect(DB_PTH)
    cur = conn.cursor()

    def __init__(self, tn="curUser", data=[]):
        super(UpdateDB, self).__init__()
        if tn == "curUser":
            self.update_curUser(data)
        elif tn == 'tmpConfig':
            self.update_tmpCfg(data[0])

    def update_curUser(self, data):
        self.cur.execute("INSERT INTO curUser (username, token, cookie, remember) VALUES (?,?,?,?)", (data[0], data[1], data[2], data[3]))
        self.conn.commit()
        return True

    def update_tmpCfg(self, data):
        self.cur.execute("INSERT INTO curUser (username, token, cookie, remember) VALUES (?,?)", (data[0], data[1]))
        self.conn.commit()
        return True

class RemoveDB(PObj):

    key = 'delete db'

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

class TimeLog(PObj):

    key = 'timelog object'

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
# Created by panda on 3/06/2018 - 3:58 AM
# Pipeline manager - DAMGteam