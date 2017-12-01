# -*- coding: utf-8 -*-
"""
Script Name: __createdb.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to create database

"""


import sqlite3 as lite


conn = lite.connect('sqllocal.db')
c = conn.cursor()
cr = c.execute

def create_table():
    cr("CREATE TABLE IF NOT EXISTS accountCf (unix REAL, username TEXT, password TEXT)")
    return True

def data_entry():

    cr("INSERT INTO accountCf VALUES(99, 'Tester', '313233343536')")
    cr("INSERT INTO accountCf VALUES(13, 'Trinh.Do', '61647361647361')")
    conn.commit()
    c.close()
    conn.close()
    return True

create_table()
data_entry()
