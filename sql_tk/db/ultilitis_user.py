# -*- coding: utf-8 -*-
"""
Script Name: ultilitis_user.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to create database

"""

import datetime
import logging
import sqlite3 as lite
import time

from sql_tk.db import ultilitis_master as umaster
from tk import appFuncs as func

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

conn = lite.connect('meta_data.db')
c = conn.cursor()
ce = c.execute

table_login = 'loginCf'
table_timelog = 'timelog'
table_local_pc = 'local_pc'
table_pipeline = 'pipelineCf'

#--------------------------------------------------------
# CREATE TABLE
def create_table_new_user(username, password):
    table_name = table_login
    new_field1 = ('unix', 'token', 'username', 'password')
    field_type1 = ('VARCHAR(20)', 'VARCHAR(20)', 'VARCHAR(20)', 'VARCHAR(20)')
    unix, token, time_stamp, date_stamp = func.generate_set_unix_id()
    umaster.create_table_with_4_column(table_name, new_field1, field_type1)
    umaster.create_table_user_profile_by_unix(table_name=unix)
    umaster.dynamic_user_account_entry(table_name, unix, token, username, password)
    # Create timelog table
    new_field2 = ('datelog', 'unix', 'log_action', 'timelog')
    umaster.create_table_with_4_column('timelog', new_field2, field_type1)
    # Create pipeline config table
    new_field3 = ('unix', 'token', 'product_id')
    field_type = ('VARCHAR(20)', 'VARCHAR(20)', 'VARCHAR(20)')
    umaster.create_table_pipeline_config(table_pipeline, new_field3, field_type)

#--------------------------------------------------------
# FROM USER




def update_password_by_user(unix, new_password):
    password_new = func.encoding(new_password)
    ce("SELECT * FROM loginCf")
    # rows = c.fetchall()
    ce("UPDATE loginCf Set password = (?) WHERE unix = (?)", (password_new, unix))
    conn.commit()

def dynamic_new_login_user_entry(unix, username, password):
    password = func.encoding(password)
    token = func.create_new_unique_id()
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


    ce("INSERT INTO pipelineCf (unix, token, product_id, maya, max3dds, zbrush, mudbox, houdini, mari, substance, "
       "nukex, hiero, ae, pr, pts, illus, pycharm, sublime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "
       "?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (unix, token, product_id, maya, max3ds, zbrush, mudbox, houdini, mari,
                                         substance, nukex, hiero, ae, pr, pts, illus, pycharm, sublime))
    conn.commit()

#--------------------------------------------------------
# QUERY DATA
def query_unix_used_list_from_unix(unix):
    ce("SELECT unix FROM loginCf")
    rows = ce.fetchal()
    unix_list = [row[0] for row in rows]
    unix_index = unix_list.index(unix)
    return unix_index, unix_list

def query_token_list_from_token(token):
    ce("SELECT token FROM loginCf")
    rows = c.fetchall()
    token_list = [row[0] for row in rows]
    token_index = token_list.index(token)
    return token_index, token_list

def query_token_list_from_unix(unix):
    unix_index, unix_list = query_unix_used_list_from_unix(unix)
    ce("SELECT token FROM loginCf")
    rows = c.fetchall()
    token_list = [row[0] for row in rows]
    token = token_list[unix_index]
    token_index = unix_index
    return token_index, token, token_list

def query_token_list_and_unix_list(unix):
    unix_index, unix_list = query_unix_used_list_from_unix(unix)
    token_index, token, token_list = query_token_list_from_unix(unix)
    index = token_index
    return index, token, unix_list, token_list

def query_token_from_unix(unix):
    index, token, unix_list, token_list = query_token_list_and_unix_list(unix)
    return index, token

def query_product_id_from_unix(unix):
    index, token = query_token_from_unix(unix)
    ce("SELECT product_id FROM local_pc")
    rows = c.fetchall()
    product_id_list = [row[0] for row in rows]
    product_id = product_id_list[index]
    return product_id

def query_product_id_from_token(token):
    ce("SELECT token, product_id FROM local_pc")
    rows = c.fetchall()
    product_id_list = [row[0] for row in rows]
    token_index, token_list = query_token_list_from_token(token)
    product_id = product_id_list[token_index]
    return product_id

def query_value_login_remember_from_unix(unix):
    ce("SELECT * FROM settingCf")
    rows = c.fetchall()
    unix_list = [row[0] for row in rows]
    value_list = [row[1] for row in rows]
    value_setting_remember = value_list[unix_list.index(unix)]
    return value_setting_remember

def query_local_info_pc_from_unix(unix):
    ce("SELECT * FROM local_pc")
    rows = c.fetchall()
    local_pc_info = [row for row in rows if row[0] == unix]
    return local_pc_info

#--------------------------------------------------------
# INSERT DATA
