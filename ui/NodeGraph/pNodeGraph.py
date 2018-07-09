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
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMenu, QGraphicsScene, QMenuBar
from PyQt5.QtGui import QIcon, QColor, QFont

# Plt
from utilities import utils as func

from appData.scr._pNN import *

from ui.NodeGraph.Node import Node
from ui.NodeGraph.pView import pView
from ui.NodeGraph.pMenuBar import pMenuBar

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" NoderViewer """

class pScene(QGraphicsScene):

    def __init__(self, parent=None):
        super(pScene, self).__init__(parent)

        self.setSceneRect(0, 0, 100, 30)

class pNodeGraph(QWidget):

    def __init__(self, parent=None):
        super(pNodeGraph, self).__init__(parent)

        self.setWindowTitle("Scenegraph PLM")
        self.setWindowIcon(QIcon(func.getLogo(32, 'Logo')))

        self.menuBar = pMenuBar(self)

        self.scene = pScene()
        self.view = pView()
        self.view.setScene(self.scene)
        self.view.setRenderHint(ANTIALIAS)
        self.view.setViewportUpdateMode(UPDATE_FULLVIEW)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

        self.pNodes = []

        node1 = Node("Node 1")
        node1.setPos(0, 0)

        node2 = Node("Node 2")
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
        super(pNodeGraph, self).keyPressEvent(event)

    def contextMenuEvent(self, event):
        pass

    def resizeEvent(self, event):
        print(self.width(), self.height())

def main():
    nodeGrahp = QApplication(sys.argv)
    # nodeGrahp.setStyleSheet(nodeGrahp.load_stylesheet())
    layout = pNodeGraph()
    layout.show()
    nodeGrahp.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved