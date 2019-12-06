# -*- coding: utf-8 -*-
"""

Script Name: Application.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__, __envKey__, ROOT, preSetting, __ignoreIDs__, __tobuildCmds__, __tobuildUis__
""" Import """

# Python
import sys, argparse, helpdev

# PyQt5
from PyQt5.QtWidgets                import QApplication
from PyQt5.QtGui                    import QPalette

# PLM
from appData import __version__


class Application(QApplication):

    Type                            = 'DAMGAPPLICATION'
    key                             = 'Application'
    _name                           = 'DAMG Application'
    _envKey                         = __envKey__
    _root                           = ROOT

    _copyright                      = __copyright__()

    _login                          = False

    trackRecieveSignal             = preSetting.tracks.recieveSignal
    trackBlockSignal               = preSetting.tracks.blockSignal
    trackCommand                   = preSetting.tracks.command
    trackRegistLayout              = preSetting.tracks.registLayout
    trackJobsTodo                  = preSetting.tracks.jobsToDo
    trackShowLayoutError           = preSetting.tracks.showLayoutError
    trackEvents                    = preSetting.tracks.events

    timeReset                       = 5

    ignoreIDs                       = __ignoreIDs__()
    toBuildUis                      = __tobuildUis__()
    toBuildCmds                     = __tobuildCmds__()

    TODO                            = dict(toBuildUis = toBuildUis, toBuildCmds = toBuildCmds)

    showLayout_old                  = []
    executing_old                   = []
    setSetting_old                  = []
    openBrowser_old                 = []
    sysNotify_old                   = []

    _styleSheet                     = None

    _allowLocalMode                 = True

    parser = argparse.ArgumentParser(description="damgteam helper. Use the option --all to report bugs",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    pallete = QPalette()

    def default_parser(self):
        self.parser.add_argument('-i', '--information', action='store_true', help="Show information about environment")
        self.parser.add_argument('-b', '--bindings', action='store_true', help="Show available bindings for Qt")
        self.parser.add_argument('-a', '--abstractions', action='store_true', help="Show available abstraction layers for Qt bindings")
        self.parser.add_argument('-d', '--dependencies', action='store_true', help="Show information about dependencies")
        self.parser.add_argument('-v', '--version', action='version', version='v{}'.format(__version__))
        self.parser.add_argument('-all', '--all', action='store_true', help="Show all information options at once")
        return self.parser

    def checkSignalRepeat(self, old, data):
        new = [i for i in data]

        if len(new) == 0:
            repeat = False
        elif len(new) == len(old):
            repeat = True
            for i in range(len(new)):
                if not new[i] == old[i]:
                    repeat = False
                    break
        else:
            repeat = False

        old = new
        return old, repeat

    def startLoop(self):
        # parsing arguments from command line
        args = self.parser.parse_args()
        no_args = not len(sys.argv) > 1
        info = {}

        if no_args:
            self.parser.print_help()

        if args.information or args.all:
            info.update(helpdev.check_os())
            info.update(helpdev.check_python())

        if args.bindings or args.all:
            info.update(helpdev.check_qt_bindings())

        if args.abstractions or args.all:
            info.update(helpdev.check_qt_abstractions())

        if args.dependencies or args.all:
            info.update(helpdev.check_python_packages(packages='helpdev,damgteam'))

        helpdev.print_output(info)

        return sys.exit(self.exec_())

    def setRecieveSignal(self, bool):
        preSetting.tracks.recieveSignal = bool
        self.trackRecieveSignal = bool

    def setBlockSignal(self, bool):
        preSetting.tracks.blockSignal = bool
        self.trackBlockSignal = bool

    def setTrackCommand(self, bool):
        preSetting.tracks.command = bool
        self.trackCommand = bool

    def setRegistLayout(self, bool):
        preSetting.tracks.registLayout = bool
        self.trackRegistLayout = bool

    def setJobsTodo(self, bool):
        preSetting.tracks.jobsToDo = bool
        self.trackJobsTodo = bool

    def setShowLayout(self, bool):
        preSetting.tracks.showLayoutError = bool
        self.trackShowLayoutError = bool

    def setTrackEvent(self, bool):
        preSetting.tracks.events = bool
        self.trackEvents = bool

    def countDownReset(self, limit):
        self.count += 1
        if self.count == limit:
            self.showLayout_old     = []
            self.executing_old      = []
            self.setSetting_old     = []
            self.openBrowser_old    = []
            self.sysNotify_old      = []

    @property
    def login(self):
        return self._login

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                  = val

    @login.setter
    def login(self, val):
        self._login                 = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/12/2019 - 8:49 AM
# © 2017 - 2018 DAMGteam. All rights reserved