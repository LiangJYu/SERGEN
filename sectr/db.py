import sqlite3

class transaction_db:

    def __init__(self):
        self.db_file = ''
        self.conn = ''

    def create_connection(self):
        try:
            self.conn = sqlite3.connect()
        except Error as e:
            print(e)
    
    def create_table(self, sql):
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

