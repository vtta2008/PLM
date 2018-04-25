# -*- coding: utf-8 -*-
"""

Script Name: core.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    this script is to setup everything necessary in the begining for you.

"""
# -------------------------------------------------------------------------------------------------------------
setup = dict(

__appname__ = "Pipeline Tool",
__module__ = "Plt",
__version__ = "13.0.1",
__organization__ = "DAMG team",
__website__ = "www.dot.damgteam.com",
__email__ = "dot@damgteam.com",
__author__ = "Trinh Do, a.k.a: Jimmy",
__root__ = "PLT_RT",
__db__ = "PLT_DB",

)

format = dict(

__format1__ = "%(asctime)s %(levelname)s %(message)s",
__format2__ = "%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s",

)

name = dict(
    
__key__ = "PIPELINE_TOOL",
__core__ = "core",
__log__ = "core.log",
__data__ = "core.db",
    
)


message = dict(

DISALLOW = "Sorry, but only Admin can do this function, please contact JimJim for details.",
TIT_BLANK = 'Blank title will be set to "Tester"',
PW_BLANK = "Password is blank.",
PW_WRONG = "Your password is wrong.",
PW_UNMATCH = "Password doesn't match",
PW_CHANGED = "Your password has changed",
FN_BLANK = "Firstname cannot be blank",
LN_BLANK = "Lastname cannot be blank",
SEC_BLANK = "Every sections should not be blank, please try again.",
USER_CHECK_REQUIRED = "I agree to the DAMG Terms of Service",
USER_BLANK = "Your username is blank.",
USER_CHECK_FAIL = "Wrong username or password",
USER_NOT_EXSIST = "The username does not exists",
USER_CONDITION = "This username is under condition and can not log in, please contact to admin.",
SYSTRAY_UNAVAI = "Systray could not detect any system tray on this system",

)

questions = ["What is zero divided by zero?", "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
            "I’m drunk?", "Make me a sandwich?", "Read me a haiku?", "What’s your favorite movie?", "What is ‘Inception’ about?",
            "Do you have a boyfriend?", "Do you have any pets?", "What is your favorite animal?", "What are you wearing?",
            "I’m naked", "Do you follow the three laws of robotics?", "Do you believe in God?", "What is the meaning of life?",
            "When will the world end?", "What is the best operating system?", "What phone is the best?", "What’s better: Windows or Mac?",
            "Tell me a story?", "Beatbox?", "I am your father!", "What came first: The chicken or the egg?",
            "What do you think about Google Now?", "Where is Elvis Presley?", "Are you her?", "Where did I put my keys?",
            "How many Apple Store geniuses does it take to screw in a lightbulb?", "How do I look?", "What are you doing later?",
            "What is your best pickup line?", "Are you on Facebook?", "Are you intelligent?", "Are you serious?",
            "Are you stupid?", "Is John Snow dead?", "Is winter coming?", "What are you afraid of?", "Are you human?",
            "Blah blah blah blah.", "Do I look good in this dress?", "Do these pants make me look fat?", "Do you prefer iPhone or Mac?",
            "Do you like the Apple Watch?", "Can you sing?", "Why am I here?", "What can you answer?",]


tryIt = [q.decode('utf-8') for q in questions]

__root__ = "PLT_RT"
account = ["username", "password", "firstname", "lastname", "title", "email", "phone", "address1", "address2", "postal", "city", "country"]

# -------------------------------------------------------------------------------------------------------------
# Python
import os
import sys
import logging
import sqlite3 as lite
import requests
import re
import platform
import uuid
import datetime
import time

# PyQt5
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QSettings
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QSizePolicy, QLineEdit, QLabel, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, QTabWidget, QSystemTrayIcon, QAction, QMenu, QFileDialog, QComboBox)

