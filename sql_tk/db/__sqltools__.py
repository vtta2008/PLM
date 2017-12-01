# -*- coding: utf-8 -*-
"""
Script Name: __sqltools__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to create database

"""

import sqlite3 as lite
import time, datetime, random, logging
from tk import appFuncs as func
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

conn = lite.connect('local.db')
c = conn.cursor()
ce = c.execute


def graph_data():
    ce("SELECT")

#--------------------------------------------------------
# CREATE TABLE
def create_table_server_query()
    ce("CREATE TABLE IF NOT EXISTS current_querry (login CURRENT_USER , current_unix REAL, token VARCHAR(20))")
    logger.info('server_querry table created')
    return True

def create_table_login_user_setting():
    ce("CREATE TABLE IF NOT EXISTS settingCf (unix REAL, remember_login INT)")
    logger.info('settingCf table created')
    return True

def create_table_user_account():
    ce("CREATE TABLE IF NOT EXISTS loginCf (unix REAL, token VARCHAR(20), username USER, password VARCHAR(20), ")
    logger.info('loginCf table created')
    return True

def creaate_table_user_profile():
    ce("CREATE TABLE IF NOT EXISTS accountCf (unix REAL, class VARCHAR(20), title VARCHAR(20), lastname VARCHAR(20), "
       "firstname VARCHAR(20), avatar VARCHAR(20) create_time VARCHAR(20))")
    logger.info('accountCf table created')
    return True

def create_table_user_timelog():
    ce("CREATE TABLE IF NOT EXISTS timelog (datelog VARCHAR(20), unix VARCHAR(20), "
       "log_action VARCHAR(20) timelog VARCHAR(20))")
    logger.info('timelog table created')
    return True

def create_table_local_pc():
    ce("CREATE TABLE IF NOT EXISTS local_pc (unix VARCHAR(20), token VARCHAR(20), product_id VARCHAR(20), "
       "python_ver VARCHAR(20), platform VARCHAR(20), total_ram VARCHAR(20))")
    logger.info('local_pc table created')
    return True

def create_table_pipeline_config():
    ce("CREATE TABLE IF NOT EXISTS pipelineCf (token VARCHAR(20), product_id VARCHAR(20), maya INT, max3ds INT, "
       "zbrush INT, mudbox INT, houdini INT, mari INT, substance INT, nukex INT, hiero INT, ae INT, pr, INT, pts INT, "
       "illus INT, pycharm INT, sublime INT)")
    logger.info('pipelineCf table created')
    return True

def create_all_table():
    create_table_server_query()
    create_table_login_user_setting()
    create_table_user_account()
    creaate_table_user_profile()
    create_table_user_timelog()
    create_table_local_pc()
    create_table_pipeline_config()
    return True

def create_new_unix_value():
    rows = ce("SELECT unix FROM loginCf")
    unix_list = [row[0] for row in rows]
    while True:
        for unix_exists in unix_list:
            unix_test = random.randrange(1,100)
            if unix_test == unix_exists:
                continue
            else:
                unix = unix_test
                break
        return unix

#--------------------------------------------------------
# FROM USER
def query_info_from_username(username):
    ce("SELECT * FROM loginCf")
    rows = ce.fetchall()
    unix = [row[0] for row in rows if row[2] == username]
    token = [row[1] for row in rows if row[2] == username]
    password = [row[3] for row in rows if row[2] == username]
    return unix, token, password

def check_password_log_in(username, password):
    input = func.encoding(password)
    unix, token, match = query_info_from_username(username)
    if input == match:
        returning = "PASS"
    else:
        returning = "DENY"
    return returning

def update_password_by_user(new_password):
    password_new = func.encoding(new_password)
    ce("SELECT * FROM loginCf")
    rows = ce.fetchall()

def dynamic_new_login_user_entry(unix, username, password):
    password = func.encoding(password)
    token = func.createToken()
    ce("INSERT INTO accountCf (unix, token, username, password) VALUES (?, ?, ?, ?)",
       (unix, token, username, password))
    conn.commit()
    return True

