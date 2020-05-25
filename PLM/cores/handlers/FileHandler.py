# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from PLM.api.damg import DAMG


class FileHandler(DAMG):

    key                         = 'FileHandler'

    def __init__(self):
        super(FileHandler, self).__init__()

    def find(self, name, path):
        """ find/search """
        pass

    def save(self, path):
        """ save/write """
        pass

    def create(self, path):
        pass

    def load(self, path):
        """ read/load """
        pass

    def hide(self, path):
        """ hide file """
        pass

    def show(self, path):
        """ show file """
        pass

    def setPermission(self, path):
        pass

    def copy(self, source, destination):
        pass

    def remove(self, path):
        pass

    def profile(self, path):
        """ check profile of a file (size, date created etc.) """
        pass

    def zip(self, path):
        pass

    def unzip(self, path):
        pass

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved