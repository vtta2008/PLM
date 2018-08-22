# -*- coding: utf-8 -*-
"""

Script Name: Handlers.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import re

from PyQt5.QtWidgets import QUndoCommand

from __rc__.element import DError
from __rc__.element import DObj
from core.Loggers import Loggers
logger = Loggers
report = logger.report

class AuthorityError(DError):
    pass

class IsADirectoryError(DError):
    pass

class FileNotFoundError(DError):
    pass

class DropException(DError):
    pass

class MetaValueError(DError):
    pass

class FormatSettingError(DError):
    pass

class PathSettingError(DError):
    pass

class KeySettingError(DError):
    pass

class ScopeSettingError(DError):
    pass

class QtNodesError(DError):
    """Base custom exception."""
    pass

class UnregisteredNodeClassError(DError):
    """The Node class is not registered."""
    pass

class UnknownFlowError(DError):
    """The flow style can not be recognized."""
    pass

class KnobConnectionError(DError):
    """Something went wrong while trying to connect two Knobs."""
    pass

class DuplicateKnobNameError(DError):
    """A Node's Knobs must have unique names."""
    pass

class StandardError(DError):
    pass

class SettingError(DError):
    pass


class InvalidSlot(DError):
    """Slot is not longer valid"""
    pass

class NotRregisteredSignal(DError):
    """Signal not registered in factory beforehand"""
    pass

class DockerException(DError):
    pass


class Errors(DError):

    def AuthorityError(self):
        return AuthorityError()

    def IsADirectoryError(self):
        return IsADirectoryError()

    def FileNotFoundError(self):
        return FileNotFoundError()

    def DropException(self):
        return DropException()

    def MetaValueError(self):
        return MetaValueError()

    def FormatSettingError(self):
        return FormatSettingError()

    def PathSettingError(self):
        return PathSettingError()

    def KeySettingError(self):
        return KeySettingError()

    def ScopeSettingError(self):
        return ScopeSettingError

    def UnregisteredNodeClassError(self):
        return UnregisteredNodeClassError()

    def UnknownFlowError(self):
        return UnknownFlowError()

    def KnobConnectionError(self):
        return KnobConnectionError()

    def DuplicateKnobNameError(self):
        return DuplicateKnobNameError()

    def StandardError(self):
        return StandardError()

    def SettingError(self):
        return SettingError

    def InvalidSlot(self):
        return InvalidSlot()

    def NotRregisteredSignal(self):
        return NotRregisteredSignal()

    def DockerException(self):
        return DockerException()

class EventHandler(DObj):

    def __init__(self, sender):

        self.callbacks = []
        self.sender = sender
        self.blocked = False

    def __call__(self, *args, **kwargs):
        if not self.blocked:
            return [callback(self.sender, *args, **kwargs) for callback in self.callbacks]
        return []

    def __iadd__(self, callback):
        self.add(callback)
        return self

    def __isub__(self, callback):
        self.remove(callback)
        return self

    def __len__(self):
        return len(self.callbacks)

    def __getitem__(self, index):
        return self.callbacks[index]

    def __setitem__(self, index, value):
        self.callbacks[index] = value

    def __delitem__(self, index):
        del self.callbacks[index]

    def blockSignals(self, block):
        self.blocked = block

    def add(self, callback):
        if not callable(callback):
            raise TypeError("callback must be callable")
        self.callbacks.append(callback)

    def remove(self, callback):
        self.callbacks.remove(callback)

class SceneNodesCommand(QUndoCommand):

    def __init__(self, old, new, scene, msg=None, parent=None):
        QUndoCommand.__init__(self, parent)

        self.restored = True
        self.scene = scene

        self.data_old = old
        self.data_new = new

        self.diff = DictDiffer(old, new)
        self.setText(self.diff.output())

        # set the current undo view message
        if msg is not None:
            self.setText(msg)

    def id(self):
        return (0xAC00 + 0x0002)

    def undo(self):
        self.scene.restoreNodes(self.data_old)

    def redo(self):
        if not self.restored:
            self.scene.restoreNodes(self.data_new)
        self.restored = False

class SceneChangedCommand(QUndoCommand):

    def __init__(self, old, new, scene, msg=None, parent=None):
        QUndoCommand.__init__(self, parent)

        self.restored = True
        self.scene = scene

        self.data_old = old
        self.data_new = new

        self.diff = DictDiffer(old, new)
        self.setText(self.diff.output())

        if msg is not None:
            self.setText(msg)

    def id(self):
        return (0xAC00 + 0x0003)

    def undo(self):
        self.scene.restoreNodes(self.data_old)

    def redo(self):
        if not self.restored:
            self.scene.restoreNodes(self.data_new)
        self.restored = False

class DictDiffer(object):

    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

    def output(self):
        msg = ""
        if self.changed():
            for x in self.changed():
                msg += "%s," % x
            msg = re.sub(",$", "", msg)
            msg += " changed"

        return msg


