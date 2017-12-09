# -*- coding: utf-8 -*-
"""
Script Name: ultilitis_user.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to create database

"""

import datetime
import logging
import os
import sqlite3 as lite
import sys
import time
import uuid

import requests

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

dataPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData/database.db')

table_info = {}
conn = lite.connect(dataPth)
c = conn.cursor()

USERCLASSDATA = ['Tester, DemoUser, NormalUser', 'Artist', 'Instructor', 'CEO', 'Supervisor', 'Leader']

tdKeys = ['Maya', 'HoudiniFX', 'ZBrush', 'UVLayout', 'Mudbox', '3dsMax']
vfxKeys = ['Hiero', 'NukeX', 'PremierePro']
artKeys = ['Illustrator CC', 'Photoshop']
devKeys = ['PyCharm', 'SublimeText', 'QtDesigner']
subKeys = ['Snipping', 'Wordpad']

tableName = 'Pipeline'


""" Tool to config info """
# -------------------------------------------------------------------------------------------------------------
def query_local_pc_info(*args):
    from util import variables as var
    import platform, re
    package = var.MAIN_PACKPAGE
    # python version
    pythonVersion = sys.version
    # os
    windowOS = platform.system()
    # os version
    windowVersion = platform.version()
    # create dictionary to store info in
    sysInfo = {}
    # store python info
    sysInfo['python'] = pythonVersion
    # store os info
    sysInfo['os'] = windowOS + "|" + windowVersion
    # check if info folder exists, if not, create one
    sysOpts = package['sysOpts']
    cache = os.popen2("SYSTEMINFO")
    source = cache[1].read()
    sysInfo['pcUser'] = platform.node()
    sysInfo['operating system'] = platform.system() + "/" + platform.platform()
    sysInfo['python version'] = platform.python_version()
    values = {}
    for opt in sysOpts:
        values[opt] = [item.strip() for item in re.findall("%s:\w*(.*?)\n" % (opt), source, re.IGNORECASE)][0]

    for item in values:
        sysInfo[item] = values[item]

    return sysInfo

def createDatetimeLog(*args):
    datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
    return datetime_stamp

def createDateLog(*args):
    datetimeLog = createDatetimeLog()
    dayLog = datetimeLog.split('||')[0]
    return dayLog

def createTimeLog(*args):
    datetimeLog = createDatetimeLog()
    timeLog = datetimeLog.split('||')[1]
    return timeLog

def createTokenLog(*args):
    return str(uuid.uuid4())

def createSetUnixID(*args):
    unix = (str(uuid.uuid4())).split('-')[-1]
    token = createTokenLog()
    timeLog = createTimeLog()
    dateLog = createDateLog()
    return unix, token, timeLog, dateLog

def createRandomTitle():
    import random
    secure_random = random.SystemRandom()
    value = secure_random.choice(USERCLASSDATA)
    return value

def createLocationLog(*args):
    r = requests.get('https://api.ipdata.co').json()
    info = {}
    for key in r:
        k = (str(key))
        content = str(r[key])
        info[k] = content
    ip = info['ip']
    city = info['city']
    country = info['country_name']
    return ip, city, country

def encode(text):
    text = str(text)
    outPut = ''.join(["%02X" % ord(x) for x in text])
    return outPut

def decode(hex):
    hex = str(hex)
    bytes = []
    hexStr = ''.join(hex.split(" "))
    for i in range(0, len(hexStr), 2):
        bytes.append(chr(int(hexStr[i:i + 2], 16)))

    outPut = ''.join(bytes)
    return outPut


""" Template to create table """
# -------------------------------------------------------------------------------------------------------------
demaoName = "DEMO TABLE"
nf = ['col1', 'col2', 'col3', 'col4']
ft = ['TEXT', 'TEXT', 'TEXT', 'TEXT']

def create_table_with_4_column(nf=nf, ft=ft, tableName=tableName):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} {ft1}, {nf2} {ft2}, {nf3} {ft3}, {nf4} ft4);".format(
        tn=tableName, nf1=nf[1], nf2=nf[2], nf3=nf[3], nf4=nf[4], tf1=ft[1], ft2=ft[2], ft3=ft[3], ft4=ft[4]))
    conn.commit()

def create_table_with_5_column(nf1, nf2, nf3, nf4, nf5, tableName):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} TEXT, {nf2} TEXT, {nf3} TEXT, {nf4} TEXT, "
              "{nf5} TEXT)".format(tn=tableName, nf1=nf1, nf2=nf2, nf3=nf3, nf4=nf4, nf5=nf5))
    conn.commit()


""" Create Dataset Table """
# -------------------------------------------------------------------------------------------------------------
# For user account
def create_table_content():
    c.execute("CREATE TABLE IF NOT EXISTS TableContent (tableName TEXT, columnList TEXT, datetimeLog TEXT)")
    conn.commit()

