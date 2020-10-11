# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    In this directory resides our test suite. I'm not gonna go into too much detail here as we will dedicate whole
    section to testing, but just briefly:

    1. test_app.py is a test file corresponding to app.py in source directory
    2. conftest.py is probably familiar to you if you ever used Pytest - it's a file used for specifying Pytest
        fixtures, hooks or loading external plugins.
    3. context.py helps with imports of source code files from blueprint directory by manipulating class path.
        We will see how that works in sec.

"""
# -------------------------------------------------------------------------------------------------------------
# from PySide2 import QtGui
# from PySide2.QtCore import QThread, SIGNAL
# import sys
# import design
# import urllib2
# import json
# import time
#
#
# class getPostsThread(QThread):
#     def __init__(self, subreddits):
#
#         QThread.__init__(self)
#         self.subreddits = subreddits
#
#     def __del__(self):
#         self.wait()
#
#     def _get_top_post(self, subreddit):
#
#         url = "https://www.reddit.com/r/{}.json?limit=1".format(subreddit)
#         headers = {'User-Agent': 'nikolak@outlook.com tutorial code'}
#         request = urllib2.Request(url, headers=headers)
#         response = urllib2.urlopen(request)
#         data = json.load(response)
#         top_post = data['data']['children'][0]['data']
#         return "'{title}' by {author} in {subreddit}".format(**top_post)
#
#     def run(self):
#
#         for subreddit in self.subreddits:
#             top_post = self._get_top_post(subreddit)
#             self.emit(SIGNAL('add_post(QString)'), top_post)
#             self.sleep(2)
#
#
# class ThreadingTutorial(QtGui.QMainWindow, design.Ui_MainWindow):
#     """
#     How the basic structure of PyQt GUI code looks and behaves like is
#     explained in this tutorial
#     http://nikolak.com/pyqt-qt-designer-getting-started/
#     """
#
#     def __init__(self):
#         super(self.__class__, self).__init__()
#         self.setupUi(self)
#         self.btn_start.clicked.connect(self.start_getting_top_posts)
#
#     def start_getting_top_posts(self):
#         # Get the subreddits user entered into an QLineEdit field
#         # this will be equal to '' if there is no text entered
#         subreddit_list = str(self.edit_subreddits.text()).split(',')
#         if subreddit_list == ['']:  # since ''.split(',') == [''] we use that to check
#             # whether there is anything there to fetch from
#             # and if not show a message and abort
#             QtGui.QMessageBox.critical(self, "No subreddits",
#                                        "You didn't enter any subreddits.",
#                                        QtGui.QMessageBox.Ok)
#             return
#         # Set the maximum value of progress bar, can be any int and it will
#         # be automatically converted to x/100% values
#         # e.g. max_value = 3, current_value = 1, the progress bar will show 33%
#         self.progress_bar.setMaximum(len(subreddit_list))
#         # Setting the value on every run to 0
#         self.progress_bar.setValue(0)
#
#         # We have a list of subreddits which we use to create a new getPostsThread
#         # instance and we pass that list to the thread
#         self.get_thread = getPostsThread(subreddit_list)
#
#         # Next we need to connect the events from that thread to functions we want
#         # to be run when those signals get fired
#
#         # Adding post will be handeled in the add_post method and the signal that
#         # the thread will emit is  SIGNAL("add_post(QString)")
#         # the rest is same as we can use to connect any signal
#         self.connect(self.get_thread, SIGNAL("add_post(QString)"), self.add_post)
#
#         # This is pretty self explanatory
#         # regardless of whether the thread finishes or the user terminates it
#         # we want to show the notification to the user that adding is done
#         # and regardless of whether it was terminated or finished by itself
#         # the finished signal will go off. So we don't need to catch the
#         # terminated one specifically, but we could if we wanted.
#         self.connect(self.get_thread, SIGNAL("finished()"), self.done)
#
#         # We have all the events we need connected we can start the thread
#         self.get_thread.start()
#         # At this point we want to allow user to stop/terminate the thread
#         # so we enable that button
#         self.btn_stop.setEnabled(True)
#         # And we connect the click of that button to the built in
#         # terminate method that all QThread instances have
#         self.btn_stop.clicked.connect(self.get_thread.terminate)
#         # We don't want to enable user to start another thread while this one is
#         # running so we disable the start button.
#         self.btn_start.setEnabled(False)
#
#     def add_post(self, post_text):
#         """
#         Add the text that's given to this function to the
#         list_submissions QListWidget we have in our GUI and
#         increase the current value of progress bar by 1
#
#         :param post_text: text of the item to add to the list
#         :type post_text: str
#         """
#         self.list_submissions.addItem(post_text)
#         self.progress_bar.setValue(self.progress_bar.value() + 1)
#
#     def done(self):
#         """
#         Show the message that fetching posts is done.
#         Disable Stop button, enable the Start one and reset progress bar to 0
#         """
#         self.btn_stop.setEnabled(False)
#         self.btn_start.setEnabled(True)
#         self.progress_bar.setValue(0)
#         QtGui.QMessageBox.information(self, "Done!", "Done fetching posts!")
#
#
# def main():
#     app = QtGui.QApplication(sys.argv)
#     form = ThreadingTutorial()
#     form.show()
#     app.exec_()
#
#
# if __name__ == '__main__':
#     main()
#