def dynamic_new_user_entry(unix, class_, title, lastname, firstname, avatar):
    create_time = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d %H:%M:%S'))
    ce("INSERT INTO accountCf (unix, class, title, firstname, lastname, avatar, create_time) "
       "VALUES (?, ?, ?, ?, ?, ?, ?)", (unix, class_, title, firstname, lastname, avatar, create_time))
    conn.commit()
    return True

def dynamic_new_login_remember(unix, value):
    ce("INSERT INTO settingCf (unix, remember_login) VALUES (?, ?))", (unix, value))
    conn.commit()
    return True

def dynamic_new_profile_user_entry(username, password, class_, title, lastname, firstname, avatar):
    password = func.encoding(password)
    unix = create_new_unix_value()
    dynamic_new_login_user_entry(unix, username, password)
    dynamic_new_user_entry(unix, class_, title, lastname, firstname, avatar)
    return True

def dynamic_new_timelog_entry(unix, log_action):
    datelog = func.proc('date')
    timelog = func.proc('time')
    ce("INSERT INTO timelog (datelog, unix, log_action, timelog) VALUES (?, ?, ?, ?,))",
       (datelog, unix, log_action, timelog))
    conn.commit()
    return True

def dynamic_pipeline_config_entry(unix, trackKeys):
    softs_list = ['maya', '3ds Max', 'ZBrush', 'Mudbox', 'Houdini', 'Mari', 'Substance', 'NukeX', 'Hiero',
                     'After Effects', 'Premiere Pro', 'Photoshop', 'Illustrator', 'Pycharm', 'Sublime Text']
    values = {}
    token = query_token_from_unix(unix)
    product_id = query_product_id_from_unix(unix)
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


    ce("INSERT INTO pipelineCf (token, product_id, maya, max3dds, zbrush, mudbox, houdini, mari, substance, nukex, hiero,"
       "ae, pr, pts, illus, pycharm, sublime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
       (token, product_id, maya, max3ds, zbrush, mudbox, houdini, mari, substance, nukex, hiero, ae, pr, pts, illus, pycharm, sublime))

#--------------------------------------------------------
# QUERY DATA
def query_unix_list_from_unix(unix):
    ce("SELECT unix FROM loginCf")
    rows = ce.fetchal()
    unix_list = [row[0] for row in rows]
    unix_index = unix_list.index(unix)
    return unix_index, unix_list

def query_token_list_from_token(token):
    ce("SELECT token FROM loginCf")
    rows = ce.fetchall()
    token_list = [row[0] for row in rows]
    token_index = token_list.index(token)
    return token_index, token_list

def query_token_list_from_unix(unix):
    unix_index, unix_list = query_unix_list_from_unix(unix)
    ce("SELECT token FROM loginCf")
    rows = ce.fetchall()
    token_list = [row[0] for row in rows]
    token = token_list[unix_index]
    token_index = unix_index
    return token_index, token, token_list

def query_token_list_and_unix_list(unix):
    unix_index, unix_list = query_unix_list_from_unix(unix)
    token_index, token, token_list = query_token_list_from_unix(unix)
    index = token_index
    return index, token, unix_list, token_list

def query_token_from_unix(unix):
    index, token, unix_list, token_list = query_token_list_and_unix_list(unix)
    return index, token

def query_product_id_from_unix(unix):
    index, token = query_token_from_unix(unix)
    ce("SELECT product_id FROM local_pc")
    rows = ce.fetchall()
    product_id_list = [row[0] for row in rows]
    product_id = product_id_list[index]
    return product_id

def query_product_id_from_token(token):
    ce("SELECT token, product_id FROM local_pc")
    rows = ce.fetchall()
    product_id_list = [row[0] for row in rows]
    token_index, token_list = query_token_list_from_token(token)
    product_id = product_id_list[token_index]
    return product_id

def query_value_login_remember_from_unix(unix):
    ce("SELECT * FROM settingCf")
    rows = ce.fetchall()
    unix_list = [row[0] for row in rows]
    value_list = [row[1] for row in rows]
    value_setting_remember = value_list[unix_list.index(unix)]
    return value_setting_remember

def query_local_info_pc_from_unix(unix):
    ce("SELECT * FROM local_pc")
    rows = ce.fetchall()
    local_pc_info = [row for row in rows if row[0] == unix]
    return local_pc_info

#--------------------------------------------------------
# INSERT DATA
