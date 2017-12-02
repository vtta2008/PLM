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
table_current_user = 'current_user'
tlf = ['date_log', 'unix', 'log_action', 'time_log']
tcu = ['unix', 'token', 'username']
linf = ['unix', 'token', 'username', 'password']

class CreateNewUser(object):

    def __init__(self, username, password, title, lastname, firstname, avatar):
        super(CreateNewUser, self).__init__()

        password = func.encoding(password)

        self.username = username
        self.password = password

        self.create_timelog_table()

        self.create_current_login_table()

        self.create_login_account_table()

    def create_timelog_table(self):
        # Create login profile
        umaster.create_table_with_4_column(tlf[0], tlf[1], tlf[2], tlf[3], table_timelog)

    def create_current_login_table(self):
        # Create table current login user
        umaster.create_table_current_login_user(tcu[0], tcu[1], tcu[2], table_current_user)

    def create_login_account_table(self):
        # Create user account log in table
        umaster.create_table_with_4_column(linf[0], linf[1], linf[2], linf[3], table_login)

    def generate_unix_and_token_for_account(self):
        # Create unix id and token
        info = {}
        self.unix, self.token, self.datelog, self.timelog = func.generate_set_unix_id()
        info[self.username] = [self.datelog, self.timelog]
        pth = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/_bk')
        filename = '%s.%s.yml' % (self.unix, self.token)
        backupPth = os.path.join(pth, filename)
        func.dataHandle('yaml', 'w', backupPth, info)

        return self.unix, self.token, self.datelog, self.timelog

    def set_up_new_user_account(self):
        # Create user login account
        umaster.dynamic_user_account_entry(self.unix, self.token, self.username, self.password)
        # Create profile table base on unix id
        umaster.create_table_user_profile_by_unix(table_name=self.my_unix)
        # Update profile and setting
        umaster.dynamic_add_user_profile_entry(self.title, self.lastname, self.firstname, self.avatar, self.datelog, self.timelog, self.unix)

