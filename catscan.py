"""
Use article list from catscan instead of creating one manually
"""

import csv

f = open("catscan", 'rt')
try:
    reader = csv.reader(f)
    listoftitles = []
    next(reader, None)
    next(reader, None)
    for row in reader:
        print row[0]
        listoftitles.append(row[0])
finally:
    f.close()            
