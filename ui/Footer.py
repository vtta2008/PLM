#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Footer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from functools                              import partial
from damg                                   import DAMGTHREAD

# PyQt5
from PyQt5.QtWidgets                        import QApplication

# Plt
from appData                                import BTNTAGSIZE
from utils                                  import get_cpu_useage, get_ram_useage, create_signal_slot
from ui.uikits.Widget                       import Widget
from ui.uikits.GridLayout                   import GridLayout
from ui.uikits.Button                       import Button
from ui.uikits.Label                        import Label

signal_cpu, slot_cpu = create_signal_slot(argType=str, name='CPU')
signal_ram, slot_ram = create_signal_slot(argType=str, name='RAM')

class CPUuseage(DAMGTHREAD):

    key = 'FooterWorker'
    cpu = signal_cpu
    ram = signal_ram

    def __init__(self, name='CPU useage', *args, **kwargs):
        super(CPUuseage, self).__init__(self)

        self.args = args
        self.kwargs = kwargs
        self._name = name

    def run(self):
        while True:
            cpu = str(get_cpu_useage())
            ram = str(get_ram_useage())
            self.cpu.emit(cpu)
            self.ram.emit(ram)

# -------------------------------------------------------------------------------------------------------------
""" Footer """

class Footer(Widget):

    key                 = 'Footer'
    _name               = 'DAMG Footer'

    tags = dict(python  = "https://docs.anaconda.com/anaconda/reference/release-notes/",
                licence = "https://github.com/vtta2008/damgteam/blob/master/LICENCE",
                version = "https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst")

    def __init__(self, parent=None):
        super(Footer, self).__init__(parent)

        self.parent     = parent
        layout = self.buildUI()
        self.setLayout(layout)

        worker = CPUuseage()
        worker.cpu.connect(self.update_cpu_useage)
        worker.ram.connect(self.update_ram_useage)
        worker.start()

    def buildUI(self):
        layout          = GridLayout()

        # for i in range(7):
        #     layout.addWidget(Label({'txt': " "}), 0, i, 1, 1)
        #     i += 1

        i = 4
        for tag in ['python', 'licence', 'version']:
            layout.addWidget(self.createButton(tag), 0, i, 1, 2)
            i = i + 2

        self.usage_cpu = Label({'txt': 'CPU: 0%'})
        self.usage_ram = Label({'txt': 'RAM: 0%'})
        layout.addWidget(self.usage_cpu, 1, 6, 1, 2)
        layout.addWidget(self.usage_ram, 1, 8, 1, 2)

        return layout

    @slot_cpu
    def update_cpu_useage(self, val):
        return self.usage_cpu.setText('CPU: {0}%'.format(val))

    @slot_ram
    def update_ram_useage(self, val):
        return self.usage_ram.setText('RAM: {0}%'.format(val))

    def createButton(self, tagName):
        if not tagName in self.tags.keys():
            print('KeyError: tag name is not existed: {0}'.format(tagName))
            button = Button()
        else:
            button = Button({'tag': tagName,
                             'fix': BTNTAGSIZE,
                             'ics': BTNTAGSIZE,
                             'cl' : partial(self.signals.openBrowser.emit, self.tags[tagName])})
        return button

def main():
    app = QApplication(sys.argv)
    layout = Footer()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/06/2018 - 4:24 AM