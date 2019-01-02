#!/usr/bin/env python

import os
import copy
import datetime
from pdfParser import pdf_to_text

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def get_transactions(text):
    # get start and end years
    start_close_text = text[3]
    start_month = start_close_text.split()[2]
    start_year = start_close_text.split()[4][:4]
    end_month = start_close_text.split()[-3]
    end_year = start_close_text.split()[-1]

    # find line where transactions start
    i_text = 0
    while 'Payments and Credits' not in text[i_text]:
        i_text += 1
    i_text += 1
    # skip all Payments and Credits
    while text[i_text].split()[0] in months:
        i_text += 1

    transactions = []
    null_date = datetime.date(1900,1,1)
    last_transaction = [null_date,'',0.]
    while 'TOTAL FEES FOR THIS PERIOD' not in text[i_text]:
        trans_text = text[i_text].split()

        # accommodate Amazon 2 liners
        if len(trans_text) == 1:
            if last_transaction[0] != null_date:
                last_transaction[1] += ' ' + trans_text[0]
                transactions.append(last_transaction)
                last_transaction = [null_date,'',0.]
                i_text += 1
            continue

        i_month = 0 
        i_desc_start = 4
        i_desc_stop = -1
        if trans_text[i_month] not in months:
            i_month += 1
            i_desc_start += 1
            i_desc_stop -= 1
        if last_transaction[0] != null_date:
            transactions.append(last_transaction)

        trans_month = trans_text[i_month]
        trans_day = trans_text[i_month+1]
        trans_year = start_year if trans_month == start_month else end_year
        trans_date = datetime.date(int(trans_year), months.index(trans_month)+1, int(trans_day))

        trans_descip = ' '.join(trans_text[i_desc_start:i_desc_stop])

        last_transaction = [trans_date, trans_descip, float(trans_text[-1])]
        
        i_text += 1

    if last_transaction[0] != null_date:
        transactions.append(last_transaction)

    print(transactions)
    print(len(transactions))
    

def get_statement_text(f):
    if os.path.isfile(f):
        text = pdf_to_text(f, 2)
        transactions = get_transactions(text)
    else:
        print('{} is not found'.format(f))


if __name__ == '__main__':
    import sys
    get_statement_text(sys.argv[1])
