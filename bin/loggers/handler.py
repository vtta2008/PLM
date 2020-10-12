# -*- coding: utf-8 -*-
"""

Script Name: Handlers.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from bin.loggers.formatter      import FileHandler



class DamgHandler(FileHandler):

    key                        = 'DamgHandler'

    def __init__(self, filename='test.log', mode='a+', encoding=None, delay=False):
        super(DamgHandler, self).__init__(filename, mode, encoding, delay)

        self.file             = filename
        self.mode             = mode
        self.encoding         = encoding
        self.delay            = delay





# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:48 PM
# © 2017 - 2019 DAMGteam. All rights reserved