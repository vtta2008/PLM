# -*- coding: utf-8 -*-
"""
Script Name: PipelineTool.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This is main UI of PipelineTool.
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM                                import __homepage__, __appName__
from pyPLM.damg                         import DAMGDICT
from pyPLM.Widgets                      import MainWindow, Widget, GridLayout
from pyPLM.Gui                          import LogoIcon

from .components                        import MainStatusBar, MidTab, BotTab, MainHeader
from .models                            import ButtonManager, ActionManager
from PLM.cores                          import ThreadManager

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(MainWindow):

    key                                 = 'PipelineManager'
    _name                               = __appName__
    toolBars                            = DAMGDICT()
    menus                               = DAMGDICT()
    _count                              = 0

    def __init__(self, parent=None):
        super(PipelineManager, self).__init__(parent)

        self.url                        = __homepage__
        self.setObjectName(self.name)
        self.setWindowTitle(self.name)
        self.setWindowIcon(LogoIcon('PLM'))

        self.actionManager              = ActionManager(self.parent)
        self.buttonManager              = ButtonManager(self.parent)
        self.threadManager              = ThreadManager(self.parent)

        self.mainWidget                 = Widget()
        self.layout                     = GridLayout()
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)

        self.buildUI()

    def buildUI(self):

        self.header                     = MainHeader(self.parent)
        self.body                       = MidTab(self.buttonManager, self)
        self.footer                     = BotTab(self)
        self.statusBar                  = MainStatusBar(self)

        self.menus                      = self.header.menuBar.menus
        self.toolBars                   = self.header.toolBar.toolBars
        self.mns                        = self.header.menuBar.mns
        self.tbs                        = self.header.toolBar.tbs
        self.updating                   = self.header.connectStatus.updating
        self.server                     = self.header.connectStatus.server
        self.connectServer              = self.header.connectStatus.connectServer
        self.connectInternet            = self.header.connectStatus.connectInternet

        self.layouts                    = [self.header, self.body, self.footer, self.statusBar]

        self.layout.addWidget(self.header, 0, 0, 2, 9)
        self.layout.addWidget(self.body, 2, 0, 8, 9)
        self.layout.addWidget(self.footer, 10, 0, 6, 9)
        self.setStatusBar(self.statusBar)

        self.body.setFixedHeight(400)
        self.updateSize()

    def resizeEvent(self, event):
        self.updateSize()
        # print('header: {0}, body: {1}, footer: {2}'.format(self.header.height(), self.body.height(), self.footer.height()))
        super(PipelineManager, self).resizeEvent(event)

    def updateSize(self):
        bodySize = self.body.size()
        baseW = bodySize.width()
        baseH = bodySize.height()

        self.header.resize(baseW, baseH / 4)
        self.footer.resize(baseW, baseH * 3 / 4)

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val):
        self._count = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGTEAM. All rights reserved