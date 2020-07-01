import csv
import pandas as pd
import numpy as np


df = pd.read_csv('NFA 2018.csv')

headers = df.columns.tolist()
data = np.array(df)


# df.to_csv('New.csv')


for i in range(len(data)):

    y = data[i][1]

    # if pd.isna(y):
    #     y=3000
    # else:
    #     y = int(y)
    # print(y)
    
    for item in range(2,8):
        if pd.isna(data[i][item]):
             data[i][item] = data[i][8]/6

# for i in range(len(data)):
#      '''#Остались пустые только в 9 столбце'''
#     for item in range(2,11):
#             if pd.isna(data[i][item]):
#                 print('Nan: столбец-',item)
print('Выберите, как заменять пропущенные значения:\n')
print('1.Игнорировать\n')
print('2.Взять значение по-умолчанию\n')
print('3.Взять среднее значение\n')
c = input()
if c.isdigit():
    char = int(c)
    if char is 2:
        print('Значение по-умолчанию берется из предыдущей строки')
        for item in range(8,11):
            for i in range(len(data)):
                '''#8-10 столбец'''
                if pd.isna(data[i][item]):
                    if pd.isna(data[i-1][item]) is not True:
                        data[i][item] = data[i-1][item]
    elif char is 3:
        print('Среднее значение считается по всем странам')
        for item in range(8,11):
            theSum = 0
            for i in range(len(data)):
                '''#8-10 столбец'''
                if pd.isna(data[i][item]) is not True:
                    theSum = theSum + data[i][item]
            for i in range(len(data)):
                if pd.isna(data[i][item]):
                    data[i][item] = theSum/len(data)
            '''Проверка:'''
            # print('Сумма - ',theSum,' длина - ',len(data))
            # print('Программа - ',theSum/len(data))
    else:
        print('Значение игнорируется либо Вы выбрали другой вариант')
else:
    print('Значение игнорируется, т.к. Вы выбрали другой вариант')
'''#Убрать строку ниже'''
num = list(range(11))
'''#Убрать строку выше(нумерация стобцов)'''

with open('Norm.csv', "w", newline="") as file:
    writer = csv.writer(file)
    '''#Убрать строку ниже'''
    writer.writerow(num)
    '''#Убрать строку выше(нумерация стобцов)'''
    writer.writerow(headers)
    writer.writerows(data)