PLT_PKG = dict(

    job="TD|Comp|Design|Office|UV|Sound",
    TD="Maya|3ds Max|Mudbox|Houdini FX|ZBrush|Mari|Substance Painter",
    Comp="NukeX|Hiero|After Effects|Premiere Pro",
    Design="Photoshop|Illustrator",
    Office="Word|Excel",
    Sound="Audition",
    sysOpts="Host Name|Product ID|System Manufacturer|System Model|System type|BIOS Version|Domain|Windows Directory|Total Physical Memory|Available Physical Memory|Logon Server",
    filter="Non-commercial|Uninstall|Verbose|License|Skype",
    root = os.getenv(__root__),
    py = "utilities|ui",
    image="icons|imgs",
    ext=['.exe', 'PipelineTool.py', '.lnk'],

)


# Set env variables
if not os.getenv(__root__):
    os.environ[__root__] = os.getcwd().split("core")[0]
elif os.getenv(__root__) is None:
    os.environ[__root__] = os.getcwd().split("core")[0]

# Configure the current level to make it disable certain logs
logPth = os.path.join(os.getenv(__root__), "core", "core.log")
logger = logging.getLogger("core")
handler = logging.FileHandler(logPth)
formatter = logging.Formatter("%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s",)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

db_pth = os.path.join(os.getenv(__root__), "appData", "plt.db")
conn = lite.connect(db_pth)
c = conn.cursor()



def text_to_utf8(input):
    return input.encode('utf-8')

def text_to_hex(text):
    text = str(text)
    outPut = ''.join(["%02X" % ord(x) for x in text])
    return outPut

def hex_to_text(hex):
    hex = str(hex)
    bytes = []
    hexStr = ''.join(hex.split(" "))
    for i in range(0, len(hexStr), 2):
        bytes.append(chr(int(hexStr[i:i + 2], 16)))
    outPut = ''.join(bytes)
    return outPut

def get_icon(name):
    return os.path.join(os.getenv(__root__), 'icons', name + '.icon.png')

def query_table_list():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [str(t[0]) for t in c.fetchall()]

def get_location_stamp():
    r = requests.get('https://api.ipdata.co').json()

    ip = str(r['ip'])
    city = str(r['city'])
    country = str(r['country_name'])

    return ip, city, country

def query_pc_info():
    pythonVersion = sys.version
    windowOS = platform.system()
    windowVersion = platform.version()
    sysInfo = {}
    sysInfo['python'] = pythonVersion
    sysInfo['os'] = windowOS + "|" + windowVersion
    sysOpts = ["Host Name", "Product ID", "System Manufacturer", "System Model", "System type", "BIOS Version",
               "Domain", "Windows Directory", "Total Physical Memory", "Available Physical Memory", "Logon Server"]
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

