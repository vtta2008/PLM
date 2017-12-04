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

demaoName = "DEMO TABLE"
nf = ['col1', 'col2', 'col3', 'col4']
ft = ['TEXT', 'TEXT', 'TEXT', 'TEXT']

tdKeys = ['Maya', 'HoudiniFX', 'ZBrush', 'UVLayout', 'Mudbox', '3dsMax']
vfxKeys = ['Hiero', 'NukeX', 'PremierePro']
artKeys = ['Illustrator CC', 'Photoshop']
devKeys = ['PyCharm', 'SublimeText', 'QtDesigner']
subKeys = ['Snipping', 'Wordpad']

tableName = 'Pipeline'




def create_table_with_4_column(nt=nf, ft=ft, tableName=tableName):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} {ft1}, {nf2} {ft2}, {nf3} {ft3}, {nf4} ft4);".format(
        tn=tableName, nf1=nf[1], nf2=nf[2], nf3=nf[3], nf4=nf[4], tf1=ft[1], ft2=ft[2], ft3=ft[3], ft4=ft[4]))
    conn.commit()

def create_table_with_5_column(nf1, nf2, nf3, nf4, nf5, tableName):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} TEXT, {nf2} TEXT, {nf3} TEXT, {nf4} TEXT, "
              "{nf5} TEXT)".format(tn=tableName, nf1=nf1, nf2=nf2, nf3=nf3, nf4=nf4, nf5=nf5))
    conn.commit()


""" Tool to gathering info """
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


# -------------------------------------------------------------------------------------------------------------
""" Create New Table """
# -------------------------------------------------------------------------------------------------------------
def create_table_content():
    c.execute("CREATE TABLE IF NOT EXISTS TableContent (tableName TEXT, columnList TEXT, datetimeLog TEXT)")
    conn.commit()

def create_table_timelog():
    c.execute("CREATE TABLE IF NOT EXISTS TimeLog (datetimeLog TEXT , username TEXT, eventlog TEXT)")
    conn.commit()

def create_table_user_account():
    c.execute("CREATE TABLE IF NOT EXISTS AccountUser (unix TEXT, token TEXT, username TEXT, password TEXT, "
              "title TEXT, lastname TEXT,firstname TEXT, avatar TEXT, time_stamp TEXT, date_stamp TEXT)")
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

def create_table_project_list():
    c.execute("CREATE TABLE IF NOT EXISTS proj_list (proj_name VARCHAR(20), prod_code VARCHAR(20) start_date DATE end_date DATE)")

def create_table_project_crew_on_board():
    c.execute("CREATE TABLE IF NOT EXISTS pro_crew (proj_code VARCHAR(20), proj_unix UNIQUE)")

def create_table_project_pre_production():
    c.execute("CREATE TABLE IF NOT EXISTS pre_production (script VARCHAR(20), script_dateline VARCHAR(20), storyboard VARCHAR(20)"
       "storyboard_deadline VARCHAR(20), animatic2D VARCHAR(20), animatic2D_deadline VARCHAR(20), animatic3D VARCHAR(20),"
       "animatic3D_dealine VARCHAR(20))")
    conn.commit()

def create_table_project_production():
    c.execute("CREATE TABLE IF NOT EXISTS production_state (proj_code VARCHAR(20) time_long INT, unix_ppl REAL duty VARCHAR(20) "
       "period VARCHAR(20) shots INT, assets VARCHAR(20), asset_task VARCHAR(20))")

def create_table_assets_detail():
    c.execute("CREATE TABLE IF NOT EXISTS assets_task (proj_code VARCHAR(20) art VARCHAR(20) art_dateline VARCHAR(20) "
       "modeling VARCHAR(20), modeling_dateline VARCHAR(20) rigging VARCHAR(20), rigging_dateline VARCHAR(20)"
       "lookdev VARCHAR(20), lookdev_dateline TIMESTAMP)")

def create_table_shots_detail():
    c.execute("CREATE TABLE IF NOT EXISTS shots_task (proj_code VARCHAR(20), shot_code VARCHAR(20), anim VARCHAR(20)), "
       "anim_dateline VARCHAR(20), comp VARCHAR(20), comp_dateline VARCHAR(20), vfx VARCHAR(20), vfx_dateline VARCHAR(20)"
       "layout VARCHAR(20), layout_dateline VARCHAR(20), lighting VARCHAR(20), lighting_dateline(20), "
       "shot_dateline VARCHAR(20)")

def create_table_project_post_production():
    c.execute("CREATE TABLE IF NOT EXISTS pre_production (proj_code VARCHAR(20), shot_comping VARCHAR(20), "
       "shot_comp_deadline VARCHAR(20), master_comp VARCHAR(20), sound VARCHAR(20), sound_dateline VARCHAR(20), "
       "editing VARCHAR(20), deliverable_dateline VARCHAR(20))")

