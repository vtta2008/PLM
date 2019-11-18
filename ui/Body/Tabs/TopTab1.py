#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: TopTab2.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, os, json

# PyQt5
from PyQt5.QtWidgets        import QApplication

# Plt
from ui.uikits.Widget                           import Widget
from ui.uikits.GridLayout                       import GridLayout
from ui.uikits.GroupBox                         import GroupBox
from ui.uikits.BoxLayout                        import HBoxLayout, VBoxLayout
from ui.uikits.Label import Label
from cores.Task import duedate, duetime, Task
from utils import get_file_path
from appData import TASK_DIR

# -------------------------------------------------------------------------------------------------------------
class TaskInfo(GroupBox):

    key = 'TaskInfo'

    def __init__(self, task):
        super(TaskInfo, self).__init__()

        with open(task, 'r') as f:
            taskData = json.load(f)

        self.setTitle(taskData['name'])
        self.layout = VBoxLayout()

        h = int(taskData['endtime'].split(':')[0])
        m = int(taskData['endtime'].split(':')[1])
        s = int(taskData['endtime'].split(':')[2])
        d = int(taskData['enddate'].split('/')[0])
        mo = int(taskData['enddate'].split('/')[1])
        y = int(taskData['enddate'].split('/')[2])
        dtime = duetime(h, m, s)
        ddate = duedate(d, mo, y)

        self.task = Task(taskData['id'], taskData['name'], taskData['mode'], taskData['type'],
                                 taskData['project'], taskData['organisation'], dtime, ddate, taskData['details'])

        self._countdown = '{0}:{1}:{2}'.format(self.task.hours, self.task.minutes,
                                               self.task.seconds)
        self.task.countdown.connect(self.update_countdown)

        self.task_status = Label({'txt': '{0}'.format(self.task.status)})
        self.task_duedate = Label({'txt': '{0}'.format(self.task._enddate)})
        self.task_duetime = Label({'txt': '{0}'.format(self.task._endtime)})
        self.task_countdown = Label({'txt': '{0}'.format(self._countdown)})

        self.layout.addWidget(self.task_status)
        self.layout.addWidget(self.task_duedate)
        self.layout.addWidget(self.task_duetime)
        self.layout.addWidget(self.task_countdown)

        self.setLayout(self.layout)
        self.setMaximumWidth(100)

    def update_countdown(self, val):
        return self.task_countdown.setText(val)

# -------------------------------------------------------------------------------------------------------------
""" TopTab1 """

class TopTab1(Widget):

    key = 'TopTab1'

    def __init__(self, buttonManager, parent=None):
        super(TopTab1, self).__init__(parent)

        self.buttonManager = buttonManager
        self.parent = parent

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.signals.regisLayout.emit(self)

    def buildUI(self):

        prjButtons  = self.buttonManager.projectButtonsGroupBox(self.parent)
        taskButtons = self.buttonManager.taskButtonsGroupBox(self.parent)
        teamButtons = self.buttonManager.teamButtonsGroupBox(self.parent)

        self.update_tasks()

        self.prjGrp      = GroupBox("Project", prjButtons, "BtnGrid")
        self.taskGrp     = GroupBox("Task", taskButtons, "BtnGrid")
        self.teamGrp     = GroupBox('Team', teamButtons, 'BtnGrid')

        self.layout.addWidget(self.prjGrp, 4, 0, 3, 2)
        self.layout.addWidget(self.taskGrp, 4, 2, 3, 2)
        self.layout.addWidget(self.teamGrp, 4, 4, 3, 2)

    def update_tasks(self):
        self.infoGrid = HBoxLayout()

        tasks = get_file_path(TASK_DIR)
        for task in tasks:
            self.infoGrid.addWidget(TaskInfo(task))

        self.layout.addLayout(self.infoGrid, 0, 0, 4, 6)

    # def resizeEvent(self, event):
    #     w = self.width()
    #     h = self.height()
    #
    #     self.infoGrp.resize(w-4, h/2-4)
    #
    #     for grp in [self.prjGrp, self.taskGrp, self.teamGrp]:
    #         grp.resize(w/3-4, h/2-4)


def main():
    app = QApplication(sys.argv)
    layout = TopTab1()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018