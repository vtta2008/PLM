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
from PLM.commons.Widgets import GroupBox, GridLayout, Widget, GroupGrid
from PLM.ui.base import TaskInfo, TaskFilter
from PLM.utils import get_file_path
from configs                                    import TASK_DIR
from bin                                        import DAMGLIST

# -------------------------------------------------------------------------------------------------------------
""" TopTab1 """

class TopTab1(Widget):

    key                                         = 'TopTab1'
    tasks                                       = DAMGLIST()

    def __init__(self, buttonManager, parent=None):
        super(TopTab1, self).__init__(parent)

        self.buttonManager                      = buttonManager
        self.parent                             = parent

        self.layout                             = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.taskButtons                        = self.buttonManager.managerButtonGroupBox(self.parent)
        self.taskGrp                            = GroupBox("Manager", self.taskButtons, "BtnGrid")
        self.update_tasks()

        self.taskFilter                         = TaskFilter()
        self.taskFilter.overduedCB.stateChanged.connect(self.overdue)
        self.taskFilter.urgentCB.stateChanged.connect(self.urgent)
        self.taskFilter.safetyCB.stateChanged.connect(self.safety)

        self.taskTracker                        = GroupGrid('Tasks', self)

        self.taskGrp.setMaximumWidth(110)
        self.taskFilter.setMaximumWidth(110)
        self.taskTracker.setMinimumWidth(390)

        self.layout.addWidget(self.taskGrp, 0, 0, 1, 1)
        self.layout.addWidget(self.taskFilter, 1, 0, 1, 1)
        self.layout.addWidget(self.taskTracker, 0, 1, 2, 2)

    def update_tasks(self):

        tasks = get_file_path(TASK_DIR)

        i = 0
        a = 0
        h = 1
        w = 1
        for t in tasks:
            if i > 4:
                i = 1
                a = a + h

            task = TaskInfo(t)
            self.taskTracker.layout.addWidget(task, a, i, h ,w)
            self.tasks.append(task)
            i += 1

    def overdue(self, bool):
        for task in self.tasks:
            if task.task_status == 'Overdued':
                task.setVisible(bool)

    def urgent(self, bool):
        for task in self.tasks:
            if task.task._status == 'Urgent':
                task.setVisible(bool)

    def safety(self, bool):
        for task in self.tasks:
            if task.task._status not in ['Overdued, Urgent']:
                task.setVisible(bool)

    # def keyPressEvent(self, event):
    #     if event.key() == KEY_DEL:
    #         selectedNodes = [i for i in self.scene.selectedItems() if isinstance(i, NodeItem)]
    #         for node in selectedNodes:
    #             node.destroy()
    #     super(TopTab1, self).keyPressEvent(event)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018