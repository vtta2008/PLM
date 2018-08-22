# -*- coding: utf-8 -*-
"""

Script Name: pSQL.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sqlite3 as lite

# PLM
from docker.Storage import PObj

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

if __name__ == '__main__':
    SQLS()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/08/2018 - 9:20 PM
# © 2017 - 2018 DAMGteam. All rights reserved