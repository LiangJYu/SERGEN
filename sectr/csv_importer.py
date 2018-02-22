import csv
import sqlite3
from auto_classify import auto_classify

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

sql = ''' INSERT INTO transactions(date,amount,description,lender,main_category,sub_category,extra_src_info,notes)
          VALUES(?,?,?,?,?,?,?,?) '''
              
"""
convert row csv from Citi and convert to SECTR format
"""
def make_citi_db_tuple(row):
    description = ' '.join([row['Description'],row['Member Name']]),
    amount = float(row['Debit']) if row['Debit'] else float(row['Credit']),
    tpl = (row['Date']                  # date
            description,                # amount
            amount,                     # description
            'Citi',                     # lender
            auto_classifiy(description),# main category
            '',                         # sub category
            '',                         # extra source info
            '')                         # notes
    return tpl

"""
convert row csv from Discover and convert to SECTR format
"""
def make_discover_db_tuple(row):
    desciption = row['Description']
    extra_info = ''.join([row['Category'], row['Trans. Date'])
    tpl = (row['Post Date'],            # date
            -float(row['Amount']),      # amount
            description,                # description
            'Discover',                 # lender
            auto_classify(description), # main category
            '',                         # sub category
            extra_info,                 # extra source info
            '')                         # notes
    return tpl

"""
convert row csv from BofA and convert to SECTR format
"""
def make_bofa_db_tuple(row):
    desciption = ' '.join([row['Payee'],row['Address']]),
    tpl = (row['Posted Date'],          # date
            -float(row['Amount']),      # amount
            description,                # description
            'Bank of America',          # lender
            auto_classify(description), # main category
            '',                         # sub category
            row['Reference Number'],    # extra source info
            '')                         # notes
    return tpl

# dictionary of lender names and conversion function
tpl_maker = {'bofa':make_bofa_db_tuple, 'discover':make_discover_db_tuple, 'citi':make_citi_db_tuple}

def import_statement(lender, conn, path):
    with open(path, 'r') as fin:
        # DictReader uses first line in file for column headings by default
        statement_data = csv.DictReader(fin) 
        to_db = [tpl_maker[lender] for row in statement_data]

    cur = conn.cursor()
    cur.executemany(sql, to_db)
    conn.commit()
    conn.close()

