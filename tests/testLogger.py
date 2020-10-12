# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from bin.loggers.models import ColoredFormatter, StreamHandler


formatter = ColoredFormatter(
	format="%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
	dtFormat=None,
	reset=True,
	logColors={
		'DEBUG':    'cyan',
		'INFO':     'green',
		'WARNING':  'yellow',
		'ERROR':    'red',
		'CRITICAL': 'red,bg_white',
	},
	secondLogColors={},
	style='%'
)

handler = StreamHandler()
handler.setFormatter(formatter)

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
