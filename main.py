import csv
import pandas as pd
import numpy as np


df = pd.read_csv('NFA 2018.csv')
'''Список заголовков и спосок данных'''
headers = df.columns.tolist()
data = np.array(df)

# df.to_csv('New.csv')

'''Меню'''
print('Выберите, как заменять пропущенные значения:\n')
print('1.Игнорировать\n')
print('2.Взять значение по-умолчанию\n')
print('3.Взять среднее значение\n')
c = input()
if c.isdigit():
    char = int(c)
    if char is 2:
        print('Значение по-умолчанию для 2 столбца - 2020')
        print('Значение по-умолчанию для 3-8 считается из общего')
        print('Значение по-умолчанию для 1,9-11 - берется из предыдущей строки')
        for item in range(8,11):
            for i in range(len(data)):
                '''#8-10 столбец'''
                if pd.isna(data[i][item]):
                    if pd.isna(data[i-1][item]) is not True:
                        data[i][item] = data[i-1][item]
        for i in range(len(data)):
                '''#0 столбец - страна'''
                if pd.isna(data[i][0]):
                    if pd.isna(data[i-1][0]) is not True:
                        data[i][0] = data[i-1][0]
        for i in range(len(data)):
            '''#1 столбец - год'''
            if pd.isna(data[i][1]):
                data[i][1]=2020
            '''#2-7 столбец - земли'''
            for item in range(2,8):
                if pd.isna(data[i][item]):
                     data[i][item] = data[i][8]/6
    elif char is 3:
        print('Среднее значение считается по всем странам')
        print('Значение для 1 столбца - берется из предыдущей строки')
        for i in range(len(data)):
                '''#0 столбец - страна'''
                if pd.isna(data[i][0]):
                    if pd.isna(data[i-1][0]) is not True:
                        data[i][0] = data[i-1][0]
        for item in range(1,11):
            '''#1-10 столбец'''
            theSum = 0
            for i in range(len(data)):
                if pd.isna(data[i][item]) is not True:
                    theSum = theSum + data[i][item]
            for i in range(len(data)):
                if pd.isna(data[i][item]):
                    data[i][item] = theSum/len(data)
            '''Проверка:'''
            # print('Сумма - ',theSum,' длина - ',len(data))
            # print('Программа - ',theSum/len(data))
    else:
        print('Значения игнорируются либо Вы выбрали другой вариант')
else:
    print('Значения игнорируются, т.к. Вы выбрали другой вариант')

'''Делаем год значением int'''
for i in range(len(data)):
    if pd.isna(data[i][1]) is not True:
        data[i][1] = int(data[i][1])

'''#Убрать строку ниже'''
num = list(range(11))
'''#Убрать строку выше(нумерация стобцов для удобства)'''

'''!Запись в тестовый файл!'''
with open('Norm.csv', "w", newline="") as file:
    writer = csv.writer(file)
    '''#Убрать строку ниже'''
    writer.writerow(num)
    '''#Убрать строку выше(нумерация стобцов)'''
    writer.writerow(headers)
    writer.writerows(data)
