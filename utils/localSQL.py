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
import datetime, time
import sqlite3 as lite

# PLM
from appData                        import DB_PTH, DB_ATTRIBUTE_TYPE
from bin.dependencies.damg.damg import DAMG, DAMGTIMER, DAMGDATE, DAMGLIST, DAMGDICT

def get_datetime():
    datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
    return datetime_stamp

def getDate():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[0]

def getTime():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[1]


# class QuerryDB(DAMG):
#
#     key = 'QuerryDB'
#     conn = lite.connect(DB_PTH)
#     cur = conn.cursor()
#
#     def query_table(self, tn="curUser"):
#         self.cur.execute("SELECT * FROM {0}".format(tn))
#         data = self.cur.fetchall()
#         return list(data[0])
#
# class UpdateDB(DAMG):
#
#     key = 'UpdateDB'
#     conn = lite.connect(DB_PTH)
#     cur = conn.cursor()
#
#     def __init__(self, tableName="curUser", tableValue=[]):
#         super(UpdateDB, self).__init__()
#         if tableName == "curUser":
#             self.update_curUser(tableValue)
#         elif tableName == 'tmpConfig':
#             self.update_tmpCfg(tableValue[0])
#
#     def update_curUser(self, value):
#         """ Update value of table curUser in local database """
#         self.cur.execute("INSERT INTO curUser (username, token, cookie, remember) VALUES (?,?,?,?)", (value[0], value[1], value[2], value[3]))
#         self.conn.commit()
#         return True
#
#     def update_tmpCfg(self, value):
#         """ Update temporary config """
#         self.cur.execute("INSERT INTO curUser (username, token, cookie, remember) VALUES (?,?)", (value[0], value[1]))
#         self.conn.commit()
#         return True
#
#     def update_table(self, tableName, values):
#         columns = self.columnList(tableName)
#         prefix = "INSERT INTO {0}".format(tableName)
#         midfix = "VALUES"
#
#         cmd = ""
#         vcmd = ""
#         for i in range(len(columns)):
#             cmd += columns[i] + ", "
#             vcmd += values[i] + ", "
#         command = "{0} ({1}) {2} ({3})".format(prefix, cmd, midfix, vcmd)
#         self.cur.execute("{0}".format(command))
#         self.conn.commit()
#         return True
#
#     def columnList(self, tableName):
#         cursor = self.cur.execute('SELECT * FROM {0}'.format(tableName))
#         columnLst = list(map(lambda x: x[0], cursor.description))
#         return columnLst
#
# class RemoveDB(DAMG):
#
#     key = 'RemoveDB'
#
#     conn = lite.connect(DB_PTH)
#     cur = conn.cursor()
#
#     def __init__(self, tn="curUser"):
#         super(RemoveDB, self).__init__()
#
#         self.remove_data(tn)
#
#     def remove_data(self, tn):
#         self.cur.execute("SELECT * FROM {0}".format(tn))
#         self.cur.fetchall()
#         self.cur.execute("DELETE FROM {0}".format(tn))
#         self.conn.commit()
#
# class TimeLog(DAMG):
#
#     key = 'TimeLog'
#
#     conn = lite.connect(DB_PTH)
#     cur = conn.cursor()
#
#     def __init__(self, details=None):
#         super(TimeLog, self).__init__()
#
#         self.username, token, cookie, remember = QuerryDB().query_table("curUser")
#         self.time = getTime()
#         self.date = getDate()
#         self.details = details
#         self.cur.execute("INSERT INTO timelog (username, time, date, details) VALUES (?,?,?,?)", (self.username, self.time, self.date, self.details))
#         self.conn.commit()

class LocalDatabase(DAMG):

    key                                 = 'LocalDatabase'
    _dbPath                             = DB_PTH
    conn                                = lite.connect(_dbPath)
    conn.text_factory                   = str
    cur                                 = conn.cursor()
    tableNames                          = DAMGLIST()
    tables                              = DAMGDICT()
    db_types                            = DB_ATTRIBUTE_TYPE

    def __init__(self):
        super(LocalDatabase, self).__init__(self)

        self.date = DAMGDATE()
        self.time = DAMGTIMER()
        self.update()

    def update(self):
        self.tableNames = self.tableList()
        for table in self.tableNames:
            columnLst = self.columnList(table)
            self.tables.add(table, columnLst)
        self.tables.update()
        return self.tables

    def remove_data(self, tableName):
        self.cur.execute("SELECT * FROM {0}".format(tableName))
        self.cur.fetchall()
        self.cur.execute("DELETE FROM {0}".format(tableName))
        self.conn.commit()
        return

    def timelog(self, details):
        self.username, token, cookie, remember = self.query_table("curUser")
        time = self.time.currentTime()
        date = self.date.currentDate()

        self.cur.execute("INSERT INTO timelog (username, time, date, details) VALUES (?,?,?,?)", (self.username, time, date, details))
        self.conn.commit()
        return

    def update_table(self, tableName, values):
        columns = self.columnList(tableName)
        prefix = "INSERT INTO {0}".format(tableName)
        midfix = "VALUES"

        cmd = ""
        vcmd = ""
        for i in range(len(columns)):
            cmd += columns[i] + ", "
            vcmd += values[i] + ", "
        command = "{0} ({1}) {2} ({3})".format(prefix, cmd, midfix, vcmd)
        self.cur.execute("{0}".format(command))
        self.conn.commit()
        return

    def columnList(self, tableName):
        result = self.cur.execute("PRAGMA table_info({0})".format(tableName)).fetchall()
        columnLst = list(zip(*result))[1]
        return columnLst

    def tableList(self):
        result = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        if result == []:
            table_names = result
        else:
            table_names = sorted(list(zip(*result))[0])
        return table_names

    def query_table(self, tableName="curUser"):
        self.cur.execute("SELECT * FROM {0}".format(tableName))
        data = self.cur.fetchall()
        return list(data[0])

    def generate_command(self, tableDetails):
        columnLst = [c for c in tableDetails.keys()]
        cmd = ""
        for i in range(len(columnLst)):
            column_name = columnLst[i]
            attribute_key = tableDetails[columnLst[i]]
            column_attribute = self.db_types[attribute_key]
            cmd += "{0} {1}".format(column_name, column_attribute)
        cmd = cmd[:-2]
        return cmd

    def create_table(self, tableName, tableDetails):
        cmd = self.generate_command(tableDetails)
        self.cur.execute("CREATE TABLE IF NOT EXISTS `{0}` ({1})".format(tableName, cmd))
        self.conn.commit()
        self.update()
        return

    def remove_table(self, tableName):
        self.cur.execute('DROP TABLE {0}'.format(tableName))
        self.conn.commit()
        self.update()
        return

    def create_foreign(self, id_name, table_name):
        value = 'INTERGER, FOREIGN KEY ({0}) REFERENCES {1} ({0}), '.format(id_name, table_name)
        return value



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 3:58 AM
# Pipeline manager - DAMGteam