import csv

"""
load identifiers... TODO maybe put in SQLite because database
"""
def load_identifiers():
    identifiers = {}
    with open('categories.csv','r') as fin:
        category_data = csv.DictReader(fin)
        identifiers = dict((row['key'], [row['main'],row['sub']]) for row in category_data)

    return identifiers


"""
determine main and sub categories given item description
"""
def auto_classify(description):
    # init lists to store identifiers
    cat_main = []
    cat_sub = []

    # load identifiers
    identifiers = load_identifiers()

    # check for main and sub categories
    # loop through all identifiers
    for key, value in identifiers.items():
        if key in description:
            print(key,value,description,key in description)
            if value[0]:
                cat_main.append(value[0])
            if value[1]:
                cat_sub.append(value[1])
            print(cat_main, cat_sub)
            print(','.join(cat_main), ','.join(cat_sub))
    return (','.join(cat_main), ','.join(cat_sub))
