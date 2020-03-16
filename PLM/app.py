# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
""" import """

# PLM
from PLM.configs                        import SYSTRAY_UNAVAI, KEY_RELEASE
from PLM.ui.models                      import AppModel

# -------------------------------------------------------------------------------------------------------------
""" Operation """


class PLM(AppModel):

    key                                 = 'PLM'

    def __init__(self):
        AppModel.__init__(self)

        serverReady                     = self.checkConnectServer()
        userData                        = self.checkUserData()

        self.logger.info('Start app')

        if userData:
            if serverReady:
                statusCode              = self.serverAuthorization()
                if not statusCode:
                    self.mainUI.show()
                    self.splash.finish(self.mainUI)
                else:
                    if statusCode == 200:
                        if not self.sysTray.isSystemTrayAvailable():
                            self.logger.report(SYSTRAY_UNAVAI)
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
            if serverReady:
                self.signIn.show()
                self.splash.finish(self.signIn)
            else:
                self.sysNotify('Offline', 'Can not connect to Server', 'crit', 500)
                self.mainUI.show()
                self.splash.finish(self.mainUI)

    def notify(self, receiver, event):

        if event.type() == KEY_RELEASE:

            if event.key() == 16777217:
                pos = self.cursor.pos()
                self.shortcutCMD.show()
                self.shortcutCMD.move(pos)

        elif event.type() == 18:                                            # QHideEvent
            if hasattr(receiver, 'key'):
                if self.layoutManager:
                    if receiver.key in self.layouts.keys():
                        geometry = receiver.saveGeometry()
                        receiver.setValue('geometry', geometry)

        elif event.type() == 17:                                            # QShowEvent
            if hasattr(receiver, 'key'):
                if self.layoutManager:
                    if receiver.key in self.layoutManager.keys():
                        geometry = receiver.settings.value('geometry', b'')
                        receiver.restoreGeometry(geometry)

        return super(PLM, self).notify(receiver, event)


if __name__ == '__main__':
    app = PLM()
    app.run()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2019 DAMGteam. All rights reserved