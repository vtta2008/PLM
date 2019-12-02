#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: TopTab2.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """


# PLM
from toolkits.Widgets                           import GroupBox, GridLayout, Widget
from ui.base                                    import TaskInfo, TaskFilter, NodeItem
from .ScenceGraph                               import View
from utils                                      import get_file_path
from appData                                    import TASK_DIR, ANTIALIAS, UPDATE_FULLVIEW, KEY_DEL
from bin                                        import DAMGLIST

# -------------------------------------------------------------------------------------------------------------
""" TopTab1 """

class TopTab1(Widget):

    key                                         = 'TopTab1'
    tasks                                       = DAMGLIST()

    def __init__(self, buttonManager, parent=None):
        super(TopTab1, self).__init__(parent)

        self.buttonManager = buttonManager
        self.parent = parent

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.taskButtons = self.buttonManager.managerButtonGroupBox(self.parent)

        # self.update_tasks()

        self.taskGrp     = GroupBox("Manager", self.taskButtons, "BtnGrid")
        self.tabFilter   = TaskFilter()
        self.tabFilter.overduedCB.stateChanged.connect(self.overdue)
        self.tabFilter.urgentCB.stateChanged.connect(self.urgent)
        self.tabFilter.safetyCB.stateChanged.connect(self.safety)

        self.taskGrp.setMaximumWidth(100)
        self.tabFilter.setMaximumWidth(100)

        self.layout.addWidget(self.taskGrp, 0, 0, 2, 1)
        self.layout.addWidget(self.tabFilter, 2, 0, 2, 1)

        self.view = View(self)
        self.scene = self.view.scene()
        # self.view.setScene(self.scene)
        self.view.setRenderHint(ANTIALIAS)
        self.view.setViewportUpdateMode(UPDATE_FULLVIEW)
        self.scene.setSceneRect(0, 0, self.view.width(), self.view.height())
        self.layout.addWidget(self.view, 0, 3, 8, 8)

    def update_tasks(self):

        tasks = get_file_path(TASK_DIR)

        i = 1
        a = 0
        for t in tasks:
            if i > 4:
                i = 1
                a = a + 2

            task = TaskInfo(t)
            self.layout.addWidget(task, a, i, 2 ,1)
            self.tasks.append(task.task)
            i += 1

    def overdue(self, bool):
        for task in self.tasks:
            if task.task._status == 'Overdued':
                task.setVisible(bool)

    def urgent(self, bool):
        for task in self.tasks:
            if task.task.status == 'Urgent':
                task.setVisible(bool)

    def safety(self, bool):
        for task in self.tasks:
            if task.task.status not in ['Overdued, Urgent']:
                task.setVisible(bool)

    def keyPressEvent(self, event):
        if event.key() == KEY_DEL:
            selectedNodes = [i for i in self.scene.selectedItems() if isinstance(i, NodeItem)]
            for node in selectedNodes:
                node.destroy()
        super(TopTab1, self).keyPressEvent(event)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018