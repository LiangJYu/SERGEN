SERGen - SimpleExpenditureReportGenerator

Objectives:

Track expenses in user defined categories

Generate monthly reports of spending and accumulation in defined categories

DONE:

+ aggregate all data into SQLite

+ multi-CSV converter - convert from multiple institution formats?

+ multi-CSV converter - format validation based on CSV header

+ duplicate entry check - possible duplicate if there exists date, amount, description, lender match

  + done outside database and in CSV parsing

+ rules for auto classification

+ visual interface http://sqlitebrowser.org/ - install and run exe

TODO/RANDOM IDEAS:

+ change SQlite data format https://stackoverflow.com/questions/4428795/sqlite-convert-string-to-date

+ save and load to/from YAML

  + categories

  + path to data

+ report generation - ipynb and SQLite->Pandas?

+ parsing for multiple categories

+ duplicate entry check - possible duplicate if there exists date, amount, description, lender match

  + done inside database after commit entries

+ multi-CSV converter - format validation based on CSV headers stored in database
    
+ implement online backup upon ?

  + export to Dropbox?  https://anands.github.io/blog/2016/11/20/continuous-backup-of-dot-files-using-python-and-dropbox/

+ run on pi

  + database storage

  + run web interface https://github.com/coleifer/sqlite-web

+ plaid testing integration https://plaid.com/pricing/

+ bank account tracking with respect to deductions
