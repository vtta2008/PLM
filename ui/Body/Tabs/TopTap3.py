# -*- coding: utf-8 -*-
"""

Script Name: QTerminal2.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

""" Import """

# Python
import os, shlex, getpass, socket

# PyQt5
from PyQt5.QtCore                       import QSysInfo, QStandardPaths, Qt, QEvent
from PyQt5.QtGui                        import QTextCursor


# PLM
from bin                                import DAMGLIST
from appData                            import SCROLLBAROFF, NO_WRAP
from devkit.Widgets                     import Widget, PlainTextEdit, ShortCut, VBoxLayout, StatusBar
from devkit.Core                        import Process

class TopTap3(Widget):

    key                                 = 'TerminalLayout'
    _name                               = 'TerminalLayout'

    commands                            = DAMGLIST()
    shotcuts                            = DAMGLIST()
    tracker                             = 0
    _cwd                                = os.getcwd().replace('\\', '/')
    _user                               = getpass.getuser()
    _host                               = socket.gethostname()

    def __init__(self, buttonManager, parent=None):
        super(TopTap3, self).__init__(parent)

        self.buttonManager = buttonManager
        self.parent = parent

        self.layout = VBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.setStyleSheet(mystylesheet(self))

    def buildUI(self):
        self.process                    = Process(self.dataReady, self.onError, self.onOutput, self.isFinished, self)
        self.cmdField                   = PlainTextEdit({'lwm': NO_WRAP, 'sfh': 25, 'vsbp': SCROLLBAROFF, 'adr': True})
        self.textWindow                 = PlainTextEdit({'rol': True}, self)
        self.cursor                     = self.cmdField.textCursor()
        self.copySelectedTextAction     = ShortCut('Copy', 'Copy', 'Shift+Ctrl+c', self.copyText, self)
        self.cancelAction               = ShortCut('Cancel', 'Cancel', 'Ctrl+c', self.killProcess, self)
        self.pasteTextAction            = ShortCut('Paste', 'Paste', 'Shift+Ctrl+v', self.pasteText, self)

        self.textWindow.addActions([self.cancelAction, self.copySelectedTextAction])
        self.cmdField.addAction(self.pasteTextAction)
        self.cmdField.installEventFilter(self)
        self.cursorEnd()

        sysinfo                         = QSysInfo()
        myMachine                       = "CPU Architecture: {0}***{1}***{2}***{3}".format(
                                                                                        sysinfo.currentCpuArchitecture(),
                                                                                        sysinfo.prettyProductName(),
                                                                                        sysinfo.kernelType(),
                                                                                        sysinfo.kernelVersion()
                                                                                            )
        self.statusBar = StatusBar(self)
        self.statusBar.showMessage(myMachine, 0)
        self.layout.addWidget(self.textWindow)
        self.layout.addWidget(self.cmdField)
        self.layout.addWidget(self.statusBar)

    def getUsername(self):
        return "{0}@{1}:{2}$".format(self._user, self._host, self._cwd)

    def cursorEnd(self):
        self.cmdField.setPlainText(self.getUsername())
        self.cursor.movePosition(11, 0)
        self.cmdField.setTextCursor(self.cursor)
        self.cmdField.setFocus()

    def eventFilter(self, source, event):
        if source == self.cmdField:
            if (event.type() == QEvent.DragEnter):
                event.accept()
                return True
            elif (event.type() == QEvent.Drop):
                # print('Drop')
                self.setDropEvent(event)
                return True
            elif (event.type() == QEvent.KeyPress):
                cursor = self.cmdField.textCursor()
                # print('key press:', (event.key(), event.text()))
                if event.key() == Qt.Key_Backspace:
                    if cursor.positionInBlock() <= len(self.getUsername()):
                        return True
                    else:
                        return False

                elif event.key() == Qt.Key_Return:
                    self.run()
                    return True

                elif event.key() == Qt.Key_Left:
                    if cursor.positionInBlock() <= len(self.getUsername()):
                        return True
                    else:
                        return False

                elif event.key() == Qt.Key_Delete:
                    if cursor.positionInBlock() <= len(self.getUsername()) - 1:
                        return True
                    else:
                        return False

                elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
                    self.killProcess()
                    return True

                elif event.key() == Qt.Key_Up:
                    try:
                        if self.tracker != 0:
                            cursor.select(QTextCursor.BlockUnderCursor)
                            cursor.removeSelectedText()
                            self.cmdField.appendPlainText(self.getUsername())

                        self.cmdField.insertPlainText(self.commands[self.tracker])
                        self.tracker -= 1

                    except IndexError:
                        self.tracker = 0
                    return True

                elif event.key() == Qt.Key_Down:
                    try:
                        if self.tracker != 0:
                            cursor.select(QTextCursor.BlockUnderCursor)
                            cursor.removeSelectedText()
                            self.cmdField.appendPlainText(self.getUsername())

                        self.cmdField.insertPlainText(self.commands[self.tracker])
                        self.tracker += 1

                    except IndexError:
                        self.tracker = 0
                    return True

                else:
                    return False
            else:
                return False
        else:
            return False

    def copyText(self):
        self.textWindow.copy()

    def pasteText(self):
        self.cmdField.paste()

    def killProcess(self):
        # print("cancelled")
        self.process.kill()
        self.textWindow.appendPlainText("cancelled")
        self.cursorEnd()

    def setDropEvent(self, event):
        self.cmdField.setFocus()
        if event.mimeData().hasUrls():
            f = str(event.mimeData().urls()[0].toLocalFile())
            # print("is file:", f)
            if " " in f:
                self.cmdField.insertPlainText("'{}'".format(f))
            else:
                self.cmdField.insertPlainText(f)
            event.accept()
        elif event.mimeData().hasText():
            ft = event.mimeData().text()
            # print("is text:", ft)
            if " " in ft:
                self.cmdField.insertPlainText("'{}'".format(ft))
            else:
                self.cmdField.insertPlainText(ft)
        else:
            event.ignore()

    def run(self):

        self.textWindow.setFocus()
        self.textWindow.appendPlainText(self.cmdField.toPlainText())
        cli = shlex.split(self.cmdField.toPlainText().replace(self.getUsername(), '').replace("'", '"'), posix=False)
        cmd = str(cli[0])  ### is the executable

        if cmd == "exit":
            quit()
        elif 'cd' in cmd:
            if len(cli) == 1:
                command_argument = cmd.split('cd')[1]
            else:
                command_argument = cli[1]

            if cmd == 'cd' or cmd == 'cd.':
                if len(cli) == 1:
                    pass
                else:
                    if os.path.isdir(command_argument):
                        # print('{0} is dir'.format(command_argument))
                        check = True
                        for char in command_argument:
                            if not char == '.':
                                check = False
                                break
                        if not check:
                            pth = os.path.join(self._cwd, command_argument)
                            if os.path.exists(pth):
                                self._cwd = pth
                            else:
                                self.command_not_found(cmd)
                        else:
                            # print('{0} is not dir'.format(command_argument))
                            pass
                    else:
                        if os.path.exists(command_argument):
                            # print('{0} is path'.format(command_argument))
                            self._cwd = command_argument
                        else:
                            # print('{0} is path but not exists'.format(command_argument))
                            pth = os.path.join(self._cwd, command_argument)
                            # print(pth, self._cwd)
                            if os.path.exists(pth):
                                self._cwd = pth
                            else:
                                self.command_not_found(cmd)
            else:
                if len(command_argument) <= 1:
                    if command_argument == '/' or command_argument == '\\':
                        self._cwd = os.path.splitdrive(self._cwd)[0] + '/'
                    else:
                        self.command_not_found()
                elif len(command_argument) >= 2:
                    if command_argument[0:2] == '..':
                        check = True
                        for char in command_argument:
                            if not char == '.':
                                check = False
                        if check:
                            for i in range(len(command_argument)-1):
                                self._cwd = os.path.dirname(self._cwd)
                        else:
                            self.command_not_found(cmd)
                    else:
                        self.command_not_found(cmd)
                else:
                    self.command_not_found(cmd)

            self.updateWorkingDirectory(self._cwd)
        else:
            if (QStandardPaths.findExecutable(cmd)):
                self.commands.append(self.cmdField.toPlainText().replace(self.getUsername(), ""))
                # print("command", cmd, "found")
                t = " ".join(cli)
                if self.process.state() != 2:
                    self.process.waitForStarted()
                    self.process.waitForFinished()
                    if "|" in t or ">" in t or "<" in t:
                        # print("special characters")
                        self.process.start('sh -c "' + cmd + ' ' + t + '"')
                        # print("running", ('sh -c "' + cmd + ' ' + t + '"'))
                    else:
                        self.process.start(cmd + " " + t)
                        # print("running", (cmd + " " + t))
            else:
                self.command_not_found(cmd)

    def command_not_found(self, cmd):
        self.textWindow.appendPlainText("command not found: {0}".format(cmd))
        self.cursorEnd()

    def dataReady(self):
        try:
            out = str(self.process.readAll(), encoding='utf8').rstrip()
        except TypeError:
            out = str(self.process.readAll()).rstrip()
            self.textWindow.moveCursor(self.cursor.Start)  ### changed
        self.textWindow.appendPlainText(out)

    def onError(self):
        self.error = self.process.readAllStandardError().data().decode()
        self.textWindow.appendPlainText(self.error.strip('\n'))
        self.cursorEnd()

    def onOutput(self):
        self.result = self.process.readAllStandardOutput().data().decode()
        self.textWindow.appendPlainText(self.result.strip('\n'))
        self.cursorEnd()
        self.state = self.process.state()
        # print(self.state)

    def isFinished(self):
        # print("finished")
        self.cmdField.setPlainText(self.getUsername())
        self.cursorEnd()

    def updateWorkingDirectory(self, pth=os.getcwd()):
        # print('Working Dir: {0}'.format(pth))
        fixName = os.path.basename(pth)
        fixPath = os.path.dirname(pth)
        self._cwd = os.path.join(fixPath, fixName).replace('\\', '/')
        self.process.setWorkingDirectory(self._cwd)
        self.cursorEnd()
            

def mystylesheet(self):
    return """
QMainWindow{
background-color: #212121; }
QMainWindow:title
{
background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);
color: #3465a4;
}
QPlainTextEdit
 {font-family: Noto Sans Mono; 
font-size: 8pt; 
background-color: #212121; 
color: #f3f3f3; padding: 2; 
border: none;}
QPlainTextEdit:focus { 
border: none; }
QScrollBar {            
border: 1px solid #2e3436;
background: #292929;
width:8px;
height: 8px;
margin: 0px 0px 0px 0px;
}
QScrollBar::handle {
background: #2e3436;
min-height: 0px;
min-width: 0px;
}
QScrollBar::add-line {
background: #2e3436;
height: 0px;
width: 0px;
subcontrol-position: bottom;
subcontrol-origin: margin;
}
QScrollBar::sub-line {
background: #2e3436;
height: 0px;
width: 0px;
subcontrol-position: top;
subcontrol-origin: margin;
}
QStatusBar {
font-family: Noto Sans Mono; 
font-size: 7pt; 
color: #729fcf;}
"""

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved