# -*- coding: utf-8 -*-
"""

Script Name: pythonconsolewidget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtCore import pyqtSignal, QEvent, Qt
from PyQt5.QtWidgets import QApplication, QLineEdit


class PythonConsoleWidget(QLineEdit):
    """PythonConsoleWidget(QLineEdit)

    Provides a custom widget to accept Python expressions and emit output
    to other components via a custom signal.
    """

    pythonOutput = pyqtSignal(str)

    def __init__(self, parent=None):

        super(PythonConsoleWidget, self).__init__(parent)

        self.history = []
        self.current = -1

        self.returnPressed.connect(self.execute)

    def keyReleaseEvent(self, event):

        if event.type() == QEvent.KeyRelease:

            if event.key() == Qt.Key_Up:
                current = max(0, self.current - 1)
                if 0 <= current < len(self.history):
                    self.setText(self.history[current])
                    self.current = current

                event.accept()

            elif event.key() == Qt.Key_Down:
                current = min(len(self.history), self.current + 1)
                if 0 <= current < len(self.history):
                    self.setText(self.history[current])
                else:
                    self.clear()
                self.current = current

                event.accept()

    def execute(self):

        # Define this here to give users something to look at.
        qApp = QApplication.instance()

        self.expression = self.text()
        try:
            result = str(eval(str(self.expression)))

            # Emit the result of the evaluated expression.
            self.pythonOutput.emit(result)
            print(result)

            # Clear the line edit, append the successful expression to the
            # history, and update the current command index.
            self.clear()
            self.history.append(self.expression)
            self.current = len(self.history)
        except:
            pass


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    widget = PythonConsoleWidget()
    widget.show()
    sys.exit(app.exec_())
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/08/2018 - 6:56 AM
# © 2017 - 2018 DAMGteam. All rights reserved