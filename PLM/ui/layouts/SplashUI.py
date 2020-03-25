# -*- coding: utf-8 -*-
"""

Script Name: SplashUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtWidgets                    import QApplication

# PLM
from PLM                                import globalSetting
from PLM.ui.components.Loading          import StaticLoading, RealtimeLoading
from PLM.cores.models                   import AutoLoadingThread, RealtimeUpdatingThread
from PLM.configs                        import (ERROR_APPLICATION, FRAMELESS, SPLASHSCREEN, ERROR_LAYOUT_COMPONENT,
                                                splashImagePth,
                                                ConfigPython, ConfigUrl, ConfigApps, ConfigPipeline, ConfigIcon,
                                                ConfigAvatar, ConfigLogo, ConfigImage, ConfigEnvVar, ConfigMachine,
                                                ConfigServer, ConfigFormats, ConfigDirectory, ConfigPath, ConfigFonts)
from PLM.commons.Widgets                import SplashScreen, MessageBox, ProgressBar
from PLM.commons.Gui                    import LogoIcon, Pixmap
from PLM.commons.Core                   import Timer
from PLM.cores                          import MultiThreadManager, StyleSheet



class LoadingBar(ProgressBar):

    key                                 = 'ProgressUI'
    _name                               = 'DAMG Progress UI'

    def __init__(self, parent=None):
        super(LoadingBar, self).__init__(parent)

        self.parent                     = parent

        if not self.parent:
            MessageBox(self, 'Loading Layout Component', 'critical', ERROR_LAYOUT_COMPONENT)
            sys.exit()
        else:
            self.num                    = self.parent.num
            self.pix                    = self.parent.splashPix
            self.setMinimum(0)
            self.setMaximum(self.num*10)
            self.setGeometry(50, self.pix.height() - 50, self.pix.width() - 100, 20)
            self.setTextVisible(True)
            self.setStyleSheet(StyleSheet.progressBar())

    def start(self):
        self.show()


class SplashUI(SplashScreen):

    key                                 = 'SplashUI'

    _bufferH                            = 100
    _bufferW                            = 200

    pythonInfo                          = None
    dirInfo                             = None
    pthInfo                             = None
    urlInfo                             = None
    envInfo                             = None
    iconInfo                            = None
    avatarInfo                          = None
    logoInfo                            = None
    imageInfo                           = None
    serverInfo                          = None
    formatInfo                          = None
    fontInfo                            = None
    deviceInfo                          = None
    appInfo                             = None
    plmInfo                             = None

    _cfgCount                           = 0
    _percentCount                       = 0
    _num                                = 16

    def __init__(self, app=None):
        super(SplashUI, self).__init__(app)

        self.app                        = app

        if not self.app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()

        self.splashPix                  = Pixmap(splashImagePth)
        self.setPixmap(self.splashPix)
        self.setMask(self.splashPix.mask())

        self.setWindowIcon(LogoIcon('DAMGTEAM'))
        self.setWindowFlags(SPLASHSCREEN | FRAMELESS)

        self.timer                      = Timer(self)
        self.threadManager              = MultiThreadManager(self)
        self.screen                     = self.app.desktop().availableGeometry()

        self.realtimeLoading            = RealtimeLoading(self)
        self.staticLoading              = StaticLoading(self)

        self.autoThread                 = AutoLoadingThread(self.staticLoading, self)
        self.realtimeThread             = RealtimeUpdatingThread(self.realtimeLoading, self)
        self.progress                   = LoadingBar(self)

        self.start()

        self.app.processEvents()

    def autoConfig(self):

        words = ['Python', 'Directories', 'File Paths', 'Urls & Links', 'System Environment Variable', 'Icons', 'Avatars',
                 'Logo', 'Images', 'Servers', 'Formats', 'Fonts', 'Local Devices', 'App Installed', 'Pipeline']

        for i in range(len(words)):

            self.setText('Config {0}'.format(words[i]))

            if i == 0:
                self.pythonInfo             = ConfigPython()
            elif i == 1:
                self.dirInfo                = ConfigDirectory()
            elif i == 2:
                self.pthInfo                = ConfigPath()
            elif i == 3:
                self.urlInfo                = ConfigUrl()
            elif i == 4:
                self.envInfo                = ConfigEnvVar()
            elif i == 5:
                self.iconInfo               = ConfigIcon()
            elif i == 6:
                self.avatarInfo             = ConfigAvatar()
            elif i == 7:
                self.logoInfo               = ConfigLogo()
            elif i == 8:
                self.imageInfo              = ConfigImage()
            elif i == 9:
                self.serverInfo             = ConfigServer()
            elif i == 10:
                self.formatInfo             = ConfigFormats()
            elif i == 11:
                self.fontInfo               = ConfigFonts()
            elif i == 12:
                self.deviceInfo             = ConfigMachine()
            elif i == 13:
                self.appInfo                = ConfigApps()
            else:
                if self.iconInfo and self.appInfo and self.urlInfo and self.dirInfo and self.pthInfo:
                    self.plmInfo = ConfigPipeline(self.iconInfo, self.appInfo, self.urlInfo, self.dirInfo, self.pthInfo)

            if i == 14:
                self.setProgress(2)
            else:
                self.setProgress(1)

            self._cfgCount = i + 1

            if self._cfgCount == len(words):
                check = True
                for info in [self.pythonInfo, self.dirInfo, self.pthInfo, self.urlInfo, self.envInfo, self.iconInfo,
                             self.avatarInfo, self.logoInfo, self.imageInfo, self.serverInfo, self.formatInfo,
                             self.fontInfo, self.deviceInfo, self.appInfo, self.plmInfo]:
                    if not info:
                        print('{0} is None.'.format(info.key))
                        check = False
                globalSetting.setCfgAll(check)
            else:
                globalSetting.setCfgAll(False)

    def updatePosition(self):
        return self.move((self.screen.width() - self.width())/2, (self.screen.height() - self.height())/2)

    def start(self):

        self.autoThread.signal.result.connect(self.threadManager.print_output)
        self.autoThread.signal.finished.connect(self.threadManager.worker_completed)
        self.autoThread.signal.progress.connect(self.threadManager.progress_fn)

        self.realtimeThread.signal.result.connect(self.threadManager.print_output)
        self.realtimeThread.signal.finished.connect(self.threadManager.worker_completed)
        self.realtimeThread.signal.progress.connect(self.threadManager.progress_fn)

        self.autoThread.start()
        self.realtimeThread.start()
        # self.threadManager.start(self.configTask)

        self.updatePosition()
        self.show()
        self.progress.show()
        self.autoConfig()

    def resizeEvent(self, event):
        self.resize(event.size().width() + self.bufferW, event.size().height() + self.bufferH)
        self.staticLoading.resize(self.size())
        self.realtimeLoading.resize(self.size())
        event.accept()

    def setText(self, text):
        self.realtimeThread.setText(text)

    def setProgress(self, val):
        value = int((100*val)/(self.num*10))
        for i in range(value):
            self._percentCount += (i+1)
            self.progress.setValue(self._percentCount)
            self.realtimeThread.setProgress(str(self._percentCount))

    @property
    def bufferH(self):
        return self._bufferH

    @property
    def bufferW(self):
        return self._bufferW

    @property
    def cfgCount(self):
        return self._cfgCount

    @property
    def num(self):
        return self._num

    @property
    def percentCount(self):
        return self._percentCount

    @percentCount.setter
    def percentCount(self, val):
        self._percentCount              = val

    @num.setter
    def num(self, val):
        self._num                       = val

    @cfgCount.setter
    def cfgCount(self, val):
        self._cfgCount                  = val

    @bufferW.setter
    def bufferW(self, val):
        self._bufferW                   = val

    @bufferH.setter
    def bufferH(self, val):
        self._bufferH                   = val


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ui = SplashUI(app)
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:56 PM
# © 2017 - 2019 DAMGteam. All rights reserved