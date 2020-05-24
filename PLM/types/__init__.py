# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

RAM_TYPE                         = {0: 'Unknown', 1: 'Other', 2: 'DRAM', 3: 'Synchronous DRAM', 4: 'Cache DRAM',
                                    5: 'EDO', 6: 'EDRAM', 7: 'VRAM', 8: 'SRAM', 9: 'RAM', 10: 'ROM', 11: 'Flash',
                                    12: 'EEPROM', 13: 'FEPROM', 14: 'EPROM', 15: 'CDRAM', 16: '3DRAM', 17: 'SDRAM',
                                    18: 'SGRAM', 19: 'RDRAM', 20: 'DDR', 21: 'DDR2', 22: 'DDR2 FB-DIMM', 24: 'DDR3',
                                    25: 'FBD2', }


FORM_FACTOR                      = {0: 'Unknown', 1: 'Other', 2: 'SIP', 3: 'DIP', 4: 'ZIP', 5: 'SOJ', 6: 'Proprietary',
                                    7: 'SIMM', 8: 'DIMM', 9: 'TSOP', 10: 'PGA', 11: 'RIMM', 12: 'SODIMM', 13: 'SRIMM',
                                    14: 'SMD', 15: 'SSMP', 16: 'QFP', 17: 'TQFP', 18: 'SOIC', 19: 'LCC', 20: 'PLCC',
                                    21: 'BGA', 22: 'FPBGA', 23: 'LGA', 24: 'FB-DIMM', }


CPU_TYPE                         = {1: 'Other', 2: 'Unknown', 3: 'Central Processor', 4: 'Math Processor', 5: 'DSP Processor',
                                    6: 'Video Processor', }


DRIVE_TYPE                       = {0 : "Unknown", 1 : "No Root Directory", 2 : "Removable Disk", 3 : "Local Disk",
                                    4 : "Network Drive", 5 : "Compact Disc", 6 : "RAM Disk", }


DB_ATTRIBUTE_TYPE               = { 'int_auto_increment'    : 'INTERGER PRIMARY KEY AUTOINCREMENT, ',
                                    'int_primary_key'       : 'INT PRIMARY KEY, ',
                                    'text_not_null'         : 'TEXT NOT NULL, ',
                                    'text'                  : 'TEXT, ',
                                    'bool'                  : 'BOOL, ',
                                    'varchar'               : 'VARCHAR, ',
                                    'varchar_20'            : 'VACHAR(20,)  ', }


CMD_VALUE_TYPE                  = { 'dir'                   : 'directory',
                                    'pth'                   : 'path',
                                    'url'                   : 'link',
                                    'func'                  : 'function',
                                    'cmd'                   : 'commandPrompt',
                                    'event'                 : 'PLM Event',
                                    'stylesheet'            : 'PLMstylesheet',
                                    'shortcut'              : 'shortcut',
                                    'uiKey'                 : 'PLM Layout Key', }


from .version                   import Version
from .properties                import DamgProperty
from .propData                  import PropData

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved