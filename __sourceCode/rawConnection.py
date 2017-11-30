import os, sys, logging, time, datetime, random

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)



def createConnection():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('D:\pipeline\PipelineTool\sql_tk\db\userApp.db')
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

    q.exec_("create table user_profile(id int primary key, datestamp varchar(20) , token varchar(20), "
                "username varchar(20), fullname varchar(20), title varchar(20), aka varchar(20), password varchar(20), "
                "grp varchar, avatar varchar(20))")

    q.exec_("INSERT INTO user_profile VALUES(13, '2017-11-19 11:03:59', 'd025957b-c566-41cc-b519-7cc7197972b9', "
                "'Trinh.Do', 'Do Trinh', 'PipelineTD', 'JimJim', '61647361647361', 'Admin', "
            "'http://download1642.mediafire.com/aelarre1jylg/1lky5y52cqg5pfd/TrinhDo.avatar.jpg')")

    q.exec_("INSERT INTO user_profile VALUES(03, '2017-11-19 11:03:59', '4e7b2c1a-1406-400f-9628-1e2d0486059c', "
                "'Oliver.Hilbert', 'Ollie Hilbert', 'UnKnown', 'Ollie', '313233343536', 'Lecture', "
            "'http://download1583.mediafire.com/fyow3crwwkrg/3gkk1bzb18w0hd1/OliverHillbert.avatar.jpg')")

    q.exec_("INSERT INTO user_profile VALUES(01, '2017-11-19 11:03:59', '15e4388d-9868-4992-afe0-c2b1102660b6', "
                "'Duc.DM', 'Duc Duong Minh', 'Multimedia Design', 'UP', '313233343536', 'Admin', "
            "'http://download948.mediafire.com/t2t8r879noyg/u5xe01h9m15e9vm/DucDM.avatar.jpg')")

    q.exec_("INSERT INTO user_profile VALUES(02, '2017-11-19 11:03:59', 'e618141e-8db6-4f9c-ac0d-843a9b2cc4ba', "
                "'Harry.He', 'Harry He', 'CEO', 'Harry', '123456', 'Admin', "
            "'http://download1494.mediafire.com/flo33n62a2fg/zkhebcod5z3v181/HarryHe.avatar.jpg')")

    q.exec_("INSERT INTO user_profile VALUES(04, '2017-11-19 11:03:59', '73aa8c48-1f54-4a4a-829f-4be85b9a67ec', "
                "'Arjun.Shama', 'Arjun Shama', 'Lighting Artist', 'Mr.Lazy', '313233343536', 'Artist', "
            "'http://download1477.mediafire.com/akwduaa28lgg/4cft2gz486d9j1o/Arjun.avatar.jpg')")

    q.exec_("INSERT INTO user_profile VALUES(05, '2017-11-19 11:03:59', '55d26936-c3fc-4423-810c-34448ce1fc8e', "
                "'Anine Samuelsen', 'Anine Samuelsen', 'Lookdev Artist',  'Olala', '313233343536', 'Artist', "
            "'http://download1320.mediafire.com/3b21586drarg/gw7axjmj2f6bu92/Annie.avatar.jpg')")

    q.exec_("INSERT INTO user_profile VALUES(06, '2017-11-19 11:03:59', '6afb673e-a254-4a44-9ea8-994b739d6262', "
                "'Tam.Nguyen', 'Dieu Tam Nguyen', '3D artist', 'UnKnown', '313233343536', 'Artist', "
            "'http://download943.mediafire.com/nnzyg7gzw6ig/y0c5131uu6348b1/DieuTam.avatar.jpg')")

    q.exec_("INSERT INTO user_profile VALUES(07, '2017-11-19 11:03:59', 'ba2fdb2d-39d2-47ed-8845-3ddae93cfbbd', "
                "'Tho.Nguyen', 'Luong Tho Nguyen', 'Modeling artist', 'UnKnown', '313233343536', 'Artist', "
            "'http://download1511.mediafire.com/hduever8kycg/ycnenb3htik8g79/NguyenTho.avatar.jpg')")
    return True


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    createConnection()