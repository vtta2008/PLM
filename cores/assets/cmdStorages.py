# -*- coding: utf-8 -*-
"""

Script Name: cmdStorages.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import globalSetting

import os

from devkit.Widgets import UndoCommand

from __buildtins__ import __envKey__, ROOT


class CmdBase(UndoCommand):

    key = 'CmdBase'
    task = None

    def __init__(self, app=None):
        super(CmdBase, self).__init__()

        self.app = app
        self.process = app.getAppProcess()

    def exec(self, cmd):
        args = [arg for arg in cmd.split(' ')]
        t = " ".join(args)
        if self.process.state() != 2:
            self.process.waitForStarted()
            self.process.waitForFinished()
            if "|" in t or ">" in t or "<" in t:
                self.process.start('sh -c "' + cmd + ' ' + t + '"')
            else:
                self.process.start(cmd + " " + t)
        try:
            output = str(self.process.readAll(), encoding='utf8').rstrip()
        except TypeError:
            output = str(self.process.readAll()).rstrip()

        return output

class DebugCmd(CmdBase):

    key = 'debug'

    def __init__(self, app):
        super(DebugCmd, self).__init__(app)

        self.task = self.app.mainUI.botTabUI.botTab2.test

    def run(self):
        return self.task()

    def undo(self):
        pass

    def redo(self):
        return self.task()

class CmdCmd(CmdBase):

    key = 'cmd'

    def __init__(self, app):
        super(CmdCmd, self).__init__(app)

        self.task = self.process

    def run(self):
        cmd = 'start /wait cmd'
        os.system(cmd)

    def undo(self):
        pass

    def redo(self):
        self.run()

class CleanPycCmd(CmdBase):

    key = 'cleanpyc'

    def __init__(self, app):
        super(CleanPycCmd, self).__init__(app)

        self.task = self.run()

    def run(self):
        from utils import clean_file_ext
        return clean_file_ext('.pyc')

    def redo(self):
        from utils import clean_file_ext
        return clean_file_ext('.pyc')

class ReConfigCmd(CmdBase):

    key = 'reconfig'

    def __init__(self, app):
        super(ReConfigCmd, self).__init__(app)

        self.task = self.run()

    def run(self):
        from cores.ConfigManager import ConfigManager
        self.app.dataConfig = ConfigManager(__envKey__, ROOT, globalSetting.modes)

    def redo(self):
        from cores.ConfigManager import ConfigManager
        self.app.dataConfig = ConfigManager(__envKey__, ROOT, globalSetting.modes)

class ExitCmd(CmdBase):

    key = 'Exit'

    def __init__(self, app):
        super(ExitCmd, self).__init__(app)

        self.task = self.app.exitEvent

    def run(self):
        return self.task()

class DarkCmd(CmdBase):

    key = 'dark'

    def __init__(self, app):
        super(DarkCmd, self).__init__(app)

        self.task = self.app.setStyleSheet
        self.prevStyle = self.app.styleSheet()

    def run(self):
        return self.task(self.key)

    def undo(self):
        return self.task(self.prevStyle)

    def redo(self):
        return self.task(self.key)

class BrightCmnd(CmdBase):

    key = 'bright'

    def __init__(self, app):
        super(BrightCmnd, self).__init__(app)

        self.task = self.app.setStyleSheet
        self.prevStyle = self.app.styleSheet()

    def run(self):
        return self.task(self.key)

    def undo(self):
        return self.task(self.prevStyle)

    def redo(self):
        return self.task(self.key)

class ChacoalCmd(CmdBase):

    key = 'chacoal'

    def __init__(self, app):
        super(ChacoalCmd, self).__init__(app)

        self.task = self.app.setStyleSheet
        self.prevStyle = self.app.styleSheet()

    def run(self):
        return self.task(self.key)

    def undo(self):
        return self.task(self.prevStyle)

    def redo(self):
        return self.task(self.key)

class NukerCmd(CmdBase):
    key = 'nuker'

    def __init__(self, app):
        super(NukerCmd, self).__init__(app)

        self.task = self.app.setStyleSheet
        self.prevStyle = self.app.styleSheet()

    def run(self):
        return self.task(self.key)

    def undo(self):
        return self.task(self.prevStyle)

    def redo(self):
        return self.task(self.key)

class ShowallCmd(CmdBase):

    key = 'showallevent'

    def __init__(self, app):
        super(ShowallCmd, self).__init__(app)

        self.task = self.app.showAllEvent

    def run(self):
        self.task()

class HideallCmd(CmdBase):

    key = 'hideallevent'

    def __init__(self, app):
        super(HideallCmd, self).__init__(app)

        self.task = self.app.hideAllEvent

    def run(self):
        return self.task()

class SwitchAccCmnd(CmdBase):

    key = 'switchaccountevent'

    def __init__(self, app):
        super(SwitchAccCmnd, self).__init__(app)

        self.task = self.app.switchAccountEvent

    def run(self):
        self.task()

class SignInCmd(CmdBase):

    key = 'signinevent'

    def __init__(self, app):
        super(SignInCmd, self).__init__(app)

        self.task = self.app.signInEvent

    def run(self):
        return self.task()

class SignOutCmd(CmdBase):

    key = 'signoutevent'

    def __init__(self, app):
        super(SignOutCmd, self).__init__(app)

        self.task = self.app.signOutEvent

    def run(self):
        return self.task()

class SignUpCmd(CmdBase):
    key = 'signupevent'

    def __init__(self, app):
        super(SignUpCmd, self).__init__(app)

        self.task = self.app.signUpEvent

    def run(self):
        return self.task()

class ShowLayoutCmd(CmdBase):

    key = 'showlayout'

    def __init__(self, key, app):
        super(ShowLayoutCmd, self).__init__(app)

        if key in self.app.registerLayout.keys():
            if key in self.app.ignoreIDs:
                if not key in self.app.toBuildUis:
                    self.app.logger.report("Commander: '{0}' is not registerred yet.".format(key))
                    self.app.toBuildUis.append(key)
            else:
                self.task = self.app.registryLayout[key]

    def run(self):
        pos = self.task.getValue('pos')
        size = self.task.getValue('size')
        state = self.task.getValue('state')

        if pos:
            self.task.move(pos)
        if size:
            self.task.resize(size)
        if state:
            self.task.setState(state)

        self.task.show()

    def undo(self):
        self.task.setValue('pos', self.task.pos())
        self.task.setValue('size', self.task.size())
        self.task.setValue('state', self.task.state())
        self.task.hide()

    def redo(self):
        return self.run()

class HideLayoutCmd(CmdBase):

    key = 'hidelayout'

    def __init__(self, key, app):
        super(HideLayoutCmd, self).__init__(app)

        if key in self.app.registerLayout.keys():
            if key in self.app.ignoreIDs:
                if not key in self.app.toBuildUis:
                    self.app.logger.report("Commander: '{0}' is not registerred yet.".format(key))
                    self.app.toBuildUis.append(key)
            else:
                self.task = self.app.registryLayout[key]

    def run(self):
        self.task.setValue('pos', self.task.pos())
        self.task.setValue('size', self.task.size())
        self.task.setValue('state', self.task.state())
        self.task.hide()

    def undo(self):
        pos = self.task.getValue('pos')
        size = self.task.getValue('size')
        state = self.task.getValue('state')

        if pos:
            self.task.move(pos)
        if size:
            self.task.resize(size)
        if state:
            self.task.setState(state)

        self.task.show()

    def redo(self):
        return self.run()

class CloseLayoutCmd(CmdBase):

    key = 'closelayout'

    def __init__(self, key, app):
        super(CloseLayoutCmd, self).__init__(app)
        if key in self.app.registryLayout.keys():
            if key in self.app.ignoreIDs:
                if not key in self.app.toBuildUis:
                    self.app.logger.report("Commander: '{0}' is not registerred yet.".format(key))
                    self.app.toBuildUis.append(key)
            else:
                self.task = self.app.registryLayout[key]

    def run(self):
        self.task.setValue('pos', self.task.pos())
        self.task.setValue('size', self.task.size())
        self.task.setValue('state', self.task.state())
        self.task.close()
        self.app.registerLayout.deRegister(self.task)

    def undo(self):
        pos = self.task.getValue('pos')
        size = self.task.getValue('size')
        state = self.task.getValue('state')

        if pos:
            self.task.move(pos)
        if size:
            self.task.resize(size)
        if state:
            self.task.setState(state)

        self.task.show()

    def redo(self):
        return self.run()

class ShowMaximizedCmd(CmdBase):

    key = 'showmaximized'

    def __init__(self, key, app):
        super(ShowMaximizedCmd, self).__init__(app)

        if key in self.app.registryLayout.keys():
            if key in self.app.ignoreIDs:
                if not key in self.app.toBuildUis:
                    self.app.logger.report("Commander: '{0}' is not registerred yet.".format(key))
                    self.app.toBuildUis.append(key)
            else:
                self.task = self.app.registryLayout[key]

    def run(self):

        pos = self.task.getValue('pos')
        size = self.task.getValue('size')
        state = self.task.getValue('state')

        if pos:
            self.task.move(pos)
        if size:
            self.task.resize(size)
        if state:
            self.task.setState(state)

        self.task.showMaximized()

    def undo(self):
        self.task.setValue('pos', self.task.pos())
        self.task.setValue('size', self.task.size())
        self.task.setValue('state', self.task.state())
        self.task.hide()

    def redo(self):
        return self.run()

class ShowMinimizedCmd(CmdBase):

    key = 'showminimized'

    def __init__(self, key, app):
        super(ShowMinimizedCmd, self).__init__(app)

        if key in self.app.registryLayout.keys():
            if key in self.app.ignoreIDs:
                if not key in self.app.toBuildUis:
                    self.app.logger.report("Commander: '{0}' is not registerred yet.".format(key))
                    self.app.toBuildUis.append(key)
            else:
                self.task = self.app.registryLayout[key]

    def run(self):
        self.task.setValue('pos', self.task.pos())
        self.task.setValue('size', self.task.size())
        self.task.setValue('state', self.task.state())

        self.task.showMinimized()

    def undo(self):
        pos = self.task.getValue('pos')
        size = self.task.getValue('size')
        state = self.task.getValue('state')

        if pos:
            self.task.move(pos)
        if size:
            self.task.resize(size)
        if state:
            self.task.setState(state)
        self.task.hide()

    def redo(self):
        return self.run()

class ShowRestoreCmd(CmdBase):

    key = 'showrestore'

    def __init__(self, key, app):
        super(ShowRestoreCmd, self).__init__(app)

        if key in self.app.registryLayout.keys():
            if key in self.app.ignoreIDs:
                if not key in self.app.toBuildUis:
                    self.app.logger.report("Commander: '{0}' is not registerred yet.".format(key))
                    self.app.toBuildUis.append(key)
            else:
                self.task = self.app.registryLayout[key]

    def run(self):

        pos = self.task.getValue('pos')
        size = self.task.getValue('size')
        state = self.task.getValue('state')

        if pos:
            self.task.move(pos)
        if size:
            self.task.resize(size)
        if state:
            self.task.setState(state)

        self.task.showRestore()

    def undo(self):
        self.task.setValue('pos', self.task.pos())
        self.task.setValue('size', self.task.size())
        self.task.setValue('state', self.task.state())
        self.task.hide()

    def redo(self):
        return self.run()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/12/2019 - 2:10 PM
# © 2017 - 2018 DAMGteam. All rights reserved