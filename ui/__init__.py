# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

# from ui.AppToolbar.MainToolBar          import MainToolBar
# from ui.AppToolbar.DockToolBar          import DockToolBar
# from ui.Funcs.ForgotPassword            import ForgotPassword
# from ui.Funcs.SignIn                    import SignIn
# from ui.Funcs.SignUp                    import SignUp
# from ui.Info.About                      import About
# from ui.Info.CodeConduct                import CodeConduct
# from ui.Info.Credit                     import Credit
# from ui.Info.Contributing               import Contributing
# from ui.Info.LicenceMIT                 import LicenceMIT
# from ui.Info.Reference                  import Reference
# from ui.Info.Version                    import Version
# from ui.Menus.MainMenuBar               import MainMenuBar
# from ui.Menus.SubMenuBar                import SubMenuBar
# from ui.Menus.config.Preferences        import Preferences
# from ui.Menus.config.Configuration      import Configuration
# from ui.Network.ServerConfig            import ServerConfig
# from ui.Network.ConnectStatus           import ConnectStatus
# from ui.NodeGraph.NodeGraph             import NodeGraph
# from ui.Projects.NewProject             import NewProject
# from ui.Settings.SettingUI              import SettingUI
# from ui.Settings.UserSetting            import UserSetting
# from ui.Tools.Calculator                import Calculator
# from ui.Tools.Calendar                  import Calendar
# from ui.Tools.EnglishDictionary         import EnglishDictionary
# from ui.Tools.FindFiles                 import FindFiles
# from ui.Tools.ImageViewer               import ImageViewer
# from ui.Tools.NoteReminder              import NoteReminder
# from ui.Tools.Screenshot                import Screenshot
# from ui.Tools.TextEditor.TextEditor     import TextEditor
# from ui.Web.PLMBrowser                  import PLMBrowser
# from ui.Debugger                        import Debugger
# from ui.Footer                          import Footer
# from ui.GeneralSetting                  import GeneralSetting
# from ui.StatusBar                       import StatusBar
# from ui.SysTray                         import SysTray
# from ui.TopTab1                         import TopTab1
# from ui.TopTab2                         import TopTab2
# from ui.TopTab3                         import TopTab3
# from ui.TopTab4                         import TopTab4
# from ui.TopTab5                         import TopTab5