def create_table_timelog():
    c.execute("CREATE TABLE IF NOT EXISTS TimeLog (datetimeLog TEXT , username TEXT, eventlog TEXT)")
    conn.commit()

def create_table_user_account():
    c.execute("CREATE TABLE IF NOT EXISTS AccountUser (unix TEXT, token TEXT, username TEXT, password TEXT, "
              "title TEXT, lastname TEXT,firstname TEXT, avatar TEXT, time_stamp TEXT, date_stamp TEXT, status TEXT)")
    conn.commit()

def create_table_current_user():
    c.execute("CREATE TABLE IF NOT EXISTS CurrentUser (unix TEXT , token TEXT, username TEXT, rememberLogin TEXT)")
    conn.commit()

def create_table_token_log():
    c.execute("CREATE TABLE IF NOT EXISTS TokenLog (token TEXT, username TEXT, "
              "productID TEXT, ip TEXT, city TEXT, country TEXT, rememberLogin TEXT)")
    conn.commit()

def create_table_productID():
    c.execute("CREATE TABLE IF NOT EXISTS ProductID (token TEXT, username TEXT, productID TEXT, os TEXT, "
              "pcUser TEXT, python TEXT, datetimeLog TEXT )")
    conn.commit()

def create_table_userClass():
    c.execute("CREATE TABLE IF NOT EXISTS UserClassDB (unix TEXT, username TEXT, UserClass TEXT)")
    conn.commit()

# For production
def create_table_project_list():
    c.execute("CREATE TABLE IF NOT EXISTS ProjectList (proj_name VARCHAR(20), proj_code VARCHAR(20), "
              "start_date VARCHAR(20), end_date VARCHAR(20), status VARCHAR(20))")

    conn.commit()

def create_table_project_crew_on_board():
    c.execute("CREATE TABLE IF NOT EXISTS ProjectCrew (proj_code VARCHAR(20), unix VARCHAR(20))")
    conn.commit()

def create_table_project_tracking():
    c.execute("CREATE TABLE IF NOT EXISTS TaskTracking (taskName VARCHAR(20), assignedTo VARCHAR(20), "
              "proj_code VARCHAR(20), start_date VARCHAR(20), end_date VARCHAR(20))")
    conn.commit()

def create_table_project_plan():
    c.execute("CREATE TABLE IF NOT EXISTS ProjectPlan (proj_code VARCHAR(20), sections VARCHAR(20), "
              "section_details VARCHAR(20), sections_task VARCHAR(20), assignedTo VARCHAR(20), start_date VARCHAR(20), "
              "end_date VARCHAR(20), path TEXT)")

    conn.commit()

def create_table_pipeline_config():
    c.execute("CREATE TABLE IF NOT EXISTS PipelineConfig (productID TEXT, appName VARCHAR(20), path_config VARCHAR(20))")
    conn.commit()


# -------------------------------------------------------------------------------------------------------------
""" Query Data From Table """
# -------------------------------------------------------------------------------------------------------------
def query_table_list():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [str(t[0]) for t in c.fetchall()]

def query_column_list(tableName):
    c.execute("SELECT * FROM {tn}".format(tn=tableName))
    return [str(m[0]) for m in c.description]

def query_user_list():
    c.execute("SELECT username FROM AccountUser")
    data = [str(r[0]) for r in c.fetchall()]
    return data

def query_unix_list():
    c.execute("SELECT unix FROM AccountUser")
    data = [str(r[0]) for r in c.fetchall()]
    return data

def query_token_list():
    c.execute("SELECT token FROM TokenLog")
    data = [str(r[0]) for r in c.fetchall()]
    return data

def query_token_user_list():
    c.execute("SELECT token FROM AccountUser")
    data = [str(r[0]) for r in c.fetchall()]
    return data

def query_productID_list():
    c.execute("SELECT productID FROM TokenLog")
    data = [str(t[0]) for t in c.fetchall()]
    return data

def query_password_list():
    c.execute("SELECT password FROM AccountUser")
    data = [str(r[0]) for r in c.fetchall()]
    return data

def query_user_profile(name, typeName=None):
    c.execute("SELECT * FROM AccountUser")
    profileLst = c.fetchall()
    if typeName == 'unix':
        checkList = query_unix_list()
    elif typeName == 'token':
        checkList = query_token_user_list()
    else:
        checkList = query_user_list()
    index = checkList.index(name)
    data = [str(p) for p in profileLst[index]]
    return data

def query_current_user():
    c.execute("SELECT * FROM CurrentUser")
    data = c.fetchall()
    if len(data) == 0:
        user = ["", "", "", "False"]
    else:
        user = [str(p) for p in list(data[0])]
    return user

