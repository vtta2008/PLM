# -*- coding: utf-8 -*-
"""

Script Name: pNodeGraph.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtCore import pyqtSignal, QRectF
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout

# Plt
from core.Specs import Specs
from core.Loggers import SetLogger
from appData.scr._nodeGraph import *

from ui.NodeGraph.Node import Node
from ui.NodeGraph.View import View
from ui.NodeGraph.MenuBar import MenuBar
from ui.Libs.UiPreset import IconPth

# -------------------------------------------------------------------------------------------------------------
""" NoderViewer """

class Scene(QGraphicsScene):

    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)

        self.setSceneRect(0, 0, 100, 30)

class NodeGraph(QWidget):

    key = 'nodeGraph'
    showLayout = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(NodeGraph, self).__init__(parent)

        self.specs = Specs(self.key, self)
        self.logger = SetLogger(self)

        self.setWindowIcon(IconPth(32, 'NodeGraph'))
        self.menuBar = MenuBar(self)

        self.scene = Scene()
        self.view = View()
        self.view.setScene(self.scene)
        self.view.setRenderHint(ANTIALIAS)
        self.view.setViewportUpdateMode(UPDATE_FULLVIEW)

        self.layout = QGridLayout()
        self.layout.addWidget(self.menuBar, 0, 0, 1, 1)
        self.layout.addWidget(self.view, 1, 0, 1, 1)
        self.setLayout(self.layout)

        self.Nodes = []

        node1 = Node({'name': 'Node1'})
        node1.setPos(0, 0)

        node2 = Node({'name': 'Node2'})
        node2.setPos(20, 20)


        self.scene.addItem(node1)
        self.scene.addItem(node2)

        self.resize(1000, 500)

    def createNode(self):
        pass

    def regisNode(self):
        pass

    def clearScene(self):
        pass

    def addSceneMenuAction(self, menu):
        pass

    def loadScene(self):
        pass

    def mergeScene(self):
        pass

    def storeCurrentScene(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == KEY_DEL:
            selectedNodes = [i for i in self.scene.selectedItems() if isinstance(i, Node)]
            for node in selectedNodes:
                node.destroy()
        super(NodeGraph, self).keyPressEvent(event)

    def contextMenuEvent(self, event):
        pass

    def resizeEvent(self, event):
        print(self.width(), self.height())

def main():
    nodeGrahp = QApplication(sys.argv)
    # nodeGrahp.setStyleSheet(nodeGrahp.load_stylesheet())
    layout = NodeGraph()
    layout.show()
    nodeGrahp.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved