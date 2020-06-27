import csv


with open('NFA 2018.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

123
