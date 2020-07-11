import matplotlib.pyplot as plt
import csv
import math
from scipy.stats import chi2_contingency
from scipy.stats import chi2
import pandas as pd
import numpy as np

def del_dup(data):    #Функция удаления дубликатов
    print('Пункт 1. Удаление дубликатов данных\n')
    seen = set()
    seen.add(data[0][1])
    data1 = data[0]
    print('Идет удаление... Дождитесь его окончания.')
    for i in range(1, (int(len(data))-1)):
        if data[i][0] == data[i-1][0]:
            if data[i][1] in seen:
                continue
            else:
                data_plg = data[i]
                data1 = np.vstack([data1, data_plg])
                seen.add(data[i][1])
        else:
            seen.clear()
            seen.add(data[i][1])
    print('Операция прошла успешно\n')
    return data1

def Sum(item,data):     #Функция нахождения среднего арифмитического
    sum = 0
    for i in range(len(data)):
        if pd.isna(data[i][item]) is not True:
            sum = sum + data[i][item]
    arif_mean = sum/len(data)
    return arif_mean

def missed (data):      #Функция замены пропущенных
    print('Пункт 2. Замена пропущенных значений\n')
    '''Меню'''
    print('Названия столбцов:\n'
              '0.country        1.year          2.crop_land\n'
              '3.grazing_land   4.forest_land   5.fishing_ground\n'
              '6.built_up_land  7.carbon        8.total\n'
              '9.percapita      10.population\n')
    print('Выберите, как заменять пропущенные значения:')
    print('1.Игнорировать')
    print('2.Взять значение по-умолчанию')
    print('3.Взять среднее значение')
    c = input()
    if c.isdigit():
        char = int(c)
        if char is 2:
            print('Значение по-умолчанию для 1 столбца - 2020')
            print('Значение по-умолчанию для 2-7 считается из общего')
            print('Значение по-умолчанию для 0,8-10 - берется из предыдущей строки')
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
            print('Значение для 0 столбца - берется из предыдущей строки')
            '''#0 столбец - страна'''
            for i in range(len(data)):
                    if pd.isna(data[i][0]):
                        if pd.isna(data[i-1][0]) is not True:
                            data[i][0] = data[i-1][0]
            for item in range(1,11):
                theSum = Sum(item,data)
                '''#1-10 столбец'''
                for i in range(len(data)):
                    if pd.isna(data[i][item]):
                        data[i][item] = theSum
                '''Проверка:'''
                # print('Сумма - ',theSum,' длина - ',len(data))
                # print('Программа - ',theSum/len(data))
            print('Все пропущенные значения заменены\n')
        else:
            print('Значения игнорируются либо Вы выбрали другой вариант\n')
    else:
        print('Значения игнорируются, т.к. Вы выбрали другой вариант\n')
    return data

def is_digit(string):   #Функция проверки на число для int, float
        if string.isdigit():
            return True
        else:
            try:
                float(string)
                return True
            except ValueError:
                return False

def norm(data):     #Функция нормализации
    print('Пункт 3. Нормализация.\n')
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
            return data
        else:
            c = c[:n] + '.'+ c[n:]
    '''Умножение на коэффициент'''
    k = float(c)
    print('Названия столбцов:\n'
          '2.crop_land          3.grazing_land      4.forest_land\n'
          '5.fishing_ground     6.built_up_land     7.carbon\n'
          '8.total              9.percapita         10.population\n')
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
                col2 = input("Повторите ввод конечного столбца -  ")
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
    else:
        print('Нормализация не прошла успешно, т.к. Вы выбрали другой вариант\n')
    return data

def z_graph(Z,item):    #Функция построения графика для Z-оценки
    x = np.arange(len(Z), dtype = int)
    fig = plt.figure()
    for j in range(len(Z)-1,-1,-1):
        if Z[j] is None:
            x = np.delete(x,j)
            Z = np.delete(Z,j)
    plt.scatter(x, Z)
    for j in range(len(Z)-1,-1,-1):
        if (float(Z[j]) > 1.96) or (float(Z[j]) < -1.96):
            x = np.delete(x,j)
            Z = np.delete(Z,j)
    plt.plot(x,Z,marker = 'o',markersize = 10,color = 'red')
    grid1 = plt.grid(True)
    gr_name = 'График_2.png'
    if item > 2:
        gr_name = gr_name[:7] + str(item) + gr_name[8:]
    print(gr_name)
    fig.savefig(gr_name)

