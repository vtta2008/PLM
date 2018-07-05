# -*- coding: utf-8 -*-
"""

Script Name: sqlBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
import sqlite3 as lite
from appData.Loggers import SetLogger
logger = SetLogger()

# -------------------------------------------------------------------------------------------------------------
""" Resource database """

TN = ['curUser', 'userTokenLogin', 'timelog', ]                         # Table name
IDN = ['id', 'userid', 'tokenid', 'pcid', ]                             # ID name
CTN = ['username', 'token', 'cookie', 'remember', 'details']            # Common table name
TCN = ['date', 'time', 'datetime']                                      # Time column name

# Table attribute name
IDA = ['INTEGER PRIMARY KEY AUTOINCREMENT, ', 'INT PRIMARY KEY, ']
CTA = ['TEXT NOT NULL, ', 'TEXT, ', 'BOOL, ', ]
STA = ['VACHAR(20,) ', 'VARCHAR, ']

# Command to create table
CC = "CREATE TABLE IF NOT EXISTS "

ATD = dict(
    id = IDA[0],
    userid = IDA[1],
    tokenid = IDA[0],
    pcid = IDA[0],
    username = CTA[0],
    token = CTA[1],
    cookie = CTA[1],
    remember = CTA[2],
    details = CTA[1],
    date = CTA[1],
    time = CTA[1],
    datetime = CTA[1],
)

# Local table details
LTD = dict(
    curUser = [CTN[0], CTN[1], CTN[2], CTN[3]],
    userTokenLogin = [IDN[2], CTN[0], CTN[1], TCN[2], ],
    timelog = [CTN[0], TCN[1], TCN[0], CTN[4], ]
)

# -------------------------------------------------------------------------------------------------------------
""" Create database """

class GenerateResource(object):

    appDataDir = os.path.dirname(__file__).split('scr')[0]
    dbLocalFileName = "local.db"
    dbLocal = os.path.join(appDataDir, dbLocalFileName)

    conn = lite.connect(dbLocal)
    cur = conn.cursor()

    def __init__(self):
        super(GenerateResource, self).__init__()

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
        logger.info(" Created table: {0}".format(tn))
        self.conn.commit()

if __name__ == '__main__':
    GenerateResource()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 12:40 AM
# Pipeline manager - DAMGteam