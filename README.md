SERGen - SimpleExpenditureReportGenerator

Objectives:

Track expenses in user defined categories

Generate monthly reports of spending and accumulation in defined categories

DONE:

    aggregate all data into SQLite

    multi-CSV converter - convert from multiple institution formats?

    multi-CSV converter - format validation based on CSV header

    duplicate entry check - possible duplicate if there exists date, amount, description, lender match
        do this outside database and in CSV parsing

TODO/RANDOM IDEAS:

    multi-CSV converter - format validation based on CSV headers stored in database

    rules for auto classification

    parsing for multiple categories

    report generation - ipynb and SQLite->Pandas?
    
    visual interface http://sqlitebrowser.org/

    implement online backup upon ?
    export to Dropbox?  https://anands.github.io/blog/2016/11/20/continuous-backup-of-dot-files-using-python-and-dropbox/

    run on pi zero
    database storage
    run web interface https://github.com/coleifer/sqlite-web

    plaid testing integration https://plaid.com/pricing/

    bank account tracking with respect to deductions