def query_original_pcToken(productID):
    idLst = query_productID_list()
    tokenLst = query_token_list()
    if len(idLst) == 1:
        token = createTokenLog()
    elif len(tokenLst) == 1:
        token = createTokenLog()
    elif len(idLst) > 1 and len(tokenLst) > 1:
        token = tokenLst[idLst.index[productID]]
    else:
        token = createTokenLog()
    return token

def query_user_class(unix, username):
    c.execute("SELECT * FROM UserClassDB")
    rows = c.fetchall()
    userClass = 'UnKnown'
    for row in rows:
        data = [str(f) for f in row]
        if unix == data[0] and username == data[1]:
            userClass = row[2]
        else:
            pass
    return userClass

def query_user_status(username):
    userData = query_user_profile(username)
    status = userData[-1]
    return status


# -------------------------------------------------------------------------------------------------------------
""" Check Data If Exists or Match """
# -------------------------------------------------------------------------------------------------------------
def check_data_exists(name, typeName='username'):
    if typeName == 'unix':
        checkList = query_unix_list()
    elif typeName == 'token':
        checkList = query_token_list()
    else:
        checkList = query_user_list()

    if name in checkList:
        return True
    else:
        return False

def check_productID_exists(productID):
    idList = query_productID_list()
    if idList is None or idList == []:
        return False
    else:
        if productID in idList:
            return True
        else:
            return False

def check_password_match(username, password):
    usernameLst = query_user_list()
    passwordLst = query_password_list()
    passCheck = passwordLst[usernameLst.index(username)]
    if password == passCheck:
        check = True
    else:
        check = False
    return check

def check_sys_configuration(username):
    info = query_local_pc_info()
    productID = info['Product ID']
    check = check_productID_exists(productID)
    if check:
        token = query_original_pcToken(productID)
        update_sysInfo_config(token, info)
    else:
        token = createTokenLog()
        dynamic_insert_newToKenLogData(username, token, productID)

    return productID

# -------------------------------------------------------------------------------------------------------------
""" Insert New Data To Table """
# -------------------------------------------------------------------------------------------------------------
def dynamic_new_user_entry(unix, token, username, password, title,
                           lastname, firstname, avatar, time_stamp, date_stamp):
    password = encode(password)
    c.execute("INSERT INTO AccountUser (unix, token, username, password, title, lastname, firstname, "
              "avatar, time_stamp, date_stamp) VALUES (?,?,?,?,?,?,?,?,?,?)",
              (unix, token, username, password, title, lastname, firstname, avatar, time_stamp, date_stamp))
    value = createRandomTitle()
    c.execute("INSERT INTO UserClassDB (unix, username, UserClass) VALUES (?,?,?)", (unix, username, value))
    conn.commit()
    dynamic_insert_timelog('inserted to table AccountUser')

def dynamic_insert_timelog(eventlog):
    username = query_current_user()[2]
    datetimeLog = createDatetimeLog()
    c.execute("INSERT INTO TimeLog (datetimeLog, username, eventLog) VALUES (?,?,?)",
              (datetimeLog, username, eventlog))
    conn.commit()
    return True

def dynamic_insert_tokenlog(token, username, productID, ip, city, country, rememberLogin):
    c.execute("INSERT INTO TokenLog (token, username, productID, ip, city, country, rememberLogin) VALUES (?,?,?,?,?,?,?)",
              (token, username, productID, ip, city, country, rememberLogin))
    conn.commit()

def dynamic_insert_localLog(username, token, info):
    datetimeLog = createDatetimeLog()
    productID = info["Product ID"]
    OS = info['os']
    pcUser = info['pcUser']
    python = info['python']
    c.execute("INSERT INTO ProductID (token, username, productID, os, pcUser, python, datetimeLog) VALUES (?,?,?,?,?,?,?)",
              (token, username, productID, OS, pcUser, python, datetimeLog))
    conn.commit()

def dynamic_insert_newToKenLogData(username, token, productID):
    info = query_local_pc_info()
    curUserData = query_current_user()
    rememberLogin = curUserData[3]
    ip, city, country = createLocationLog()
    dynamic_insert_tokenlog(token, username, productID, ip, city, country, rememberLogin)
    dynamic_insert_localLog(username, token, info)

def dynamic_insert_classUser(unix, username, value):
    c.execute("INSERT INTO UserClassDB (unix, username, UserClass) VALUES (?,?,?)", (unix, username, value))
    conn.commit()

def dynamic_pipeline_config_entry():
    currentUserData = query_current_user()
    username = currentUserData[2]
    productID = check_sys_configuration(username)

    conn.commit()


# -------------------------------------------------------------------------------------------------------------
""" Delete Data """
# -------------------------------------------------------------------------------------------------------------
def remove_all_data_table(table_name):
    # Delete old data first
    c.execute("SELECT * FROM {tn}".format(tn=table_name))
    c.fetchall()
    c.execute("DELETE FROM {tn}".format(tn=table_name))
    conn.commit()
    dynamic_insert_timelog('Clean old data')


