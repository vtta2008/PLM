# -*- coding: utf-8 -*-
"""

Script Name: Application.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
import ctypes

try:
    from ctypes.wintypes            import HRESULT
except ImportError:
    from ctypes                     import HRESULT
finally:
    from ctypes                     import wintypes



# PyQt5
from PyQt5.QtWidgets                import QApplication
from PyQt5.QtGui                    import QColor

# PLM
from PLM                            import __copyright__, ROOT, globalSetting
from PLM.configs                    import __version__, __appname__, __organization__, __website__, DarkPalette, PLMAPPID
from PLM.cores                      import Loggers, SignalManager, SettingManager, StyleSheet
from PLM.commons.Core               import Process
from PLM.commons.Gui                import Cursor, LogoIcon
from PLM.commons.Widgets            import MessageBox
from PLM.plugins                    import Qt

PCWSTR                              = ctypes.c_wchar_p
AppUserModelID                      = ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID
AppUserModelID.argtypes             = [PCWSTR]
AppUserModelID.restype              = HRESULT


class Application(QApplication):

    Type                            = 'DAMGAPPLICATION'
    key                             = 'Application'
    _name                           = 'DAMG Application'
    _copyright                      = __copyright__()

    _login                          = False
    _styleSheetData                 = None

    _server                         = None
    _verify                         = False

    threadManager                   = None
    eventManager                    = None
    layoutManager                   = None

    appInfo                         = None
    plmInfo                         = None
    layouts                         = None

    token                           = None
    cookie                          = None

    browser                         = None
    mainUI                          = None
    sysTray                         = None
    shortcutCMD                     = None
    signIn                          = None
    signUp                          = None
    forgotPW                        = None

    _appID                          = None

    def __init__(self):
        super(Application, self).__init__(sys.argv)

        sys.path.insert(0, ROOT)

        self.setWindowIcon(LogoIcon("DAMG"))                        # Setup icon
        self.setOrganizationName(__organization__)
        self.setApplicationName(__appname__)
        self.setOrganizationDomain(__website__)
        self.setApplicationVersion(__version__)
        self.setApplicationDisplayName(__appname__)
        self.setCursorFlashTime(1000)
        self.setQuitOnLastWindowClosed(False)
        self.setDesktopSettingsAware(True)

        self.logger                     = Loggers(__name__)
        self.settings                   = SettingManager(self)
        self.signals                    = SignalManager(self)
        self.appStyle                   = StyleSheet(self)
        self.set_styleSheet('dark')

        self.cursor                     = Cursor(self)
        self.process                    = self.getAppProcess()
        self.settings._settingEnable    = True

        if Qt.__binding__ == 'PyQt5':
            self.palette                = self.palette()
            self.palette.setColor(self.palette.Normal, self.palette.Link, QColor(DarkPalette.COLOR_BACKGROUND_LIGHT))
            self.setPalette(self.palette)

        appID                           = PLMAPPID
        hresult                         = AppUserModelID(appID)
        assert hresult == 0, "SetCurrentProcessExplicitAppUserModelID failed"

    def sys_message(self, parent=None, title="auto", level="auto", message="test message", btn='ok', flag=None):
        messBox =  MessageBox(parent, title, level, message, btn, flag)
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
        lpBuffer                        = wintypes.LPWSTR()
        appID                           = lpBuffer.value
        AppUserModelID(ctypes.cast(ctypes.byref(lpBuffer), wintypes.LPWSTR))
        ctypes.windll.kernel32.LocalFree(lpBuffer)
        self.logger.info('Get AppID: {0}'.format(appID))
        return appID

    def run(self):
        self._appID                     = self.getAppID()
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

    @property
    def appID(self):
        return self._appID

    @property
    def server(self):
        return self._server

    @property
    def verify(self):
        return self._verify

    @styleSheetData.setter
    def styleSheetData(self, val):
        self._styleSheetData        = val

    @name.setter
    def name(self, val):
        self._name                  = val

    @login.setter
    def login(self, val):
        self._login                 = val

    @appID.setter
    def appID(self, val):
        self._appID                 = val

    @server.setter
    def server(self, val):
        self._server               = val

    @verify.setter
    def verify(self, val):
        self._verify               = val

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