# Слияние 2-х упорядоченных списков и их сортировка
# Списки обязательно должны быть отсортированы

a = [3, 7, 8, 10, 12]
b = [2, 6, 8, 11, 15, 17]

c = []
i = 0
j = 0

while i < len(a) and j < len(b):
    if a[i] <= b[j]:
        c.append(a[i])
        i += 1
    else:
        c.append(b[j])
        j += 1
    # print(i, j)
c = c + a[i:] + b[i:]
print(c)

# Сортировка 2-х неупорядоченных списков слянием
# Для этого делим список до тех пора пока не будут отдельные цифры. А после
# сравниваем их методом слияние, как выше и на выходе будем иметь
# отсортированный список

def sort(a, b):
    i = 0
    j = 0
    c = []
    # print('SORT A', a)
    # print('SORT B', b)
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    c += a[i:] + b[j:]
    # print('SORT C', c)
    return c

def divide_list(s):
    n = len(s) // 2
    a = s[:n] # деление списка пополам
    b = s[n:]
    # print('AA', a)
    # print('BB', b)

    if len(a) > 1:
        a = divide_list(a)
    if len(b) > 1:
        b = divide_list(b)

    return sort(a, b)

s = [3, 7, -8, 10, 12, 2, 6, -6, 1, -15, 4]
s = divide_list(s)
print(s)


# Сортировка Хоара. Берется за начальную точку первый элемент массива и
# разбивается на массивы со значениями <, ==, > этого элемента. Затем,
# те массивы, что больше 1 также разбиваются до тех пор пока не буде одного
# числа. После этого все собирается обратно


def quick_sort(v):
    if len(v) > 1:
        x = v[0]
        minlist = [u for u in v if u < x]
        med = [u for u in v if u == x]
        maxim = [u for u in v if u > x]
        v = quick_sort(minlist) + med + quick_sort(maxim)
    return v

v = [3, 7, -8, 10, 12, 2, 6, -6, 1, -15, 4]
print(quick_sort(v))
