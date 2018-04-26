#!/usr/bin/env python3

from PyQt5.QtWidgets import *
import sys

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        layout = QGridLayout()
        self.setLayout(layout)

        tabbar = QTabBar()
        tabbar.addTab("Tab 1")
        tabbar.addTab("Tab 2")
        tabbar.addTab("Tab 3")
        layout.addWidget(tabbar, 0, 0)

app = QApplication(sys.argv)

screen = Window()
screen.show()

sys.exit(app.exec_())