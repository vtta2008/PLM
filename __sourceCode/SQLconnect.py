import os, sys, logging, time, datetime, random
import sqlite3 as lite
from tk import appFuncs as func

# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

conn = lite.connect("D:\pipeline\PipelineTool\sql_tk\db\local.db")
c = conn.cursor()

def create_user_table():

    c.execute("CREATE TABLE IF NOT EXISTS user_profile(id INT PRIMARY KEY, token TEXT, datestamp TEXT, username TEXT, fullname TEXT, title TEXT, aka TEXT, password TEXT, grp TEXT, avatar TEXT)")

    c.execute("INSERT INTO user_profile VALUES(13, '2017-11-19 11:03:59', 'd025957b-c566-41cc-b519-7cc7197972b9', 'Trinh.Do', 'Do Trinh', 'PipelineTD', 'JimJim', 'adsadsa', 'Admin', 'TrinhDo.avatar.png')")
    c.execute("INSERT INTO user_profile VALUES(03, '2017-11-19 11:03:59', '4e7b2c1a-1406-400f-9628-1e2d0486059c', 'Oliver.Hilbert', 'Ollie Hilbert', 'UnKnown', 'Ollie', '123456', 'Lecture', 'OliverHilbert.avatar.png')")
    c.execute("INSERT INTO user_profile VALUES(01, '2017-11-19 11:03:59', '15e4388d-9868-4992-afe0-c2b1102660b6', 'Duc.DM', 'Duc Duong Minh', 'Multimedia Design', 'UP', '123456', 'Admin', 'DucDM.avatar.png')")
    c.execute("INSERT INTO user_profile VALUES(02, '2017-11-19 11:03:59', 'e618141e-8db6-4f9c-ac0d-843a9b2cc4ba', 'Harry.He', 'Harry He', 'CEO', 'Harry', '123456', 'Admin', 'HarryHe.avatar.png')")
    c.execute("INSERT INTO user_profile VALUES(04, '2017-11-19 11:03:59', '73aa8c48-1f54-4a4a-829f-4be85b9a67ec', 'Arjun.Shama', 'Arjun Shama', 'Lighting Artist', 'Mr.Lazy', '123456', 'Artist', 'Arjun.avatar.png')")
    c.execute("INSERT INTO user_profile VALUES(05, '2017-11-19 11:03:59', '55d26936-c3fc-4423-810c-34448ce1fc8e', 'Anine Samuelsen', 'Anine Samuelsen', 'Lookdev Artist',  'Olala', '123456', 'Artist', 'Annie.avatar.png')")
    c.execute("INSERT INTO user_profile VALUES(06, '2017-11-19 11:03:59', '6afb673e-a254-4a44-9ea8-994b739d6262', 'Tam.Nguyen', 'Dieu Tam Nguyen', '3D artist', 'UnKnown', '123456', 'Artist', 'DieuTam.avatar.png')")
    c.execute("INSERT INTO user_profile VALUES(07, '2017-11-19 11:03:59', 'ba2fdb2d-39d2-47ed-8845-3ddae93cfbbd', 'Tho.Nguyen', 'Luong Tho Nguyen', 'Modeling artist', 'UnKnown', '123456', 'Artist', 'NguyenTho.avatar.png')")

    conn.commit()
    c.close()
    conn.close()

def create_new_table(tableName, tableProfile=None):

    logger.info("Analysing to create new data")

    if tableProfile is None:
        logger.info('No table is created')
        sys.exit()

    command_start = "CREATE TABLE IF NOT EXISTS %s" % tableName + " ("
    command_end = " )"
    space = " "

    command = command_start

    for key in tableProfile:
        attribute = tableProfile[key]
        command_details = space + key + space + attribute + space
        command += command_details

    finnal_command = command + command_end

    c.execute("%s" % finnal_command)

    logger.info('Create successful table: %s' % tableName)

def insert_data_user(username, id, fullname, title, aka, password, grp, avatar, *args):

    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    keyword = 'Python'
    value = random.randrange(0, 10)

    if username is None:
        logger.info("No user is added")
        sys.exit()

    c.execute("INSERT INTO user_profile VALUES(username, id, fullname, title, aka, password, grp, avatar)")
    conn.commit()
    c.close()
    conn.close()
    logger.info("Adding successful %s" % username)

create_user_table()