class Plt_data_setup():

    def __init__(self, data):

        self.username = data[0]

        sysInfo = query_pc_info()
        datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))

        self.token = self.get_token()
        self.unixStamp = self.token.split('-')[-1]
        self.ip, self.city, self.country = get_location_stamp()
        self.dateStamp = datetime_stamp.split('||')[0]
        self.timeStamp = datetime_stamp.split('||')[1]
        self.productID = sysInfo['Product ID']
        self.os = sysInfo['os']
        self.pcUser = sysInfo['pcUser']
        self.python = sysInfo['python']

        self.build_tableConfig()
        self.build_all_tables()
        self.build_user_data(data)

    def query_userData(self, username):
        c.execute("SELECT * FROM userData")
        return [str(r[0]) for r in c.fetchall()]

    def build_username(self, username):
        c.execute("CREATE TABLE IF NOT EXISTS {username} (password TEXT, firstname TEXT, lastname TEXT, title TEXT,"
        "email TEXT, phone TEXT, address1 TEXT, address2 TEXT, postal TEXT, city TEXT, country TEXT)".format(username=username))
        tableName = username
        columnList = "password|firstname|lastname|title|email|phone|address1|address2|postal|city|country"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_user_data(self, data):

        self.build_username(data[0])

        c.execute("INSERT INTO {username} (password, firstname, lastname, title, email, phone, address1, address2, "
                  "postal, city, country) VALUES (?,?,?,?,?,?,?,?,?,?,?)".format(username=self.username),
            (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11]))

        timelog = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))

        c.execute("INSERT INTO tokenID (token, username, timelog, productID, ip, city, country) VALUES (?,?,?,?,?,?,?)",
                  (self.token, self.username, timelog, self.productID, self.ip, self.city, self.country))

        c.execute("INSERT INTO userData (username, unix, token, question1, answer1, question2, answer2, dateCreate) "
                  "VALUES (?,?,?,?,?,?,?,?)", (self.username, self.unixStamp, self.token, tryIt[6],
                                               tryIt[23], tryIt[6], tryIt[35], self.dateStamp))

        c.execute("INSERT INTO pcid (token, productid, os, pcuser, python) VALUES (?,?,?,?,?)", (self.token,
                    self.productID, self.os, self.pcUser, self.python))

        self.remove_all_data_table('username')
        self.remove_all_data_table('autoLogin')

        c.execute("INSERT INTO curUser (username, autoLogin) VALUES (?,?)", (self.username, True))

        c.execute("INSERT INTO userClass (username, class, status) VALUES (?,?,?)",(self.username, "Administrator Privilege'", "Never"))

        logger.info("Created table for %s" % self.username)

        conn.commit()

    def remove_all_data_table(self, tableName):
        # Delete old data first
        c.execute("SELECT * FROM {tableName}".format(tableName=tableName))
        c.fetchall()
        c.execute("DELETE FROM {tableName}".format(tableName=tableName))
        conn.commit()

    def build_prjTaskID(self, projName):
        c.execute("CREATE TABLE IF NOT EXISTS {projName} (projStage TEXT, assetID TEXT, shotID TEXT, taskID TEXT, "
                  "status TEXT, assign TEXT, start TEXT, end TEXT)".format(projName=projName))
        logger.info("table %s created" % projName)
        tableName = "projName"
        columnList = "projStage|assetID|shotID|taskID|status|assign|start|end"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def sysConfig(self, username):
        info = self.get_local_pc()
        productID = info['Product ID']
        check = self.check_localPC(productID)
        if check:
            token = self.query_tokenLst()
            self.update_sysInfo(token, info)
        else:
            token = self.get_token()
            self.insert_tokenID(username, token, productID)
        return productID

    def build_all_tables(self):
        self.build_userData()
        self.build_userSetting()
        self.build_userLog()
        self.build_userClass()
        self.build_curUser()
        self.build_timeLog()
        self.build_tokenID()
        self.build_pcID()
        self.build_prjLst()
        self.build_prjCrew()
        self.build_pltConfig()
        self.build_prjLst()
        self.build_prjCrew()

    def build_userData(self):
        c.execute("CREATE TABLE IF NOT EXISTS userData (username TEXT, unix TEXT, token TEXT, "
                  "question1 TEXT, answer1 TEXT, question2 TEXT, answer2 TEXT, dateCreate TEXT)")
        tableName = "userData"
        columnList = "username|dateCreate|unix|token|question1|answer1|question2|answer2|dateCreate"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_userSetting(self):
        c.execute("CREATE TABLE IF NOT EXISTS userSetting (username TEXT, settingPth TXT, avatarPth TEXT showToolBar)")
        logger.info("table userSetting created")
        tableName = "userSetting"
        columnList = "username|settingPth|unix|avatarPth|showToolBar"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_userLog(self):
        c.execute("CREATE TABLE IF NOT EXISTS userLog (username TEXT, date TEXT, login TEXT, logout TEXT)")
        logger.info("table userLog created")
        tableName = "userLog"
        columnList = "username|date|login|logout"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_userClass(self):
        c.execute("CREATE TABLE IF NOT EXISTS userClass (username TEXT, class TEXT, status TEXT)")
        tableName = "userClass"
        columnList = "username|class|status"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_curUser(self):
        c.execute("CREATE TABLE IF NOT EXISTS curUser (username TEXT, autoLogin TEXT)")
        logger.info("curUser created")
        tableName = "curUser"
        columnList = "username|autoLogin|"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_timeLog(self):
        c.execute("CREATE TABLE IF NOT EXISTS timeLog (dateTime TEXT , username TEXT, eventlog TEXT)")
        logger.info("timeLog created")
        tableName = "timeLog"
        columnList = "dateTime|username|eventlog"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_tokenID(self):
        c.execute("CREATE TABLE IF NOT EXISTS tokenID (token TEXT, username TEXT, timelog TEXT, productID TEXT, ip TEXT, "
                  "city TEXT, country TEXT)")
        logger.info("tokenID created")
        tableName = "tokenID"
        columnList = "token|username|timelog|productID|ip"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_pcID(self):
        c.execute("CREATE TABLE IF NOT EXISTS pcID (token TEXT, productID TEXT, os TEXT, pcUser TEXT, python TEXT)")
        logger.info("pcID created")
        tableName = "pcID"
        columnList = "token|productID|os|pcUser|python"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_prjLst(self):
        c.execute("CREATE TABLE IF NOT EXISTS prjLst (status TEXT, projName TEXT, start TEXT, end TEXT )")
        logger.info("prjLst created")
        tableName = "prjLst"
        columnList = "status|projName|start|end"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_prjCrew(self):
        c.execute("CREATE TABLE IF NOT EXISTS projCrew (projID TEXT, username TEXT, position TEXT)")
        logger.info("projCrew created")
        tableName = "projCrew"
        columnList = "projID|username|position"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_pltConfig(self):
        c.execute("CREATE TABLE IF NOT EXISTS pltConfig (appName TEXT, version VARCHAR(20), exePth VARCHAR(20))")
        logger.info("table plt created")
        tableName = "pltConfig"
        columnList = "appName|version|exePth"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_tableConfig(self):
        c.execute("CREATE TABLE IF NOT EXISTS tableConfig (tableName TEXT, columnList TEXT, datetimeLog TEXT)")
        logger.info("tableConfig created")
        tableName = "tableConfig"
        columnList = "tableName|columnList|datetimeLog"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def build_pathConfig(self):
        c.execute("CREATE TABLE IF NOT EXISTS varConfig (keyName TEXT, keyValue TEXT, message TEXT, name TEXT, format TEXT)")
        logger.info("dataConfig created")
        tableName = "varConfig"
        columnList = "envKey|envValue|message|name|format|"
        self.insert_tableLst(tableName, columnList)
        conn.commit()

    def insert_tableLst(self, tableName, columnList):
        datetimeLog = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
        c.execute("INSERT INTO tableConfig (tableName, columnList, datetimeLog) VALUES (?,?,?)", (tableName, columnList,
                                                                                                  datetimeLog))

