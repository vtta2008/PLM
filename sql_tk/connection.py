import os, sys, logging, time, datetime, random

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets

from tk import appFuncs as func

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

dbPth = os.path.join(os.path.abspath(os.getenv('PIPELINE_TOOL')), 'sql_tk\db\userApp.db')
db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName(dbPth)
if not db.open():
    QMessageBox.critical(None, "Cannot open database",
                         "Unable to establish a database connection.py.\n"
                         "This example needs SQLite support. Please read the Qt SQL "
                         "driver documentation for information how to build it.\n\n"
                         "Click Cancel to exit.",
                         QMessageBox.Cancel)


def dynamic_data_entry():

    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    keyword = 'Python'
    value = random.randrange()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