# -------------------------------------------------------------------------------------------------------------
""" Update Data """
# -------------------------------------------------------------------------------------------------------------
def update_current_user(unix, token, username, rememberLogin):
    c.execute("SELECT * FROM CurrentUser")
    data = c.fetchall()
    c.execute("DELETE FROM CurrentUser")
    c.execute("INSERT INTO CurrentUser (unix,token,username,rememberLogin) VALUES (?,?,?,?)",
              (unix, token, username, rememberLogin))
    conn.commit()

def update_user_remember_login(token, newValue):
    c.execute("SELECT * FROM TokenLog")
    c.fetchall()
    c.execute("UPDATE TokenLog SET rememberLogin = (?) WHERE token = (?)", (newValue, token))
    conn.commit()
    dynamic_insert_timelog('Update New User Login')

def update_sysInfo_config(token, info):
    c.execute("SELECT * FROM ProductID")
    data = c.fetchall()
    datetimeLog = createDatetimeLog()
    productID = info["Product ID"]
    OS = info['os']
    pcUser = info['pcUser']
    python = info['python']
    c.execute("""UPDATE ProductID
              SET OS=(?), pcUser=(?), python=(?), datetimelog=(?) 
              WHERE productID=(?) AND token=(?)""", (OS, pcUser, python, datetimeLog, productID, token))
    
    conn.commit()

def update_table_content():
    c.execute("SELECT * FROM TableContent")
    data = c.fetchall()
    c.execute("DELETE FROM TableContent")
    tableLst = query_table_list()

    if 'UserClassDB' in tableLst:
        tableLst.remove('UserClassDB')

    for tableName in tableLst:
        cll = query_column_list(tableName)
        columnContent = ""
        for column in cll:
            columnContent = columnContent + column + "||"
        datetimeLog = createDatetimeLog()
        c.execute("INSERT INTO TableContent (tableName, columnList, datetimeLog) VALUES (?,?,?)",
                  (tableName, columnContent, datetimeLog))

    conn.commit()
    event = 'Update table all content'
    dynamic_insert_timelog(event)

def update_title_user(text):
    unix = query_current_user()[0]
    username = query_current_user()[2]
    c.execute("SELECT * FROM UserClassDB")
    data = c.fetchall()
    c.execute("""UPDATE UserClassDB 
                 SET UserClass=(?) 
                 WHERE unix=(?) AND username=(?)""", (unix, username, text))
    
    conn.commit()
    return True

def update_password_user(unix, new_password):
    password_new = encode(new_password)
    c.execute("SELECT * FROM AccountUser")
    rows = c.fetchall()
    c.execute("UPDATE AccountUser Set password = (?) WHERE unix = (?)", (password_new, unix))
    conn.commit()
    dynamic_insert_timelog('Changed password')


# -------------------------------------------------------------------------------------------------------------
""" Class: Create A New Account """
# -------------------------------------------------------------------------------------------------------------
class CreateNewUser(object):

    def __init__(self, firstname, lastname, title, password):
        super(CreateNewUser, self).__init__()

        self.username = '%s.%s' % (lastname, firstname)
        self.password = password
        self.title = title
        self.lastname = lastname
        self.firstname = firstname
        self.avatar = lastname + firstname
        if self.username == 'Demo.User':
            pass
        else:
            self.set_up_new_user_account()

        # self.set_up_new_user_account()

    def set_up_new_user_account(self):
        self.unix, self.token, timelog, datelog = createSetUnixID()
        # Create user login account
        dynamic_new_user_entry(self.unix, self.token, self.username, self.password, self.title, self.lastname,
                               self.firstname, self.avatar, timelog, datelog)
        update_current_user(self.unix, self.token, self.username, 'False')
        eventLog = "User: '%s' is created" % self.username
        dynamic_insert_timelog(eventLog)
        check_sys_configuration(self.username)
        value = createRandomTitle()
        update_title_user(value)


def create_table_set():
    create_table_timelog()
    create_table_content()
    create_table_token_log()
    create_table_user_account()
    create_table_current_user()
    create_table_productID()
    create_table_userClass()
    update_table_content()

def create_project_table_set():
    create_table_project_crew_on_board()
    create_table_project_list()
    create_table_project_plan()
    create_table_project_tracking()
    # create_table_pipeline_config()
    update_table_content()

# def create_member_set():
#     CreateNewUser('User', 'Demo', 'A demo user account', '123456')
#     CreateNewUser('User', 'Test', 'A test user account', '123456')
#     CreateNewUser('DM', 'Duc', 'Multimedia Design', '123456')
#     CreateNewUser('Do', 'Trinh', 'PipelineTD', 'adsadsa')