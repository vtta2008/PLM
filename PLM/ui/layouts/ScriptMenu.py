# -*- coding: utf-8 -*-
"""

Script Name: ScriptMenu.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from collections                import defaultdict
import os

from PyQt5.QtCore               import pyqtSignal
from PyQt5.QtWidgets            import QApplication

from PLM.cores import Loggers
from PLM.ui.framework.Widgets import Menu, WidgetAction, Action, LineEdit
from PLM.ui.framework.Gui import Icon


class ScriptAction(Action):

    _root                 = None
    _tags                 = list()
    _command              = None
    _sourcetype           = None
    _iconfile             = None
    _label                = None

    _COMMAND              = """        
                            import imp
                            f, filepath, descr = imp.find_module('{module_name}', ['{dirname}'])
                            module = imp.load_module('{module_name}', f, filepath, descr)
                            module.{module_name}()
                            """

    def __init__(self, parent=None):
        Action.__init__(self, parent=parent)



    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        self._command = value

    @property
    def sourcetype(self):
        return self._sourcetype

    @sourcetype.setter
    def sourcetype(self, value):
        self._sourcetype = value

    @property
    def iconfile(self):
        return self._iconfile

    @iconfile.setter
    def iconfile(self, value):
        self._iconfile = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    def run_command(self):
        app = QApplication.instance()
        modifiers = app.keyboardModifiers()

        registered = self._root.registered_callbacks
        callbacks = registered.get(int(modifiers), [])
        for callback in callbacks:
            signal = callback(self)
            if signal != 0:
                return

        exec(self.process_command())

    def process_command(self):
        if self._sourcetype == "python":
            return self._command

        if self._sourcetype == "mel":
            # Escape single quotes
            conversion = self._command.replace("'", "\\'")
            return "import maya; maya.mel.eval('{}')".format(conversion)

        if self._sourcetype == "file":
            if os.path.isabs(self._command):
                filepath = self._command
            else:
                filepath = os.path.normpath(os.path.expandvars(self._command))

            return self._wrap_filepath(filepath)

    def has_tag(self, tag):
        for tagitem in self.tags:
            if tag not in tagitem:
                continue
            return True
        return False

    def _wrap_filepath(self, file_path):
        dirname = os.path.dirname(r"{}".format(file_path))
        dirpath = dirname.replace("\\", "/")
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        return self._COMMAND.format(module_name=module_name, dirname=dirpath)


class ScriptsMenu(Menu):

    key                         = 'ScriptsMenu'
    updated                     = pyqtSignal(Menu)

    searchbar                   = None
    update_action               = None
    _script_actions             = []
    _callbacks                  = defaultdict(list)

    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.logger             = Loggers(__name__)

        parent                  = kwargs.get("parent", None)            # Automatically add it to the parent menu
        if parent:
            parent.addMenu(self)
        objectname              = kwargs.get("objectName", "scripts")
        title                   = kwargs.get("title", "Scripts")

        self.setObjectName(objectname)
        self.setTitle(title)
        self.create_default_items()

    def on_update(self):
        self.updated.emit(self)

    @property
    def registered_callbacks(self):
        return self._callbacks.copy()

    def create_default_items(self):
        searchbar                   = LineEdit()
        searchbar.setFixedWidth(120)
        searchbar.setPlaceholderText("Search ...")
        searchbar.textChanged.connect(self._update_search)
        self.searchbar              = searchbar

        searchbar_action            = WidgetAction(parent=self)                             # create widget holder
        searchbar_action.setDefaultWidget(self.searchbar)                                   # add widget to widget holder
        searchbar_action.setObjectName("Searchbar")

        update_action               = Action({'txt': 'Update Scripts', 'son': 'Update Scripts', 'vsb': False}, self)      # add update button and link function
        update_action.triggered.connect(self.on_update)
        self.update_action          = update_action

        self.addAction(searchbar_action)                                                    # add action to menu
        self.addAction(update_action)
        separator = self.addSeparator()                                                     # add separator object
        separator.setObjectName("separator")

    def add_menu(self, title, parent=None):
        if not parent:
            parent = self
        menu = Menu(parent, title)
        menu.setTitle(title)
        menu.setObjectName(title)
        menu.setTearOffEnabled(True)
        parent.addMenu(menu)
        return menu

    def add_script(self, parent, title, command, sourcetype, icon=None, tags=None, label=None, tooltip=None):

        assert tags is None or isinstance(tags, (list, tuple))

        tags = list() if tags is None else list(tags)       # Ensure tags is a list
        tags.append(title.lower())

        assert icon is None or isinstance(icon, str), ("Invalid data type for icon, supported : None, string")


        script_action = ScriptAction(parent)               # create new action
        script_action.setText(title)
        script_action.setObjectName(title)
        script_action.tags = tags

        script_action.root          = self                  # link action to root for callback library
        script_action.sourcetype    = sourcetype            # Set up the command
        script_action.command       = command

        try:
            script_action.process_command()
        except RuntimeError as e:
            raise RuntimeError("Script action can't be processed: {}".format(e))

        if icon:
            iconfile                = os.path.expandvars(icon)
            script_action.iconfile  = iconfile
            script_action_icon      = Icon(iconfile)
            script_action.setIcon(script_action_icon)

        if label:
            script_action.label     = label

        if tooltip:
            script_action.setStatusTip(tooltip)

        script_action.triggered.connect(script_action.run_command)
        parent.addAction(script_action)

        self._script_actions.append(script_action)          # Add to our searchable actions
        return script_action

    def build_from_configuration(self, parent, configuration):
        for item in configuration:
            assert isinstance(item, dict), "Configuration is wrong!"
            item_type               = item.get('type', None)               # skip items which have no `type` key
            if not item_type:
                self.logger.warning("Missing 'type' from configuration item")
                continue

            if item_type == "separator":                                # add separator, Special behavior for separators
                parent.addSeparator()
            elif item_type == "menu":                                   # add submenu, items should hold a collection of submenu items (dict)
                assert "items" in item, "Menu is missing 'items' key"
                menu                = self.add_menu(parent=parent, title=item["title"])
                self.build_from_configuration(menu, item["items"])
            elif item_type == "action":                                 # add script, filter out `type` from the item dict
                config = {key: value for key, value in
                          item.items() if key != "type"}
                self.add_script(parent=parent, **config)

    def set_update_visible(self, state):
        self.update_action.setVisible(state)

    def clear_menu(self):
        for _action in self.actions()[3:]:
            self.removeAction(_action)

    def register_callback(self, modifiers, callback):
        self._callbacks[modifiers].append(callback)

    def _update_search(self, search):
        if not search:
            for action in self._script_actions:
                action.setVisible(True)
        else:
            for action in self._script_actions:
                if not action.has_tag(search.lower()):
                    action.setVisible(False)

        # Set visibility for all submenus
        for action in self.actions():
            if not action.menu():
                continue

            menu = action.menu()
            visible = any(action.isVisible() for action in menu.actions())
            action.setVisible(visible)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 6:05 PM
# © 2017 - 2018 DAMGteam. All rights reserved