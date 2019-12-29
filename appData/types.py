# -*- coding: utf-8 -*-
"""

Script Name: types.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


RAMTYPE = {
    0: 'Unknown',
    1: 'Other',
    2: 'DRAM',
    3: 'Synchronous DRAM',
    4: 'Cache DRAM',
    5: 'EDO',
    6: 'EDRAM',
    7: 'VRAM',
    8: 'SRAM',
    9: 'RAM',
    10: 'ROM',
    11: 'Flash',
    12: 'EEPROM',
    13: 'FEPROM',
    14: 'EPROM',
    15: 'CDRAM',
    16: '3DRAM',
    17: 'SDRAM',
    18: 'SGRAM',
    19: 'RDRAM',
    20: 'DDR',
    21: 'DDR2',
    22: 'DDR2 FB-DIMM',
    24: 'DDR3',
    25: 'FBD2',
}

FORMFACTOR = {
    0: 'Unknown',
    1: 'Other',
    2: 'SIP',
    3: 'DIP',
    4: 'ZIP',
    5: 'SOJ',
    6: 'Proprietary',
    7: 'SIMM',
    8: 'DIMM',
    9: 'TSOP',
    10: 'PGA',
    11: 'RIMM',
    12: 'SODIMM',
    13: 'SRIMM',
    14: 'SMD',
    15: 'SSMP',
    16: 'QFP',
    17: 'TQFP',
    18: 'SOIC',
    19: 'LCC',
    20: 'PLCC',
    21: 'BGA',
    22: 'FPBGA',
    23: 'LGA',
    24: 'FB-DIMM',
}

CPUTYPE = {

    1: 'Other',
    2: 'Unknown',
    3: 'Central Processor',
    4: 'Math Processor',
    5: 'DSP Processor',
    6: 'Video Processor',
}

DRIVETYPE = {
  0 : "Unknown",
  1 : "No Root Directory",
  2 : "Removable Disk",
  3 : "Local Disk",
  4 : "Network Drive",
  5 : "Compact Disc",
  6 : "RAM Disk"
}


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 29/12/2019 - 22:23
# © 2017 - 2019 DAMGteam. All rights reserved