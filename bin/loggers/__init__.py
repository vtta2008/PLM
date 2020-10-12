# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import logging, sys
from bin.loggers.formatter 		import DamgFormatter, StreamHandler
from bin.loggers.handler 		import DamgHandler
from bin.options 				import logColorOpts, LogLevel


class DamgLogger(logging.RootLogger):

	key 					= 'DamgLogger'

	logLevel = {LogLevel.Silent: logging.NOTSET,
				LogLevel.Debug: logging.DEBUG,
				LogLevel.Normal: logging.INFO,
				LogLevel.Trace: logging.WARNING,
				LogLevel.Error: logging.ERROR,
				LogLevel.Critical: logging.CRITICAL, }


	def __init__(self, name=None, level='DEBUG', filepth=None):

		if not name:
			self.name 		= __name__
		else:
			self.name 		= name

		super(DamgLogger, self).__init__(level)

		# ::TODO:: Adding TRACE level is not working
		vbTrace 			= self.lvlValue('TRACE')
		TRACE 				= self.config_logLevel(vbTrace)
		self.addLoggingLevel(levelNum=TRACE, levelName='TRACE')

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
			self.critical('Type: {0}, \nValue: {1}'.format(exc_type, exc_value))
			return sys.__excepthook__(exc_type, exc_value, exc_tb)

		self.error('Uncaught exception: \nType: {0}, \nValue: {1}'.format(exc_type, exc_value),)

		exception = traceback.format_exception(exc_type, exc_value, exc_tb)

		if exc_tb:
			pdb.post_mortem(exc_tb)

		return exception

	def addLoggingLevel(self, levelName, levelNum, methodName=None):

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

	def lvlName(self, lvl):

		name_levels = {
			logging.FATAL: 'FATAL',
			logging.CRITICAL: 'CRITICAL',
			logging.ERROR: 'ERROR',
			logging.WARNING: 'WARNING',
			logging.INFO: 'INFO',
			logging.DEBUG: 'DEBUG',
			logging.NOTSET: 'NOTSET',
		}

		return name_levels[lvl]

	def lvlValue(self, lvl):

		if lvl in ['FATAL', 'Fatal']:
			verbose_level = logging.FATAL
		elif lvl in ['DEBUG', 'Debug']:
			verbose_level = logging.DEBUG
		elif lvl in ['INFO', 'Info']:
			verbose_level = logging.INFO
		elif lvl in ['WARN', 'WARNING', 'Warn', 'Warning']:
			verbose_level = logging.WARNING
		elif lvl in ['ERROR', 'Error']:
			verbose_level = logging.ERROR
		elif lvl in ['CRITICAL', 'Critical']:
			verbose_level = logging.CRITICAL
		else:
			verbose_level = logging.NOTSET

		return verbose_level

	def config_logLevel(self, level):
		verboseLvl = self.lvlValue(level)
		loggingLvl = LogLevel.getbyverbosity(verboseLvl)
		return self.logLevel[loggingLvl]



if __name__ == '__main__':

	lvls = ['DEBUG', 'INFO', 'TRACE', 'WARNING', 'ERROR', 'CRITICAL']

	testLogger = DamgLogger(__file__, 'DEBUG', 'testlogger.log')

	testLogger.Trace('test trace')
	#
	# for level in lvls:
	# 	testLogger.log(testLogger.lvlValue(level), 'This is a test log of {0}'.format(level))


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:44 PM
# © 2017 - 2019 DAMGteam. All rights reserved