import os, logging

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('sqllocal')

if not db.open():
    QMessageBox.critical(None, "Cannot open database",
                         "Unable to establish a database connection.py.\n"
                         "This example needs SQLite support. Please read the Qt SQL "
                         "driver documentation for information how to build it.\n\n"
                         "Click Cancel to exit.",
                         QMessageBox.Cancel)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
