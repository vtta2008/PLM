#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: MayaPythonProc.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It basically checkes all the files in folder to makes ure everthing is there. Then copy some files to folders
    as required like userSetup.py or saving the path of DAMG tool folder to sys.path for next use.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os
import getpass
import json
import logging
import platform
import shutil
import sys

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds  # Maya_tk Python command

from appPackages.maya.plt_modules import MayaVariables as var

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
NAMES = var.MAINVAR
SCRPTH = os.path.join(os.getenv(__root__), 'appData', 'config')

# -------------------------------------------------------------------------------------------------------------
# MAKE MAYA UNDERSTAND QT UI AS MAYA WINDOW,  FIX PLM_VERSION CONVENTION
# -------------------------------------------------------------------------------------------------------------
# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------- #
""" Check file and folders """

class MayaPythonProc(object):
    # file list in Installation folder
    icons_lst = [f for f in os.listdir(os.path.join(os.getenv(__root__), 'imgs', 'maya.icon')) if
                 f.endswith('.png') or f.endswith('.jpg')]
    modules_lst = [f for f in os.listdir(os.path.join(os.getenv(__root__), 'packages', 'maya', 'plt_modules')) if f.endswith('.py')]
    scrRoot_lst = [f for f in os.listdir(os.path.join(os.getenv(__root__), 'packages', 'maya')) if f.endswith('.py')]

    # ---------------------------------------------------------
    # List file names for CHECK LIST
    checkList = dict(icons=NAMES['mayaIcon'], modules=NAMES['mayaModule'], master=NAMES['mayaRoot'])
    fileList = dict(icons=icons_lst, modules=modules_lst, master=scrRoot_lst)
    # ---------------------------------------------------------
    # Make variables just in case you miss something.
    message_missing = []

    def __init__(self):
        super(MayaPythonProc, self).__init__()

        # self.checkAllFiles()

        self.setupFolderAndPath()

    def checkAllFiles(self):
        for part in self.checkList:
            # logger.info('start inspecting %s folder' % part)
            for file in self.checkList[part]:
                if file in self.fileList[part]:
                    # logger.info("%s exists, keep seeking..." % file)
                    pass
                else:
                    logger.info("could not find: %s in: %s" % (file, (os.path.join(NAMES['mayaRootDir'], part))))
                    self.message_missing.append("%s in %s" % (file, (os.path.join(NAMES['mayaRootDir'], part))))

        if self.message_missing == []:
            # logger.info("Finish checking, all files are there")
            pass
        else:
            self.showMissing()

    def setupFolderAndPath(self, **info):
        infoUser = {}
        userPath = os.path.join(SCRPTH, NAMES['maya'][0])
        infoUser['source folder'] = NAMES['mayaRootDir']
        infoUser['user name'] = getpass.getuser()
        infoUser['artist name'] = platform.node()
        infoUser['operating system'] = platform.system() + "/" + platform.platform()
        infoUser['python version'] = platform.python_version()

        with open(userPath, 'w') as f:
            json.dump(infoUser, f, indent=4)

        # logger.info('Saving file to %s' % userPath)

        # infoPath = {}
        # toolPath = os.path.join( SCRPTH, '%s' % NAMES[ 'maya' ][1] )
        # for part in ['plt.maya.icon', 'plt_modules', 'packages']:
        #     infoPath[part] = os.path.join(NAMES['mayaRootDir'], part)
        #
        # with open(toolPath, 'w') as f:
        #     json.dump(infoPath, f, indent=4)
        #
        # print 'Fuck toolpath: %s' % toolPath
        #
        # logger.info('Saving file to %s' % toolPath)

        # self.applyToolPathIntoSystem()

    def applyToolPathIntoSystem(self, *args):
        srcInfo = os.path.join(SCRPTH, NAMES['maya'][1])
        if os.path.exists(srcInfo):
            with open(srcInfo, 'r') as f:
                paths = json.load(f)
            for path in paths:
                if os.path.exists(paths[path]):
                    if not paths[path] in sys.path:
                        sys.path.append(paths[path])
                    else:
                        pass
                else:
                    continue
        else:
            message = ('Could not find %s in %s,\n' % (NAMES['maya'][1], srcInfo))
            self.warningMessage(message=message)

    def updateLayout(self):
        folName = ['workspaces', 'shelves', ]
        for i in range(0, 2):
            scr = os.path.join(NAMES['mayaRootDir'], 'layout', NAMES['mayaLayout'][i])
            if not os.path.exists(scr):
                message = "missing %s, it should be in: %s, ignore." % (NAMES['mayaLayout'][i], scr)
                logger.info(message)
                cmds.warning(message)
            else:
                des = os.path.join(NAMES['mayaRootDir'], folName[i], NAMES['mayaLayout'][i])
                if os.path.exists(des):
                    logger.info('Already updated %s layout, ignore.' % folName[i])
                else:
                    logger.info('updating %s...' % folName[i])
                    shutil.copy2(scr, des)
                i += 1

    def showMissing(self, *args):
        message = " "
        for m in self.message_missing:
            message = 'missing file: ' + message + m + ";"
        self.warningMessage(message=message)
        logger.info(message)
        sys.exit()

    def warningMessage(self, message="None"):
        cmds.confirmDialog(
            t='Warning',
            m=(message + "\n"
                         "please re-install the tool, or contact Jimmy for help" + "\n"
               ),
            b='OK'
        )
        logger.info(message)
        cmds.warning(message)


if __name__ == 'main':
    MayaPythonProc()

    # -------------------------------------------------------------------------------------------------------------
    # END OF CODE
    # -------------------------------------------------------------------------------------------------------------
