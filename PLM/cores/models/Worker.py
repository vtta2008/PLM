# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, traceback

# PyQt5
from PyQt5.QtCore                           import pyqtSignal

# PLM
from PLM.api.damg                           import DAMG
from PLM.api.Core                           import Runnable



class Grabber(DAMG):

    key                                 = 'Grabber'

    # report when error occur
    error                               = pyqtSignal(tuple, name='Error')

    # send out result
    result                              = pyqtSignal(object, name='result')

    # realtime performance
    progress                            = pyqtSignal(int, name='progress')

    def __init__(self, parent=None):
        super(Grabber, self).__init__(parent)

        self.parent                     = parent
        self.key                        = '{0}:{1}'.format(self.key, self.parent.key)


class Worker(Runnable):

    """
    Worker thread

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    """

    key                                 = 'Worker'
    getOutPut                           = False

    INSTANCES                           = []
    FINISHED                            = []

    _uid                                = None

    def __init__(self, task, *args, **kwargs):
        super(Worker, self).__init__(task)

        self.task                       = task
        self.args                       = args
        self.kwargs                     = kwargs
        self.grabber                    = Grabber(self)

        self.setAutoDelete(True)
        self.cancelled                  = False

        # Add the callback to our kwargs
        # self.kwargs['progress_callback'] = self.grabber.progress

        Worker.INSTANCES.append(self)

        #release all of the finished tasks
        Worker.FINISHED                  = []

    def run(self):
        """

        Method automatically called by Qt when the runnable is ready to run.
        This will run in a separate thread.

        Initialise the runner function with passed args, kwargs.

        """

        # this allows us to "cancel" queued tasks if needed, should be done
        # on shutdown to prevent the app from hanging

        if self.cancelled:
            self.cleanup()
            return

        try:
            result = self.task(*self.args, **self.kwargs)

            if self.cancelled:
                # cleanup happens in 'finally' statement
                return
            self.grabber.result.emit(result)
        except:
            if self.cancelled:
                # cleanup happens in 'finally' statement
                return
            traceback.print_exc()
            exctype, value              = sys.exc_info()[:2]
            self.grabber.error.emit((exctype, value, traceback.format_exc()))
        else:
            self._output                = result
            self.grabber.result.emit(self.output())
        finally:
            # this will run even if one of the above return statements
            # is executed inside of the try/except statement see:
            # https://docs.python.org/2.7/tutorial/errors.html#defining-clean-up-actions

            print('task finished: {0}'.format(self.task.__name__))
            self.getOutPut = True
            self.cleanup(self.grabber)

    def output(self):
        return self._output

    def cleanup(self, grabber=None):
        """ remove references to any object or method for proper ref counting """

        self.task                       = None
        self.args                       = None
        self.kwargs                     = None
        self._output                    = None
        self.getOutPut                  = None
        self.setuid(None)

        if grabber:
            grabber.deleteLater()

        # make sure this python obj gets cleaned up
        self.remove()

    def remove(self):

        """
        when the next request is created, it will clean this one up
        this will help us avoid this object being cleaned up
        when it's still being used
        """

        try:
            Worker.INSTANCES.remove(self)
            Worker.FINISHED.append(self)
        except ValueError:
            # there might be a race condition on shutdown, when shutdown()
            # is called while the thread is still running and the instance
            # has already been removed from the list
            return

    def shutdown(self):
        for inst in Worker.INSTANCES:
            inst.cancelled = True
        Worker.INSTANCES = []
        Worker.FINISHED = []

    def setuid(self, val):
        self._uid                       = val

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, val):
        self._uid                       = val


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved