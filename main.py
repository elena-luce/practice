import csv
import pandas as pd
import numpy as np


df = pd.read_csv('NFA 2018.csv',index_col='country')
data = np.array(df)


# df.to_csv('New.csv')


for i in range(len(data)):
    
    y = data[i][0]
    # if pd.isna(y):
    #     y=3000
    # else:
    #     y = int(y)
    # print(y)
    
    for item in range(1,7):
        if pd.isna(data[i][item]):
             data[i][item] = data[i][7]/6

with open('Norm.csv', "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)
