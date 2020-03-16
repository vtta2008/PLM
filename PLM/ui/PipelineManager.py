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
from PLM.configs                        import __homepage__, __appname__, SiPoMin, dockB
from PLM.commons                        import DAMGDICT
from PLM.commons.Widgets                import MainWindow, Widget, GridLayout, ToolBar
from PLM.commons.Gui                    import LogoIcon
from .components                        import ConnectStatus, Footer, MainStatusBar, Notification
from .layouts                           import TopTab, BotTab
from .models                            import ActionManager, ButtonManager
from PLM.utils                          import str2bool, bool2str

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(MainWindow):

    key                                 = 'PipelineManager'
    _name                               = __appname__
    toolBars                            = DAMGDICT()
    menus                               = DAMGDICT()
    _count                              = 0

    mainMenuBar                         = None
    mainToolBar                         = None

    def __init__(self, threadManager, parent=None):
        super(PipelineManager, self).__init__(parent)

        self.url                        = __homepage__
        self.setObjectName(self._name)
        self.setWindowTitle(__appname__)
        self.setWindowIcon(LogoIcon('PLM'))

        self.actionManager              = ActionManager(self)
        self.buttonManager              = ButtonManager(self)
        self.threadManager              = threadManager

        self.mainWidget                 = Widget()
        self.layout                     = GridLayout()
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)

        self.setup_menuBar()
        self.setup_toolBars()
        self.buildUI()

    def buildUI(self):

        self.connectStatus              = ConnectStatus(self)

        self.topTabUI                   = TopTab(self.buttonManager, self)
        self.botTabUI                   = BotTab(self)
        self.notification               = Notification(self.threadManager, self)

        self.footer                     = Footer(self.buttonManager, self.threadManager, self)
        self.statusBar                  = MainStatusBar(self)

        self.layouts =  [self.connectStatus    , self.notification,
                         self.topTabUI   , self.botTabUI         , self.footer           , self.statusBar, ]


        self.layout.addWidget(self.connectStatus, 0, 7, 1, 2)

        self.layout.addWidget(self.topTabUI, 1, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 5, 0, 3, 6)
        self.layout.addWidget(self.notification, 5, 6, 3, 3)

        self.layout.addWidget(self.footer, 8, 0, 1, 9)
        self.setStatusBar(self.statusBar)


    def setup_menuBar(self):

        self.mainMenuBar            = self.menuBar()

        self.appMenu                = self.build_app_menu()
        self.goMenu                 = self.build_goTo_menu()
        self.editMenu               = self.build_edit_menu()
        self.viewMenu               = self.build_view_menu()
        self.officeMenu             = self.build_officceMenu()
        self.toolsMenu              = self.build_toolMenu()
        self.pluginMenu             = self.build_pluins_menu()
        self.libMenu                = self.build_libs_menu()
        self.helpMenu               = self.build_help_menu()

        for menu in [self.appMenu, self.goMenu, self.editMenu, self.viewMenu, self.officeMenu, self.toolsMenu,
                     self.pluginMenu, self.libMenu, self.helpMenu]:
            menu.key                = '{0}_Menu_{1}'.format(self.key, menu.title())
            menu._name              = '{0} Menu {1}'.format(self.key, menu.title())

            self.menus.add(menu.key, menu)

        self.mns                    = [mn for mn in self.menus.values()]

    def setup_toolBars(self):

        self.tdToolBar                  = self.build_toolBar("TD")
        self.preToolBar                 = self.build_toolBar('PRE')
        self.compToolBar                = self.build_toolBar("VFX")
        self.artToolBar                 = self.build_toolBar("ART")
        self.textureToolBar             = self.build_toolBar('TEX')
        self.postToolBar                = self.build_toolBar('POST')
        self.officeToolBar              = self.build_toolBar('MCO')

        self.tbs                        = [tb for tb in self.toolBars.values()]

        for tb in self.tbs:
            tb.settings._settingEnable = True
            state = tb.getValue('visible')
            if state is None:
                tb.setVisible(True)
            else:
                tb.setVisible(str2bool(state))

        self.artToolBar.setVisible(False)
        self.officeToolBar.setVisible(False)

        self.updateWidth()

    def build_toolBar(self, name=''):

        toolBar = ToolBar(self)
        toolBar.key = '{0}_{1}'.format(self.key, name)
        toolBar._name = toolBar.key
        toolBar.setWindowTitle(name)

        actions = self.getActions(name)

        for action in actions:
            toolBar.add_action(action)

        toolBar.setSizePolicy(SiPoMin, SiPoMin)
        toolBar.visibilityChanged.connect(self.updateWidth)
        self.toolBars[name] = toolBar
        self.addToolBar(toolBar)
        return toolBar

    def build_app_menu(self):
        menu                        = self.mainMenuBar.addMenu("&App")
        actions                     = self.actionManager.appMenuActions(self.parent)
        self.add_actions_to_menu(menu, actions[0:3])
        menu.addSeparator()
        self.add_actions_to_menu(menu, actions[3:7])
        menu.addSeparator()
        self.add_actions_to_menu(menu, actions[7:])
        return menu

    def build_goTo_menu(self):
        menu                        = self.mainMenuBar.addMenu('&Go To')
        actions                     = self.actionManger.goMenuActions(self.parent)
        self.add_actions_to_menu(menu, actions)
        return menu

    def build_edit_menu(self):
        menu                        = self.addMenu('&Edit')
        editActions                 = self.actionManger.editMenuActions(self.parent)
        self.add_actions_to_menu(menu, editActions)
        return menu

    def build_view_menu(self):
        menu                        = self.addMenu('&View')

        self.stylesheetMenu         = menu.addMenu('&Stylesheet')
        stylesheetActions           = self.actionManger.stylesheetMenuActions(self.parent)
        self.add_actions_to_menu(self.stylesheetMenu, stylesheetActions)

        viewActions                 = self.actionManger.viewMenuActions(self.parent)
        self.add_actions_to_menu(menu, viewActions)
        return menu

    def build_officceMenu(self):
        menu                        = self.mainMenuBar.addMenu("&Office")
        action                      = self.actionManger.officeMenuActions(self.parent)
        self.add_actions_to_menu(menu, action)
        return menu


    def build_pluins_menu(self):
        menu                        = self.addMenu("&Plug-ins")
        actions                     = self.actionManger.pluginMenuActions(self.parent)
        self.add_actions_to_menu(menu, actions)
        return menu

    def build_toolMenu(self):
        menu                        = self.addMenu("&Tools")
        actions                     = self.actionManger.toolsMenuActions(self.parent)
        self.add_actions_to_menu(menu, actions[0:8])
        menu.addSeparator()
        self.add_actions_to_menu(menu, actions[8:11])
        menu.addSeparator()
        self.add_actions_to_menu(menu, actions[11:])
        return menu

    def build_libs_menu(self):
        menu                        = self.addMenu("&Libs")
        actions                     = self.actionManger.libMenuActions(self.parent)
        self.add_actions_to_menu(menu, actions)
        return menu

    def build_help_menu(self):
        menu                        = self.addMenu("&Help")
        actions                     = self.actionManger.helpMenuActions(self.parent)
        self.add_actions_to_menu(menu, actions[0:2])
        menu.addSeparator()
        self.add_actions_to_menu(menu, actions[2:5])
        menu.addSeparator()
        self.add_actions_to_menu(menu, actions[5:7])
        menu.addSeparator()
        self.add_actions_to_menu(menu, actions[7:])
        return menu

    def getActions(self, title):
        if title == 'TD':
            actions = self.actionManager.tdToolBarActions(self)
        elif title == 'PRE':
            actions = self.actionManager.preToolbarActions(self)
        elif title == 'VFX':
            actions = self.actionManager.vfxToolBarActions(self)
        elif title == 'ART':
            actions = self.actionManager.artToolBarActions(self)
        elif title == 'TEX':
            actions = self.actionManager.texToolBarActions(self)
        elif title == 'POST':
            actions = self.actionManager.postToolBarActions(self)
        elif title == 'MCO':
            actions = self.actionManager.officeMenuActions(self)
        else:
            print('WindowTitleError: There is no toolBar name: {0}'.format(title))
            actions = self.actionManager.extraToolActions(self)

        return actions

    def show_toolBar(self, toolbar, mode):
        if toolbar in self.toolBars.keys():
            tb = self.toolBars[toolbar]
            tb.setVisible(str2bool(mode))
            self.settings.initSetValue('visible', bool2str(mode), tb.key)
        else:
            for tb in self.toolBars.values():
                tb.setVisible(str2bool(mode))
                self.settings.iniSetValue('visible', bool2str(mode), tb.key)

    def add_actions_to_menu(self, menu, actions):
        for action in actions:
            menu.addAction(action)

    def add_dockWidget(self, dock, pos=dockB):

        dock.signals.showLayout.connect(self.signals.showLayout)
        dock.signals.setSetting.connect(self.signals.setSetting)
        dock.signals.executing.connect(self.signals.executing)
        dock.signals.regisLayout.connect(self.signals.regisLayout)
        dock.signals.openBrowser.connect(self.signals.openBrowser)

        self.addDockWidget(pos, dock)

    def updateWidth(self):
        i = 0
        for tb in self.tbs:
            if tb.isVisible():
                i += 1

        w = i*32
        print(i, w)
        self.setMinimumWidth(w)


    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val):
        self._count = val

    @property
    def mode(self):
        return self.connectStatus.mode

# -------------------------------------------------------------------------------------------------------------