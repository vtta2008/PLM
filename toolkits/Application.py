# -*- coding: utf-8 -*-
"""

Script Name: Application.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__, __envKey__, ROOT, glsetting
""" Import """

# Python
import sys, argparse, helpdev, ctypes
from ctypes                         import wintypes

# PyQt5
from PyQt5.QtWidgets                import QApplication
from PyQt5.QtGui                    import QPalette

# PLM
from appData                        import __version__, __appname__, __organization__, __website__
from cores.Loggers                  import Loggers
from cores.SignalManager            import SignalManager
from cores.Settings                 import Settings
from cores.StyleSheet               import StyleSheet
from .Core                          import Process
from .Gui                           import Cursor
from .Widgets                       import LogoIcon

class Application(QApplication):

    Type                            = 'DAMGAPPLICATION'
    key                             = 'Application'
    _name                           = 'DAMG Application'
    _envKey                         = __envKey__
    _root                           = ROOT

    _copyright                      = __copyright__()

    _login                          = False

    _styleSheet                     = None

    parser = argparse.ArgumentParser(description="damgteam helper. Use the option --all to report bugs",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    pallete = QPalette()


    def __init__(self):
        super(Application, self).__init__(sys.argv)

        sys.path.insert(0, ROOT)
        self.default_parser()
        self.setWindowIcon(LogoIcon("Logo"))  # Setup icon
        self.setOrganizationName(__organization__)
        self.setApplicationName(__appname__)
        self.setOrganizationDomain(__website__)
        self.setApplicationVersion(__version__)
        self.setApplicationDisplayName(__appname__)
        self.setCursorFlashTime(1000)
        self.setQuitOnLastWindowClosed(False)
        self.setDesktopSettingsAware(False)

        self.logger                     = Loggers(self.__class__.__name__)
        self.settings                   = Settings(self)
        self.signals                    = SignalManager(self)
        self.cursor                     = Cursor(self)
        self.appStyle                   = StyleSheet(self)

        self.process                    = self.getAppProcess()

        self.settings._settingEnable    = True
        self.appInfo                    = self.dataConfig.appInfo  # Configuration qssPths

    def set_styleSheet(self, style):
        self.appStyle.getQssFile(style)
        self.appStyle.changeStyleSheet(style)
        self.settings.initSetValue('styleSheet', style, self.key)

    def getAppProcess(self):
        proc = Process(parent=self)
        proc.setStandardInputFile(proc.nullDevice())
        proc.setStandardOutputFile(proc.nullDevice())
        proc.setStandardErrorFile(proc.nullDevice())
        self.process = proc
        return self.process

    def getAppID(self):
        lpBuffer            = wintypes.LPWSTR()
        AppUserModelID      = ctypes.windll.shell32.GetCurrentProcessExplicitAppUserModelID
        appID               = lpBuffer.value
        ctypes.windll.kernel32.LocalFree(lpBuffer)
        AppUserModelID(ctypes.cast(ctypes.byref(lpBuffer), wintypes.LPWSTR))
        self.logger.info('Get AppID: {0}'.format(appID))

        return appID

    def default_parser(self):
        self.parser.add_argument('-i', '--information', action='store_true', help="Show information about environment")
        self.parser.add_argument('-b', '--bindings', action='store_true', help="Show available bindings for Qt")
        self.parser.add_argument('-a', '--abstractions', action='store_true', help="Show available abstraction layers for Qt bindings")
        self.parser.add_argument('-d', '--dependencies', action='store_true', help="Show information about dependencies")
        self.parser.add_argument('-v', '--version', action='version', version='v{}'.format(__version__))
        self.parser.add_argument('-all', '--all', action='store_true', help="Show all information options at once")
        return self.parser

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

        self.appID                      = self.getAppID()
        return sys.exit(self.exec_())

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

    def setRecieveSignal(self, bool):
        glsetting.tracks.recieveSignal = bool
        self.commander.trackRecieveSignal = bool

    def setBlockSignal(self, bool):
        glsetting.tracks.blockSignal = bool
        self.commander.trackBlockSignal = bool

    def setTrackCommand(self, bool):
        glsetting.tracks.command = bool
        self.commander.trackCommand = bool

    def setRegistLayout(self, bool):
        glsetting.tracks.registLayout = bool
        self.commander.trackRegistLayout = bool

    def setJobsTodo(self, bool):
        glsetting.tracks.jobsToDo = bool
        self.commander.trackJobsTodo = bool

    def setShowLayout(self, bool):
        glsetting.tracks.showLayoutError = bool
        self.commander.trackShowLayoutError = bool

    def setTrackEvent(self, bool):
        glsetting.tracks.events = bool
        self.commander.trackEvents = bool


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/12/2019 - 8:49 AM
# © 2017 - 2018 DAMGteam. All rights reserved