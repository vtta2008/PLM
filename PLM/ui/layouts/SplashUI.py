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
            self.setMaximum(100)

            self.setGeometry((self.pix.width()-self.width())/2 + 115, self.pix.height() - 115, self.pix.width()/10, 10)
            self.setTextVisible(False)
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
        self.autoLoading                = StaticLoading(self)
        self.autoThread                 = AutoLoadingThread(self.autoLoading, self.app)

        self.realtimeLoading            = RealtimeLoading(self)
        self.realtimeThread             = RealtimeUpdatingThread(self.realtimeLoading, self.app)

        self.autoThread.rotate.connect(self.update_rotate)
        self.autoThread.signal.result.connect(self.threadManager.print_output)
        self.autoThread.signal.finished.connect(self.threadManager.worker_completed)
        self.autoThread.signal.progress.connect(self.threadManager.progress_fn)

        self.realtimeThread.signal.result.connect(self.threadManager.print_output)
        self.realtimeThread.signal.finished.connect(self.threadManager.worker_completed)
        self.realtimeThread.signal.progress.connect(self.threadManager.progress_fn)

        self.updatePosition()
        self.autoThread.start()
        self.realtimeThread.start()

        self.progress                   = LoadingBar(self)
        self.progress.show()
        self.show()
        self.autoConfig()

    def autoConfig(self):

        words = ['Python', 'Directories', 'File Paths', 'Urls & Links', 'Environment Variable', 'Icons', 'Avatars',
                 'Logo', 'Images', 'Servers', 'Formats', 'Fonts', 'Local Devices', 'Installed Apps', 'Pipeline Functions']

        configs = [ConfigPython, ConfigDirectory, ConfigPath, ConfigUrl, ConfigEnvVar, ConfigIcon, ConfigAvatar,
                   ConfigLogo, ConfigImage, ConfigServer, ConfigFormats, ConfigFonts, ConfigMachine, ConfigApps,
                   ConfigPipeline]

        for i in range(len(words)):
            if not i == (len(words) - 1):
                self.setText('Config {0}'.format(words[i]))
                if i == 0:
                    self.pythonInfo = configs[i]()
                elif i == 1:
                    self.dirInfo    = configs[i]()
                elif i == 2:
                    self.pthInfo    = configs[i]()
                elif i == 3:
                    self.urlInfo    = configs[i]()
                elif i == 4:
                    self.envInfo    = configs[i]()
                elif i == 5:
                    self.iconInfo   = configs[i]()
                elif i == 6:
                    self.avatarInfo = configs[i]()
                elif i == 7:
                    self.logoInfo   = configs[i]()
                elif i == 8:
                    self.imageInfo  = configs[i]()
                elif i == 9:
                    self.serverInfo = configs[i]()
                elif i == 10:
                    self.formatInfo = configs[i]()
                elif i == 11:
                    self.fontInfo   = configs[i]()
                elif i == 12:
                    self.deviceInfo = configs[i]()
                elif i == 13:
                    self.appInfo    = configs[i]()
                self.setProgress(1)
            else:
                self.setText('Config {0}'.format('Pipeline Functions'))
                if self.iconInfo and self.appInfo and self.urlInfo and self.dirInfo and self.pthInfo:
                    self.plmInfo = ConfigPipeline(self.iconInfo, self.appInfo, self.urlInfo, self.dirInfo, self.pthInfo)
                    self.setProgress(2)
                else:
                    print('Can not conducting Pipeline Functions configurations, some of other configs has not been done yet.')
                    self.app.exit()

            self._cfgCount += 1
            self.processEvents()

        check = False

        if self.cfgCount == len(words):
            for info in [self.pythonInfo, self.dirInfo, self.pthInfo, self.urlInfo, self.envInfo, self.iconInfo,
                         self.avatarInfo, self.logoInfo, self.imageInfo, self.serverInfo, self.formatInfo,
                         self.fontInfo, self.deviceInfo, self.appInfo, self.plmInfo]:
                if not info:
                    print('{0} is None.'.format(info.key))
                    check = False
                else:
                    check = True
            self.stopThreads()

        globalSetting.setCfgAll(check)

    def resizeEvent(self, event):
        self.resize(event.size().width() + self.bufferW, event.size().height() + self.bufferH)
        self.autoLoading.resize(self.size())
        self.realtimeLoading.resize(self.size())
        event.accept()

    def processEvents(self):
        if not self.app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()
        else:
            return self.app.processEvents()

    def update_rotate(self, bool):
        self.autoLoading.rotate()

    def setText(self, text):
        self.realtimeLoading.setText(text)
        # self.processEvents()

    def setProgress(self, val):
        value                   = (100*val)/self.num
        for i in range(int(value)):
            self._percentCount  += 1
            if self.progress:
                self.progress.setValue(self.percentCount)
            self.realtimeLoading.setProgress('{0}%'.format(str(self.percentCount)))

            if self.percentCount == 96:
                for i in range(4):
                    self._percentCount  += 1
                    if self.progress:
                        self.progress.setValue(self.percentCount)
                    self.realtimeLoading.setProgress('{0}%'.format(str(self.percentCount)))


    def updatePosition(self):
        return self.move((self.screen.width() - self.width())/2, (self.screen.height() - self.height())/2)

    def stopThreads(self):
        self.autoThread.stop()
        self.realtimeThread.stop()
        self.autoThread.wait()
        self.realtimeThread.wait()
        self.killThreads()
        self.processEvents()

    def killThreads(self):
        self.autoThread.terminate()
        self.realtimeThread.terminate()

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