# coding=utf-8
"""
Script Name: getApps.py
Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script contains some basic functions that would be able to use many times
"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import os, sys, subprocess, logging, json, datetime
from tk import defaultVariable as var
from tk import encode

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
PLUGIN = var.MAIN_PLUGIN
PACKAGE = var.MAIN_PACKPAGE
NAMES = var.MAIN_NAMES
USER = var.USERNAME

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------- #
"""                MAIN CLASS: GET MODULE INFO - GET ALL INFO OF MODULES, ICONS, IMAGES                     """
# ----------------------------------------------------------------------------------------------------------- #
class Proc():
    """
    This is some function that will use many time
    """
    dt = datetime.datetime

    def __init__(self):
        # logger.info('Start procedural')
        pass

    def getDate(self):
        t = datetime.datetime.timetuple( datetime.datetime.now() )
        dateOutput = '%s/%s/%s' % (str(t.tm_mday), str(t.tm_mon), str(t.tm_year))
        return dateOutput

    def getTime(self):
        t = datetime.datetime.timetuple(datetime.datetime.now() )
        timeOutput = '%s:%s' % (str(t.tm_hour), str(t.tm_min))
        return timeOutput

    def executing(self, name, path):
        """
        Executing a python file
        :param name: python file name
        :param path: path to python file
        :return: executing in command prompt
        """
        # logger.info( 'Executing %s from %s' % (name, path) )
        pth = os.path.join(path, name)
        if os.path.exists(pth):
            subprocess.call([sys.executable, pth])

    def pip(self, name):
        """
        Install python component via command prompt
        :param name: name of component
        :return:
        """
        # logger.info( 'Using pip install %s' % name )
        os.system('pip install %s' % name)

    def checkPlugin(self, name):
        """
        check python component, if false, it will install component
        :param name:
        :return:
        """
        # logger.info( 'Trying to import %s' % name )
        try:
            import name
        except ImportError:
            logger.info('ImportError')
            self.pip(PLUGIN[name])

    def createLog(self, event='Create Log', names=NAMES, package=PACKAGE):
        log = {}
        log[proc('date')] = event
        with open( os.path.join(package['appData'], names['log']), 'a+') as f:
            json.dump(log, f, indent=4)

def endconding(message):
    output = encode.encode(message, mode='hex')
    return output

def decoding(message):
    output = encode.encode(message, mode='str')
    return output

def logRecord(event):
    # logger.info('Log created')
    output = Proc().createLog(event=event)
    return output

def proc(operation=None, name=NAMES['log'], path=PACKAGE['info']):
    t = Proc().getTime()
    d = Proc().getDate()
    u = USER

    if operation == 'exe':
        output = Proc().executing( name, path )
    elif operation == 'pip':
        output = Proc().pip(name)
    elif operation == 'plug':
        output = Proc().checkPlugin( name )
    elif operation == 'date':
        output = Proc().getDate()
    elif operation == 'time':
        output = Proc().getTime()
    elif operation == 'log out':
        output = logRecord('User %s logged out at %s' % (u,t))
    elif operation == 'log in':
        output = logRecord('User %s logged in at %s' % (u,t))
    elif operation == 'update':
        output = logRecord('Update data at %s' % t)
    elif operation == 'restart':
        output = logRecord('User %s restart app at %s' % (u, t) )
    else:
        output=None

    return output

# ----------------------------------------------------------------------------------------------------------- #
"""                                                END OF CODE                                              """
# ----------------------------------------------------------------------------------------------------------- #