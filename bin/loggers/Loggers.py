# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import logging, sys
from bin.loggers.formatter 		import DamgFormatter, StreamHandler
from bin.loggers.handler 		import DamgHandler
from bin.options 				import logColorOpts, LogLevel


class DamgLogger(logging.Logger):

	key 					= 'DamgLogger'

	logLevel = {LogLevel.Silent: logging.NOTSET,
				LogLevel.Debug: logging.DEBUG,
				LogLevel.Normal: logging.INFO,
				LogLevel.Trace: logging.WARNING,
				LogLevel.Error: logging.ERROR,
				LogLevel.Critical: logging.CRITICAL, }


	def __init__(self, name=None, level='DEBUG', filepth=None):

		if not name:
			self.name 		= __file__
		else:
			self.name 		= name

		super(DamgLogger, self).__init__(level)

		vbTrace 			= self.lvlValue('TRACE')
		TRACE 				= self.config_logLevel(vbTrace)
		self.addLogLvl(levelNum=TRACE, levelName='TRACE')

		self.parent 		= logging.getLogger(self.name)
		self.level 			= level
		self.file			= filepth
		self.fileHandler	= DamgHandler(self.file, 'a+', None, False)
		self.streamHandler	= StreamHandler(sys.stdout)
		self.formatter 		= DamgFormatter(logColorOpts['fmt'], logColorOpts['datefmt'], logColorOpts['style'][0],
											logColorOpts['logColors'], logColorOpts['reset'][0],
											logColorOpts['secondLogColors'])
		self.fileHandler.setFormatter(self.formatter)
		self.streamHandler.setFormatter(self.formatter)

		self.addHandler(self.streamHandler)
		self.addHandler(self.fileHandler)
		self.setLevel(self.level)

		sys.excepthook = self.exception_handler

	def exception_handler(self, exc_type, exc_value, exc_tb):
		import pdb, traceback

		if hasattr(sys, 'ps1') or not sys.stderr.isatty():
			return sys.__excepthook__(exc_type, exc_value, exc_tb)

		self.error('Uncaught exception: \nType: {0}, \nValue: {1}'.format(exc_type, exc_value),)

		exception = traceback.format_exception(exc_type, exc_value, exc_tb)

		if exc_tb:
			pdb.post_mortem(exc_tb)

		return exception

	def addLogLvl(self, levelName, levelNum, methodName=None):

		if not methodName or methodName is None:
			methodName = levelName.lower()

		if hasattr(logging, levelName):
			# print('{0} registered (level)'.fmt(levelName))
			regisable = False
		elif hasattr(logging, methodName):
			# print('{0} registered (method)'.fmt(methodName))
			regisable = False
		elif hasattr(logging.getLoggerClass(), methodName):
			# print('{0} registered (class)'.fmt(methodName))
			regisable = False
		else:
			regisable = True

		def logForLevel(self, message, *args, **kwargs):
			if self.isEnabledFor(levelNum):
				self._log(levelNum, message, args, **kwargs)

		def logToRoot(message, *args, **kwargs):
			logging.log(levelNum, message, *args, **kwargs)

		if regisable:
			# print('begin adding level name: {0}'.fmt(levelName))
			logging.addLevelName(levelNum, levelName)
			setattr(logging, levelName, levelNum)
			setattr(logging.getLoggerClass(), methodName, logForLevel)
			setattr(logging, methodName, logToRoot)
			self.info(methodName, levelName, levelNum)

	def lvlName(self, lvl):

		return  {
			logging.FATAL: 'FATAL',
			logging.CRITICAL: 'CRITICAL',
			logging.ERROR: 'ERROR',
			logging.WARNING: 'WARNING',
			logging.INFO: 'INFO',
			logging.DEBUG: 'DEBUG',
			logging.NOTSET: 'NOTSET',
		}[lvl]

	def lvlValue(self, lvl):

		if lvl in ['FATAL', 'Fatal']:
			return logging.FATAL
		elif lvl in ['DEBUG', 'Debug']:
			return logging.DEBUG
		elif lvl in ['INFO', 'Info']:
			return logging.INFO
		elif lvl in ['Trace', 'TRACE']:
			return LogLevel.Trace
		elif lvl in ['WARN', 'WARNING', 'Warn', 'Warning']:
			return logging.WARNING
		elif lvl in ['ERROR', 'Error']:
			return logging.ERROR
		elif lvl in ['CRITICAL', 'Critical']:
			return logging.CRITICAL
		else:
			return logging.NOTSET

	def config_logLevel(self, level):
		loggingLvl = LogLevel.getbyverbosity(level)
		return self.logLevel[loggingLvl]


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
