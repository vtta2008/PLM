# -*- coding: utf-8 -*-
"""

Script Name: Storages.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM.cores.base.BaseStorage             import BaseStorage
from PLM.commons                            import DAMGLIST
from PLM.commons.Core                       import Thread, Worker
from PLM.cores.Errors                       import (ThreadNotFoundError, WorkerNotFoundError, CreateThreadError,
                                                    CreateWorkerError)

# -------------------------------------------------------------------------------------------------------------
""" Storages """



class ThreadStorage(BaseStorage):

    key                                     = 'ThreadStorage'
    threads                                 = DAMGLIST()

    def __init__(self):
        BaseStorage.__init__(self)
        self.update()

    def getThread(self, key):
        if key in self.keys():
            return self[key]
        else:
            return ThreadNotFoundError('Could not find thread: {0}'.format(key))

    def createThread(self, key):
        if key not in self.keys():
            thread                              = Thread
            thread.key                          = key
            self.threads.append(thread)
            self.register(thread)
            return thread
        else:
            CreateThreadError('Could not create thread: {0}, key already existed'.format(key))



class WorkerStorage(BaseStorage):

    key                                     = 'WorkerStorage'
    workers                                 = DAMGLIST()

    def __init__(self):
        super(WorkerStorage, self).__init__()
        self.update()

    def getWorker(self, key):
        if key in self.keys():
            return self[key]
        else:
            return WorkerNotFoundError('Could not find worker: {0}'.format(key))

    def createWorker(self, key):
        if key not in self.keys():
            worker                              = Worker
            worker.key                          = key
            self.workers.append(worker)
            self.register(worker)
            return worker
        else:
            CreateWorkerError('Could not create worker: {0}, key already existed'.format(key))



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/21/2020 - 3:08 AM
# © 2017 - 2019 DAMGteam. All rights reserved