# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------

import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt



def asyncs(method, args, uid, readycb, errorcb=None):

    """
    Asynchronously runs a task

    :param func method: the method to run in a thread
    :param object uid: a unique identifier for this task (used for verification)
    :param slot updatecb: the callback when data is receieved cb(uid, data)
    :param slot errorcb: the callback when there is an error cb(uid, errmsg)

    The uid option is useful when the calling code makes multiple async calls
    and the callbacks need some context about what was sent to the async method.
    For example, if you use this method to thread a long running database call
    and the user decides they want to cancel it and start a different one, the
    first one may complete before you have a chance to cancel the task.  In that
    case, the "readycb" will be called with the cancelled task's data.  The uid
    can be used to differentiate those two calls (ie. using the sql query).

    :returns: Request instance
    """
    request = Request(method, args, uid, readycb, errorcb)
    QtCore.QThreadPool.globalInstance().start(request)
    return request


class Request(QtCore.QRunnable):
    """
    A Qt object that represents an asynchronous task

    :param func method: the method to call
    :param list args: list of arguments to pass to method
    :param object uid: a unique identifier (used for verification)
    :param slot readycb: the callback used when data is receieved
    :param slot errorcb: the callback used when there is an error

    The uid param is sent to your error and update callbacks as the
    first argument. It's there to verify the data you're returning

    After created it should be used by invoking:

    .. code-block:: python

       task = Request(...)
       QtCore.QThreadPool.globalInstance().start(task)

    """
    INSTANCES = []
    FINISHED = []
    def __init__(self, method, args, uid, readycb, errorcb=None):
        super(Request, self).__init__()
        self.setAutoDelete(True)
        self.cancelled = False

        self.method = method
        self.args = args
        self.uid = uid
        self.dataReady = readycb
        self.dataError = errorcb

        Request.INSTANCES.append(self)

        # release all of the finished tasks
        Request.FINISHED = []

    def run(self):
        """
        Method automatically called by Qt when the runnable is ready to run.
        This will run in a separate thread.
        """
        # this allows us to "cancel" queued tasks if needed, should be done
        # on shutdown to prevent the app from hanging
        if self.cancelled:
            self.cleanup()
            return

        # runs in a separate thread, for proper async signal/slot behavior
        # the object that emits the signals must be created in this thread.
        # Its not possible to run grabber.moveToThread(QThread.currentThread())
        # so to get this QObject to properly exhibit asynchronous
        # signal and slot behavior it needs to live in the thread that
        # we're running in, creating the object from within this thread
        # is an easy way to do that.
        grabber = Requester()
        grabber.Loaded.connect(self.dataReady, Qt.QueuedConnection)
        if self.dataError is not None:
            grabber.Error.connect(self.dataError, Qt.QueuedConnection)

        try:
            result = self.method(*self.args)
            if self.cancelled:
                # cleanup happens in 'finally' statement
                return
            grabber.Loaded.emit(self.uid, result)
        except Exception as error:
            if self.cancelled:
                # cleanup happens in 'finally' statement
                return
            grabber.Error.emit(self.uid, tuple)
        finally:
            # this will run even if one of the above return statements
            # is executed inside of the try/except statement see:
            # https://docs.python.org/2.7/tutorial/errors.html#defining-clean-up-actions
            self.cleanup(grabber)

    def cleanup(self, grabber=None):
        # remove references to any object or method for proper ref counting
        self.method = None
        self.args = None
        self.uid = None
        self.dataReady = None
        self.dataError = None

        if grabber is not None:
            grabber.deleteLater()

        # make sure this python obj gets cleaned up
        self.remove()

    def remove(self):
        try:
            Request.INSTANCES.remove(self)

            # when the next request is created, it will clean this one up
            # this will help us avoid this object being cleaned up
            # when it's still being used
            Request.FINISHED.append(self)
        except ValueError:
            # there might be a race condition on shutdown, when shutdown()
            # is called while the thread is still running and the instance
            # has already been removed from the list
            return

    @staticmethod
    def shutdown():
        for inst in Request.INSTANCES:
            inst.cancelled = True
        Request.INSTANCES = []
        Request.FINISHED = []


class Requester(QtCore.QObject):
    """
    A simple object designed to be used in a separate thread to allow
    for asynchronous data fetching
    """

    #
    # Signals
    #

    Error = QtCore.pyqtSignal(object, str)
    """
    Emitted if the fetch fails for any reason

    :param unicode uid: an id to identify this request
    :param unicode error: the error message
    """

    Loaded = QtCore.pyqtSignal(object, object)
    """
    Emitted whenever data comes back successfully

    :param unicode uid: an id to identify this request
    :param list data: the json list returned from the GET
    """

    NetworkConnectionError = QtCore.pyqtSignal(str)
    """
    Emitted when the task fails due to a network connection error

    :param unicode message: network connection error message
    """

    def __init__(self, parent=None):
        super(Requester, self).__init__(parent)


class ExampleObject(QtCore.QObject):
    def __init__(self, parent=None):
        super(ExampleObject, self).__init__(parent)
        self.uid = 0
        self.request = None

    def ready_callback(self, uid, result):
        if uid != self.uid:
            return
        print("Data ready from %s: %s" % (uid, result))

    def error_callback(self, uid, error):
        if uid != self.uid:
            return
        print("Data error from %s: %s" % (uid, error))

    def fetch(self):
        if self.request is not None:
            # cancel any pending requests
            self.request.cancelled = True
            self.request = None

        self.uid += 1
        self.request = asyncs(slow_method, ["arg1", "arg2"], self.uid,
                             self.ready_callback,
                             self.error_callback)


def slow_method(arg1, arg2):
    print("Starting slow method")
    time.sleep(1)
    return arg1 + arg2


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    obj = ExampleObject()

    dialog = QtWidgets.QDialog()
    layout = QtWidgets.QVBoxLayout(dialog)
    button = QtWidgets.QPushButton("Generate", dialog)
    progress = QtWidgets.QProgressBar(dialog)
    progress.setRange(0, 0)
    layout.addWidget(button)
    layout.addWidget(progress)
    button.clicked.connect(obj.fetch)
    dialog.show()

    app.exec_()
    app.deleteLater()

    # avoids some QThread messages in the shell on exit
    # cancel all running tasks avoid QThread/QTimer error messages
    # on exit

    Request.shutdown()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:17 AM
# © 2017 - 2019 DAMGteam. All rights reserved