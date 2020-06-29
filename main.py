import pandas


df = pandas.read_csv('NFA 2018.csv',index_col='country')
# print(df)
df.to_csv('New.csv')
