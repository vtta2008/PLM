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
__module__ = "plt",
__version__ = "13.0.1",
__organization__ = "DAMG team",
__website__ = "www.dot.damgteam.com",
__email__ = "dot@damgteam.com",
__author__ = "Trinh Do, a.k.a: Jimmy",

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

# Set env variables
if not os.getenv("PIPELINE_TOOL"):
    os.environ["PIPELINE_TOOL"] = os.getcwd().split("core")[0]
elif os.getenv("PIPELINE_TOOL") is None:
    os.environ["PIPELINE_TOOL"] = os.getcwd().split("core")[0]

# Configure the current level to make it disable certain logs
logPth = os.path.join(os.getenv("PIPELINE_TOOL"), "core", "core.log")
logger = logging.getLogger("core")
handler = logging.FileHandler(logPth)
formatter = logging.Formatter("%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s",)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

db_pth = os.path.join(os.getenv("PIPELINE_TOOL"), "appData", "plt.db")
conn = lite.connect(db_pth)
c = conn.cursor()

demodata = ["demo", "70617373776F7264", "Mr.", "Nobody", "Homeless", "dot@damgteam.com", "1234567890", "forever",
            "homeless", "no postal", "anywhere", "in the world"]

def query_table_list():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [str(t[0]) for t in c.fetchall()]

class Create_table_set(object):

    def __init__(self):

        self.buildDB()

    def buildDB(self):

        c.execute("CREATE TABLE IF NOT EXISTS token (token TEXT, username TEXT, productID TEXT, ip TEXT, city TEXT, country TEXT)")
        logger.info("Created table token")

        c.execute("CREATE TABLE IF NOT EXISTS user_data (username TEXT, date_create TEXT, unix TEXT, token TEXT )")
        logger.info("Created table user_data")

        c.execute("CREATE TABLE IF NOT EXISTS user_log (username TEXT, date_login TEXT, date_logout TEXT)")
        logger.info("Created table user_log")

        c.execute("CREATE TABLE IF NOT EXISTS class (username TEXT, class TEXT, status TEXT)")
        logger.info("Created table class")

        c.execute("CREATE TABLE IF NOT EXISTS pcid (token TEXT, productid TEXT, os TEXT, pcuser TEXT, python TEXT)")
        logger.info("Created table pcid")

        c.execute("CREATE TABLE IF NOT EXISTS user_setting (username TEXT, showToolbar TXT, avatar TEXT)")
        logger.info("Created table user_setting")

        c.execute("CREATE TABLE IF NOT EXISTS data_set (setup TEXT, account TEXT, message TEXT, name TEXT, format TEXT)")
        logger.info("Created table data_set")

        c.execute("CREATE TABLE IF NOT EXISTS curUser (username TEXT, auto_login TEXT)")
        logger.info("Created table curUser")

        conn.commit()

class Insert_user_data(object):

    def __init__(self, data=None):
        super(Insert_user_data, self).__init__()

        self.username = data[0]

        Create_table_set()

        sysInfo = self.query_pc_info()
        datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))

        self.token = str(uuid.uuid4())
        self.unixStamp = self.token.split('-')[-1]
        self.ip, self.city, self.country = self.get_location_stamp()
        self.dateStamp = datetime_stamp.split('||')[0]
        self.timeStamp = datetime_stamp.split('||')[1]
        self.productID = sysInfo['Product ID']
        self.os = sysInfo['os']
        self.pcUser = sysInfo['pcUser']
        self.python = sysInfo['python']

        self.build_user_data(data)


    def build_user_data(self, data):

        if not len(data) == 12:
            logger.warning("Can not process, need atleast 12 items, you have %" % str(len(data)))
            return False
        else:
            c.execute("CREATE TABLE IF NOT EXISTS {username} (password TEXT, firstname TEXT, lastname TEXT, title TEXT,"
                      "email TEXT, phone TEXT, address1 TEXT, address2 TEXT, postal TEXT, city TEXT, country TEXT)".format(username=self.username))

            logger.info("slot for %s has been created" % self.username)

            c.execute("INSERT INTO {username} (password, firstname, lastname, title, email, phone, address1, address2, "
                      "postal, city, country) VALUES (?,?,?,?,?,?,?,?,?,?,?)".format(username=self.username),
                (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11]))

            c.execute("INSERT INTO token (token, username, productID, ip, city, country) VALUES (?,?,?,?,?,?)", (self.token,
                        self.username, self.productID, self.ip, self.city, self.country))

            c.execute("INSERT INTO user_data (username, date_create, unix, token) VALUES (?,?,?,?)", (self.username,
                    self.dateStamp, self.unixStamp, self.token))


            c.execute("INSERT INTO pcid (token, productid, os, pcuser, python) VALUES (?,?,?,?,?)", (self.token,
                        self.productID, self.os, self.pcUser, self.python))

            c.execute("INSERT INTO curUser (username) VALUES (?)", (self.username,))

            logger.info("Created table for %s" % self.username)

            conn.commit()

    def get_location_stamp(self):
        r = requests.get('https://api.ipdata.co').json()

        ip = str(r['ip'])
        city = str(r['city'])
        country = str(r['country_name'])

        return ip, city, country

    def query_pc_info(*args):

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


Insert_user_data(demodata)


