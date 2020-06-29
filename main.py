import pandas


df = pandas.read_csv('NFA2018.csv',index_col='country')
# print(df)
df.to_csv('New.csv')
