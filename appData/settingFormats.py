# -*- coding: utf-8 -*-
"""

Script Name: settingFormats.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore           import QSettings, QDateTime

INI                         = QSettings.IniFormat
Native                      = QSettings.NativeFormat
Invalid                     = QSettings.InvalidFormat

# -------------------------------------------------------------------------------------------------------------
""" Format """

LOG_FORMAT = dict(

    fullOpt                 = "%(levelname)s: %(asctime)s %(name)s, line %(lineno)s: %(message)s",
    rlm                     = "(relativeCreated:d) (levelname): (message)",
    tlm1                    = "{asctime:[{lvelname}: :{message}",
    tnlm1                   = "%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s",
    tlm2                    = '%(asctime)s|%(levelname)s|%(message)s|',
    tnlm2                   = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)

DT_FORMAT = dict(

    dmyhms                  = "%d/%m/%Y %H:%M:%S",
    mdhm                    = "'%m-%d %H:%M'",
    fullOpt                 = '(%d/%m/%Y %H:%M:%S)',
)

ST_FORMAT = dict(

    ini                     = INI,
    native                  = Native,
    invalid                 = Invalid,
)

datetTimeStamp = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")             # datestamp

IMGEXT = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

DB_ATTRIBUTE_TYPE = dict(

    int_auto_increment = 'INTERGER PRIMARY KEY AUTOINCREMENT, ',
    int_primary_key = 'INT PRIMARY KEY, ',
    text_not_null = 'TEXT NOT NULL, ',
    text = 'TEXT, ',
    bool = 'BOOL, ',
    varchar = 'VARCHAR, ',
    varchar_20 = 'VACHAR(20,)  ',

)

RAMTYPE = {
    '0': 'Unknown',
    '1': 'Other',
    '2': 'DRAM',
    '3': 'Synchronous DRAM',
    '4': 'Cache DRAM',
    '5': 'EDO',
    '6': 'EDRAM',
    '7': 'VRAM',
    '8': 'SRAM',
    '9': 'RAM',
    '10': 'ROM',
    '11': 'Flash',
    '12': 'EEPROM',
    '13': 'FEPROM',
    '14': 'EPROM',
    '15': 'CDRAM',
    '16': '3DRAM',
    '17': 'SDRAM',
    '18': 'SGRAM',
    '19': 'RDRAM',
    '20': 'DDR',
    '21': 'DDR2',
    '22': 'DDR2 FB-DIMM',
    '24': 'DDR3',
    '25': 'FBD2',
}

FORMFACTOR = {
    '0': 'Unknown',
    '1': 'Other',
    '2': 'SIP',
    '3': 'DIP',
    '4': 'ZIP',
    '5': 'SOJ',
    '6': 'Proprietary',
    '7': 'SIMM',
    '8': 'DIMM',
    '9': 'TSOP',
    '10': 'PGA',
    '11': 'RIMM',
    '12': 'SODIMM',
    '13': 'SRIMM',
    '14': 'SMD',
    '15': 'SSMP',
    '16': 'QFP',
    '17': 'TQFP',
    '18': 'SOIC',
    '19': 'LCC',
    '20': 'PLCC',
    '21': 'BGA',
    '22': 'FPBGA',
    '23': 'LGA',
    '24': 'FB-DIMM',
}

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/10/2019 - 2:50 AM
# © 2017 - 2018 DAMGteam. All rights reserved