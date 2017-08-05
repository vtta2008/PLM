# coding=utf-8
"""
Script Name: shortcut.py
Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script has function to create shortcut or get link from shortcut or modify shortcut
"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import os
import sys
import glob
import winshell

# ----------------------------------------------------------------------------------------------------------- #
"""                   MAIN CLASS: SHORTCUT - CREATE OR READ A SHORTCUT                          """
# ----------------------------------------------------------------------------------------------------------- #

class ShorCut(object):
    """
    It will create a shortcut or get the link of exe file base on given shortcut file
    """
    def __init__(self, operation, tmpPth, desktopPth, filename):
        """
        Take input variables to operate functions
        :param tmpPth: the temporary path by default
        :param desktopPth:  the user desktop path
        :param filename: the shortcut file name
        """
        print 'initializing ShotCut class'

        if operation=='create':
            self.createShortCut(tmpPth, desktopPth, filename)
        elif operation=='read':
            self.getPthFromShortCut(filename)
        elif operation=='modify':
            self.modifyShortCut()
        else:
            pass

    def createShortCut(self, tempPth, desktopPth, filename):
        """
        Create new shortcut
        :param tempPth: working directory, default as temporary folder
        :param desktopPth: user desktop directory
        :param filename: name of shortcut file
        :return: new shortcut file in desktop
        """
        shortcut = winshell.shortcut(sys.executable)
        shortcut.working_directory = tempPth
        shortcut.write(os.path.join(desktopPth, filename))
        shortcut.dump()

    def getPthFromShortCut(self, filename):
        """
        Get the link from shortcut file
        :param filename: shortcut file name
        :return: path
        """
        for lnk in glob.glob(os.path.join(winshell.programs(), filename)):
            shortcut = winshell.shortcut(lnk)
            shortcut.dump()
            break
        else:
            print 'None Found'

    def modifyShortCut(self):
        """
        this function will be built later
        :return:
        """
        pass