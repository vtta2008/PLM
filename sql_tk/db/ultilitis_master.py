# -*- coding: utf-8 -*-
"""
Script Name: ultilitis_user.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to create database

"""

import logging
import os
import sqlite3 as lite

from tk import appFuncs as func

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

table_bk_pth = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/_bk/table.map.yml')

table_info = {}
conn = lite.connect('meta_data.db')
c = conn.cursor()

table_login = 'loginCf'
table_timelog = 'timelog'
table_local_pc = 'local_pc'
table_pipeline = 'pipelineCf'
table_current_user = 'current_user'

def create_table_pipeline_config(nf1, nf2, nf3, table_name=table_pipeline):

    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} TEXT, {nf2} TEXT, {nf3} TEXT, maya TEXT, "
              "max3ds TEXT, zbrush TEXT, mudbox TEXT, houdini TEXT, "
              "mari TEXT, substance TEXT, nukex TEXT, hiero TEXT, after_effect TEXT, "
              "premiere pro  TEXT, photoshop TEXT)".format(tn=table_name, nf1=nf1, nf2=nf2, nf3=nf3))

    conn.commit()

    logger.info('table: %s created' % table_name)

def create_table_with_4_column(nf1, nf2, nf3, nf4, table_name=table_login):

    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} TEXT, {nf2} TEXT, {nf3} TEXT, {nf4} TEXT);".format(
        tn=table_name, nf1=nf1, nf2=nf2, nf3=nf3, nf4=nf4))

    conn.commit()
    logger.info('%s table created' % table_name)

def create_table_with_5_column(nf1, nf2, nf3, nf4, nf5, table_name):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} TEXT, {nf2} TEXT, {nf3} TEXT, {nf4} TEXT, "
              "{nf5} TEXT)".format(tn=table_name, nf1=nf1, nf2=nf2, nf3=nf3, nf4=nf4, nf5=nf5))

    conn.commit()

    logger.info('%s table created' % table_name)

def create_table_user_profile_by_unix(table_name):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} (title TEXT, lastname TEXT,firstname TEXT, avatar TEXT, "
              "time_stamp TEXT, date_stamp TEXT, remember_login INT, maya INT, max3ds INT, zbrush INT, mudbox INT, "
              "houdini INT, mari INT, substance INT, nukex INT, hiero INT, after_effects INT, premiere_pro INT, "
              "photoshop INT, illustrator INT )".format(tn=table_name))

    conn.commit()

    logger.info('table: %s created' % table_name)

def create_table_current_login_user(unix, token, username, table_name=table_current_user):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} TEXT , {nf2} TEXT, {nf3} TEXT)".
              format(tn=table_name, nf1=unix, nf2=token, nf3=username))

    conn.commit()

    logger.info('server_querry table created')

def delete_all_database_from_table(table_name=table_current_user):
    # Delete old data first
    c.execute("SELECT * FROM {tn}".format(tn=table_name))
    rows = c.fetchall()
    logger.info('Clean old data')
    c.execute("DELETE FROM {tn}".format(tn=table_name))
    conn.commit()
    return True

def query_info_from_username(username, table_name=table_login):
    c.execute("SELECT * FROM {tn}".format(tn=table_name))
    rows = c.fetchall()
    unix = [row[0] for row in rows if row[2] == username]
    token = [row[1] for row in rows if row[2] == username]
    password = [row[3] for row in rows if row[2] == username]
    return unix, token, password

def check_password_log_in(username, password):
    input = func.encoding(password)
    table_name = table_login
    unix, token, match = query_info_from_username(table_name, username)
    if input == match:
        returning = "PASS"
    else:
        returning = "DENY"
    return returning

def query_unix_used_list_from_unix(unix, table_name=table_login):
    """
    use login table

    """
    c.execute("SELECT unix FROM {tn}".format(tn=table_name))
    rows = c.fetchal()
    unix_list = [row[0] for row in rows]
    unix_index = unix_list.index(unix)
    return unix_index, unix_list

def query_token_list_from_token(token, table_name=table_login):
    """
    use login table

    """
    c.execute("SELECT token FROM {tn}".format(table_name))
    rows = c.fetchall()
    token_list = [row[0] for row in rows]
    token_index = token_list.index(token)
    return token_index, token_list

