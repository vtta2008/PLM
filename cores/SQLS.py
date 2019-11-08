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
from bin.data.damg                         import DAMG

# -------------------------------------------------------------------------------------------------------------
""" Resource database """

TABLENAME                   = ['curUser'   , 'userTokenLogin'       , 'timelog'             , 'tmpConfig', ]

IDNAME                      = ['id'        , 'userid'               , 'tokenid'             , 'pcid'     , ]
COMMONNAME                  = ['username'  , 'token'                , 'cookie'              , 'remember' , 'details', ]
TIMECOLUMNNAME              = ['date'      , 'time'                 , 'datetime'            , ]
CONFIGCOLUMNNAME            = ['lastConfig', 'curSettingPth'        , ]

IDATTRIBUTE                 = ['INTEGER PRIMARY KEY AUTOINCREMENT, ', 'INT PRIMARY KEY, '   , ]
COMMONATTRIBUTE             = ['TEXT NOT NULL, '                    , 'TEXT, '              , 'BOOL, ', ]
STRINGATTRIBUTE             = ['VACHAR(20,) '                       , 'VARCHAR, '           , ]

CREATETABLECOMMAND          = "CREATE TABLE IF NOT EXISTS "

# Attribute preset
ATD = dict(id               = IDATTRIBUTE[0],
           userid           = IDATTRIBUTE[1],
           tokenid          = IDATTRIBUTE[0],
           pcid             = IDATTRIBUTE[0],
           username         = COMMONATTRIBUTE[0],
           token            = COMMONATTRIBUTE[1],
           cookie           = COMMONATTRIBUTE[1],
           remember         = COMMONATTRIBUTE[2],
           details          = COMMONATTRIBUTE[1],
           lastConfig       = STRINGATTRIBUTE[1],
           curSettingPth    = COMMONATTRIBUTE[1],
           date             = COMMONATTRIBUTE[1],
           time             = COMMONATTRIBUTE[1],
           datetime         = COMMONATTRIBUTE[1], )

# Local table details
LTD = dict(
            curUser         = [COMMONNAME[0], COMMONNAME[1], COMMONNAME[2], COMMONNAME[3], ],
            userTokenLogin  = [IDNAME[2], COMMONNAME[0], COMMONNAME[1], TIMECOLUMNNAME[2], ],
            timelog         = [COMMONNAME[0], TIMECOLUMNNAME[1], TIMECOLUMNNAME[0], COMMONNAME[4], ],
            tmpConfig       = [CONFIGCOLUMNNAME[0], CONFIGCOLUMNNAME[1], ],
)

# -------------------------------------------------------------------------------------------------------------
""" Create database """

class SQLS(DAMG):

    key = "SQLS"

    def __init__(self, filename, parent=None):
        super(SQLS, self).__init__(parent)

        self.fn = filename
        self.conn = lite.connect(self.fn)
        self.cur = self.conn.cursor()

        for tn in TABLENAME:
            self.create_table(tn)

    def generate_command(self, tableName = TABLENAME[0]):
        cl = LTD[tableName]
        cmd = ""
        for i in range(len(cl)):
            cmd += cl[i] + " " + ATD[cl[i]]
        cmd = cmd[:-2]
        return cmd

    def create_table(self, tableName = TABLENAME[0]):
        command = self.generate_command(tableName)
        self.cur.execute("CREATE TABLE IF NOT EXISTS `{0}` ({1})".format(tableName, command))
        self.conn.commit()

if __name__ == '__main__':
    SQLS()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/08/2018 - 9:20 PM
# © 2017 - 2018 DAMGteam. All rights reserved