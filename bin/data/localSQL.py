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
import time, datetime, os, re

from bin.data.damg import DAMG

# -------------------------------------------------------------------------------------------------------------
""" Resource database """

TN  = ['curUser'     , 'userTokenLogin', 'timelog' , 'tmpConfig', 'metadata', ]                   # Table name

MTN = ['organisation', 'application'   , 'domain'  , 'version'  , 'display' , 'author', ]         # Metadata name
IDN = ['id'          , 'userid'        , 'tokenid' , 'pcid'     , ]                               # ID name
CTN = ['username'    , 'token'         , 'cookie'  , 'remember' , 'details' , ]                   # Common name
TCN = ['date'        , 'time'          , 'datetime', ]                                            # Time column name
CCN = ['lastConfig'  , 'curSettingPth' , ]                                                        # Config column name

IDA = ['INTEGER PRIMARY KEY AUTOINCREMENT, ', 'INT PRIMARY KEY, ', ]                              # ID attribute
CTA = ['TEXT NOT NULL, '                    , 'TEXT, '           , 'BOOL, '  , ]                  # Common attribute
STA = ['VACHAR(20,) '                       , 'VARCHAR, '        , ]                              # String attribute

CC = "CREATE TABLE IF NOT EXISTS "                                                                # Create table

# Attribute preset
ATD = dict( id            = IDA[0], userid = IDA[1], tokenid  = IDA[0], pcid     = IDA[0], username     = CTA[0],
            token         = CTA[1], cookie = CTA[1], remember = CTA[2], details  = CTA[1], lastConfig   = STA[1],
            curSettingPth = CTA[1], date   = CTA[1], time     = CTA[1], datetime = CTA[1], organisation = CTA[0],
            application   = CTA[0], domain = CTA[0], version  = CTA[0], display  = CTA[0], author       = CTA[0], )

# Local table details
LTD = dict(
            curUser         = [CTN[0], CTN[1], CTN[2], CTN[3], ],
            userTokenLogin  = [IDN[2], CTN[0], CTN[1], TCN[2], ],
            timelog         = [CTN[0], TCN[1], TCN[0], CTN[4], ],
            tmpConfig       = [CCN[0], CCN[1], ],
            metadata        = MTN
)

# -------------------------------------------------------------------------------------------------------------
""" Create database """

def get_datetime():
    datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
    return datetime_stamp

def getDate():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[0]

def getTime():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[1]

if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'metadatas.py'), "rb") as f:
        metadata = f.read().decode('utf-8')
else:
    with open(os.path.join(os.getenv('DAMGTEAM'), 'bin', 'data', 'metadatas.py').replace('\\', '/'), 'rb') as f:
        metadata = f.read().decode('utf-8')

def parse(pattern):
    return re.search(pattern, metadata).group(1).replace('"', '').strip()

class SQLS(DAMG):

    key = "Resource DB"

    def __init__(self, filename='local.db', parent=None):
        super(SQLS, self).__init__(parent)

        self.fn = filename
        self.conn = lite.connect(self.fn)
        self.cur = self.conn.cursor()

        for tn in TN:
            self.create_table(tn)

        orgname = parse(r'__organization__\s+=\s+(.*)')
        appname = parse(r'__softwareName__\s+=\s+(.*)')
        domain = parse(r'__website__\s+=\s+(.*)')
        version = parse((r'__version__\s+=\s+(.*)'))
        author = parse(r'__author__\s+=\s+(.*)')
        display = parse(r'__appname__\s+=\s+(.*)')

        data = [orgname, appname, domain, version, author, display]
        print(data)

        self.cur.execute("INSERT INTO metadata ('organisation', 'application', 'domain', 'version', 'display', 'author') VALUES (?,?,?,?,?,?)",
                         (orgname, appname, domain, version, display, author))
        self.conn.commit()


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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 3:58 AM
# Pipeline manager - DAMGteam