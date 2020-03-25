# -*- coding: utf-8 -*-
"""

Script Name: Workers.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
import traceback

# PLM
from PLM.cores.base                         import TaskWorker


# -------------------------------------------------------------------------------------------------------------
""" Workers """


class ConfigTaskWorker(TaskWorker):

    key                                             = 'ConfigTaskWorker'

    def __init__(self, task, parent):
        super(ConfigTaskWorker, self).__init__(task, parent)


    def run(self):
        if self.running:
            try:
                result = self.task()
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signal.error.emit((exctype, value, traceback.format_exc()))
            else:
                self.signal.result.emit(result)
            finally:
                self.signal.finished.emit()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/25/2020 - 11:35 PM
# © 2017 - 2019 DAMGteam. All rights reserved