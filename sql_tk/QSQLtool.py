import os, sys, logging, time, datetime, random

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)



def createConnection():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('D:\PipelineTool\sql_tk\db\dbAcc.db')
    print db.open()

    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
                             "Unable to establish a database connection.py.\n"
                             "This example needs SQLite support. Please read the Qt SQL "
                             "driver documentation for information how to build it.\n\n"
                             "Click Cancel to exit.",
                             QMessageBox.Cancel)
        return False

    q = QSqlQuery()
    q.exec_("create table accountdb (id int primary key, username varchar(20), password varchar(20)")
    q.exec_("insert into current_login values (13, 'Trinh.Do', '61647361647361')")

    return True


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    con = createConnection()