import datetime
import logging
import random
import sys
import time

# Deal with minor differences between PySide2 and PyQt5
try:
    from PySide2 import QtCore, QtGui, QtWidgets
    Signal = QtCore.Signal
    Slot = QtCore.Slot
except ImportError:
    from PyQt5 import QtCore, QtGui, QtWidgets
    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot



logger = logging.getLogger(__name__)

class Signaller(QtCore.QObject):
    signal = Signal(str, logging.LogRecord)



class QtHandler(logging.Handler):
    def __init__(self, slotfunc, *args, **kwargs):
        super(QtHandler, self).__init__(*args, **kwargs)
        self.signaller = Signaller()
        self.signaller.signal.connect(slotfunc)

    def emit(self, record):
        s = self.format(record)
        self.signaller.signal.emit(s, record)


def ctname():
    return QtCore.QThread.currentThread().objectName()



LEVELS = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)


class Worker(QtCore.QObject):

    @Slot()

    def start(self):
        extra = {'qThreadName': ctname() }
        logger.debug('Started work', extra=extra)
        i = 1

        while not QtCore.QThread.currentThread().isInterruptionRequested():
            delay = 0.5 + random.random() * 2
            time.sleep(delay)
            level = random.choice(LEVELS)
            logger.log(level, 'Message after delay of %3.1f: %d', delay, i, extra=extra)
            i += 1

class Window(QtWidgets.QWidget):

    COLORS = {
        logging.DEBUG: 'black',
        logging.INFO: 'blue',
        logging.WARNING: 'orange',
        logging.ERROR: 'red',
        logging.CRITICAL: 'purple',
    }

    def __init__(self, app):
        super(Window, self).__init__()

        self.app = app

        self.textedit = te = QtWidgets.QPlainTextEdit(self)
        # Set whatever the default monospace font is for the platform
        f = QtGui.QFont('nosuchfont')
        f.setStyleHint(f.Monospace)
        te.setFont(f)
        te.setReadOnly(True)
        PB = QtWidgets.QPushButton
        self.work_button = PB('Start background work', self)
        self.log_button = PB('Log a message at a random level', self)
        self.clear_button = PB('Clear log window', self)
        self.handler = h = QtHandler(self.update_status)
        # Remember to use qThreadName rather than threadName in the format string.
        fs = '%(asctime)s %(qThreadName)-12s %(levelname)-8s %(message)s'
        formatter = logging.Formatter(fs)
        h.setFormatter(formatter)
        logger.addHandler(h)
        # Set up to terminate the QThread when we exit
        app.aboutToQuit.connect(self.force_quit)

        # Lay out all the widgets
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(te)
        layout.addWidget(self.work_button)
        layout.addWidget(self.log_button)
        layout.addWidget(self.clear_button)
        self.setFixedSize(900, 400)

        # Connect the non-worker slots and signals
        self.log_button.clicked.connect(self.manual_update)
        self.clear_button.clicked.connect(self.clear_display)

        # Start a new worker thread and connect the slots for the worker
        self.start_thread()
        self.work_button.clicked.connect(self.worker.start)
        # Once started, the button should be disabled
        self.work_button.clicked.connect(lambda : self.work_button.setEnabled(False))

    def start_thread(self):

        self.worker = Worker()
        self.worker_thread = QtCore.QThread()
        self.worker.setObjectName('Worker')
        self.worker_thread.setObjectName('WorkerThread')  # for qThreadName
        self.worker.moveToThread(self.worker_thread)
        # This will start an event loop in the worker thread
        self.worker_thread.start()

    def kill_thread(self):
        # Just tell the worker to stop, then tell it to quit and wait for that
        # to happen
        self.worker_thread.requestInterruption()
        if self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()
        else:
            print('worker has already exited.')

    def force_quit(self):
        # For use when the window is closed
        if self.worker_thread.isRunning():
            self.kill_thread()

    # The functions below update the UI and run in the main thread because
    # that's where the slots are set up

    @Slot(str, logging.LogRecord)
    def update_status(self, status, record):
        color = self.COLORS.get(record.levelno, 'black')
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.textedit.appendHtml(s)

    @Slot()
    def manual_update(self):
        # This function uses the formatted message passed in, but also uses
        # information from the record to format the message in an appropriate
        # color according to its severity (level).
        level = random.choice(LEVELS)
        extra = {'qThreadName': ctname() }
        logger.log(level, 'Manually logged!', extra=extra)

    @Slot()
    def clear_display(self):
        self.textedit.clear()


def main():
    QtCore.QThread.currentThread().setObjectName('MainThread')
    logging.getLogger().setLevel(logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    example = Window(app)
    example.show()
    sys.exit(app.exec_())




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:11 PM
# © 2017 - 2019 DAMGteam. All rights reserved