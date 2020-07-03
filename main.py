import csv
import pandas as pd
import numpy as np


def missed (data):
    print('Пункт 1:\n')
    '''Меню'''
    print('Выберите, как заменять пропущенные значения:')
    print('1.Игнорировать')
    print('2.Взять значение по-умолчанию')
    print('3.Взять среднее значение')
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
            print('Все пропущенные значения заменены\n')
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
            print('Все пропущенные значения заменены\n')
        else:
            print('Значения игнорируются либо Вы выбрали другой вариант\n')
    else:
        print('Значения игнорируются, т.к. Вы выбрали другой вариант\n')
    return data

def is_digit(string):
        if string.isdigit():
           return True
        else:
            try:
                float(string)
                return True
            except ValueError:
                return False

def norm(data):
    print('Пункт 2:\n')
    '''Меню'''
    c = input('Введите коэффициент для нормализации:')
    while is_digit(c) is not True:
        c = input('Введите числовое значение коэффициента нормализации:\n '
              '(используйте точки вместо запятых для десятичных дробей)')
    '''Проверка, что коэф не 0, 0.0 и т.д.'''
    n = c.find('.')
    if n >= 0:
        c = c[:n] + c[n+1:]
    if (c.count('0') is len(c)):
        print('Нормализация не прошла успешно, т.к. Вы ввели 0\n')
    else:
        c = c[:n] + '.'+ c[n:]
        '''Умножение на коэффициент'''
        k = float(c)
        print('К каким столбцам применить коэффициент?')
        print('1.Один столбец')
        print('2.Несколько столбцов')
        c = input()
        if c.isdigit():
            char = int(c)
            if char is 1:
                col = input("Нормализуется столбец -  ")
                while col.isdigit() is False or int(col) > 10 or int(col) < 2:
                    col = input('Это должно быть число в пределах 2-10.\n'
                                ' Повторите ввод нормализуемого столбца -  ')
                col = int(col)
                for i in range(len(data)):
                    data[i][col] = data[i][col]*k
                print('Нормализация прошла успешно\n')
            elif char is 2:
                col1 = input("Нормализуются значения столбцов начиная от - ")
                col2 = input("И до - ")
                while col1.isdigit() is False or int(col1) > 10 or int(col1) < 2:
                    col1 = input("Повторите ввод начального столбца -  ")
                while col2.isdigit() is False or int(col2) > 10 or int(col2) < 2:
                    col2 = input("Повторите ввод начального столбца -  ")
                col1 = int(col1)
                col2 = int(col2)
                if col2 < col1:
                    col = col2
                    col2 = col1
                    col1 = col
                    print('Столбцы поменяли местами:'
                          'от - ', col1,', до - ',col2)
                for item in range(col1,col2+1):
                    '''#выбранные столбцы'''
                    for i in range(len(data)):
                        data[i][item] = data[i][item]*k
                print('Нормализация прошла успешно\n')
            else:
                print('Нормализация не прошла успешно, т.к. Вы выбрали другой вариант\n')
    return data

def main():
    df = pd.read_csv('NFA 2018.csv')
    '''Список заголовков и спосок данных'''
    headers = df.columns.tolist()
    dt = np.array(df)
    dt = missed(dt)
    dt = norm(dt)
    '''Делаем год значением int'''
    for i in range(len(dt)):
        if pd.isna(dt[i][1]) is not True:
            dt[i][1] = int(dt[i][1])

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
        writer.writerows(dt)

# df.to_csv('New.csv')

if __name__=="__main__":
    main()