def z_value(data,item):     #Функция рассчета Z-значения
    print('Столбец - ',item)
    A = Sum(item,data)
    k = 0
    for i in range(len(data)):
        if pd.isna(data[i][item]) is not True:
            k = k + (data[i][item]-A)**2
    sigma = math.sqrt(k/(len(data)-1))
    z = []
    for i in range(len(data)):
        if pd.isna(data[i][item]) is False:
            nz = str(data[i][item])
            n = nz.find('.')
            if n >= 0:
                nz = nz[:n] + nz[n+1:]
            if (nz.count('0') is len(nz)):
                z.append(None)
            else:
                z.append((data[i][item]-A)/sigma)
        else:
            z.append(None)
    b = False
    i = -1
    while(i < len(z)-1 and b is False):
        i+=1
        if z[i] is None:
            b = False
        else:
            b = True
    if b is True:
        d1 = []
        for j in range(len(data)):
            d2 = []
            for i in range(2):
                d2.append(data[j][i])
            d2.append(z[j])
            d1.append(d2)
        filename = 'Z_2.csv'
        if item > 2:
            filename = filename[:2] + str(item) + filename[3:]
        print(filename)
        with open(filename, "w", newline="", encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerows(d1)
        for j in range(len(z)-1,-1,-1):
            if z[j] is not None:
                if (float(z[j]) > 1.96) or (float(z[j]) < -1.96):
                    data = np.delete(data,j,0)
        z_graph(z,item)
        print('Операция прошла успешно для текущего столбца\n')
    else:
        print('Невозможно провести Z-оценку, т.к. столбец содержит пустые значения или нули')
    return data

def z_menu(data):       #Функция меню для Z-оценки
    print('Пункт 4. Удаление аномалий с помощью Z-оценки\n')
    print('Названия столбцов:\n'
              '2.crop_land          3.grazing_land      4.forest_land\n'
              '5.fishing_ground     6.built_up_land     7.carbon\n'
              '8.total              9.percapita         10.population\n')
    print('К каким столбцам применить Z-оценку?')
    print('1.Один столбец')
    print('2.Несколько столбцов')
    c = input()
    if c.isdigit():
        char = int(c)
        if char is 1:
            col = input("Z-оценка для столбца -  ")
            while col.isdigit() is False or int(col) > 10 or int(col) < 2:
                col = input('Это должно быть число в пределах 2-10.\n'
                            ' Повторите ввод значения столбца -  ')
            col = int(col)
            print('Z-значения столбца хранятся в файлах:')
            data = z_value(data,col)
        elif char is 2:
            col1 = input("Z-оценка для солбцов от - ")
            col2 = input("И до - ")
            while col1.isdigit() is False or int(col1) > 10 or int(col1) < 2:
                col1 = input("Повторите ввод начального столбца -  ")
            while col2.isdigit() is False or int(col2) > 10 or int(col2) < 2:
                col2 = input("Повторите ввод конечного столбца -  ")
            col1 = int(col1)
            col2 = int(col2)
            if col2 < col1:
                col = col2
                col2 = col1
                col1 = col
                print('Столбцы поменяли местами:'
                      'от - ', col1,', до - ',col2)
            print('Z-значения каждого столбца хранятся в файлах:')
            for item in range(col1,col2+1):
                data = z_value(data,item)
        else:
            print('Операция не прошла успешно, т.к. Вы выбрали другой вариант\n')
    else:
        print('Операция не прошла успешно, т.к. Вы выбрали другой вариант\n')
    return data

def dependent(table1):
    # print(table1)
    D = False
    I = False
    stat, p, dof, expected = chi2_contingency(table1)
    # print('dof=%d' % dof)
    # print(expected)
    prob = 0.95
    critical = chi2.ppf(prob, dof)
    # print('probability=%.3f, critical=%.3f, stat=%.3f' % (prob, critical, stat))
    if abs(stat) >= critical:
        D = True #Dependent
    else:
        D = False #Independent

    alpha = 1.0 - prob
    # print('significance=%.3f, p=%.3f' % (alpha, p))
    if p <= alpha:
        I = True #Dependent
    else:
        I = False #Independent
    rem = False
    if D is False and I is False:
        rem = True     #Независимы
    elif D is True and I is True:
        rem = False     #Зависимы
    else:
        print('Две оценки теста Хи-квадрат показали противоположные результаты.'
              ' Удалять ли столбец?')
        c = input()
        if c is 'yes' or 'да':
            rem = True
        elif c is 'no' or 'нет':
            rem = False
        else:
            print('Вы не ввели ожидаемый ответ. Столбец не будет удален.')
    return rem

def remove(table):
    table1 =table[2:10]     #10col
    if dependent(table1) is True:
        table1 = np.delete(table,10,0)
        return table1,10
    table1 = table[2:9]+ table[10]    #9col
    if dependent(table1) is True:
        table1 = np.delete(table,9,0)
        return table1,9
    table1 = table[2:8]+ table[9:11]     #8col
    if dependent(table1) is True:
        table1 = np.delete(table,8,0)
        return table1,8
    table1 = table[2:7]+ table[8:11]     #7col
    if dependent(table1) is True:
        table1 = np.delete(table,7,0)
        return table1,7
    table1 = table[2:6]+ table[7:11]     #6col
    if dependent(table1) is True:
        table1 = np.delete(table,6,0)
        return table1,6
    table1 = table[2:5]+ table[6:11]     #5col
    if dependent(table1) is True:
        table1 = np.delete(table,5,0)
        return table1,5
    table1 = table[2:4]+ table[5:11]     #4col
    if dependent(table1) is True:
        table1 = np.delete(table,4,0)
        return table1,4
    table1 =table[2]+table[4:11]     #3col
    if dependent(table1) is True:
        table1 = np.delete(table,3,0)
        return table1,3
    table1 =table[3:11]     #2col
    if dependent(table1) is True:
        table1 = np.delete(table,2,0)
        return table1,2

def chi_sqr(data):
    print('Пункт 5. Удаление столбцов на основе Хи-квадрат теста\n')
    Na = 0
    col = 0
    for item in range(2,11):
        for i in range(len(data)):
            if pd.isna(data[i][item]) is False:
                Na += 1
    if Na ==len(data)*9:
        table = data.transpose()
        table1 = table[2:11]
        D = False
        I = False
        stat, p, dof, expected = chi2_contingency(table1)
        # print('dof=%d' % dof)
        # print(expected)
        prob = 0.95
        critical = chi2.ppf(prob, dof)
        # print('probability=%.3f, critical=%.3f, stat=%.3f' % (prob, critical, stat))
        if abs(stat) >= critical:
            D = True #Dependent
        else:
            D = False #Independent

        alpha = 1.0 - prob
        # print('significance=%.3f, p=%.3f' % (alpha, p))
        if p <= alpha:
            I = True #Dependent
        else:
            I = False #Independent

        if D is False and I is False:
            print('Столбцы независимы')
        elif D is True and I is True:
            print('Столбцы зависимы')
            table,col = remove(table)
            data = table.transpose()
        else:
            print('Две оценки теста Хи-квадрат показали противоположные результаты.'
              ' Удалять ли столбцы?')
            c = input()
            if c is 'yes' or 'да':
                print('Столбцы приняты зависимыми')
                table,col = remove(table)
                data = table.transpose()
            elif c is 'no' or 'нет':
                print('Столбцы приняты независимыми')
            else:
                print('Вы не ввели ожидаемый ответ. Столбцы не будет удалены.')
        print('Зависимые столбцы удалены.\n')
    else:
        print('Операция не прошла успешно, т.к. таблица содержит пустые занчения,'
              ' с которыми Хи-квадрат тест не работает\n')
    return data,col



def main():
    df = pd.read_csv('NFA 2018.csv')
    '''Список заголовков и спосок данных'''
    headers = df.columns.tolist()
    dt = np.array(df)
    dt = del_dup(dt)
    dt = missed(dt)
    dt = norm(dt)
    dt = z_menu(dt)
    ki,col = chi_sqr(dt)
    del headers[col]

    '''Делаем год значением int'''
    for i in range(len(dt)):
        if pd.isna(dt[i][1]) is not True:
            dt[i][1] = int(dt[i][1])

    print('Очищенные данные хранятся в файле "New.csv"')
    with open('New.csv', "w", newline="", encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(dt)


if __name__=="__main__":
    main()
