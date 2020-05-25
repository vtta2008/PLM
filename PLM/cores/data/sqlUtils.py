# -*- coding: utf-8 -*-
"""

Script Name: sqlPreset.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import time, datetime, os
import sqlite3 as lite

# PLM
from PLM                            import create_path, __appName__, __organization__
from PLM.configs                    import DB_ATTRIBUTE_TYPE
from PLM.api.Core                   import Timer, Date
from PLM.api.damg                   import DAMG, DAMGLIST, DAMGDICT


LOCAL_DB                            = create_path(os.getenv('LOCALAPPDATA'), __organization__, __appName__, 'local.db')


def get_datetime():
    datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
    return datetime_stamp

def getDate():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[0]

def getTime():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[1]


class sqlUtils(DAMG):

    key                                 = 'LocalDatabase'
    _dbPath                             = LOCAL_DB
    conn                                = lite.connect(_dbPath)
    conn.text_factory                   = str
    cur                                 = conn.cursor()
    tableNames                          = DAMGLIST()
    tables                              = DAMGDICT()
    db_types                            = DB_ATTRIBUTE_TYPE

    def __init__(self, parent=None):
        super(sqlUtils, self).__init__(parent)

        self.date                       = Date()
        self.time                       = Timer()
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

    def timelog(self, details):
        self.username, token, cookie, remember = self.query_table("curUser")
        time = self.time.currentTime()
        date = self.date.currentDate()
        self.cur.execute("INSERT INTO timelog (username, time, date, details) VALUES (?,?,?,?)", (self.username, time, date, details))
        self.conn.commit()

    def update_user_login(self, username, token, cookie, remember):
        self.cur.execute("SELECT * FROM curUser")
        self.cur.fetchall()
        self.cur.execute("DELETE FROM curUser")
        self.cur.execute("INSERT INTO curUser ('username', 'token', 'cookie', 'remember') VALUES (?,?,?,?)", (username, token, cookie, remember))
        self.conn.commit()

    def update_table(self, tableName, values):
        columns = self.columnList(tableName)
        cmd = ""
        vcmd = ""
        for i in range(len(columns)):
            cmd += '{0}, '.format(str(columns[i]))
            vcmd += '{0}, '.format(values[i])
        command = "INSERT INTO {0} ({1}) VALUES ({2})".format(tableName, cmd[0:-2], vcmd[0:-2])

        self.cur.execute("{0} ".format(command), )
        self.conn.commit()

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