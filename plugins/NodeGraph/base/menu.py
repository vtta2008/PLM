#!/usr/bin/python

from distutils.version                  import LooseVersion

from plugins.NodeGraph                  import QtGui, QtCore
from cores.Errors                       import NodeMenuError
from plugins.NodeGraph.widgets.actions  import BaseMenu, GraphAction, NodeAction

class NodeGraphMenu(object):

    def __init__(self, graph, qmenu):
        self._graph                     = graph
        self._qmenu                     = qmenu

    def __repr__(self):
        return '<{}("{}") object at {}>'.format(
            self.__class__.__name__, self.name(), hex(id(self)))

    @property
    def qmenu(self):
        return self._qmenu

    def name(self):
        return self.qmenu.title()

    def get_menu(self, name):
        menu = self.qmenu.get_menu(name)
        if menu:
            return NodeGraphMenu(self._graph, menu)

    def get_command(self, name):
        for action in self.qmenu.actions():
            if not action.menu() and action.text() == name:
                return NodeGraphCommand(self._graph, action)

    def all_commands(self):
        def get_actions(menu):
            actions = []
            for action in menu.actions():
                if not action.menu():
                    if not action.isSeparator():
                        actions.append(action)
                else:
                    actions += get_actions(action.menu())
            return actions
        child_actions = get_actions(self.qmenu)
        return [NodeGraphCommand(self._graph, a) for a in child_actions]

    def add_menu(self, name):
        menu = BaseMenu(name, self.qmenu)
        self.qmenu.addMenu(menu)
        return NodeGraphMenu(self._graph, menu)

    def add_command(self, name, func=None, shortcut=None):
        action = GraphAction(name, self._graph.viewer())
        action.graph = self._graph
        if LooseVersion(QtCore.qVersion()) >= LooseVersion('5.10'):
            action.setShortcutVisibleInContextMenu(True)
        if shortcut:
            action.setShortcut(shortcut)
        if func:
            action.executed.connect(func)
        qaction = self.qmenu.addAction(action)
        return NodeGraphCommand(self._graph, qaction)

    def add_separator(self):
        self.qmenu.addSeparator()


class NodesMenu(NodeGraphMenu):

    def add_command(self, name, func=None, node_type=None):
        if not node_type:
            raise NodeMenuError('Node type not specified!')

        node_menu = self.qmenu.get_menu(node_type)
        if not node_menu:
            node_menu = BaseMenu(node_type, self.qmenu)
            self.qmenu.addMenu(node_menu)

        if not self.qmenu.isEnabled():
            self.qmenu.setDisabled(False)

        action = NodeAction(name, self._graph.viewer())
        action.graph = self._graph
        if LooseVersion(QtCore.qVersion()) >= LooseVersion('5.10'):
            action.setShortcutVisibleInContextMenu(True)
        if func:
            action.executed.connect(func)
        qaction = node_menu.addAction(action)
        return NodeGraphCommand(self._graph, qaction)


class NodeGraphCommand(object):

    def __init__(self, graph, qaction):
        self._graph = graph
        self._qaction = qaction

    def __repr__(self):
        return '<{}("{}") object at {}>'.format(
            self.__class__.__name__, self.name(), hex(id(self)))

    @property
    def qaction(self):
        return self._qaction

    def name(self):
        return self.qaction.text()

    def set_shortcut(self, shortcut=None):
        shortcut = shortcut or QtGui.QKeySequence()
        self.qaction.setShortcut(shortcut)

    def run_command(self):
        self.qaction.trigger()
