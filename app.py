# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
""" import """

# Python
import sys
from PLM import __organization__, __envKey__, __version__

try:
    # Include in try/except block if you're also targeting Mac/Linux
    from PySide2.QtWinExtras import QtWin
    myappid = '{0}.{1}.{2}'.format(__organization__, __envKey__, __version__)
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


# PLM
from PLM.ui.models                      import AppModel
from PLM.ui                             import LayoutManager
from PLM.configs                        import configPropText
p = configPropText()

from PLM.ui.layouts                     import SplashUI


# -------------------------------------------------------------------------------------------------------------
""" Operation """


class PLM(AppModel):

    key                                 = 'PLM'

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        self.splash                     = SplashUI(self)
        self.layoutManager              = LayoutManager(self.threadManager, self)
        self.layoutManager.registLayout(self.browser)
        self.layoutManager.buildLayouts()
        self.mainUI, self.sysTray, self.shortcutCMD, self.signIn, self.signUp, self.forgotPW = self.layoutManager.mains
        self.layoutManager.globalLayoutSetting()

        self.layouts                    = self.layoutManager.register
        self.connectServer              = self.checkConnectServer()
        userData                        = self.checkUserData()
        if userData:
            if self.connectServer:
                statusCode              = self.serverAuthorization()
                if not statusCode:
                    self.mainUI.show()
                    self.splash.finish(self.mainUI)
                else:
                    if statusCode == 200:
                        if not self.sysTray.isSystemTrayAvailable():
                            self.logger.debug(p['SYSTRAY_UNAVAILABLE'])
                            self.exitEvent()
                        else:
                            self.loginChanged(True)
                            self.sysTray.log_in()
                            self.mainUI.show()
                            self.splash.finish(self.mainUI)
                    else:
                        self.signIn.show()
                        self.splash.finish(self.signIn)
            else:
                self.sysNotify('Offline', 'Can not connect to Server', 'crit', 500)
                self.mainUI.show()
                self.splash.finish(self.mainUI)
        else:
            if self.connectServer:
                # print('here?')
                self.signInEvent()
                self.signIn.show()
                self.splash.finish(self.signIn)
            else:
                self.sysNotify('Offline', 'Can not connect to Server', 'crit', 500)
                self.mainUI.show()
                self.splash.finish(self.mainUI)

    def notify(self, receiver, event):
        # press tab to show shortcut command ui
        if event.type() == p['KEY_RELEASE']:
            if self.login and event.key() == 16777217:
                pos = self.cursor.pos()
                self.shortcutCMD.show()
                self.shortcutCMD.move(pos)

        # save ui geometry when it is closed
        elif event.type() == 18:                                            # QHideEvent
            if hasattr(receiver, 'key'):
                if self.layoutManager:
                    if receiver.key in self.layouts.keys():
                        geometry = receiver.saveGeometry()
                        receiver.setValue('geometry', geometry)

        # load ui geometry when it is showed
        elif event.type() == 17:                                            # QShowEvent
            if hasattr(receiver, 'key'):
                if self.layoutManager:
                    if receiver.key in self.layoutManager.keys():
                        geometry = receiver.settings.value('geometry', b'')
                        receiver.restoreGeometry(geometry)

        return super(PLM, self).notify(receiver, event)

    def run(self):
        """
        avoids some QThread messages in the shell on exit, cancel all running tasks avoid QThread/QTimer error messages,
        on exit
        """
        self.exec_()
        self.deleteLater()



if __name__ == '__main__':
    app = PLM()
    app.run()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2019 DAMGteam. All rights reserved