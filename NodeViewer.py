# -*- coding: utf-8 -*-
"""

Script Name: NoderViewer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QPointF, Qt, qrand, qAbs, QLineF, QPointF, QRectF, QSizeF, qsrand, QTime
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QColor, QPainter, QIcon

# Plt
import appData as app
from ui import uirc as rc
from utilities import utils as func

import pNode

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.logger

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" NoderViewer """



class GridScene(QGraphicsScene):

    def __init__(self, parent=None):
        super(GridScene, self).__init__(parent)

        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        self.buildUI()

    def buildUI(self):

        self.applySetting()

    def applySetting(self):

        self.setSceneRect(-200, -200, 400, 400)


class GridView(QGraphicsView):

    def __init__(self, *args, **kwargs):
        super(GridView, self).__init__(*args, **kwargs)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.centerNode = pNode(self)
        self.centerNode.setPos(0, 0)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            self.centerNode.moveBy(0, -20)
        elif key == Qt.Key_Down:
            self.centerNode.moveBy(0, 20)
        elif key == Qt.Key_Left:
            self.centerNode.moveBy(-20, 0)
        elif key == Qt.Key_Right:
            self.centerNode.moveBy(20, 0)
        elif key == Qt.Key_Plus:
            self.scaleView(1.2)
        elif key == Qt.Key_Minus:
            self.scaleView(1 / 1.2)
        elif key == Qt.Key_Space or key == Qt.Key_Enter:
            for item in self.scene().items():
                if isinstance(item, pNode):
                    item.setPos(-150 + qrand() % 300, -150 + qrand() % 300)
        else:
            super(GridView, self).keyPressEvent(event)

    def timerEvent(self, event):
        nodes = [i for i in self.scene().item() if isinstance(i, pNode)]

        for node in nodes:
            node.calculateForces()

class NodeViewer(QWidget):

    def __init__(self, parent=None):
        super(NodeViewer, self).__init__(parent)

        self.setWindowTitle("Scenegraph PLM")
        self.setWindowIcon(QIcon(func.getLogo(32, 'Logo')))

        self.scene = GridScene()
        self.view = GridView()
        self.view.setScene(self.scene)




def main():
    app = QApplication(sys.argv)
    layout = NodeViewer()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 17/06/2018 - 1:45 PM
# © 2017 - 2018 DAMGteam. All rights reserved