def query_token_list_from_unix(unix, table_name=table_login):
    """
    use login table

    """
    unix_index, unix_list = query_unix_used_list_from_unix(unix)
    c.execute("SELECT token FROM {tn}".format(tn=table_name))
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

def query_product_id_from_unix(unix, table_name=table_local_pc):
    index, token = query_token_from_unix(unix)
    c.execute("SELECT product_id FROM {tn}".format(table_name))
    rows = c.fetchall()
    product_id_list = [row[0] for row in rows]
    product_id = product_id_list[index]
    return product_id

def query_product_id_from_token(token, table_name=table_local_pc):
    c.execute("SELECT token, product_id FROM {tn}".format(table_name))
    rows = c.fetchall()
    product_id_list = [row[0] for row in rows]
    token_index, token_list = query_token_list_from_token(token)
    product_id = product_id_list[token_index]
    return product_id

def query_value_login_remember_from_unix(unix):
    c.execute("SELECT * FROM {tn}".format(unix))
    rows = c.fetchall()
    index = 7
    for row in rows:
        value_setting_remember = row[7]

    return value_setting_remember

def query_local_info_pc_from_unix(unix):
    c.execute("SELECT * FROM local_pc")
    rows = c.fetchall()
    local_pc_info = [row for row in rows if row[0] == unix]
    return local_pc_info

def dynamic_user_account_entry(dt1, dt2, dt3, dt4, table_name=table_login):
    password = func.encoding(dt4)
    c.execute("INSERT INTO {tn} (unix, token, username, password) VALUES (?,?,?,?)".
              format(tn=table_name),(dt1, dt2, dt3, password))
    conn.commit()
    logger.info('inserted to table loginCf')

def dynamic_update_current_user(unix, token, username, table_name=table_current_user):
    c.execute("INSERT INTO {tn} (unix,token,username) VALUES (?,?,?)".format(tn=table_name),(unix, token, username))

def dynamic_new_user_entry(unix, class_, title, firstname, lastname, avatar, remember):
    time_stamp = func.create_time_stamp()
    date_stamp = func.create_date_stamp()
    c.execute("INSERT INTO {tn} (class_, title, lastname, firstname, avatar, time_stamp, date_stamp, remember) "
       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)".format(tn=unix),(class_, title, firstname, lastname, avatar, time_stamp,
                                                          date_stamp, remember))
    conn.commit()

def dynamic_update_password_by_user(unix, new_password, table_name=table_login):
    password_new = func.encoding(new_password)
    c.execute("SELECT * FROM {tn}".format(table_name))
    rows = c.fetchall()
    c.execute("UPDATE {tn} Set password = (?) WHERE unix = (?)".format(tn=table_name), (password_new, unix))
    conn.commit()

def dynamic_new_login_remember(unix, value):
    c.execute("INSERT INTO {tn} (remember_login) VALUES (?))".format(tn=unix), (value))
    conn.commit()
    return True

def dynamic_new_timelog_entry(unix, log_action, table_name=table_timelog):
    datelog = func.create_date_stamp()
    timelog = func.create_time_stamp()

    c.execute("INSERT INTO {tn} (datelog, unix, log_action, timelog) VALUES (?, ?, ?, ?,))".format(tn=table_name),
       (datelog, unix, log_action, timelog))

    conn.commit()
    return True

def dynamic_add_user_profile_entry(title, lastname, firstname, avatar, time_stamp, date_stamp, table_name):
    c.execute("INSERT INTO {tn} (title, lastname, firstname, avatar, time_stamp, date_stamp, remember_login) VALUES (?,"
        "?,?,?,?,?,?,?)".format(tn=table_name),(title, lastname, firstname, avatar, time_stamp, date_stamp))

    conn.commit()

    logger.info('table: %s created' % table_name)

def dynamic_pipeline_config_entry(unix, trackKeys, table_name=table_pipeline):
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


    c.execute("INSERT INTO {tn} (unix, token, product_id, maya, max3dds, zbrush, mudbox, houdini, mari, substance, "
       "nukex, hiero, ae, pr, pts, illus, pycharm, sublime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "
       "?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(tn=table_name), (unix, token, product_id, maya, max3ds, zbrush, mudbox, houdini, mari,
                                         substance, nukex, hiero, ae, pr, pts, illus, pycharm, sublime))

    conn.commit()

def connect_to_core_data():
    core = lite.connect('core.db')