# -*- coding: utf-8 -*-
"""

Script Name: Handlers.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------

import os
from logging                    import FileHandler



class DamgHandler(FileHandler):

    key                        = 'DamgHandler'

    def __init__(self, filename='test.logger', mode='a+', encoding=None, delay=False):
        super(DamgHandler, self).__init__(filename, mode, encoding, delay)

        self.file             = filename
        self.mode             = mode
        self.encoding         = encoding
        self.delay            = delay

    def setFile(self, filePath):
        self.close()
        self.baseFilename     = os.path.abspath(os.fspath(filePath))
        if not self.mode:
            self.mode          = 'a+'
        super(DamgHandler, self)._open()



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:48 PM
# © 2017 - 2019 DAMGteam. All rights reserved