def create_table_project_config_software_path():
    c.execute("CREATE TABLE IF NOT EXISTS software_path (proj_code VARCHAR(20) maya_path VARCHAR(20), zbrush_path VARCHAR(20),"
       "houdini VARCHAR(20), photoshop VARCHAR(20), nukex VARCHAR(20), after_effects VARCHAR(20), premiere_pro VARCHAR(20)"
       "mari VARCHAR(20))")

def create_table_project_folder_path():
    c.execute("CREATE TABLE IF NOT EXISTS proj_path (prod_master VARCHAR(20), )")

def create_table_pipeline_config(nf1, nf2, nf3, table_name):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} TEXT, {nf2} TEXT, {nf3} TEXT, maya TEXT, "
              "max3ds TEXT, zbrush TEXT, mudbox TEXT, houdini TEXT, "
              "mari TEXT, substance TEXT, nukex TEXT, hiero TEXT, after_effect TEXT, "
              "premiere pro  TEXT, photoshop TEXT)".format(tn=table_name, nf1=nf1, nf2=nf2, nf3=nf3))
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
    rows = [str(r[0]) for r in c.fetchall()]
    for row in rows:
        if unix in row and username in row:
            userClass = row[2]
        else:
            userClass = 'Tester'
    dynamic_insert_timelog("Query userclass: %s" % username)
    return userClass


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
    if int(password)==int(passCheck):
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

def dynamic_pipeline_config_entry(username, trackKeys):
    softs_list = ['maya', '3ds Max', 'ZBrush', 'Mudbox', 'Houdini', 'Mari', 'Substance', 'NukeX', 'Hiero',
                     'After Effects', 'Premiere Pro', 'Photoshop', 'Illustrator', 'Pycharm', 'Sublime Text']
    values = {}
    for real_key in trackKeys:
        for check_key in softs_list:
            if check_key in real_key:
                values[check_key] = 1
            else:
                values[check_key] = 0

    maya = values['maya']
    max3ds = values['3ds Max']
    zbrush = values['ZBrush']
    mudbox = values['Mudbox']
    houdini = values['Houdini']
    mari = values['Mari']
    substance = values['Substance']
    nukex = values['NukeX']
    hiero = values['Hiero']
    ae = values['AfterEffects']
    pr = values['Primiere Pro']
    pts = values['Photoshop']
    illus = values['Illustrator']
    pycharm = values['Pycharm']
    sublime = values['Sublime']


    c.execute("INSERT INTO {tn} (unix, token, product_id, maya, max3dds, zbrush, mudbox, houdini, mari, substance, "
       "nukex, hiero, ae, pr, pts, illus, pycharm, sublime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "
       "?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(tn=table_name), (unix, token, product_id, maya, max3ds, zbrush, mudbox, houdini, mari,
                                         substance, nukex, hiero, ae, pr, pts, illus, pycharm, sublime))

    conn.commit()


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
    dynamic_insert_classUser(unix, username, value)
    conn.commit()
    dynamic_insert_timelog('inserted to table AccountUser')

def dynamic_update_current_user(unix, token, username, rememberLogin):
    delete_all_data_table('currentUser')
    c.execute("INSERT INTO currentUser (unix,token,username,rememberLogin) VALUES (?,?,?,?)",
              (unix, token, username, rememberLogin))
    conn.commit()

def dynamic_insert_timelog(eventlog):
    username = query_current_user()[2]
    datetimeLog = createDatetimeLog()
    c.execute("INSERT INTO TimeLog (datetimeLog, username, eventLog) VALUES (?,?,?)",
              (datetimeLog, username, eventlog))
    conn.commit()

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


# -------------------------------------------------------------------------------------------------------------
""" Delete Data """
# -------------------------------------------------------------------------------------------------------------
def delete_all_data_table(table_name):
    # Delete old data first
    c.execute("SELECT * FROM {tn}".format(tn=table_name))
    c.fetchall()
    c.execute("DELETE FROM {tn}".format(tn=table_name))
    conn.commit()
    dynamic_insert_timelog('Clean old data')


# -------------------------------------------------------------------------------------------------------------
""" Edit Data """
# -------------------------------------------------------------------------------------------------------------
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
    dynamic_insert_timelog('update sysInfo')

def update_table_content():
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
        dynamic_insert_timelog('Update content table (%s) into TableContent' % tableName)
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
        # if self.username == 'Demo.User':
        #     pass
        # else:
        #     self.set_up_new_user_account()

        self.set_up_new_user_account()

    def set_up_new_user_account(self):
        self.unix, self.token, timelog, datelog = createSetUnixID()
        # Create user login account
        dynamic_new_user_entry(self.unix, self.token, self.username, self.password, self.title, self.lastname,
                               self.firstname, self.avatar, timelog, datelog)
        dynamic_update_current_user(self.unix, self.token, self.username, 'False')
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

# def create_member_set():
#     CreateNewUser('User', 'Demo', 'A demo user account', '123456')
#     CreateNewUser('User', 'Test', 'A test user account', '123456')
#     CreateNewUser('DM', 'Duc', 'Multimedia Design', '123456')
#     CreateNewUser('Do', 'Trinh', 'PipelineTD', 'adsadsa')


