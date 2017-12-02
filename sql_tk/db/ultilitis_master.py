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
varchar = 'VARCHAR(20)'

def create_table_with_4_column(table_name, new_field, field_type):

    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} {ft1}, {nf2} {ft2}, {nf3} {ft3}, {nf4} {ft4".
              format(tn=table_name, nf1=new_field[0], ft1=field_type[0], nf2=new_field[1],
                     ft2=field_type[1], nf3=new_field[2], ft3=field_type[2],
                     ft4=field_type[3], nf4=field_type[3]))

    conn.commit()
    datetime_stamp = func.create_date_time_stamp()
    table_info[datetime_stamp] = [table_name, new_field, field_type]
    func.dataHandle('yaml', 'a+', table_bk_pth, table_info)
    logger.info('%s table created' % table_name)
    return True

def create_table_with_5_column(table_name, new_field, field_type):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} {ft1}, {nf2} {ft2}, {nf3} {ft3}, {nf4} {ft4}, {nf5} {ft5})".
              format(tn=table_name, nf1=new_field[0], ft1=field_type[0], nf2=new_field[1], ft2=field_type[1],
                     nf3=new_field[2], ft3=field_type[2], nf4=new_field[3], ft4=field_type[3],
                     nf5=new_field[4], ft5=field_type[4]))

    conn.commit()
    datetime_stamp = func.create_date_time_stamp()
    table_info[datetime_stamp] = [table_name, new_field, field_type]
    func.dataHandle('yaml', 'a+', table_bk_pth, table_info)
    logger.info('%s table created' % table_name)

    return True

def create_table_user_profile_by_unix(unix):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} (class VARCHAR(20), title VARCHAR(20), lastname VARCHAR(20), "
              "firstname VARCHAR(20), avatar VARCHAR(20), time_stamp VARCHAR(20), date_stamp VARCHAR(20), "
              "remember_login INT, maya INT, max3ds INT, zbrush INT, mudbox INT, houdini INT, mari INT, substance INT, "
              "nukex INT, hiero INT, after_effects INT, premiere_pro INT, photoshop INT,illustrator INT, pycharm INT, "
              "sublime INT)".format(tn=unix))

    conn.commit()
    datetime_stamp = func.create_date_time_stamp()
    table_info[datetime_stamp] = [unix, 'class', 'title', 'lastname', 'firstname', 'avatar', 'time_stamp', 'date_stamp',
                                  'remember_login', 'maya', 'max3ds', 'zbrush', 'mudbox', 'houdini', 'mari',
                                  'substance',
                                  'nukex', 'hiero', 'after_effects', 'premiere_pro', 'photoshop', 'illustrator']
    func.dataHandle('yaml', 'a+', table_bk_pth, table_info)
    logger.info('table: %s created' % unix)
    return True

def create_table_pipeline_config(table_name, new_field, field_type):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} {ft1}, {nf2} {ft2}, {nf3}{ft3}, maya VARCHAR(20), "
              "max3ds VARCHAR(20), zbrush VARCHAR(20), mudbox VARCHAR(20), houdini VARCHAR(20), "
              "mari VARCHAR(20), substance VARCHAR(20), nukex VARCHAR(20), hiero VARCHAR(20), ae VARCHAR(20), "
              "pr VARCHAR(20), pts VARCHAR(20), illus VARCHAR(20), pycharm VARCHAR(20), sublime VARCHAR(20))".
              format(tn=table_name, nf1=new_field[0], ft1=field_type[0], nf2=new_field[1], ft2=field_type[1],
                     nf3=new_field[2], ft3=field_type[2]))

    conn.commit()
    datetime_stamp = func.create_date_time_stamp()
    table_info[datetime_stamp] = [ table_name, new_field, field_type,
                                  'maya', 'max3ds', 'zbrush', 'mudbox', 'houdini', 'mari', 'substance', 'nukex',
                                  'hiero', 'after_effects', 'premiere_pro', 'photoshop', 'illustrator']

    func.dataHandle('yaml', 'a+', table_bk_pth, table_info)

    logger.info('table: %s created' % table_name)
    return True

def create_table_current_login_user(table_name, unix, token, username):
    c.execute("CREATE TABLE IF NOT EXISTS {tn} ({nf1} {ft1} , {nf2} {ft2}, {nf3} {ft3})".
              format(tn=table_name, nf1=unix, ft1=varchar, nf2=token, ft2=varchar, nf3=username, ft3=varchar, ))
    conn.commit()
    logger.info('server_querry table created')
    return True

def query_info_from_username(username):
    c.execute("SELECT * FROM {tn}".format(tn=table_login))
    rows = c.fetchall()
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


def dynamic_user_account_entry(table_name, unix, token, username, password):

    c.execute("INSERT INTO TABLE {tn} ({dt1},{dt2},{dt3},{dt4}) VALUES (?, ?, ?, ?)), "
              "(unix, token, username, password)".format(tn=table_name, dt1=unix, dt2=token, dt3=username, dt4=password))

    conn.commit()
    logger.info('inserted to table %s' % table_name)
    return True

def dynamic_update_current_login_account(table_name, unix, token, username):
    # Delete old data first
    c.execute("SELECT * FROM {tn}".format(tn=table_name))
    rows = c.fetchall()



