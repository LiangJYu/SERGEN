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
    description = ' '.join([row['Description'],row['Member Name']])
    amount = float(row['Debit']) if row['Debit'] else float(row['Credit'])
    tpl = (row['Date'],                 # date
            amount,                     # amount
            description,                # description
            'Citi',                     # lender
            auto_classify(description), # main category
            '',                         # sub category
            '',                         # extra source info
            '')                         # notes
    return tpl

"""
convert row csv from Discover and convert to SECTR format
"""
def make_discover_db_tuple(row):
    description = row['Description']
    extra_info = ' '.join([row['Category'], row['Trans. Date']])
    tpl = (row['Post Date'],            # date
            float(row['Amount']),       # amount
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
    description = ' '.join([row['Payee'],row['Address']])
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

# dictionary of CSV header. TODO: move this else where (maybe in a db)
csv_headers = {}
csv_headers['bofa'] = ['Posted Date', 'Reference Number', 'Payee', 'Address', 'Amount']
csv_headers['citi'] = ['Status', 'Date', 'Description', 'Debit', 'Credit', 'Member Name', '', 'Main Categories', 'Other Catergories']
csv_headers['discover']=['Trans. Date', 'Post Date', 'Description', 'Amount', 'Category']

def import_statement(lender, conn, path):
    with open(path, 'r') as fin:
        # DictReader uses first line in file for column headings by default
        statement_data = csv.DictReader(fin) 
        
        # continue if CSV headers match
        if csv_headers[lender] == reader.fieldnames:
            # read in all data
            to_db = [tpl_maker[lender](row) for row in statement_data]

            # insert all data into database
            cur = conn.cursor()
            cur.executemany(sql, to_db)
            conn.commit()
            conn.close()

