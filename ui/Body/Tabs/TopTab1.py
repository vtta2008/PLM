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
from ui.uikits.Label                            import Label
from ui.uikits.CheckBox                         import CheckBox
from cores.Task                                 import duedate, duetime, Task
from utils                                      import get_file_path
from appData                                    import TASK_DIR

# -------------------------------------------------------------------------------------------------------------
class TaskInfo(GroupBox):

    key = 'TaskInfo'

    def __init__(self, task):
        super(TaskInfo, self).__init__()

        with open(task, 'r') as f:
            self._data = json.load(f)

        self.setTitle(self._data['id'])
        self.layout = VBoxLayout()

        self._id = self._data['id']
        self.key = self._id
        self._name = self._data['name']
        self._mode = self._data['mode']
        self._type = self._data['type']

        self._project = self._data['project']
        self._organisation = self._data['organisation']
        self._details = self._data['details']

        self._hour = int(self._data['endtime'].split(':')[0])
        self._minute = int(self._data['endtime'].split(':')[1])
        self._second = int(self._data['endtime'].split(':')[2])

        self._day = int(self._data['enddate'].split('/')[0])
        self._month = int(self._data['enddate'].split('/')[1])
        self._year = int(self._data['enddate'].split('/')[2])

        self.duetime = duetime(self._hour, self._minute, self._second)
        self.duedate = duedate(self._day, self._month, self._year)

        self.task = Task(self._id, self._name, self._mode, self._type, self._project, self._organisation,
                         self.duetime, self.duedate, self._details)

        self._countdown = '{0}:{1}:{2}'.format(self.task.hours, self.task.minutes, self.task.seconds)
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
        self.setMaximumSize(100, 100)

    def update_countdown(self, val):
        if self.task.status == 'Overdued':
            self.task_status.setStyleSheet('color: red')
        elif self.task.status == 'Urgent':
            self.task_status.setStyleSheet('color: orange')
        else:
            self.task_status.setStyleSheet('color: green')

        return self.task_countdown.setText(val)

    @property
    def id(self):
        return self._id

    @property
    def mode(self):
        return self._mode

    @property
    def type(self):
        return self._type

    @property
    def project(self):
        return self._project

    @property
    def organisation(self):
        return self._organisation

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    @property
    def day(self):
        return self._day

    @property
    def month(self):
        return self._month

    @property
    def year(self):
        return self._year

    @id.setter
    def id(self, val):
        self._id = val

    @mode.setter
    def mode(self, val):
        self._mode = val

    @type.setter
    def type(self, val):
        self._type = val

    @project.setter
    def project(self, val):
        self._project = val

    @organisation.setter
    def organisation(self, val):
        self._organisation = val

    @hour.setter
    def hour(self, val):
        self._hour = val

    @minute.setter
    def minute(self, val):
        self._minute = val

    @second.setter
    def second(self, val):
        self._second = val

    @day.setter
    def day(self, val):
        self._day = val

    @month.setter
    def month(self, val):
        self._month = val

    @year.setter
    def year(self, val):
        self._year = val

class TopTap1Filter(GroupBox):

    key = 'TopTab1Info'

    def __init__(self):
        super(TopTap1Filter, self).__init__()

        self.setTitle('Fillter')
        self.layout = GridLayout(self)
        self.setLayout(self.layout)

        # self.tasks = Label({'txt': 'Tasks: '})
        # self.currentTask = Label({'txt': 'Current Task: '})
        #
        # self.layout.addWidget(self.tasks, 0, 0, 1, 3)
        # self.layout.addWidget(self.currentTask, 1, 0, 1, 3)

        self.overduedCB = CheckBox()
        self.urgentCB = CheckBox()
        self.safetyCB = CheckBox()
        self.allTabCheckBox = CheckBox()
        self.allTabCheckBox.stateChanged.connect(self.allTabCheckBoxStateChanged)

        odl = 0
        ugl = odl + 1
        stl = ugl + 1
        al = stl + 1

        self.layout.addWidget(Label({'txt': 'Overdued', 'sss': 'color: red'}), odl, 0, 1, 2)
        self.layout.addWidget(self.overduedCB, odl, 2, 1, 1)
        self.layout.addWidget(Label({'txt': 'Urgent', 'sss': 'color: orange'}), ugl, 0, 1, 2)
        self.layout.addWidget(self.urgentCB, ugl, 2, 1, 1)
        self.layout.addWidget(Label({'txt': 'Others', 'sss': 'color: green'}), stl, 0, 1, 2)
        self.layout.addWidget(self.safetyCB, stl, 2, 1, 1)
        self.layout.addWidget(Label({'txt': 'All'}), al, 0, 1, 2)
        self.layout.addWidget(self.allTabCheckBox, al, 2, 1, 1)

    def allTabCheckBoxStateChanged(self, bool):
        self.overduedCB.setChecked(bool)
        self.urgentCB.setChecked(bool)
        self.safetyCB.setChecked(bool)

# -------------------------------------------------------------------------------------------------------------
""" TopTab1 """

class TopTab1(Widget):

    key = 'TopTab1'
    tasks = []

    def __init__(self, buttonManager, parent=None):
        super(TopTab1, self).__init__(parent)

        self.buttonManager = buttonManager
        self.parent = parent

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.prjButtons  = self.buttonManager.projectButtonsGroupBox(self.parent)
        self.taskButtons = self.buttonManager.taskButtonsGroupBox(self.parent)
        self.teamButtons = self.buttonManager.teamButtonsGroupBox(self.parent)

        self.update_tasks()

        self.prjGrp      = GroupBox("Project", self.prjButtons, "BtnGrid")
        self.taskGrp     = GroupBox("Task", self.taskButtons, "BtnGrid")
        self.teamGrp     = GroupBox('Team', self.teamButtons, 'BtnGrid')
        self.tabFilter   = TopTap1Filter()
        self.tabFilter.overduedCB.stateChanged.connect(self.overdue)
        self.tabFilter.urgentCB.stateChanged.connect(self.urgent)
        self.tabFilter.safetyCB.stateChanged.connect(self.safety)

        self.layout.addWidget(self.prjGrp, 5, 0, 2, 2)
        self.layout.addWidget(self.taskGrp, 5, 2, 2, 2)
        self.layout.addWidget(self.teamGrp, 5, 4, 2, 2)
        self.layout.addWidget(self.tabFilter, 5, 6, 2, 3)

    def update_tasks(self):
        try:
            self.layout.removeItem(self.taskLayout)
        except AttributeError:
            self.taskLayout = HBoxLayout()
        else:
            for w in self.taskLayout.children():
                self.taskLayout.removeWidget(w)
            self.taskLayout = HBoxLayout()

        tasks = get_file_path(TASK_DIR)

        for t in tasks:
            task = TaskInfo(t)
            self.taskLayout.addWidget(task)
            self.tasks.append(task)
        self.layout.addLayout(self.taskLayout, 1, 0, 3, 9)

    def overdue(self, bool):
        for task in self.tasks:
            if task.task.status == 'Overdued':
                task.setVisible(bool)

    def urgent(self, bool):
        for task in self.tasks:
            if task.task.status == 'Urgent':
                task.setVisible(bool)

    def safety(self, bool):
        for task in self.tasks:
            if task.task.status not in ['Overdued, Urgent']:
                task.setVisible(bool)

def main():
    app = QApplication(sys.argv)
    layout = TopTab1()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018