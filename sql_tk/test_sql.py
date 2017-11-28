import os, sys, sqlite3


class TestSQL(object):
    scrDatabase = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk')
    userDataPth = os.path.join(scrDatabase, 'user.db')

    def __init__(self):
        super(TestSQL, self).__init__()

        self.testSQL()

    def testSQL(self):

        print 'will do it later'

        userDataPth = os.path.join(self.scrDatabase, 'user.db')
        userConnection = sqlite3.connect(userDataPth)
        with userConnection:
            cur = userConnection.cursor()
            cur.execute("CREATE TABLE Users(usernme TEXT, ID INT,  passwork TEXT, group TEXT, avatar TEXT, aka TEXT, title TEXT)")


def initialize():
    TestSQL()
