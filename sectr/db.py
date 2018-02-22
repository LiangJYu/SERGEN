import sqlite3

class db:

    def __init__(self):
        self.db_file = '../data/transactions.db'
        self.conn = ''

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
    
    def create_table(self):
        sql = """ CREATE TABLE IF NOT EXISTS transactions(
                        date text PRIMARY KEY,
                        amount float,
                        description text NOT NULL,
                        lender text NOT NULL,
                        main_category text NOT NULL,
                        sub_category text NOT NULL,
                        exta_src_info text NOT NULL,
                        notes text NOT NULL); """
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

