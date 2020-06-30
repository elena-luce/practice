import pandas as pd
import numpy as np


df = pd.read_csv('NFA 2018.csv',index_col='country')
data = np.array(df)


# df.to_csv('New.csv')


for i in range(len(data)):
    
    y = data[i][0]
    if pd.isna(y):
        y=3000
    else:
        y = int(y)
    print(y)
