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
import traceback


# PLM
from PLM                        import globalSetting
from PLM.configs                import (FRAMELESS, bottom, center, colorLibs, splashImagePth, ERROR_APPLICATION,
                                        ConfigPython, ConfigUrl, ConfigApps, ConfigPipeline, ConfigIcon,
                                        ConfigAvatar, ConfigLogo, ConfigImage, ConfigEnvVar, ConfigMachine,
                                        ConfigServer, ConfigFormats, ConfigDirectory, ConfigPath)

from PLM.cores.Errors           import LayoutComponentError
from PLM.commons.Widgets        import SplashScreen, MessageBox
from PLM.commons.Gui            import Pixmap
from PLM.ui.components          import AutoLoading, CircleLoading, PotionLoading


class SplashUI(SplashScreen):

    key                         = 'SplashScreen'
    _value                      = 0
    _num                        = 16
    _textColor                  = colorLibs.CYAN

    iconInfo                    = None
    appInfo                     = None
    urlInfo                     = None
    dirInfo                     = None
    pthInfo                     = None
    deviceInfo                  = None
    pythonInfo                  = None
    avatarInfo                  = None
    logoInfo                    = None
    imageInfo                   = None
    envInfo                     = None
    serverInfo                  = None
    formatInfo                  = None

    def __init__(self, app=None):
        super(SplashUI, self).__init__()

        self.app                = app

        if not self.app:
            MessageBox(self, 'Application Error', 'critical', ERROR_APPLICATION)
            sys.exit()

        self.pix                = Pixmap(splashImagePth)

        self.setPixmap(self.pix)
        self.setWindowFlags(FRAMELESS)
        self.setMask(self.pix.mask())
        self.setEnabled(False)

        self.autoLoading            = AutoLoading(self)

        if globalSetting.splashLoadingMode == 'progress':
            self.progressBar        = PotionLoading(self)
        elif globalSetting.splashLoadingMode == 'loading':
            self.progressBar        = CircleLoading(self)
        else:
            LayoutComponentError('There is no progress bar mode: {0}'.format(globalSetting.splashLoadingMode))
            sys.exit()

        self.show()
        self.autoLoading.start()
        self.progressBar.start()
        self.start_configuring()
        self.app.processEvents()

    def start_configuring(self):

        ws = ['Icons', 'Installed apps', 'Urls', 'Directories', 'Paths', 'Local Device', 'Python', 'Avatars', 'Logo',
              'Images', 'Evironment Variables', 'Server', 'Formats', 'Pipeline', ]

        fs = [ConfigIcon, ConfigApps, ConfigUrl, ConfigDirectory, ConfigPath, ConfigMachine, ConfigPython, ConfigAvatar,
              ConfigLogo, ConfigImage, ConfigEnvVar, ConfigServer, ConfigFormats, ConfigPipeline]

        vs = [1,1,1,1,1,1,1,1,1,1,1,1,1,2]

        for i in range(len(ws)):
            w = ws[i]
            f = fs[i]
            v = vs[i]
            self.process_config(w, f, v)

    def process_config(self, w, f, v):

        try:
            self.show_message('Config {0}'.format(w))
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            print(exctype, value, traceback.format_exc())

        try:
            if w == 'Icons':
                self.iconInfo = f()
            elif w == 'Installed apps':
                self.appInfo = f()
            elif w == 'Urls':
                self.urlInfo = f()
            elif w == 'Directories':
                self.dirInfo = f()
            elif w == 'Paths':
                self.pthInfo = f()
            elif w == 'Local Device':
                self.deviceInfo = f()
            elif w == 'Python':
                self.pythonInfo = f()
            elif w == 'Avatars':
                self.avatarInfo = f()
            elif w == 'Logo':
                self.logoInfo = f()
            elif w == 'Images':
                self.imageInfo = f()
            elif w == 'Evironment Variables':
                self.envInfo = f()
            elif w == 'Server':
                self.serverInfo = f()
            elif w == 'Formats':
                self.formatInfo = f()
            else:
                self.plmInfo = f(self.iconInfo, self.appInfo, self.urlInfo, self.dirInfo, self.pthInfo)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            print(exctype, value, traceback.format_exc())

        try:
            self.updateProgress(v)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            print(exctype, value, traceback.format_exc())

    def show_message(self, mess):
        if globalSetting.splashLoadingMode == 'progress':
            self.showMessage(mess, bottom|center, colorLibs.CYAN)
        elif globalSetting.splashLoadingMode == 'loading':
            pass
        else:
            pass

    def updateProgress(self, value):
        if globalSetting.splashLoadingMode == 'progress':
            if value == 0:
                self.progressBar.setValue(0)
            else:
                value = value*10
                for i in range(value):
                    self.value += 1
                    self.progressBar.setValue(self.value)
                    i += 1
        elif globalSetting.splashLoadingMode == 'loading':
            self.progressBar.setProgress(value)
        else:
            pass

    @property
    def value(self):
        return self._value

    @property
    def num(self):
        return self._num

    @property
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, val):
        self._textColor             = val

    @value.setter
    def value(self, val):
        self._value                 = val

    @num.setter
    def num(self, val):
        self._num                   = val


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ui = SplashUI(app)
    sys.exit(app.exec_())


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:56 PM
# © 2017 - 2019 DAMGteam. All rights reserved