class SceneEventHandler(DObj):
    def __init__(self, parent=None):
        DObj.__init__(self, parent)

        self.ui = None  # reference to the parent MainWindow
        self.graph = None  # reference to the Graph instance
        self._initialized = False  # indicates the current scene has been read & built

        if parent is not None:
            self.ui = parent.ui
            self.ui.action_evaluate.triggered.connect(self.evaluate)
            self.ui.action_update_graph.triggered.connect(self.graphUpdated)

            if not self.connectGraph(parent):
                report('cannot connect SceneEventHandler to Graph.')

    def updateStatus(self, msg, level='info'):
        self.ui.updateStatus(msg, level=level)

    @property
    def scene(self):
        return self.parent()

    @property
    def view(self):
        return self.ui.view

    @property
    def undo_stack(self):
        return self.ui.undo_stack

    def connectGraph(self, scene):
        if hasattr(scene, 'graph'):
            graph = scene.graph
            if graph.mode == 'standalone':
                self.graph = graph
                self.graph.handler = self

                # connect graph signals
                self.graph.nodesAdded += self.nodesAddedEvent
                self.graph.edgesAdded += self.edgesAddedEvent
                self.graph.graphUpdated += self.graphUpdated
                self.graph.graphAboutToBeSaved += self.graphAboutToBeSaved
                self.graph.graphRefreshed += self.graphAboutToBeSaved

                self.graph.graphRead += self.graphReadEvent

                self.graph.mode = 'ui'
                report('SceneHandler: connecting Graph...')

                # start the autosave timer for 2min (120s x 1000)
                self.ui.autosave_timer.start(30000)
                return True
        return False

    def resetScene(self):

        self.scene.clear()

    def graphReadEvent(self, graph, **kwargs):

        self._initialized = True

        if not self.ui.ignore_scene_prefs:
            self.ui.initializePreferencesPane(**kwargs)
            self.scene.updateScenePreferences(**kwargs)
            for attr, value in kwargs.iteritems():
                if hasattr(self.ui, attr):
                    setattr(self.ui, attr, value)

    def restoreGeometry(self, **kwargs):

        pos = kwargs.pop('pos', (0.0, 0.0))
        scale = kwargs.pop('scale', (1.0, 1.0))

        self.view.resetTransform()
        self.view.centerOn(*pos)
        self.view.scale(*scale)

    def evaluate(self):
        return True

    def nodesAddedEvent(self, graph, ids):

        old_snapshot = self.graph.snapshot()
        self.scene.addNodes(ids)

        new_snapshot = self.graph.snapshot()
        self.undo_stack.push(SceneNodesCommand(old_snapshot, new_snapshot, self.scene, msg='nodes added'))

    def edgesAddedEvent(self, graph, edges):
        old_snapshot = self.graph.snapshot()
        self.scene.addEdges(edges)

        new_snapshot = self.graph.snapshot()
        self.undo_stack.push(SceneNodesCommand(old_snapshot, new_snapshot, self.scene, msg='edges added'))

    def removeSceneNodes(self, nodes):

        old_snapshot = self.graph.snapshot()
        if not nodes:
            report('no nodes specified.')
            return False

        for node in nodes:
            if self.scene:
                if self.scene.is_node(node):
                    dag = node.dagnode
                    nid = dag.id
                    if self.graph.remove_node(nid):
                        report('removing dag node: %s' % nid)
                    node.close()

            if self.scene.is_edge(node):
                if node.ids in self.graph.network.edges():
                    report('removing edge: %s' % str(node.ids))
                    self.graph.remove_edge(*node.ids)
                node.close()

        new_snapshot = self.graph.snapshot()
        self.undo_stack.push(SceneNodesCommand(old_snapshot, new_snapshot, self.scene, msg='nodes deleted'))

    def getInterfacePreferences(self):
        result = dict()
        for attr in self.ui.qsettings.prefs_keys():
            if hasattr(self.ui, attr):
                value = getattr(self.ui, attr)
                result[str(attr)] = value
        return result

    def graphAboutToBeSaved(self, graph):

        result = self.getInterfacePreferences()
        self.graph.updateGraphPreferences(**result)

    def graphUpdated(self, *args):
        widgets_to_remove = []
        for id in self.scene.scenenodes:
            widget = self.scene.scenenodes.get(id)
            if self.scene.is_node(widget):
                if widget.id not in self.graph.network.nodes():
                    widgets_to_remove.append(widget)

            if self.scene.is_edge(widget):
                if widget.ids not in self.graph.network.edges():
                    widgets_to_remove.append(widget)

        for node in widgets_to_remove:
            if self.scene.is_edge(node):
                src_conn = node.source_item
                dest_conn = node.dest_item

                report('# DEBUG: removing edge: {}'.format(node))
                node.close()

            if self.scene.is_node(node):
                report('# DEBUG: removing node: {}'.format(node))
                node.close()

    def dagNodesUpdatedEvent(self, dagnodes):
        if dagnodes:
            print
            '# DEBUG: dag nodes updated: ', [node.name for node in dagnodes]

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/08/2018 - 10:04 PM
# © 2017 - 2018 DAMGteam. All rights reserved