import csv
import sqlite3
import sys
import os
# from auto_classify import auto_classify

"""
SECTR fields
date
amount
description
lender - which CC was used
main category(ies) - eventually add in $/% split
sub category(ies)
extra_src_info - info of unused fields from source concatnated
notes

read in csv from different financial institutions and convert them to SECTR format
"""

sql = ''' INSERT INTO transactions(date,amount,description,lender,category,extra_src_info,notes)
          VALUES(?,?,?,?,?,?,?) '''
              
"""
convert row csv from Citi and convert to SECTR format
"""
def make_citi_db_tuple(row):
    description = ' '.join([row['Description'],row['Member Name']])
    # cat_main, cat_sub = auto_classify(description)
    cat_main = ''
    amount = float(row['Debit']) if row['Debit'] else float(row['Credit'])
    tpl = (row['Date'],                 # date
            amount,                     # amount
            description,                # description
            'Citi',                     # lender
            cat_main,                   # main category
            '',                         # extra source info
            '')                         # notes
    return tpl

"""
convert row csv from Discover and convert to SECTR format
"""
def make_discover_db_tuple(row):
    description = row['Description']
    # cat_main, cat_sub = auto_classify(description)
    cat_main = ''
    extra_info = ' '.join([row['Category'], row['Trans. Date']])
    tpl = (row['Post Date'],            # date
            float(row['Amount']),       # amount
            description,                # description
            'Discover',                 # lender
            cat_main,                   # main category
            extra_info,                 # extra source info
            '')                         # notes
    return tpl

"""
convert row csv from BofA and convert to SECTR format
"""
def make_bofa_db_tuple(row):
    description = ' '.join([row['Payee'],row['Address']])
    # cat_main, cat_sub = auto_classify(description)
    cat_main = ''
    #print(cat_main, cat_sub)
    tpl = (row['Posted Date'],          # date
            -float(row['Amount']),      # amount
            description,                # description
            'Bank of America',          # lender
            cat_main,                   # main category
            row['Reference Number'],    # extra source info
            '')                         # notes
    return tpl

# dictionary of lender names and conversion function
tpl_maker = {'bofa':make_bofa_db_tuple, 'discover':make_discover_db_tuple, 'citi':make_citi_db_tuple}

# dictionary of CSV header. TODO: move this else where (maybe in a db)
csv_headers = {}
csv_headers['bofa'] = ['Posted Date', 'Reference Number', 'Payee', 'Address', 'Amount']
csv_headers['citi'] = ['Status', 'Date', 'Description', 'Debit', 'Credit', 'Member Name']
csv_headers['discover']=['Trans. Date', 'Post Date', 'Description', 'Amount', 'Category']

def import_statement(lender, conn, path):
    with open(path, 'r') as fin:
        # DictReader uses first line in file for column headings by default
        statement_data = csv.DictReader(fin) 
        
        # continue if CSV headers match
        if csv_headers[lender] == statement_data.fieldnames:
            # read in all data
            # check for duplicates and mark them as needed
            # is dup if date, amount, and description are repeated
            to_db = []
            unique_list = []
            for row in statement_data:
                temp_tpl = tpl_maker[lender](row)
                dup_check = temp_tpl[:3]
                if dup_check in unique_list:
                    temp_tpl = list(temp_tpl)
                    temp_tpl[5] = 'duplicate'
                    temp_tpl = tuple(temp_tpl)
                else:
                    unique_list.append(dup_check)
                to_db.append(temp_tpl)

            # insert all data into database
            cur = conn.cursor()
            cur.executemany(sql, to_db)
            conn.commit()
            conn.close()
        else:
            print("headers do not match")


if __name__ == '__main__':
    db_file = '../data/transactions.db'
    conn = sqlite3.connect(db_file)
    lender = sys.argv[1]
    path = sys.argv[2]
    import_statement(lender, conn, os.path.expanduser(path))
