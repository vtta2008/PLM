# -*- coding: utf-8 -*-
"""

Script Name: ScenceGraph.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# PLM
from toolkits.Widgets           import GroupBox, TabBar, Widget, HBoxLayout, MenuBar, ToolBar, GridLayout
from ui.Body.Tabs.NodeManager import NodeManager
from ui.base                    import View, Scene
from bin                        import DAMGLIST
from appData                    import SELECTABLE, MOVEABLE

class ViewWidget(GroupBox):

    key = 'SceneTab'

    def __init__(self, parent=None):
        super(ViewWidget, self).__init__()

        self.layout             = HBoxLayout()
        self.parent             = parent
        self.view               = View(self)
        self.scene              = Scene(self.view)

        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
        self.scene.setSceneRect(0, 0, self.parent.width(), self.parent.height())

class SceneGraph(Widget):

    key                     = 'SceneGraph'
    tabs                    = DAMGLIST()
    selection               = DAMGLIST()
    nodeManager             = NodeManager()

    def __init__(self, buttonManager, parent=None):
        super(SceneGraph, self).__init__(parent)

        self.layout         = GridLayout()

        self.buttonManager  = buttonManager
        # self.taskButtons    = self.buttonManager.managerButtonGroupBox(self.parent)
        # self.taskGrp        = GroupBox("Manager", self.taskButtons, "BtnGrid")

        self.menuBar        = MenuBar(self)
        self.toolBar        = ToolBar(self)
        self.nodeViewer     = ViewWidget(self)

        # self.nodeViewer.view.scene().addWidget(self.taskGrp)

        self.layout.addWidget(self.menuBar, 0, 0, 1, 9)
        self.layout.addWidget(self.nodeViewer, 1, 0, 7, 9)
        self.layout.addWidget(self.toolBar, 9, 0, 1, 9)

        self.setLayout(self.layout)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 1:18 AM
# © 2017 - 2018 DAMGteam. All rights reserved