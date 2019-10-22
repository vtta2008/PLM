# -*- coding: utf-8 -*-
"""

Script Name: Handlers.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
from cores import Commands
from cores.Loggers import Loggers
# -------------------------------------------------------------------------------------------------------------
from cores.base import DAMG

logger = Loggers()
log = logger.report

class SceneEventHandler(DAMG):
    def __init__(self, parent=None):
        DAMG.__init__(self, parent)

        self.ui = None  # reference to the parent MainWindow
        self.graph = None  # reference to the Graph instance
        self._initialized = False  # indicates the current scene has been read & built

        if parent is not None:
            self.ui = parent.ui
            self.ui.action_evaluate.triggered.connect(self.evaluate)
            self.ui.action_update_graph.triggered.connect(self.graphUpdated)

            if not self.connectGraph(parent):
                log('cannot connect SceneEventHandler to Graph.')

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
                log.info('SceneHandler: connecting Graph...')

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
        self.undo_stack.push(Commands.SceneNodesCommand(old_snapshot, new_snapshot, self.scene, msg='nodes added'))

    def edgesAddedEvent(self, graph, edges):
        old_snapshot = self.graph.snapshot()
        self.scene.addEdges(edges)

        new_snapshot = self.graph.snapshot()
        self.undo_stack.push(Commands.SceneNodesCommand(old_snapshot, new_snapshot, self.scene, msg='edges added'))

    def removeSceneNodes(self, nodes):

        old_snapshot = self.graph.snapshot()
        if not nodes:
            log('no nodes specified.')
            return False

        for node in nodes:
            if self.scene:
                if self.scene.is_node(node):
                    dag = node.dagnode
                    nid = dag.id
                    if self.graph.remove_node(nid):
                        log.debug('removing dag node: %s' % nid)
                    node.close()

            if self.scene.is_edge(node):
                if node.ids in self.graph.network.edges():
                    log.debug('removing edge: %s' % str(node.ids))
                    self.graph.remove_edge(*node.ids)
                node.close()

        new_snapshot = self.graph.snapshot()
        self.undo_stack.push(Commands.SceneNodesCommand(old_snapshot, new_snapshot, self.scene, msg='nodes deleted'))

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

                log('# DEBUG: removing edge: {}'.format(node))
                node.close()

            if self.scene.is_node(node):
                print
                log('# DEBUG: removing node: {}'.format(node))
                node.close()

    def dagNodesUpdatedEvent(self, dagnodes):
        if dagnodes:
            print('# DEBUG: dag nodes updated: ', [node.name for node in dagnodes])

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 17/08/2018 - 12:44 AM
# © 2017 - 2018 DAMGteam. All rights reserved