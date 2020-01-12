# -*- coding: utf-8 -*-
"""

Script Name: Application.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__, __envKey__, ROOT, globalSetting
""" Import """

# Python
import sys, argparse, helpdev, ctypes
from ctypes                         import wintypes

# PyQt5
from PyQt5.QtWidgets                import QApplication
from PyQt5.QtGui                    import QColor

# PLM
from appData                        import __version__, __appname__, __organization__, __website__, DarkPalette, STAY_ON_TOP
from cores.Loggers                  import Loggers
from cores.SignalManager            import SignalManager
from cores.Settings                 import Settings
from cores.StyleSheet               import StyleSheet
from .Core                          import Process
from .Gui                           import Cursor, LogoIcon, Color
from .Widgets                       import MessageBox
from plugins                        import Qt
qt_api                              = Qt.__binding__

class Application(QApplication):

    Type                            = 'DAMGAPPLICATION'
    key                             = 'Application'
    _name                           = 'DAMG Application'
    _copyright                      = __copyright__()

    _login                          = False
    _styleSheetData                 = None

    threadManager                   = None
    eventManager                    = None
    layoutManager                   = None

    appInfo                         = None
    plmInfo                         = None

    layouts                         = None

    def __init__(self):
        super(Application, self).__init__(sys.argv)

        sys.path.insert(0, ROOT)
        self.default_parser()
        self.setWindowIcon(LogoIcon("Logo"))                        # Setup icon
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

        if qt_api == 'PyQt5':
            self.palette = self.palette()
            self.palette.setColor(self.palette.Normal, self.palette.Link, QColor(DarkPalette.COLOR_BACKGROUND_LIGHT))
            self.setPalette(self.palette)

    def messageBox(self, parent=None, title="auto", level="auto", message="test message", btn='ok'):
        messBox = MessageBox(parent, title, level, message, btn)
        messBox.setWindowFlag(STAY_ON_TOP)
        return messBox

    def set_styleSheet(self, style):
        self._styleSheetData            = self.appStyle.getStyleSheet(style)
        self.setStyleSheet(self._styleSheetData)
        self.settings.initSetValue('styleSheet', style, self.key)

    def clearStyleSheet(self):
        self._styleSheetData            = ''
        self.setStyleSheet(self._styleSheetData)
        self.settings.initSetValue('styleSheet', None, self.key)

    def changeStyleSheet(self, style):
        self.clearStyleSheet()
        self.set_styleSheet(style)

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
        if appID is None:
            appID           = self.key
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)
            except:
                print("Could not set the app model ID. If the plaftorm is older than Windows 7, this is normal.")

        ctypes.windll.kernel32.LocalFree(lpBuffer)
        AppUserModelID(ctypes.cast(ctypes.byref(lpBuffer), wintypes.LPWSTR))
        self.logger.info('Get AppID: {0}'.format(appID))

        return appID

    def default_parser(self):
        parser = argparse.ArgumentParser(description="damgteam helper. Use the option --all to report bugs",
                                         formatter_class=argparse.RawDescriptionHelpFormatter)

        parser.add_argument('-i', '--information', action='store_true', help="Show information about environment")
        parser.add_argument('-b', '--bindings', action='store_true', help="Show available bindings for Qt")
        parser.add_argument('-a', '--abstractions', action='store_true', help="Show available abstraction layers for Qt bindings")
        parser.add_argument('-d', '--dependencies', action='store_true', help="Show information about dependencies")
        parser.add_argument('-v', '--version', action='version', version='v{}'.format(__version__))
        parser.add_argument('-all', '--all', action='store_true', help="Show all information options at once")

        return parser

    def startLoop(self):
        # parsing arguments from command line
        parser = self.default_parser()
        args = parser.parse_args()
        no_args = not len(sys.argv) > 1
        info = {}

        if no_args:
            parser.print_help()

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

    @property
    def styleSheetData(self):
        return self._styleSheetData

    @styleSheetData.setter
    def styleSheetData(self, val):
        self._styleSheetData        = val

    @name.setter
    def name(self, val):
        self._name                  = val

    @login.setter
    def login(self, val):
        self._login                 = val

    def setRecieveSignal(self, bool):
        globalSetting.tracks.recieveSignal = bool

    def setBlockSignal(self, bool):
        globalSetting.tracks.blockSignal = bool

    def setTrackCommand(self, bool):
        globalSetting.tracks.command = bool

    def setRegistLayout(self, bool):
        globalSetting.tracks.registLayout = bool

    def setJobsTodo(self, bool):
        globalSetting.tracks.jobsToDo = bool

    def setShowLayout(self, bool):
        globalSetting.tracks.showLayoutError = bool

    def setTrackEvent(self, bool):
        globalSetting.tracks.events = bool


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/12/2019 - 8:49 AM
# © 2017 - 2018 DAMGteam. All rights reserved