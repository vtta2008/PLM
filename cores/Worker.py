# -*- coding: utf-8 -*-
"""

Script Name: Worker.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import time, traceback, sys

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QThread, QThreadPool

from cores.base import DAMG
from appData import __copyright__

# PLM

# -------------------------------------------------------------------------------------------------------------
""" Signals """

class WorkerSignals(DAMG):

    finished            = pyqtSignal()
    error               = pyqtSignal(tuple)
    result              = pyqtSignal(object)
    progress            = pyqtSignal(int)

    quit_thread         = pyqtSignal(name='close_thread')

# -------------------------------------------------------------------------------------------------------------
""" Worker & Thread """

class WorkerBase(QRunnable):

    Type                    = 'DAMGWORKER'
    _id                     = 'DAMG worker'

    def __init__(self, task, *args, **kwargs):
        QRunnable.__init__(self)

        self._copyright     = __copyright__

        self.task           = task                             # Store constructor arguments (re-used for processing)
        self.args           = args
        self.kwargs         = kwargs
        self.signals        = WorkerSignals()

    @pyqtSlot()
    def run(self):

        try:
            self.task(*self.args, **self.kwargs, status = self.signals.status, progress=self.signals.progress)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit()                                          # Return the result of the processing
        finally:
            self.signals.finished.emit()                                        # Done

    @property
    def copyright(self):
        return self._copyright

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, newId):
        self._name = newId

class ThreadBase(QThread):

    Type                    = 'DAMGTHREAD'
    _id                     = 'DAMG thread'

    def __init__(self, task):
        super(ThreadBase, self).__init__()

        self.task = task

    def run(self):

        if 'user' in self.task:
            self.query_user_data()
        elif 'host' in self.task:
            self.query_hosts_data()
        elif 'service' in self.task:
            self.query_services_data()
        elif 'alignakdaemon' in self.task:
            self.query_daemons_data()
        elif 'livesynthesis' in self.task:
            self.query_livesynthesis_data()
        elif 'history' in self.task:
            self.query_history_data()
        elif 'notifications' in self.task:
            self.query_notifications_data()
        else:
            pass

    @property
    def copyright(self):
        return self._copyright

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, newId):
        self._name = newId

class ThreadPoolBase(QThreadPool):

    Type = 'DAMGTHREADPOOL'
    _id = 'DAMG thread pool'

    def __init__(self):
        super(ThreadPoolBase, self).__init__()
        self._copyright = __copyright__

    @property
    def copyright(self):
        return self._copyright

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, newId):
        self._name = newId

class DAMGWORKER(WorkerBase):

    def __init__(self, task, *args, **kwargs):
        super(DAMGWORKER, self).__init__(self)

        self.task           = task
        self.args           = args
        self.kwargs         = kwargs

class DAMGTHREAD(ThreadBase):

    def __init__(self, task):
        super(DAMGTHREAD, self).__init__(self)

        self.task = task

class DAMGWT(WorkerBase, ThreadBase):

    def __init__(self, task, *args, **kwargs):
        super(DAMGWT, self).__init__()

        self.task           = task
        self.args           = args
        self.kwargs         = kwargs


    def run(self):

        try:
            self.task(*self.args, **self.kwargs, status=self.signals.status, progress=self.signals.progress)
        except:
            if 'user' in self.task:
                self.query_user_data()
            elif 'host' in self.task:
                self.query_hosts_data()
            elif 'service' in self.task:
                self.query_services_data()
            elif 'alignakdaemon' in self.task:
                self.query_daemons_data()
            elif 'livesynthesis' in self.task:
                self.query_livesynthesis_data()
            elif 'history' in self.task:
                self.query_history_data()
            elif 'notifications' in self.task:
                self.query_notifications_data()
            else:
                pass
        else:
            self.signals.result.emit()
        finally:
            self.signals.finished.emit()

    @staticmethod
    def query_user_data():
        """Launch request for "user" endpoint"""
        print('Query user data')

    @staticmethod
    def query_hosts_data():
        """Launch request for "host" endpoint"""
        print('Query hosts')

    @staticmethod
    def query_services_data():
        """Launch request for "service" endpoint"""
        print("Query services")

    @staticmethod
    def query_daemons_data():
        """Launch request for "alignakdaemon" endpoint"""
        print('Query daemons')

    @staticmethod
    def query_livesynthesis_data():
        """ Launch request for "livesynthesis" endpoint """
        print('query livesynthesis')

    @staticmethod
    def query_history_data():
        """ Launch request for "history" endpoint but only for hosts in "data_manager" """
        print('Query history')

    @staticmethod
    def query_notifications_data():
        """Launch request for "history" endpoint but only for notifications of current user"""
        print('Query notifications')


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 14/06/2018 - 9:58 PM
# © 2017 - 2018 DAMGteam. All rights reserved