#----------------------------------------------------------

    def query_tableLst(self):
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [str(t[0]) for t in c.fetchall()]

    def query_userData(self, username):
        c.execute("SELECT * FROM userData")
        return [str(r[0]) for r in c.fetchall()]

    def query_columnLst(self, tableName):
        c.execute("SELECT * FROM {tn}".format(tn=tableName))
        return [str(m[0]) for m in c.description]

    def query_userLst(self):
        c.execute("SELECT username FROM AccountUser")
        data = [str(r[0]) for r in c.fetchall()]
        return data

    def query_unixLst(self):
        c.execute("SELECT unix FROM userData")
        data = [str(r[0]) for r in c.fetchall()]
        return data

    def query_tokenLst(self):
        c.execute("SELECT token FROM TokenLog")
        data = [str(r[0]) for r in c.fetchall()]
        return data

    def query_userTokenLst(self):
        c.execute("SELECT token FROM AccountUser")
        data = [str(r[0]) for r in c.fetchall()]
        return data

    def query_appIDLst(self):
        c.execute("SELECT productID FROM TokenLog")
        data = [str(t[0]) for t in c.fetchall()]
        return data

    def query_curUser(self):
        c.execute("SELECT * FROM curUser")
        data = c.fetchall()
        if len(data) == 0:
            user = ["", "", "", "False"]
        else:
            user = [str(p) for p in list(data[0])]
        return user

    def query_userClass(self, username):
        c.execute("SELECT * FROM userClass")
        rows = c.fetchall()
        userClass = 'UnKnown'
        for row in rows:
            data = [str(f) for f in row]
            if username == data[1]:
                userClass = row[2]
            else:
                pass
        return userClass

    def query_userStatus(self, username):
        userData = self.query_userClass(username)
        status = userData[-1]
        return status

    def query_securityQts(self, username):
        userData = self.userProfile(username)
        question1 = userData[-3]
        question2 = userData[-2]
        return question1, question2
    
    def query_account(self, name, typeName='username'):
        if typeName == 'unix':
            checkList = self.query_unixLst()
        elif typeName == 'token':
            checkList = self.query_tokenLst()
        else:
            checkList = self.query_userLst()

        if name in checkList:
            return True
        else:
            return False

    def query_localPC(self, productID):
        idList = self.query_appIDLst()
        if idList is None or idList == []:
            return False
        else:
            if productID in idList:
                return True
            else:
                return False

    def check_pw_match(self, username, password):
        usernameLst = self.query_userLst()
        passwordLst = self.query_passwordLst()
        passCheck = passwordLst[usernameLst.index(username)]
        if password == passCheck:
            check = True
        else:
            check = False
        return check
    
    def query_curUser(self, username, rememberLogin):
        c.execute("SELECT * FROM CurrentUser")
        data = c.fetchall()
        c.execute("DELETE FROM CurrentUser")
        c.execute("INSERT INTO CurrentUser (username,rememberLogin) VALUES (?,?)",(username, rememberLogin))
        conn.commit()

    def rememberLogin(self, token, newValue):
        c.execute("SELECT * FROM TokenLog")
        c.fetchall()
        c.execute("UPDATE TokenLog SET rememberLogin = (?) WHERE token = (?)", (newValue, token))
        conn.commit()
        self.insert_timeLog('Update New User Login')

    def sysInfo(self, token, info):
        c.execute("SELECT * FROM ProductID")
        productID = info["Product ID"]
        os = info['os']
        pcUser = info['pcUser']
        python = info['python']
        c.execute("UPDATE pcid SET token=(?), productID=(?), os=(?), pcUser=(?), python=(?)",
                  (token, productID, os, pcUser, python))
        conn.commit()

    def tableLst(self):
        c.execute("SELECT * FROM TableContent")
        data = c.fetchall()
        c.execute("DELETE FROM TableContent")
        tableLst = self.query_tableLst()

        if 'UserClassDB' in tableLst:
            tableLst.remove('UserClassDB')

        for tableName in tableLst:
            cll = self.query_columnLst(tableName)
            columnContent = ""
            for column in cll:
                columnContent = columnContent + column + "||"
            datetimeLog = self.get_datetime()
            c.execute("INSERT INTO TableContent (tableName, columnList, datetimeLog) VALUES (?,?,?)",
                      (tableName, columnContent, datetimeLog))
        conn.commit()
        event = 'Update table all content'
        self.insert_timeLog(event)

    def update_password(self, unix, new_password):
        c.execute("SELECT * FROM AccountUser")
        rows = c.fetchall()
        c.execute("UPDATE AccountUser Set password = (?) WHERE unix = (?)", (new_password, unix))
        conn.commit()
        self.insert_timeLog('Changed password')

    def update_curUser(self, username, rememberLogin):
        c.execute("SELECT * FROM CurrentUser")
        data = c.fetchall()
        c.execute("DELETE FROM CurrentUser")
        c.execute("INSERT INTO CurrentUser (username,rememberLogin) VALUES (?,?)",(username, rememberLogin))
        conn.commit()

    def update_rememberLogin(self, token, newValue):
        c.execute("SELECT * FROM TokenLog")
        c.fetchall()
        c.execute("UPDATE TokenLog SET rememberLogin = (?) WHERE token = (?)", (newValue, token))
        conn.commit()
        self.insert_timeLog('Update New User Login')

    def update_sysInfo(self, token, info):
        c.execute("SELECT * FROM ProductID")
        productID = info["Product ID"]
        os = info['os']
        pcUser = info['pcUser']
        python = info['python']
        c.execute("UPDATE pcid SET token=(?), productID=(?), os=(?), pcUser=(?), python=(?)",
                  (token, productID, os, pcUser, python))
        conn.commit()

    def update_tableLst(self):
        c.execute("SELECT * FROM TableContent")
        data = c.fetchall()
        c.execute("DELETE FROM TableContent")
        tableLst = self.query_tableLst()

        if 'UserClassDB' in tableLst:
            tableLst.remove('UserClassDB')

        for tableName in tableLst:
            cll = self.query_columnLst(tableName)
            columnContent = ""
            for column in cll:
                columnContent = columnContent + column + "||"
            datetimeLog = self.get_datetime()
            c.execute("INSERT INTO TableContent (tableName, columnList, datetimeLog) VALUES (?,?,?)",
                      (tableName, columnContent, datetimeLog))
        conn.commit()
        event = 'Update table all content'
        self.insert_timeLog(event)

    def update_update_password(self, unix, new_password):
        c.execute("SELECT * FROM AccountUser")
        rows = c.fetchall()
        c.execute("UPDATE AccountUser Set password = (?) WHERE unix = (?)", (new_password, unix))
        conn.commit()
        self.insert_timeLog('Changed password')

    def get_token(self):
        return str(uuid.uuid4())

    def insert_userTable(self, data):
        username = data[0]
        c.execute("INSERT INTO {username} (password, firstname, lastname, title, email, phone, address1, address2, "
                  "postal, city, country) VALUES (?,?,?,?,?,?,?,?,?,?,?)".format(username = username),
            (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11]))
        conn.commit()

    def insert_userData(self, data):
        c.execute("INSERT INTO userData (username, dateCreate, unix, token, question1, answer1, question2, answer2) "
                  "VALUES (?,?,?,?,?,?,?,?)", (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
        conn.commit()

    def insert_tokenID(self, data):
        c.execute("INSERT INTO token (token, username, productID, ip, city, country) VALUES (?,?,?,?,?,?)",
                  (data[0], data[1], data[2], data[3], data[4], data[5]))
        conn.commit()

    def insert_timeLog(self, eventlog):
        username = self.query_curUser()[2]
        datetimeLog = self.get_datetime()
        c.execute("INSERT INTO TimeLog (datetimeLog, username, eventLog) VALUES (?,?,?)",
                  (datetimeLog, username, eventlog))
        conn.commit()
        return True

    def insert_pcid(self, username, token, info):
        datetimeLog = self.get_datetime()
        productID = info["Product ID"]
        OS = info['os']
        pcUser = info['pcUser']
        python = info['python']
        c.execute("INSERT INTO pcid (token, productid, os, pcuser, python) VALUES (?,?,?,?,?)",
                  (token, username, productID, OS, pcUser, python, datetimeLog))
        conn.commit()

    def insert_userClass(self, data):
        c.execute("INSERT INTO userClass (username, class, status) VALUES (?,?,?)", (data[0], data[1], data[2]))
        conn.commit()

    def insert_pcID(self, data):
        c.execute("INSERT INTO pcid (token, productID, os, pcUser, python) VALUES (?,?,?,?,?)",
                  (data[0], data[1], data[2], data[3], data[4]))
        conn.commit()

    def insert_curUser(self, username):
        c.execute("INSERT INTO curUser (username) VALUES (?)", (username,))

Plt_data_setup()

